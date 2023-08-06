import datetime
from _decimal import Decimal


try:
    from NEMO.models import Discipline as ProjectDiscipline
except:
    from NEMO.models import ProjectDiscipline

from NEMO.models import AccountType
from NEMO_billing.invoices.models import Invoice, InvoiceSummaryItem
from NEMO_billing.models import CoreFacility
from NEMO_billing.rates.models import RateCategory
from django.db.models import OuterRef, Q, QuerySet, Subquery, Sum
from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET

from NEMO_reports.customizations import ReportsCustomization
from NEMO_reports.decorators import accounting_or_manager_required
from NEMO_reports.views.reporting import (
    DataDisplayTable,
    ReportingParameters,
    SummaryDisplayTable,
    get_month_range,
    get_monthly_rule,
    report_export,
    reporting_dictionary,
)
from NEMO_reports.views.reporting_invoice_item_charges import get_invoice_items


@accounting_or_manager_required
@require_GET
def invoice_charges(request):
    params = ReportingParameters(request)
    split_by_month = params.get_bool("split_by_month")
    cumulative_count = params.get_bool("cumulative_count")
    # Split since invoices are by month, any day in that month counts as the full month
    start, end = params.start, params.end
    start, start_month_end = get_month_range(start)
    end_month_start, end = get_month_range(end)
    monthly_start = None
    if cumulative_count:
        split_by_month = True
        monthly_start, monthly_end = get_month_range(start)

    data = DataDisplayTable()
    if params.get_bool("detailed_data"):
        data.headers = [
            ("invoice_number", "Invoice"),
            ("invoice_project", "Project"),
            ("invoice_date", "Date"),
            ("invoice_total", "Amount"),
        ]

        if CoreFacility.objects.exists():
            data.add_header(("core_facility", "Core Facility"))
        if ProjectDiscipline.objects.exists():
            data.add_header(("discipline", "Discipline"))
        if AccountType.objects.exists():
            data.add_header(("account_type", "Account type(s)"))
        if RateCategory.objects.exists():
            data.add_header(("rate_category", "Rate category"))

        total_data_qs = get_invoice_query_set(start, end)
        for invoice in total_data_qs:
            invoice: Invoice = invoice
            discipline = invoice.project_details.project.discipline
            account_type = invoice.project_details.project.account.type
            data_row = {
                "invoice_number": invoice.invoice_number,
                "invoice_project": invoice.project_details.name,
                "invoice_date": invoice.start.strftime("%B %Y"),
                "invoice_total": invoice.total_amount,
                "core_facility": ", ".join(
                    [
                        core_facility or "General charges"
                        for core_facility in set(invoice.invoicesummaryitem_set.values_list("core_facility", flat=True))
                    ]
                ),
                "discipline": discipline.name if discipline else "N/A",
                "account_type": account_type.name if account_type else "N/A",
                "rate_category": invoice.project_details.category.name if invoice.project_details.category else "N/A",
            }
            data.add_row(data_row)
        data.rows.sort(key=lambda x: x["invoice_number"], reverse=True)

    summary = SummaryDisplayTable()
    summary.add_header(("item", "Item"))
    summary.add_row({"item": "Total amount"})
    if CoreFacility.objects.exists():
        summary.add_row({"item": "By core facility"})
        for core_facility in CoreFacility.objects.all():
            summary.add_row({"item": f"{core_facility.name}"})
        summary.add_row({"item": "N/A"})
        summary.add_row({"item": "Taxes"})
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
    if RateCategory.objects.exists():
        summary.add_row({"item": "By project rate category"})
        for category in RateCategory.objects.all():
            summary.add_row({"item": f"{category.name}"})
    summary.add_row({"item": "By remote status"})
    summary.add_row({"item": "Remote"})
    summary.add_row({"item": "On-site"})

    if split_by_month:
        # Create new start/end of month dates
        for month in get_monthly_rule(start, end):
            month_key = f"month_{month.strftime('%Y')}_{month.strftime('%m')}"
            summary.add_header((month_key, month.strftime("%b %Y")))
            month_start, month_end = get_month_range(month)
            add_summary_info(request, summary, monthly_start or month_start, month_end, month_key)
    else:
        summary.add_header(("value", "Value"))
        add_summary_info(request, summary, start, end)

    if params.get_bool("export"):
        return report_export([summary, data], "invoice_charges", start, end)
    dictionary = {
        "data": data,
        "summary": summary,
    }
    return render(request, "NEMO_reports/report_base.html", reporting_dictionary("invoice_charges", params, dictionary))


