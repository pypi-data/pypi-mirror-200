import csv
import datetime
from _decimal import Decimal
from datetime import timedelta
from string import Formatter
from typing import Dict, List, Optional, Type

from NEMO.models import (
    AreaAccessRecord,
    BaseModel,
    ConsumableWithdraw,
    Reservation,
    StaffCharge,
    TrainingSession,
    UsageEvent,
)
from NEMO.utilities import (
    BasicDisplayTable,
    beginning_of_the_day,
    capitalize,
    end_of_the_day,
    export_format_datetime,
    extract_optional_beginning_and_end_dates,
)
from dateutil.relativedelta import relativedelta
from dateutil.rrule import MONTHLY, rrule
from django.db.models import BooleanField, Case, F, QuerySet, Value, When
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.formats import number_format
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_GET

from NEMO_reports.customizations import ReportsCustomization
from NEMO_reports.decorators import accounting_or_manager_required
from NEMO_reports.templatetags.reports_tags import app_installed

DEFAULT_PARAMETER_LIST = ["export", "start", "end", "split_by_month", "cumulative_count", "detailed_data"]
ACTIVITIES_PARAMETER_LIST = [
    "tool_usage",
    "area_access",
    "training",
    "consumables",
    "staff_charges",
    "custom_charges",
    "missed_reservations",
]


class BasicDisplayTableFormatted(BasicDisplayTable):
    def formatted_value(self, value, html: bool = False):
        if value is None:
            return ""
        if isinstance(value, Decimal):
            amount = display_amount(value)
            return f'<div class="text-right">{amount}</div>' if html else amount
        elif isinstance(value, bool) and html:
            if value:
                return '<span class="glyphicon glyphicon-ok success-highlight"></span>'
            else:
                return '<span class="glyphicon glyphicon-remove danger-highlight"></span>'
        elif isinstance(value, timedelta):
            if value == timedelta(0):
                return "0"
            else:
                return format_timedelta(value, ReportsCustomization.get("reports_timedelta_format"))
        return super().formatted_value(value)


class SummaryDisplayTable(BasicDisplayTableFormatted):
    def to_html(self):
        result = '<table id="summary-table" class="table table-bordered" style="margin-bottom:0">'
        result += "<thead>"
        result += f'<tr class="success"><th colspan="{len(self.headers)}" class="text-center">Summary</th></tr>'
        result += '<tr class="info">'
        for header_key, header_display in self.headers:
            result += f'<th class="text-center">{header_display if header_key != "item" else ""}</th>'
        result += "</tr>"
        result += "</thead>"
        result += "<tbody>"
        for row in self.rows:
            if len(row) == 1 and "item" in row:
                result += f'<tr class="info"><td colspan="{len(self.headers)}" style="font-weight: bold">{row["item"]}</td></tr>'
            else:
                result += "<tr>"
                for number, key in enumerate(row.keys()):
                    result += f'<td class="{"warning" if number == 0 and key == "item" else ""}">{self.formatted_value(row.get(key, ""), html=True)}</td>'
                result += "</tr>"
        result += "</tbody>"
        result += "</table>"
        return mark_safe(result)


class DataDisplayTable(BasicDisplayTableFormatted):
    def to_html(self):
        result = (
            '<table id="data-table" class="table table-bordered table-hover table-striped" style="margin-bottom:0">'
        )
        result += "<thead>"
        result += f'<tr class="success"><th colspan="{len(self.headers)}" class="text-center">Detailed data</th></tr>'
        result += '<tr class="info">'
        for key, value in self.headers:
            result += f"<th>{value}</th>"
        result += "</tr></thead>"
        result += "<tbody>"
        for row in self.rows:
            result += "<tr>"
            for key, value in self.headers:
                result += f'<td>{self.formatted_value(row.get(key, ""), html=True) or ""}</td>'
            result += "</tr>"
        result += "</tbody>"
        result += "</table>"
        return mark_safe(result)


