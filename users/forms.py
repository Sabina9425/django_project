from django.contrib.auth.forms import UserCreationForm

from catalog.forms import StyleFormMixIn
from users.models import User


class UserRegistrationForm(StyleFormMixIn, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")


