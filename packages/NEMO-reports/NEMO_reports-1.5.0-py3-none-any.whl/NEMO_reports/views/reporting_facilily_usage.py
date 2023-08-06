import datetime
from typing import List, Union

try:
    from NEMO.models import Discipline as ProjectDiscipline
except:
    from NEMO.models import ProjectDiscipline

from NEMO.models import (
    AccountType,
    AreaAccessRecord,
    Project,
    Reservation,
    StaffCharge,
    TrainingSession,
    UsageEvent,
)
from NEMO.views.api_billing import (
    BillableItem,
    billable_items_area_access_records,
    billable_items_missed_reservations,
    billable_items_staff_charges,
    billable_items_training_sessions,
    billable_items_usage_events,
)
from django.db.models import F, Q, Sum
from django.shortcuts import render
from django.views.decorators.http import require_GET

from NEMO_reports.decorators import accounting_or_manager_required
from NEMO_reports.views.reporting import (
    ACTIVITIES_PARAMETER_LIST,
    DEFAULT_PARAMETER_LIST,
    DataDisplayTable,
    ReportingParameters,
    SummaryDisplayTable,
    area_access,
    get_core_facility,
    get_month_range,
    get_monthly_rule,
    get_rate_category,
    missed_reservations,
    report_export,
    reporting_dictionary,
    staff_charges,
    training_sessions,
    usage_events,
)


@accounting_or_manager_required
@require_GET
def facility_usage(request):
    param_names = DEFAULT_PARAMETER_LIST + ACTIVITIES_PARAMETER_LIST
    params = ReportingParameters(request, param_names)
    start, end = params.start, params.end
    split_by_month = params.get_bool("split_by_month")
    cumulative_count = params.get_bool("cumulative_count")
    monthly_start = None
    if cumulative_count:
        split_by_month = True
        monthly_start, monthly_end = get_month_range(start)

    RateCategory = get_rate_category()
    CoreFacility = get_core_facility()

    data = DataDisplayTable()
    if params.get_bool("detailed_data"):
        data.headers = [
            ("type", "Type"),
            ("user", "Username"),
            ("project", "Project"),
            ("start", "Start"),
            ("end", "End"),
            ("details", "Details"),
            ("duration", "Duration"),
            ("onsite", "On-site"),
        ]

        if CoreFacility and CoreFacility.objects.exists():
            data.add_header(("core_facility", "Core Facility"))
        if ProjectDiscipline.objects.exists():
            data.add_header(("discipline", "Discipline"))
        if AccountType.objects.exists():
            data.add_header(("account_type", "Account type"))
        if RateCategory and RateCategory.objects.exists():
            data.add_header(("rate_category", "Rate category"))

        total_duration, billables = get_facility_usage_duration_and_data(params, start, end, data=True)
        for billable in billables:
            project = Project.objects.get(pk=billable.project_id) if getattr(billable, "project_id", None) else None
            data_row = {
                "type": billable.type,
                "user": billable.username,
                "project": project or "N/A",
                "start": billable.start,
                "end": billable.end,
                "details": billable.details,
                "duration": billable.timedelta,
                "onsite": not billable.remote,
                "core_facility": billable.core_facility,
                "discipline": project.discipline.name if project and project.discipline else "N/A",
                "account_type": project.account.type.name if project and project.account.type else "N/A",
            }
            if RateCategory and RateCategory.objects.exists():
                data_row["rate_category"] = project.projectbillingdetails.category.name if project else "N/A"
            data.add_row(data_row)
        data.rows.sort(key=lambda x: x["end"])

    summary = SummaryDisplayTable()
    summary.add_header(("item", "Item"))
    summary.add_row({"item": "Facility usage"})
    if CoreFacility and CoreFacility.objects.exists():
        summary.add_row({"item": "By core facility"})
        for core_facility in CoreFacility.objects.all():
            summary.add_row({"item": f"{core_facility.name}"})
        summary.add_row({"item": "N/A"})
    if ProjectDiscipline.objects.exists():
        summary.add_row({"item": "By project discipline"})
        for discipline in ProjectDiscipline.objects.all():
            summary.add_row({"item": f"{discipline.name}"})
        summary.add_row({"item": "N/A"})
    if AccountType.objects.exists():
        summary.add_row({"item": "By account type"})
        for account_type in AccountType.objects.all():
            summary.add_row({"item": f"{account_type.name}"})
        summary.add_row({"item": "N/A"})
    if RateCategory and RateCategory.objects.exists():
        summary.add_row({"item": "By project rate category"})
        for category in RateCategory.objects.all():
            summary.add_row({"item": f"{category.name}"})
    summary.add_row({"item": "By remote status"})
    summary.add_row({"item": "Remote"})
    summary.add_row({"item": "On-site"})

    if split_by_month:
        for month in get_monthly_rule(start, end):
            month_key = f"month_{month.strftime('%Y')}_{month.strftime('%m')}"
            summary.add_header((month_key, month.strftime("%b %Y")))
            month_start, month_end = get_month_range(month)
            add_summary_info(params, summary, monthly_start or month_start, month_end, month_key)
    else:
        summary.add_header(("value", "Value"))
        add_summary_info(params, summary, start, end)

    if params.get_bool("export"):
        return report_export([summary, data], "active_users", start, end)
    dictionary = {
        "data": data,
        "summary": summary,
    }
    return render(
        request, "NEMO_reports/report_facility_usage.html", reporting_dictionary("facility_usage", params, dictionary)
    )


