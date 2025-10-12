from django import template
register=template.Library()
@register.filter
def add_class(f,c):return f.as_widget(attrs={'class':c})
