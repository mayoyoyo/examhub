from django import template
from django import forms

register = template.Library()

@register.filter
def filter_section(passages, section):
    """Filter passages by section and return only those with questions"""
    section_num = int(section)
    return [p for p in passages if p.section == section_num and hasattr(p, 'question')]

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
        return form[key] if key in form.fields else None
    elif isinstance(form, dict):
        return form.get(key)
    return None

@register.filter
def get_answer(student_exam, question):
    """Get a student's answer for a specific question"""
    try:
        return student_exam.answers.get(question=question)
    except student_exam.answers.model.DoesNotExist:
        return None