from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from typing import Any

from .models import Announcement


class AuthenticationForm(AuthenticationForm):

    def __init__(self, request: Any = ..., *args: Any, **kwargs: Any) -> None:
        super().__init__(request, *args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class UserCreationForm(UserCreationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class AnnouncementForm(forms.ModelForm):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name not in ["category"]:
                field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Announcement
        fields = ["title", "description", "category", "price", "owner"]
