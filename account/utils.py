from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
from django.core.validators import BaseValidator
from datetime import date


class TokenGenerator(PasswordResetTokenGenerator):
    pass
    # def _make_hash_value(self, user, timestamp):
    #     return (
    #         six.text_type(user.pk) + six.text_type(timestamp)+ six.text_type(user.is_active)
    #
    #     )

account_activation_token = TokenGenerator()


def calculate_age(born):
    today = date.today()
    return today.year - born.year - \
           ((today.month, today.day) < (born.month, born.day))

@deconstructible
class MinAgeValidator(BaseValidator):
    message = _("Age must be at least %(limit_value)d.")
    code = 'min_age'

    def compare(self, a, b):
        return calculate_age(a) < b
