from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from apps.sso.models import Client, Feature, AuthTransaction, AccessAgreement

# Register your models here.

admin.site.register(Client)
admin.site.register(Feature)

class ReadOnlyAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


class AuthTransactionAdmin(ReadOnlyAdmin):
    list_display = ('id', 'state_label', 'txn_token', 'agreement_link', 'updated_at')

    def get_queryset(self, request):
        return AuthTransaction.objects.select_related('agreement', 'agreement__client', 'agreement__user')

    def agreement_link(self, obj):
        change_url = reverse('admin:sso_accessagreement_change', args=[obj.agreement.id])
        return format_html('<a href="{}">{}</a>', change_url, obj.agreement)

    agreement_link.allow_tags = True
    agreement_link.short_description = 'Access Agreement'



admin.site.register(AccessAgreement, ReadOnlyAdmin)
admin.site.register(AuthTransaction, AuthTransactionAdmin)