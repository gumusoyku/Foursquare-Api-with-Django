#-*- coding: utf-8 -*-
from __future__ import absolute_import

from django import forms

# where I handled the forms objects
class Index_Form(forms.Form):
    objct = forms.CharField(max_length = 25, initial = "I am looking for ..")
    location = forms.CharField(max_length = 25, initial = "Location ..")