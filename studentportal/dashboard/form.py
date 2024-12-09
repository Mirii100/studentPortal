from django import forms
from .models import Notes,Homework

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'description']




class DateInput(forms.DateInput):
    input_type = 'date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets ={'due_date':DateInput}
        fields = ['title', 'subject','description', 'due_date','is_finised']

