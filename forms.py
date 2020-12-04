from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import ugettext as _
from toolbox.forms import CaptchaModelForm
from postman.models import Email, Recipient


def _phone_validator(value):
    for c in value:
        if c == ' ' or c == '+' or (ord('0') <= ord(c) <= ord('9')):
            continue

        raise ValidationError(_("Your phone number is invalid. Only +, ,0,...,9 are allowed."), code='Invalid')


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient

        fields = ['email', 'is_default']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'is_default': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            })
        }

    @staticmethod
    def clean_default():
        count_default = Recipient.objects.filter(default=True).count()
        if count_default > 1:
            raise ValidationError(_('You can only set one recipient as default.'), code='Invalid')


class EmailForm(CaptchaModelForm):
    class Meta:
        model = Email

        fields = [
            'company',
            'first_name',
            'last_name',
            'email',
            'telephone',
            'message',
            'privacy_accepted',
        ]

        widgets = {
            'company': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'tel',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
            }),
            'privacy_accepted': forms.CheckboxInput(attrs={
                'class': 'custom-control-input',
            }),
            'sent': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'disabled': '',
            }),
            'received_on': forms.DateTimeInput(attrs={
                'class': 'form-check-input',
                'disabled': '',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].label = _("Company")
        self.fields['first_name'].label = "%s *" % _("First name")
        self.fields['last_name'].label = "%s *" % _("Last name")
        self.fields['email'].label = "%s *" % _("Email")
        self.fields['telephone'].label = _("Telephone")
        self.fields['message'].label = "%s *" % _("Message")
        self.fields['privacy_accepted'].label = "%s *" % _("I have read and accepted the privacy policy")

    def clean_privacy_accepted(self):
        if not self.cleaned_data.get('privacy_accepted', False):
            raise ValidationError(_('You have to accept our privacy policy to send a message'), code='Invalid')

        return True

    def clean(self):
        clean = super().clean()
        if not Recipient.objects.count():
            raise ValidationError(_('There are currently no recipients to send to'), code='Invalid')

        if not hasattr(settings, 'EMAIL_FROM'):
            raise ValidationError(_('There is currently no mail server configured'), code='Invalid')

        return clean


class EmailAdminForm(EmailForm):
    class Meta:
        widgets = {
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'disabled': '',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'disabled': '',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'disabled': '',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'disabled': '',
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'tel',
                'disabled': '',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'disabled': '',
            }),
            'privacy_accepted': forms.CheckboxInput(attrs={
                'class': 'custom-control-input',
                'disabled': '',
            }),
            'sent': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'disabled': '',
            }),
            'received_on': forms.DateTimeInput(attrs={
                'class': 'form-check-input',
                'disabled': '',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
