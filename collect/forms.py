from django import forms

class EmailForm(forms.Form):
    subject = forms.CharField(label = 'Subject', initial = 'SUBJECT_PLACEHOLDER', max_length = 100)
    body = forms.CharField(widget = forms.Textarea, initial = 'BODY_PLACEHOLDER', label = 'Body')
    recipient = forms.EmailField(widget = forms.HiddenInput())
