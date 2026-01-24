from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

BASE_INPUT_CLASSES = (
    "block w-full rounded-lg border border-slate-300 bg-white "
    "px-3 py-2 text-sm shadow-sm "
    "placeholder:text-slate-400 "
    "focus:border-slate-900 focus:ring-2 focus:ring-slate-900/20"
)

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": BASE_INPUT_CLASSES,
            })

        fields_without_helptext = {'username', 'password1', 'password2'}

        for field in fields_without_helptext:
            self.fields[field].help_text = ''

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": BASE_INPUT_CLASSES})

        # falls irgendwo help_text gesetzt wäre: entfernen
        for name in self.fields:
            self.fields[name].help_text = ""