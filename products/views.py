from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator # way 1
# from django.contrib.auth.mixins import LoginRequiredMixin

class LoginRequiredMixin(object):

  # way2
  @classmethod
  def as_view(cls, **kwargs):
    view = super(LoginRequiredMixin, cls).as_view(**kwargs)
    return login_required(view)

  # way 3
  # @method_decorator(login_required)
  # def dispatch(self, request, *args, **kwargs):
  #   return super().dispatch(request, *args, **kwargs)

class AboutTemplateView(LoginRequiredMixin, TemplateView):
  template_name = 'products/template.html'

  def get_context_data(self, *args, **kwargs):
    context = super(AboutTemplateView, self).get_context_data(*args, **kwargs)
    context["about"] = "about context"
    return context

class MyTemplateView(ContextMixin, TemplateResponseMixin, LoginRequiredMixin, View):
  
  def get(self, request, *args, **kwargs):
    context = self.get_context_data(**kwargs)
    context["title"] = "this is from 'MyTemplateView'"
    return self.render_to_response(context)

  # way 4 => for eatch dispath must do this decoration
  # @method_decorator(login_required)
  # def dispatch(self, request, *args, **kwargs):
  #   return super().dispatch(request, *args, **kwargs)