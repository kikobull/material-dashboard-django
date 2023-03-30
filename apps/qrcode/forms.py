# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms


class NewVisitorForm(forms.Form):
    gender = (
        ("M","Male"),
        ("F","Female")
    )
    firstname = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastname = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(choices=gender)
    notes = forms.CharField(max_length=400,required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))    
    email = forms.CharField(max_length=100,required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))

 