class ReportingParameters:
    def __init__(self, request: HttpRequest, parameter_names=None):
        if parameter_names is None:
            parameter_names = DEFAULT_PARAMETER_LIST
        self.parameter_names = parameter_names
        for parameter_name in parameter_names:
            setattr(self, parameter_name, request.GET.get(parameter_name, None))
        # special case here for start & end dates
        start, end = extract_optional_beginning_and_end_dates(request.GET, date_only=True)
        today = datetime.datetime.now().astimezone()  # Today's datetime in our timezone
        reports_default_daterange = ReportsCustomization.get("reports_default_daterange")
        if not start or not end:
            if reports_default_daterange == "this_year":
                start = today.replace(month=1, day=1)
                end = today.replace(month=12, day=31)
            elif reports_default_daterange == "this_month":
                start = today.replace(day=1)
                end = today + relativedelta(day=31)
            elif reports_default_daterange == "this_week":
                first_day_of_the_week = ReportsCustomization.get_int("reports_first_day_of_week")
                weekday = today.weekday() if first_day_of_the_week else today.isoweekday()
                start = today - timedelta(days=weekday)
                end = start + timedelta(days=6)
            elif reports_default_daterange == "yesterday":
                start = today - timedelta(days=1)
                end = today - timedelta(days=1)
            else:
                start = today
                end = today
        self.start, self.end = start.date(), end.date()

    def get_bool(self, parameter_name: str, default=""):
        return (getattr(self, parameter_name, default) or default) == "on"

    def get_dict(self):
        return {parameter_name: getattr(self, parameter_name) for parameter_name in self.parameter_names}


# Create your views here.
@accounting_or_manager_required
@require_GET
def reports(request):
    return render(request, "NEMO_reports/reports.html", {"report_dict": get_report_dict()})


def report_export(tables: List[BasicDisplayTable], key: str, start: datetime.date, end: datetime.date):
    response = HttpResponse(content_type="text/csv")
    writer = csv.writer(response)
    for table in tables:
        if table.headers:
            writer.writerow([capitalize(display_value) for key, display_value in table.headers])
            for row in table.rows:
                writer.writerow([table.formatted_value(row.get(key, "")) for key, display_value in table.headers])
            writer.writerow([])
    filename = f"{key}_data_{export_format_datetime(start, t_format=False)}_to_{export_format_datetime(end, t_format=False)}.csv"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def get_month_range(day_in_month: datetime.datetime) -> (datetime.datetime, datetime.datetime):
    if isinstance(day_in_month, datetime.date):
        day_in_month = datetime.datetime(year=day_in_month.year, month=day_in_month.month, day=day_in_month.day)
    first_day, last_day = day_in_month.replace(day=1), day_in_month + relativedelta(day=31)
    return beginning_of_the_day(first_day), end_of_the_day(last_day)


def get_monthly_rule(start, end):
    # Split to make sure we are getting the correct full months
    start_month_start, start_month_end = get_month_range(start)
    end_month_start, end_month_end = get_month_range(end)
    return rrule(MONTHLY, dtstart=start_month_start.date(), until=end_month_end.date())


def order_and_unique(list_with_duplicates: List) -> List:
    unique_value_list = list(set(list_with_duplicates))
    unique_value_list.sort()
    return unique_value_list


def billing_installed():
    return app_installed("NEMO_billing")


def get_rate_category() -> Type[BaseModel]:
    if billing_installed():
        from NEMO_billing.rates.models import RateCategory

        return RateCategory


def get_core_facility() -> Type[BaseModel]:
    if billing_installed():
        from NEMO_billing.models import CoreFacility

        return CoreFacility


def reporting_dictionary(key: str, parameters: ReportingParameters, dictionary: Dict):
    # Adds report information (url, title, description...) and parameters to the given dictionary
    return {**get_report_dict().get(key), **parameters.get_dict(), **dictionary}


def usage_events(start, end) -> QuerySet:
    queryset = UsageEvent.objects.filter(end__date__gte=start, end__date__lte=end)
    projects_to_exclude = ReportsCustomization.get_excluded_project_ids()
    if projects_to_exclude:
        queryset = queryset.exclude(project_id__in=projects_to_exclude)
    queryset = queryset.annotate(
        remote=Case(When(user=F("operator"), then=False), default=True, output_field=BooleanField())
    )
    if get_core_facility() and get_core_facility().objects.exists():
        queryset = queryset.annotate(
            core_facility_id=F("tool__core_rel__core_facility"),
            core_facility_name=F("tool__core_rel__core_facility__name"),
        )
    return queryset


