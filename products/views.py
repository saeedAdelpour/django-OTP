from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.views.generic.base import ContextMixin, TemplateResponseMixin
class AboutTemplateView(TemplateView):
  template_name = 'products/template.html'

  def get_context_data(self, *args, **kwargs):
    context = super(AboutTemplateView, self).get_context_data(*args, **kwargs)
    context["about"] = "about context"
    return context

class MyTemplateView(ContextMixin, TemplateResponseMixin, View):
  
  def get(self, request, *args, **kwargs):
    context = self.get_context_data(**kwargs)
    context["title"] = "this is from 'MyTemplateView'"
    return self.render_to_response(context)