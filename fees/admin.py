# vim: set fileencoding=utf-8 :
from django.contrib import admin

from . import models


class FeeHeadAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'is_active')
    search_fields = ('name', 'code')


class FeeStructureAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'fee_head', 'class_name', 'session',
        'frequency', 'amount', 'is_active',
    )
    list_filter = ('session', 'frequency', 'class_name')
    search_fields = ('fee_head__name', 'class_name__name')


class PaymentInline(admin.TabularInline):
    model = models.Payment
    extra = 0
    readonly_fields = ('receipt_no',)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_no', 'student', 'fee_head', 'amount',
        'discount', 'status', 'due_date',
    )
    list_filter = ('status', 'session', 'class_name')
    search_fields = ('invoice_no', 'student__name', 'student__unique_roll')
    readonly_fields = ('invoice_no',)
    inlines = [PaymentInline]


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('receipt_no', 'invoice', 'amount', 'method', 'paid_on', 'received_by')
    list_filter = ('method', 'paid_on')
    search_fields = ('receipt_no', 'invoice__invoice_no')
    readonly_fields = ('receipt_no',)


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.FeeHead, FeeHeadAdmin)
_register(models.FeeStructure, FeeStructureAdmin)
_register(models.Invoice, InvoiceAdmin)
_register(models.Payment, PaymentAdmin)
