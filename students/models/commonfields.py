from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone



class CommonFields(models.Model):
    is_active = models.BooleanField(
        _('Is Active'), default=True
    )
    is_deleted = models.BooleanField(
        _('Is Deleted'), default=False
    )
    created_time = models.DateTimeField(
        _('Created At'), auto_now_add=True, null=True
    )
    order = models.PositiveIntegerField(
        _("Order"), blank=True, null=True
    )
    display_order = models.CharField(
        _("Display Order"), max_length=50, blank=True, null=True
    )
    last_updated = models.DateTimeField(
        _('Last Updated'), auto_now=True, null=True,
    )
    deleted_at = models.DateTimeField(
        _('Deleted At'), blank=True, null=True
    )
    # created_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
    #     blank=True, null=True, related_name="%(app_label)s_%(class)s_created"
    # )
    # updated_user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
    #     blank=True, null=True, related_name="%(app_label)s_%(class)s_updated"
    # )
    # deleted_user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
    #     blank=True, null=True, related_name="%(app_label)s_%(class)s_deleted"
    # )

    def soft_delete(self):
        self.is_deleted = True
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()

    def soft_deactivate(self):
        self.is_active = False
        self.save()

    class Meta:
        abstract = True