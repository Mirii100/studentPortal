from django.shortcuts import render,redirect
from django.views import generic
from .form import *
from . form import DashboardForm
from.models import Homework,Todo
from django.contrib import messages
from youtubesearchpython import VideosSearch
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



def delete_homework(request,pk=None):
    homework=Homework.objects.get(id=pk)
    homework.delete()
    return redirect('homework')




def myYoutube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        # Safely get the 'text' key from the POST data
        text = request.POST.get('text', '').strip()  # Default to an empty string if 'text' is not provided
        if text:  # Proceed only if 'text' is not empty
            video = VideosSearch(text, limit=20)
            result_list = []
            for i in video.result().get('result', []):  # Safeguard against missing 'result'
                result_dict = {
                    'input': text,
                    'title': i.get('title', 'No title available'),
                    'duration': i.get('duration', 'N/A'),
                    'thumbnail': i.get('thumbnails', [{}])[0].get('url', ''),
                    'channel': i.get('channel', {}).get('name', 'Unknown channel'),
                    'views': i.get('viewCount', {}).get('short', 'N/A'),
                    'published': i.get('publishedTime', 'Unknown'),
                    'link': i.get('link', '#'),
                }

                # Extract description snippets if available
                desc = ''
                description_snippet = i.get('descriptionSnippet', [])
                if isinstance(description_snippet, list):  # Ensure it's iterable
                    for j in description_snippet:
                        desc += j.get('text', '')

                result_dict['description'] = desc
                result_list.append(result_dict)

            context = {
                'form': form,
                'results': result_list,
            }
            return render(request, 'youtube.html', context)
        else:
            # Handle the case where 'text' is empty
            context = {
                'form': form,
                'results': [],
                'error': "Please enter a search term.",
            }
            return render(request, 'youtube.html', context)

    else:
        form = DashboardForm()

    context = {'form': form}
    return render(request, 'youtube.html', context)




def my_todo(request):
    if request.method=='POST':
        form=TodoForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST['is_finished']
                if finished=='on':
                    finished=True
                else:
                    finished=False

                
            except KeyError:
                finished=False
            todos=Todo(user=request.user,
                       title=request.POST['title'],
                       is_finished=finished)
            todos.save()
            messages.success(request,f'Successfully added new todo from {request.user.username}')


    
    else:


        form=TodoForm()
    todo=Todo.objects.filter(user=request.user)

    if len(todo)==0 :
        todos_done=True
    else:
        todos_done=False


    context = {'todos':todo,
               'form':form,
               'todos_done':todos_done,} 
    return render(request, 'todo.html',context)


def update_todo(request,pk=None):
    todo=Todo.objects.get(id=pk)
    if todo.is_finished==True:
        todo.is_finished=False
    else:
        todo.is_finished=True

    todo.save()
    return redirect('todo')


def delete_todo(request,pk=None):
    todo=Todo.objects.get(id=pk)
    todo.delete()
    return redirect('todo')
