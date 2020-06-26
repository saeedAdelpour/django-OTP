from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class PostModelForm(forms.ModelForm):

  class Meta:
    model = Post
    fields = ["title", "description"]

  def clean_title(self, *args, **kwargs):
    title = self.cleaned_data.get("title")
    if(len(title) < 3):
      raise ValidationError("error: len < 3")
    return title

  def clean_description(self, *args, **kwargs):
    description = self.cleaned_data.get("description")
    if len(description) < 5:
      raise ValidationError("error: len < 5")
    return description
