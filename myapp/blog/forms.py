from django import forms

class ContactForm(forms.Form):
    name=forms.CharField(label='name',max_length=100,required=True)
    email =forms.EmailField(label='Email',required=True)
    message =forms.CharField(label='message',required=True)