from django import forms
from django.forms import modelformset_factory
from .models import Episode, Heroine, Father, Child, Marker


class EpisodeForm(forms.ModelForm):
    class Meta:
        model = Episode
        fields = ["season_number", "episode_number", "city"]
        widgets = {
            "season_number": forms.NumberInput(attrs={"class": "form-control"}),
            "episode_number": forms.NumberInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
        }


class HeroineForm(forms.ModelForm):
    class Meta:
        model = Heroine
        fields = ["heroine_name", "heroine_age", "heroine_photo"]
        widgets = {
            "heroine_name": forms.TextInput(attrs={"class": "form-control"}),
            "heroine_age": forms.NumberInput(attrs={"class": "form-control"}),
            "heroine_photo": forms.FileInput(attrs={"class": "form-control"}),
        }


class FatherForm(forms.ModelForm):
    class Meta:
        model = Father
        fields = ["father_name", "father_age", "father_photo"]
        widgets = {
            "father_name": forms.TextInput(attrs={"class": "form-control"}),
            "father_age": forms.NumberInput(attrs={"class": "form-control"}),
            "father_photo": forms.FileInput(attrs={"class": "form-control"}),
        }
        required = {
            "father_name": False,
            "father_age": False,
            "father_photo": False,
        }

def child_formset_factory(num_extra_forms):
    ChildFormSet = modelformset_factory(
        Child,
        fields=("child_name",),
        extra=num_extra_forms,
        widgets={
            "child_name": forms.TextInput(attrs={"class": "form-control"}),
        },
    )
    return ChildFormSet

class MarkerForm(forms.ModelForm):
    class Meta:
        model = Marker
        fields = ["latitude", "longitude"]
        widgets = {
            "latitude": forms.NumberInput(attrs={"class": "form-control"}),
            "longitude": forms.NumberInput(attrs={"class": "form-control"}),
        }
