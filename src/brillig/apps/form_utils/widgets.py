from django import forms
from django.forms import fields, widgets
from django.utils import datetime_safe
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from datetime import date

class DateFieldMixin(object):
    """
    Form Helper: modify all date fields in the subclassing form to use the calendar widget.
    """
    def __init__(self, *args, **kwargs):
        super(DateFieldMixin, self).__init__(*args, **kwargs)
        for fld_name in self.fields:
            fld = self.fields[fld_name]
            if isinstance(fld, (fields.DateField, fields.DateTimeField)):
                fld.input_formats = ('%d/%m/%Y',)
                fld.widget = CalendarWidget(attrs=fld.widget.attrs, format=fld.input_formats[0])

class CalendarWidget(widgets.TextInput):
    """A Calendar widget, which uses the jQuery UI Calendar."""

    class Media:
        extend = True
        css = {
            'all': ('css/jquery-ui-theme.css',)
        }
        js = ('js/ui.datepicker.js', 'js/calendar-init.js',)

    def __init__(self, attrs=None, format=None):
        super(CalendarWidget, self).__init__(attrs)
        self.attrs['class'] = 'vDateField'
        if format:
            self.format = format

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        elif hasattr(value, 'strftime'):
            value = datetime_safe.new_date(value).strftime(self.format)
        return super(CalendarWidget, self).render(name, value, attrs)

class RatingFieldRenderer(widgets.RadioFieldRenderer):
    """
    Custom rendering for the RadioSelect so it works better with our javascript.
    """

    def __iter__(self):
        for i, choice in enumerate(self.choices):
            if i == 0:
                # Hacky: Skip first (expected blank) option
                continue
            yield widgets.RadioInput(self.name, self.value, self.attrs.copy(), (choice[0], ''), i)

    def render(self):
        """Output a <p> enclosing this set of radio fields."""
        return mark_safe(u'<p class="vRatingField">%s</p>' % u'\n'.join([force_unicode(r) for r in self]))

class RatingWidget(widgets.RadioSelect):
    renderer = RatingFieldRenderer

    class Media:
        extend = True
        css = {
            'all': ('css/rating.css',)
        }
        js = ('js/jquery.rating.js',)
