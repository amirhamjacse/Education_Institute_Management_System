from django.urls import path
from fees import views

app_name = 'fees'

urlpatterns = [
    path('fee-heads/', views.FeeHeadListView.as_view(), name='fee_head_list'),

    path('fee-structures/', views.FeeStructureListView.as_view(), name='fee_structure_list'),
    path('fee-structures/add/', views.FeeStructureCreateView.as_view(), name='fee_structure_add'),
    path('fee-structures/<int:pk>/edit/', views.FeeStructureUpdateView.as_view(), name='fee_structure_edit'),

    path('invoices/generate/', views.InvoiceGenerateQueryView.as_view(), name='invoice_generate_query'),
    path(
        'invoices/generate/<int:cls>/<int:sec>/<int:fs>/<str:period>/<str:due_date>/',
        views.InvoiceGenerateBulkView.as_view(), name='invoice_generate_bulk'
    ),
    path('invoices/generate/adhoc/', views.AdHocInvoiceCreateView.as_view(), name='invoice_adhoc'),

    path('invoices/', views.InvoiceListView.as_view(), name='invoice_list'),
    path('invoices/mine/', views.MyInvoicesView.as_view(), name='my_invoices'),
    path('invoices/<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoices/<int:pk>/receipt/', views.InvoiceReceiptPrintView.as_view(), name='invoice_receipt'),
    path('invoices/overdue/', views.OverdueInvoiceListView.as_view(), name='invoice_overdue'),

    path('report/', views.FeeCollectionReportView.as_view(), name='fee_report'),
]
