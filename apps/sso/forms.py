from django import forms
from django.forms import CheckboxSelectMultiple

from apps.sso.models import AccessAgreement, Feature


class BootstrapCheckboxSelectMultiple(CheckboxSelectMultiple):
    template_name = 'sso/bootstrap-fields/checkbox-select.html'


class AccessAgreementPermissionForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(widget=BootstrapCheckboxSelectMultiple(), queryset=Feature.objects.all())

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            # We get the 'initial' keyword argument or initialize it
            # as a dict if it didn't exist.
            kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            self.instance = kwargs['instance']
            if self.instance.is_signed:
                kwargs['initial']['permissions'] = [t.pk for t in self.instance.permissions.all().only('pk')]
            else:
                kwargs['initial']['permissions'] = [t.pk for t in self.instance.client.required_features.all().only('pk')]
        super().__init__(*args, **kwargs)

    class Meta:
        model = AccessAgreement
        fields = ('permissions', )


