import re
from datetime import date
from calendar import monthrange, IllegalMonthError
from django.conf import settings
from django import forms
from django.forms.widgets import TextInput
from django.utils.translation import ugettext_lazy as _

MONTH_FORMAT = getattr(settings, 'MONTH_FORMAT', '%b')
VERIFICATION_VALUE_RE = r'^([0-9]{3,4})$'


class OrderForm(forms.Form):
    quantity = forms.IntegerField(min_value=0, initial=0, required=False)


class IngredientForm(forms.Form):
    name = forms.CharField(help_text="Ingredient name")
    quantity = forms.IntegerField(help_text="Amount ordered or currently in stock", initial=0)


class RestockForm(forms.Form):
    name = forms.CharField(help_text="Ingredient name")
    quantity = forms.IntegerField(help_text="Amount you wish to order", initial=0)


class PushOrder(forms.Form):
    orderid = forms.IntegerField(help_text="Order number you wish to mark complete", initial=0)


class TelephoneInput(TextInput):
    # switch input type to type tel so that the numeric keyboard shows on mobile devices
    input_type = 'tel'


class CreditCardField(forms.CharField):
    # validates almost all of the example cards from PayPal
    # https://www.paypalobjects.com/en_US/vhelp/paypalmanager_help/credit_card_numbers.htm
    cards = [
        {
            'type': 'maestro',
            'patterns': [5018, 502, 503, 506, 56, 58, 639, 6220, 67],
            'length': [12, 13, 14, 15, 16, 17, 18, 19],
            'cvvLength': [3],
            'luhn': True
        }, {
            'type': 'forbrugsforeningen',
            'patterns': [600],
            'length': [16],
            'cvvLength': [3],
            'luhn': True
        }, {
            'type': 'dankort',
            'patterns': [5019],
            'length': [16],
            'cvvLength': [3],
            'luhn': True
        }, {
            'type': 'visa',
            'patterns': [4],
            'length': [13, 16],
            'cvvLength': [3],
            'luhn': True
        }, {
            'type': 'mastercard',
            'patterns': [51, 52, 53, 54, 55, 22, 23, 24, 25, 26, 27],
            'length': [16],
            'cvvLength': [3],
            'luhn': True
        }, {
            'type': 'amex',
            'patterns': [34, 37],
            'length': [15],
            'cvvLength': [3, 4],
            'luhn': True
        }, {
            'type': 'dinersclub',
            'patterns': [30, 36, 38, 39],
            'length': [14],
            'cvvLength': [3],
            'luhn': True
        }, {
            'type': 'discover',
            'patterns': [60, 64, 65, 622],
            'length': [16],
            'cvvLength': [3],
            'luhn': True
        }, {
            'type': 'unionpay',
            'patterns': [62, 88],
            'length': [16, 17, 18, 19],
            'cvvLength': [3],
            'luhn': False
        }, {
            'type': 'jcb',
            'patterns': [35],
            'length': [16],
            'cvvLength': [3],
            'luhn': True
        }
    ]

    def __init__(self, placeholder=None, *args, **kwargs):
        super(CreditCardField, self).__init__(
            # override default widget
            widget=TelephoneInput(attrs={
                'placeholder': placeholder
            })
            , *args, **kwargs)

    default_error_messages = {
        'invalid': _(u'The credit card number is invalid'),
    }

    def clean(self, value):

        # ensure no spaces or dashes
        value = value.replace(' ', '').replace('-', '')

        # get the card type and its specs
        card = self.card_from_number(value)

        # if no card found, invalid
        if not card:
            raise forms.ValidationError(self.error_messages['invalid'])

        # check the length
        if not len(value) in card['length']:
            raise forms.ValidationError(self.error_messages['invalid'])

        # test luhn if necessary
        if card['luhn']:
            if not self.validate_mod10(value):
                raise forms.ValidationError(self.error_messages['invalid'])

        return value

    def card_from_number(self, num):
        # find this card, based on the card number, in the defined set of cards
        for card in self.cards:
            for pattern in card['patterns']:
                if str(pattern) == str(num)[:len(str(pattern))]:
                    return card

    def validate_mod10(self, num):
        # validate card number using the Luhn (mod 10) algorithm
        checksum, factor = 0, 1
        for c in reversed(num):
            for c in str(factor * int(c)):
                checksum += int(c)
            factor = 3 - factor
        return checksum % 10 == 0


