from django import template
import re

register = template.Library()

MSISDN_RE = re.compile(r'(\d{3})(\d{3})(\d{3})(\d+)')

@register.filter
def format_phone_number(value):
    return MSISDN_RE.sub(r'(\1) \2-\3-\4', value)