def add_summary_info(request: HttpRequest, summary: SummaryDisplayTable, start, end, summary_key=None):
    summary_key = summary_key or "value"
    monthly_invoices = get_invoice_query_set(start, end)
    summary.rows[0][summary_key] = monthly_invoices.aggregate(Sum("total_amount"))["total_amount__sum"] or Decimal(0)
    current_row = 1
    if CoreFacility.objects.exists():
        for facility in CoreFacility.objects.all():
            current_row += 1
            sub = InvoiceSummaryItem.objects.filter(
                invoice=OuterRef("pk"),
                core_facility=facility.name,
                summary_item_type=InvoiceSummaryItem.InvoiceSummaryItemType.SUBTOTAL,
            ).values("amount")
            facility_invoices = monthly_invoices.annotate(**{f"facility_total_{facility.id}": Subquery(sub)})
            summary.rows[current_row][summary_key] = facility_invoices.aggregate(Sum(f"facility_total_{facility.id}"))[
                f"facility_total_{facility.id}__sum"
            ] or Decimal(0)
        # Add general (None) subtotal too
        current_row += 1
        sub = InvoiceSummaryItem.objects.filter(
            invoice=OuterRef("pk"),
            core_facility=None,
            summary_item_type=InvoiceSummaryItem.InvoiceSummaryItemType.SUBTOTAL,
        ).values("amount")
        general_invoices = monthly_invoices.annotate(facility_total_general=Subquery(sub))
        summary.rows[current_row][summary_key] = general_invoices.aggregate(Sum("facility_total_general"))[
            "facility_total_general__sum"
        ] or Decimal(0)
        # Add taxes subtotal too
        current_row += 1
        sub = InvoiceSummaryItem.objects.filter(
            invoice=OuterRef("pk"), summary_item_type=InvoiceSummaryItem.InvoiceSummaryItemType.TAX
        ).values("amount")
        tax_invoices = monthly_invoices.annotate(tax_amount=Subquery(sub))
        summary.rows[current_row][summary_key] = tax_invoices.aggregate(Sum("tax_amount"))[
            "tax_amount__sum"
        ] or Decimal(0)
        current_row += 1  # For mid table header
    if ProjectDiscipline.objects.exists():
        for discipline in ProjectDiscipline.objects.all():
            current_row += 1
            summary.rows[current_row][summary_key] = monthly_invoices.filter(
                project_details__project__discipline=discipline
            ).aggregate(Sum("total_amount"))["total_amount__sum"] or Decimal(0)
        current_row += 1
        summary.rows[current_row][summary_key] = monthly_invoices.filter(
            project_details__project__discipline__isnull=True
        ).aggregate(Sum("total_amount"))["total_amount__sum"] or Decimal(0)
        current_row += 1  # For mid table header
    if AccountType.objects.exists():
        for account_type in AccountType.objects.all():
            current_row += 1
            summary.rows[current_row][summary_key] = monthly_invoices.filter(
                project_details__project__account__type=account_type
            ).aggregate(Sum("total_amount"))["total_amount__sum"] or Decimal(0)
        current_row += 1
        summary.rows[current_row][summary_key] = monthly_invoices.filter(
            project_details__project__account__type__isnull=True
        ).aggregate(Sum("total_amount"))["total_amount__sum"] or Decimal(0)
        current_row += 1  # For mid table header
    if RateCategory.objects.exists():
        for category in RateCategory.objects.all():
            current_row += 1
            summary.rows[current_row][summary_key] = monthly_invoices.filter(
                project_details__category=category
            ).aggregate(Sum("total_amount"))["total_amount__sum"] or Decimal(0)
        current_row += 1  # For mid table header
    current_row += 1
    params = ReportingParameters(request)
    remote_amount, remote_items = get_invoice_items(params, start, end, Q(remote=True))
    summary.rows[current_row][summary_key] = remote_amount
    current_row += 1
    onsite_amount, onsite_items = get_invoice_items(params, start, end, Q(remote=False))
    summary.rows[current_row][summary_key] = onsite_amount


def get_invoice_query_set(start: datetime.datetime, end: datetime.datetime) -> QuerySet[Invoice]:
    projects_to_exclude = ReportsCustomization.get_excluded_project_ids()
    query = Invoice.objects.filter(voided_date__isnull=True, start__gte=start, start__lte=end)
    if projects_to_exclude:
        query = query.exclude(project_details__project_id__in=projects_to_exclude)
    return query
