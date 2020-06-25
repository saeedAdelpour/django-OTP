from django.db import models
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from django.contrib.auth.models import User
from django.db.models.signals import pre_save

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

class Snippet(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  title = models.CharField(max_length=100, blank=True, default='')
  code = models.TextField()
  linenos = models.BooleanField(default=False)
  language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
  style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
  owner = models.ForeignKey(User, related_name='snippets', on_delete=models.CASCADE)
  highlighted = models.TextField(null=True)

  class Meta:
    ordering = ['created']

def snippet_pre_save(sender, instance, **kwargs):
  lexer = get_lexer_by_name(instance.language)
  linenos = 'table' if instance.linenos else False
  options = {'title': instance.title} if instance.title else {}
  formatter = HtmlFormatter(style=instance.style, linenos=linenos,full=True, **options)
  instance.highlighted = highlight(instance.code, lexer, formatter)


pre_save.connect(snippet_pre_save, sender=Snippet)