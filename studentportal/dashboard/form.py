from django import forms
from .models import Notes,Homework,Todo

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



class DashboardForm(forms.Form):
    text = forms.CharField(max_length=200,label='enter your serach here  ')


class TodoForm(forms.ModelForm):
    class Meta:
        model=Todo
        fields=['title','is_finished']