def add_summary_info(parameters: ReportingParameters, summary: SummaryDisplayTable, start, end, summary_key=None):
    RateCategory = get_rate_category()
    CoreFacility = get_core_facility()
    summary_key = summary_key or "value"
    total_duration, billables = get_facility_usage_duration_and_data(parameters, start, end)
    summary.rows[0][summary_key] = total_duration
    current_row = 1
    if CoreFacility and CoreFacility.objects.exists():
        for facility in CoreFacility.objects.all():
            current_row += 1
            f_filter = Q(core_facility_id=facility.id)
            f_duration, f_billables = get_facility_usage_duration_and_data(parameters, start, end, f_filter)
            summary.rows[current_row][summary_key] = f_duration
        # Add general (None) subtotal too
        current_row += 1
        f_filter = Q(core_facility_id__isnull=True)
        f_null_duration, f_null_billables = get_facility_usage_duration_and_data(parameters, start, end, f_filter)
        summary.rows[current_row][summary_key] = f_null_duration
        current_row += 1  # For mid table header
    if ProjectDiscipline.objects.exists():
        for discipline in ProjectDiscipline.objects.all():
            current_row += 1
            p_filter = Q(project__discipline=discipline)
            d_duration, d_billables = get_facility_usage_duration_and_data(parameters, start, end, p_filter)
            summary.rows[current_row][summary_key] = d_duration
        current_row += 1
        p_null_filter = Q(project__discipline__isnull=True)
        d_null_duration, d_null_billables = get_facility_usage_duration_and_data(parameters, start, end, p_null_filter)
        summary.rows[current_row][summary_key] = d_null_duration
        current_row += 1  # For mid table header
    if AccountType.objects.exists():
        for account_type in AccountType.objects.all():
            current_row += 1
            p_filter = Q(project__account__type=account_type)
            a_duration, a_billables = get_facility_usage_duration_and_data(parameters, start, end, p_filter)
            summary.rows[current_row][summary_key] = a_duration
        current_row += 1
        p_null_filter = Q(project__account__type__isnull=True)
        a_null_duration, a_null_billables = get_facility_usage_duration_and_data(parameters, start, end, p_null_filter)
        summary.rows[current_row][summary_key] = a_null_duration
        current_row += 1  # For mid table header
    if RateCategory and RateCategory.objects.exists():
        for category in RateCategory.objects.all():
            current_row += 1
            p_filter = Q(project__projectbillingdetails__category=category)
            r_duration, r_billables = get_facility_usage_duration_and_data(parameters, start, end, p_filter)
            summary.rows[current_row][summary_key] = r_duration
        current_row += 1  # For mid table header
    current_row += 1
    remote_filter = Q(remote=True)
    remote_duration, remote_billables = get_facility_usage_duration_and_data(parameters, start, end, remote_filter)
    summary.rows[current_row][summary_key] = remote_duration
    current_row += 1
    onsite_filter = Q(remote=False)
    onsite_duration, onsite_billables = get_facility_usage_duration_and_data(parameters, start, end, onsite_filter)
    summary.rows[current_row][summary_key] = onsite_duration


