from django import template
from django import forms

register = template.Library()

@register.filter
def has_passages_in_section(passages, section):
    """Check if there are any passages in the given section"""
    section_num = int(section)
    return any(p.section == section_num for p in passages)

@register.filter
def dict_lookup(form, key):
    """Look up a form field or dictionary value by key"""
    if hasattr(form, key):
        return getattr(form, key)
    elif isinstance(form, forms.Form):
        return form[key]
    elif isinstance(form, dict):
        return form.get(key)
    return None