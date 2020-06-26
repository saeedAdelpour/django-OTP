from django.shortcuts import render
from .forms import PostModelForm

def my_form(request):
  form = PostModelForm(request.POST or None)
  if form.is_valid():
    form.save()

  return render(request, 'core/forms.html', {"form": form})