def get_facility_usage_duration_and_data(
    params: ReportingParameters,
    start: datetime.datetime,
    end: datetime.datetime,
    extra_filter: Q = None,
    data: bool = False,
) -> (datetime.timedelta, List[BillableItem]):
    # Returns total duration and data (if the data parameter is True)
    # This allows us to use filtering and aggregate and speed up the process
    # greatly if individual data is not needed.
    total_duration = datetime.timedelta(0)
    billables = []
    if params.get_bool("tool_usage", "on"):
        tool_usages = usage_events(start, end).annotate(timedelta=F("end") - F("start"))
        if extra_filter:
            tool_usages = tool_usages.filter(extra_filter)
        total_duration += tool_usages.aggregate(Sum("timedelta"))["timedelta__sum"] or datetime.timedelta(0)
        if data:
            billables.extend(map(to_billable_items, tool_usages))
    if params.get_bool("area_access", "on"):
        area_records = area_access(start, end).annotate(timedelta=F("end") - F("start"))
        if extra_filter:
            area_records = area_records.filter(extra_filter)
        total_duration += area_records.aggregate(Sum("timedelta"))["timedelta__sum"] or datetime.timedelta(0)
        if data:
            billables.extend(map(to_billable_items, area_records))
    if params.get_bool("staff_charges", "on"):
        staff_work = staff_charges(start, end).annotate(timedelta=F("end") - F("start"))
        if extra_filter:
            staff_work = staff_work.filter(extra_filter)
        total_duration += staff_work.aggregate(Sum("timedelta"))["timedelta__sum"] or datetime.timedelta(0)
        if data:
            billables.extend(map(to_billable_items, staff_work))
    if params.get_bool("training", "on"):
        trainings = training_sessions(start, end)
        if extra_filter:
            trainings = trainings.filter(extra_filter)
        total_duration += datetime.timedelta(minutes=trainings.aggregate(Sum("duration"))["duration__sum"] or 0)
        if data:
            billables.extend(map(to_billable_items, trainings))
    if params.get_bool("missed_reservations", "on"):
        reservations = missed_reservations(start, end).annotate(timedelta=F("end") - F("start"))
        if extra_filter:
            reservations = reservations.filter(extra_filter)
        total_duration += reservations.aggregate(Sum("timedelta"))["timedelta__sum"] or datetime.timedelta(0)
        if data:
            billables.extend(map(to_billable_items, reservations))
    return total_duration, billables


def to_billable_items(
    obj: Union[UsageEvent, AreaAccessRecord, TrainingSession, StaffCharge, Reservation]
) -> BillableItem:
    billable = None
    if isinstance(obj, UsageEvent):
        billable = billable_items_usage_events([obj])[0]
    elif isinstance(obj, AreaAccessRecord):
        billable = billable_items_area_access_records([obj])[0]
    elif isinstance(obj, Reservation):
        billable = billable_items_missed_reservations([obj])[0]
    elif isinstance(obj, StaffCharge):
        billable = billable_items_staff_charges([obj])[0]
    elif isinstance(obj, TrainingSession):
        billable = billable_items_training_sessions([obj])[0]
    if billable:
        # This was added by the annotate function
        billable.timedelta = getattr(obj, "timedelta", None) or (datetime.timedelta(minutes=obj.duration) if isinstance(obj, TrainingSession) else datetime.timedelta(0))
        billable.core_facility = getattr(obj, "core_facility_name", None)
        billable.remote = getattr(obj, "remote", None)
    return billable
