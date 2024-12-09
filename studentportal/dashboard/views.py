from django.shortcuts import render,redirect
from django.views import generic
from .form import *
from.models import Homework
from django.contrib import messages
# Create your views here.
def dashboard_view(request):
    return render(request,'home.html')


def notes_view(request):
    if request.method=='POST':
        form=NotesForm(request.POST)
        if form.is_valid():
            notes=Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
            
        messages.success(request,f'Successfully added new from {request.user.username}')


    else:
        form=NotesForm()
    form=NotesForm()
    notes=Notes.objects.filter(user=request.user)
    context={'notes':notes,'form':form}
    return render(request,'notes.html',context)


def deleteNote(request,pk=None):
    Notes.objects.get(id=pk).delete()

    return redirect('notes')


class  NoteDetailView(generic.DetailView):
    model=Notes
    template_name='notes_detail.html'
    



def homework(request):
    if request.method=='POST':
        form=HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST['is_finised']
                if finished=='on':
                    finished=True
                else:
                    finished=False


            except KeyError:
                finished=False
            homeworks=Homework
            homework=Homework(user=request.user,
                               subject=request.POST['subject'],
                               title=request.POST['title'],
                               description=request.POST['description'],
                               due_date=request.POST['due_date'],
                               is_finised=finished)
            homework.save()
            
            messages.success(request,f'Successfully added new homework from {request.user.username}')


    else:

        form=HomeworkForm()
    homework=Homework.objects.filter(user=request.user)
    if len(homework)==0 :
        homework_done=True

    else:
        homework_done=False

    context={'homeworks':homework,
             'homeworks_done':homework_done,
             'form':form
    }

    return render(request,'homework.html', context)


def update_homework(request,pk=None):
    homework=Homework.objects.get(id=pk)
    if homework.is_finised():
        homework.is_finised=True
    else:
        homework.is_finised=False

    homework.save()
    return redirect('homework')


    
