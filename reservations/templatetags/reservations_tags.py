from django import template

register = template.Library()

@register.inclusion_tag('reservations/_info_tag.html')
def info_tag(reservation):
    return {'reservation':reservation,}

