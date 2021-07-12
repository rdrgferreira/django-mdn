import datetime

from django.forms import fields
from catalog.models import BookInstance

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


# Maneira mais simples de fazer, quando se trabalha apenas com poucos campos de um Model
class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text="Enter a date between now and 4 weeks (default 3).", label=_('New renewal date'))

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check if a data is not in the past
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4weeks from today)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 5 weeks ahead'))

        return data


class RenewBookModelForm(forms.ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        # Check if a data is not in the past
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4weeks from today)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 5 weeks ahead'))

        # Remember to always return the cleaned data
        return data
    
    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('New renewal date')}
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}
