from datetime import date, timedelta

from django import forms

class BootstrapTextInput(forms.TextInput):
    def init(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "form-control form-control-lg bg-white"
        super().init(*args, **kwargs)

# Define a custom widget class with Bootstrap styling for select fields
class BootstrapSelect(forms.Select):
    def init(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "form-control form-control-lg bg-white"
        super().init(*args, **kwargs)


class BootstrapDateInput(forms.DateInput):
    def init(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "form-control form-control-lg datepicker"
        super().init(*args, **kwargs)