from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class SymbolValidator:
    def validate(self, password, user=None):
        if not any(char in set('!@#$%^&*()_+-=[]{}|;:,.<>?/~`') for char in password):
            raise ValidationError(
                _("The password must contain at least one symbol: " + ''.join('!@#$%^&*()_+-=[]{}|;:,.<>?/~`')),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least one symbol: " + ''.join('!@#$%^&*()_+-=[]{}|;:,.<>?/~`')
        )

class UppercaseValidator:
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("The password must contain at least one uppercase letter."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _("Your password must contain at least one uppercase letter.")

class LowercaseValidator:
    def validate(self, password, user=None):
        if not any(char.islower() for char in password):
            raise ValidationError(
                _("The password must contain at least one lowercase letter."),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _("Your password must contain at least one lowercase letter.")
