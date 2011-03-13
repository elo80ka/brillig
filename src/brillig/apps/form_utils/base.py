from django import forms
from django.conf import settings

class MediaMixin(object):
    """
    Mix-in used to add default form media.
    """
    @property
    def media(self):
        media = forms.Media(
            extend=True,
            css=getattr(settings, 'DEFAULT_FORM_CSS', None),
            js=getattr(settings, 'DEFAULT_FORM_JS', None)
        )
        for fld_name in self.fields:
            media += self.fields[fld_name].widget.media
        return media

class ModelForm(MediaMixin, forms.ModelForm):
    """
    ModelForm base class, which automatically adds the default form media.
    """

class Form(MediaMixin, forms.Form):
    """
    Form base class, which automatically adds the default form media.
    """
