from django.urls import include, path

from NEMO_reports.views import (
    reporting,
    reporting_facilily_usage,
    reporting_unique_user_prj_acc,
)

urlpatterns = [
    path("reporting/", include([
        path("", reporting.reports, name="reporting"),
        path("facility_usage/", reporting_facilily_usage.facility_usage, name="reporting_facility_usage"),
        path("unique_users/", reporting_unique_user_prj_acc.unique_users, name="reporting_unique_users"),
        path("unique_user_project/", reporting_unique_user_prj_acc.unique_user_and_project_combinations, name="reporting_unique_user_project"),
        path("unique_user_account/", reporting_unique_user_prj_acc.unique_user_and_account_combinations, name="reporting_unique_user_account"),
    ])),
]

if reporting.billing_installed():
    from NEMO_reports.views import reporting_invoice_charges, reporting_invoice_item_charges
    urlpatterns += [
        path("reporting/invoice_charges/", reporting_invoice_charges.invoice_charges, name="reporting_invoice_charges"),
        path("reporting/invoice_item_charges/", reporting_invoice_item_charges.invoice_items, name="reporting_invoice_item_charges")
    ]
