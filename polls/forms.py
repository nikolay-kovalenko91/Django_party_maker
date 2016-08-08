# -*- coding: utf-8 -*-
from django import forms
from .models import Poll

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ('drink', 'presence')