from django.urls import path
from . import views
urlpatterns = [
    path('',views.dashboard_view,name='home'),
    path('notes/',views.notes_view,name='notes'),
    path('youtube/',views.myYoutube,name='youtube'),
    path('books/',views.books,name='books'),
    path('todo/',views.my_todo,name='todo'),
    path('dictionary/',views.dictionary,name='dictionary'),
    path('wiki/',views.wikipedia,name='wiki'),
    path('deleteNote/<int:pk>',views.deleteNote,name='deleteNote'),
    path('notes_detail/<int:pk>/',views.NoteDetailView.as_view(),name='notes_detail'),
    path('homework/',views.homework,name='homework'),
    path('update_homework/<int:pk>/',views.update_homework,name='update_homework'),
    path('delete_homework/<int:pk>/',views.delete_homework,name='delete_homework'),
    path('update_todo/<int:pk>/',views.update_todo,name='update_todo'),
    path('delete_todo/<int:pk>/',views.delete_todo,name='delete_todo'),
    path('books/<str:volume_id>/', views.book_detail, name='book_detail'),



    
]