class ExpiryDateWidget(forms.MultiWidget):
    """
    Widget containing two select boxes for selecting the month and year.
    """

    def decompress(self, value):
        return [value.month, value.year] if value else [None, None]

    def format_output(self, rendered_widgets):
        return u'<div class="expirydatefield">%s</div>' % ' '.join(rendered_widgets)


class ExpiryDateField(forms.MultiValueField):
    """
    Form field that validates credit card expiry dates.
    """

    default_error_messages = {
        'invalid_month': _(u'Please enter a valid month.'),
        'invalid_year': _(u'Please enter a valid year.'),
        'date_passed': _(u'This expiry date has passed.'),
    }

    def __init__(self, *args, **kwargs):
        today = date.today()
        error_messages = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            error_messages.update(kwargs['error_messages'])
        if 'initial' not in kwargs:
            # Set default expiry date based on current month and year
            kwargs['initial'] = today
        months = [(x, '%02d (%s)' % (x, date(2000, x, 1).strftime(MONTH_FORMAT))) for x in range(1, 13)]
        years = [(x, x) for x in range(today.year, today.year + 15)]
        fields = (
            forms.ChoiceField(choices=months, error_messages={'invalid': error_messages['invalid_month']}),
            forms.ChoiceField(choices=years, error_messages={'invalid': error_messages['invalid_year']}),
        )
        super(ExpiryDateField, self).__init__(fields, *args, **kwargs)
        self.widget = ExpiryDateWidget(widgets=[fields[0].widget, fields[1].widget])

    def clean(self, value):
        expiry_date = super(ExpiryDateField, self).clean(value)
        if date.today() > expiry_date:
            raise forms.ValidationError(self.error_messages['date_passed'])
        return expiry_date

    def compress(self, data_list):
        if data_list:
            try:
                month = int(data_list[0])
            except (ValueError, TypeError):
                raise forms.ValidationError(self.error_messages['invalid_month'])
            try:
                year = int(data_list[1])
            except (ValueError, TypeError):
                raise forms.ValidationError(self.error_messages['invalid_year'])
            try:
                day = monthrange(year, month)[1]  # last day of the month
            except IllegalMonthError:
                raise forms.ValidationError(self.error_messages['invalid_month'])
            except ValueError:
                raise forms.ValidationError(self.error_messages['invalid_year'])
            return date(year, month, day)
        return None


class VerificationValueField(forms.CharField):
    """
    Form field that validates credit card verification values (e.g. CVV2).
    See http://en.wikipedia.org/wiki/Card_Security_Code
    """

    widget = forms.TextInput(attrs={'maxlength': 4})
    default_error_messages = {
        'required': _(u'Please enter the three- or four-digit verification code for your credit card.'),
        'invalid': _(u'The verification value you entered is invalid.'),
    }

    def clean(self, value):
        value = value.replace(' ', '')
        if not value and self.required:
            raise forms.util.ValidationError(self.error_messages['required'])
        if value and not re.match(VERIFICATION_VALUE_RE, value):
            raise forms.util.ValidationError(self.error_messages['invalid'])
        return value


class CardForm(forms.Form):
    cardholder = forms.CharField(max_length=50, required=True)
    card_number = CreditCardField(placeholder=u'0000 0000 0000 0000', min_length=12, max_length=19)
    exp_date = ExpiryDateField(required=True)
    cvv=VerificationValueField(required=True)
