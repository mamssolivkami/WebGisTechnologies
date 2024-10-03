from django import forms
from .models import Episode, Heroine, Father, Child, Marker

class EpisodeForm(forms.ModelForm):
    class Meta:
        model = Episode
        fields = ['season_number', 'episode_number', 'city']

class HeroineForm(forms.ModelForm):
    class Meta:
        model = Heroine
        fields = ['heroine_name', 'heroine_age', 'heroine_photo', 'episode']

class FatherForm(forms.ModelForm):
    class Meta:
        model = Father
        fields = ['father_name', 'father_age', 'father_photo', 'episode']

class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['child_name', 'episode']

class MarkerForm(forms.ModelForm):
    class Meta:
        model = Marker
        fields = ['episode', 'latitude', 'longitude']
