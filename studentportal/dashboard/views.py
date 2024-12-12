from django.shortcuts import render,redirect
from django.views import generic
from .form import *
from . form import DashboardForm,ConversionForm,UserRegistrationForm
from.models import Homework,Todo
from django.contrib import messages
from youtubesearchpython import VideosSearch
import wikipedia
import requests
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



def books(request):
    form = DashboardForm()
    context = {
        'form': form,
    }

    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST.get('text', '').strip()  # Safely get the 'text' key
        if text:  # Proceed only if 'text' is not empty
            url = "https://www.googleapis.com/books/v1/volumes?q=" + text
            r = requests.get(url)
            answer = r.json()
              # Correctly parse the JSON response

            result_list = []
            if 'items' in answer:  # Safeguard against missing 'items'
                for i in range(min(10, len(answer['items']))):  # Avoid IndexError
                    item = answer['items'][i].get('volumeInfo', {})
                    result_dict = {
                        'title': item.get('title'),
                        'subtitle': item.get('subtitle'),
                        'description': item.get('description'),
                        'count': item.get('pageCount'),
                        'categories': item.get('categories'),
                        'rating': item.get('averageRating'),
                        'thumbnail': item.get('imageLinks').get('thumbnail'),
                        'preview': item.get('previewLinks')
                    }
                    result_list.append(result_dict)

            context = {
                'form': form,
                'results': result_list,
            }
            return render(request, 'books.html', context)
        else:
            # Handle the case where 'text' is empty
            
            return render(request, 'books.html', context)

    
    return render(request, 'books.html', context)


def book_detail(request, volume_id):
    # Google Books API URL for a specific book
    url = f"https://www.googleapis.com/books/v1/volumes/{volume_id}"
    response = requests.get(url)

    if response.status_code == 200:
        book = response.json()
        # Get the 'infoLink' which is the URL to the exact book on Google Books
        book_url = book['volumeInfo'].get('infoLink')

        if book_url:
            # Redirect to the book's Google Books page
            return redirect(book_url)
        else:
            # If the 'infoLink' is missing, redirect to a fallback URL
            return redirect('home')  # Redirect to home page or a custom page
    else:
        # If the book isn't found or there's an error, redirect to a fallback URL
        return redirect('home')  # Or redirect to a custom error page




  # Assuming this is your form


def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{text}"
        
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raises an HTTPError for bad responses
            answer = r.json()
            
            # Add detailed error checking
            if not answer or not isinstance(answer, list):
                raise ValueError("Unexpected API response format")
            
            # Safely extract data with default values
            phonetics = answer[0].get('phonetics', [{}])[0].get('text', '')
            audio = answer[0].get('phonetics', [{}])[0].get('audio', '')
            
            # Corrected spelling and added safe navigation
            meanings = answer[0].get('meanings', [{}])[0]
            definitions = meanings.get('definitions', [{}])[0]
            
            defination = definitions.get('definition', '')
            example = definitions.get('example', '')
            synonyms = definitions.get('synonyms', [])
            
            context = {
                'form': form, 
                'inputs': text, 
                'phonetics': phonetics, 
                'audio': audio, 
                'definition': defination,  # Corrected spelling
                'example': example, 
                'synonyms': synonyms,  # Corrected spelling
            }
        
        except requests.RequestException as e:
            # More specific error handling
            print(f"API Request Error: {e}")
            context = {
                'form': form, 
                'inputs': text,
                'error': f"Error fetching dictionary data: {e}"
            }
        
        except (KeyError, IndexError, ValueError) as e:
            # Handle potential data extraction errors
            print(f"Data Extraction Error: {e}")
            context = {
                'form': form, 
                'inputs': text,
                'error': f"Error processing dictionary data: {e}"
            }
        
        return render(request, 'dictionary.html', context)
    
    else:
        form = DashboardForm()
        context = {'form': form}
        return render(request, 'dictionary.html', context)
    


def mywikipedia(request):
    if request.method == 'POST':
        text=request.POST['text']
        form=DashboardForm(request.POST)
        search = wikipedia.page(text)
        context = {
            'form': form,
            'title': search.title,
            'content': search.content,
            'link': search.url,
            'details': search.summary
        }
        return render(request, 'wiki.html', context)
    else:

        form=DashboardForm()
        context = {'form': form}
    return render(request, 'wiki.html',context)


""""""
def conversion(request):

    if request.method=='POST':
        form=ConversionForm(request.POST)

        if request.POST['measurement']=='length':
            measurement_form=ConversionLengthForm()
            context={'form': form,'m_form':measurement_form,'input':True}
            if 'input' in request.POST:
                first=request.POST['measure1']
                second=request.POST['measure2']
                input=request.POST['input']
                answer=''
                if input and int(input) >=0:
                    if first =='yard' and second =='foot':
                        answer= f'{input} yard ={int(input)*3} foot )'
                    if first =='foot' and second =='yard':
                        answer= f'{input} foot ={int(input)/3} yard )'


                context={
                    'form':form, 
                         'm_form':measurement_form, 
                         'input':True,
                         'answer':answer}
        
        
        if request.POST['measurement']=='mass':
            measurement_form=ConversionMassForm()
            context={'form': form,'m_form':measurement_form,'input':True}
            if 'input' in request.POST:
                first=request.POST['measure1']
                second=request.POST['measure2']
                input=request.POST['input']
                answer=''
                if input and int(input) >=0:
                    if first =='pound' and second =='kilogram':
                        answer= f'{input} pound ={int(input)*0.453592} kilogram )'
                    if first =='kilogram' and second =='pound':
                        answer= f'{input} kilogram ={int(input)*2.20462} pound )'


                context={'form':form, 
                         'm_form':measurement_form, 
                         'input':True,
                         'answer':answer},

    


    else:
        form=ConversionForm()
        context={'form': form,'input':False}

    return render(request, 'conversion.html',context)

""""""

def conversion(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)

        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm()
            context = {'form': form, 'm_form': measurement_form, 'input': True}
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input) * 3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {int(input) / 3} yard'

                # Corrected context assignment
                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer
                }

        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context = {'form': form, 'm_form': measurement_form, 'input': True}
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {int(input) * 0.453592} kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram = {int(input) * 2.20462} pound'

                # Corrected context assignment
                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer
                }

    else:
        form = ConversionForm()
        context = {'form': form, 'input': False}

    return render(request, 'conversion.html', context)


def register(request):
    if request.method == 'POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            
            return redirect('login')
    else:   
        form=UserRegistrationForm()
    context={'form': form, }


    return render(request,'register.html', context)


def profile(request):
    homeworks=Homework.objects.filter(is_finised=False,user=request.user)
    todos=Todo.objects.filter(is_finished=False,user=request.user)
    if len(homeworks)==0:
        homework_done=True
    else:
        homework_done=False
    if len(todos)==0:
        todos_done=True
    else:
        todos_done=False

    context={
        'homeworks': homeworks,
        'todos': todos,
        'homework_done': homework_done,
        'todos_done': todos_done,
        'homework_count': len(homeworks),
        'todo_count': len(todos),
        'homework_percentage': len(homeworks)/len(Homework.objects.all())*100 if len(Homework.objects.all())>0 else 0,
        'todo_percentage': len(todos)/len(Todo.objects.all())*100 if len(Todo.objects.all())>0 else 0,
    }

    return render(request,'profile.html',context)