def area_access(start, end) -> QuerySet:
    queryset = AreaAccessRecord.objects.filter(end__date__gte=start, end__date__lte=end)
    projects_to_exclude = ReportsCustomization.get_excluded_project_ids()
    if projects_to_exclude:
        queryset = queryset.exclude(project_id__in=projects_to_exclude)
    queryset = queryset.annotate(
        remote=Case(When(staff_charge__isnull=False, then=True), default=False, output_field=BooleanField())
    )
    if get_core_facility() and get_core_facility().objects.exists():
        queryset = queryset.annotate(
            core_facility_id=F("area__core_rel__core_facility"),
            core_facility_name=F("area__core_rel__core_facility__name"),
        )
    return queryset


def staff_charges(start, end) -> QuerySet:
    queryset = StaffCharge.objects.filter(end__date__gte=start, end__date__lte=end)
    projects_to_exclude = ReportsCustomization.get_excluded_project_ids()
    if projects_to_exclude:
        queryset = queryset.exclude(project_id__in=projects_to_exclude)
    queryset = queryset.annotate(remote=Value(True, output_field=BooleanField()))
    if get_core_facility() and get_core_facility().objects.exists():
        queryset = queryset.annotate(
            core_facility_id=F("core_rel__core_facility"),
            core_facility_name=F("core_rel__core_facility__name"),
        )
    return queryset


def consumable_withdraws(start, end) -> QuerySet:
    queryset = ConsumableWithdraw.objects.filter(date__date__gte=start, date__date__lte=end)
    projects_to_exclude = ReportsCustomization.get_excluded_project_ids()
    if projects_to_exclude:
        queryset = queryset.exclude(project_id__in=projects_to_exclude)
    queryset = queryset.annotate(remote=Value(False, output_field=BooleanField()))
    if get_core_facility() and get_core_facility().objects.exists():
        queryset = queryset.annotate(
            core_facility_id=F("consumable__core_rel__core_facility"),
            core_facility_name=F("consumable__core_rel__core_facility__name"),
        )
    return queryset


def training_sessions(start, end) -> QuerySet:
    queryset = TrainingSession.objects.filter(date__date__gte=start, date__date__lte=end)
    projects_to_exclude = ReportsCustomization.get_excluded_project_ids()
    if projects_to_exclude:
        queryset = queryset.exclude(project_id__in=projects_to_exclude)
    queryset = queryset.annotate(remote=Value(False, output_field=BooleanField()))
    if get_core_facility() and get_core_facility().objects.exists():
        queryset = queryset.annotate(
            core_facility_id=F("tool__core_rel__core_facility"),
            core_facility_name=F("tool__core_rel__core_facility__name"),
        )
    return queryset


def missed_reservations(start, end) -> QuerySet:
    queryset = Reservation.objects.filter(missed=True, end__date__gte=start, end__date__lte=end)
    projects_to_exclude = ReportsCustomization.get_excluded_project_ids()
    if projects_to_exclude:
        queryset = queryset.exclude(project_id__in=projects_to_exclude)
    queryset = queryset.annotate(remote=Value(False, output_field=BooleanField()))
    if get_core_facility() and get_core_facility().objects.exists():
        queryset = queryset.annotate(
            core_facility_id=Case(
                When(tool__isnull=False, then=F("tool__core_rel__core_facility")),
                When(area__isnull=False, then=F("area__core_rel__core_facility")),
                default=None,
            ),
            core_facility_name=Case(
                When(tool__isnull=False, then=F("tool__core_rel__core_facility__name")),
                When(area__isnull=False, then=F("area__core_rel__core_facility__name")),
                default=None,
            ),
        )
    return queryset


def custom_charges(start, end) -> QuerySet:
    from NEMO_billing.models import CustomCharge

    queryset = CustomCharge.objects.filter(date__date__gte=start, date__date__lte=end)
    projects_to_exclude = ReportsCustomization.get_excluded_project_ids()
    if projects_to_exclude:
        queryset = queryset.exclude(project_id__in=projects_to_exclude)
    queryset = queryset.annotate(remote=Value(False, output_field=BooleanField()))
    if get_core_facility() and get_core_facility().objects.exists():
        queryset = queryset.annotate(
            core_facility_name=F("core_facility__name"),
        )
    return queryset


