from django import forms
from django.utils.html import html_safe
import os

class AvatarFileUploadInput(forms.ClearableFileInput):    
    template_name = "AvatarFileUploadInput.html"
    def get_context(self, name, value, attrs):
        if value:
            value.name = os.path.basename(value.name)
        context = super().get_context(name, value, attrs)       
        return context

class JalaliDateWidget(forms.TextInput):
    '''
    @property
    def media(self):
        js = ('persianDatepicker.js',)
        css = {'all' : ('persianDatepicker-default.css',) }
        return forms.Media(js=js, css=css)
    '''
    class Media:
        js = ('persianDatepicker.js',)
        css = {  'all' : ('persianDatepicker-default.css',) }

    def __init__(self, attrs=None):
        final_attrs = {'class': 'parsDate'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(JalaliDateWidget, self).__init__(attrs=final_attrs)


