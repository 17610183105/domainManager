from django import template


register = template.Library()

@register.filter
def show_ns(value):
    info = []
    for obj in value.all():
        info.append(obj)
    return "|".join(info)