def display_amount(amount: Optional[Decimal]) -> str:
    # We need to specifically check for None since amount = 0 will evaluate to False
    if amount is None:
        return ""
    rounded_amount = round(amount, 2)
    if amount < 0:
        return f"({number_format(abs(rounded_amount), decimal_pos=2)})"
    else:
        return f"{number_format(rounded_amount, decimal_pos=2)}"


# See https://stackoverflow.com/a/42320260/597548
def format_timedelta(t_delta, fmt="{D:02}d {H:02}h {M:02}m {S:02}s", input_type="timedelta"):
    """Convert a datetime.timedelta object or a regular number to a custom formatted string,
    just like the strftime() method does for datetime.datetime objects.

    The fmt argument allows custom formatting to be specified. Fields can include seconds,
    minutes, hours, days, and weeks. Each field is optional.

    Some examples:
        '{D:02}d {H:02}h {M:02}m {S:02}s' --> '05d 08h 04m 02s' (default)
        '{W}w {D}d {H}:{M:02}:{S:02}'     --> '4w 5d 8:04:02'
        '{D:2}d {H:2}:{M:02}:{S:02}'      --> ' 5d  8:04:02'
        '{H}h {S}s'                       --> '72h 800s'

    The input_type argument allows t_delta to be a regular number instead of the
    default, which is a datetime.timedelta object.  Valid input_type strings:
        's', 'seconds',
        'm', 'minutes',
        'h', 'hours',
        'd', 'days',
        'w', 'weeks'
    """

    # Convert t_delta to integer seconds.
    if input_type == "timedelta":
        remainder = int(t_delta.total_seconds())
    elif input_type in ["s", "seconds"]:
        remainder = int(t_delta)
    elif input_type in ["m", "minutes"]:
        remainder = int(t_delta) * 60
    elif input_type in ["h", "hours"]:
        remainder = int(t_delta) * 3600
    elif input_type in ["d", "days"]:
        remainder = int(t_delta) * 86400
    elif input_type in ["w", "weeks"]:
        remainder = int(t_delta) * 604800

    f = Formatter()
    desired_fields = [field_tuple[1] for field_tuple in f.parse(fmt) if field_tuple[1]]
    possible_fields = ("W", "D", "H", "M", "S")
    constants = {"W": 604800, "D": 86400, "H": 3600, "M": 60, "S": 1}
    values = {}
    for field in possible_fields:
        if field in desired_fields and field in constants:
            is_last_field = field == desired_fields[-1]
            if is_last_field:
                values[field] = remainder/constants[field]
            else:
                values[field], remainder = divmod(remainder, constants[field])
    return f.format(fmt, **values)


def get_report_dict():
    dictionary = report_dict
    if billing_installed():
        dictionary.update(billing_reports_dict)
    return dictionary


report_dict = {
    "unique_users": {
        "report_url": "reporting_unique_users",
        "report_title": "Unique users",
        "report_description": "Lists unique users based on their activity. When grouping users, the same user can be counted in more than one group.",
    },
    "unique_user_project": {
        "report_url": "reporting_unique_user_project",
        "report_title": "Unique user/project combinations",
        "report_description": "Lists unique user/project combinations. When grouping, the same combination can be counted in more than one group.",
    },
    "unique_user_account": {
        "report_url": "reporting_unique_user_account",
        "report_title": "Unique user/account combinations",
        "report_description": "Lists unique user/account combinations. When grouping, the same combination can be counted in more than one group. ",
    },
    "facility_usage": {
        "report_url": "reporting_facility_usage",
        "report_title": "Facility usage report",
        "report_description": "List facility usage time based on activities",
    },
}

billing_reports_dict = {
    "invoice_charges": {
        "report_url": "reporting_invoice_charges",
        "report_title": "Invoice charges report",
        "report_description": "Displays total invoiced charges during the date range, tax and discounts <b>included</b>",
    },
    "invoice_item_charges": {
        "report_url": "reporting_invoice_item_charges",
        "report_title": "Invoice item charges report",
        "report_description": "Displays total invoiced item charges during the date range, tax and discounts <b>not included</b>",
    },
}
