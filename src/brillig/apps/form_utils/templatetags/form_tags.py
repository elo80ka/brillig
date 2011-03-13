from django import forms, template
from django.forms import formsets
from django.conf import settings
from django.forms.util import ErrorDict
from django.template import Library, Variable
from django.utils.safestring import mark_safe

register = Library()

@register.inclusion_tag('form_utils/summary.html')
def render_form_errors(msg, *forms):
    form_list = []
    for f in forms:
        if isinstance(f, forms.BaseForm):
            form_list.append(f)
        elif isinstance(f, formsets.BaseFormSet):
            form_list.extend(f.forms)
        else:
            raise TypeError('Arguments should be instances of a Form or subclasses.')
    error_list = []
    for form in form_list:
        error_list.extend(form.non_field_errors())
    return {
        'form_list': form_list,
        'error_list': error_list,
        'message': msg,
    }

@register.filter
def is_boolean(fld):
    return isinstance(fld.field, forms.BooleanField)

@register.filter
def is_radio(fld):
    return isinstance(fld.field.widget, forms.RadioSelect)

@register.filter
def format_label(fld, required_fmt=u'%s', optional_fmt=u'%s'):
    return (fld.label and (fld.field.required and (required_fmt % fld.label) or (optional_fmt % fld.label)) or u'')

@register.simple_tag
def render_default_media():
    """Render default form media, if defined in settings.py.
    """
    default_css = getattr(settings, 'DEFAULT_FORM_CSS', ())
    default_js = getattr(settings, 'DEFAULT_FORM_JS', ())
    out = []

    for media, stylesheets in default_css.items():
        for stylesheet in stylesheets:
            out.append(u'<link rel="stylesheet" type="text/css" href="%s%s" media="%s" />' % (
                settings.MEDIA_URL, stylesheet, media
            ))
    for js in default_js:
        out.append(u'<script type="text/javascript" src="%s%s"></script>' % (
            settings.MEDIA_URL, js
        ))

    return mark_safe(u'\n'.join(out))

@register.inclusion_tag('form_utils/field.html')
def render_form_row(form, field_name, show_help=True):
    """Renders a bound form field using the `form_utils/field.html` template.
    """
    return {
        'field': form[field_name],
        'show_help': show_help,
    }

@register.inclusion_tag('form_utils/form.html')
def render_form(form, show_help=True):
    """Renders a bound form using the `form_utils/form.html` template.
    """
    return {
        'form': form,
        'show_help': show_help,
    }
