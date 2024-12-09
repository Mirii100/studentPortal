from django.urls import path
from . import views
urlpatterns = [
    path('',views.dashboard_view,name='home'),
    path('notes/',views.notes_view,name='notes'),
    path('deleteNote/<int:pk>',views.deleteNote,name='deleteNote'),
    path('notes_detail/<int:pk>/',views.NoteDetailView.as_view(),name='notes_detail'),
    path('homework/',views.homework,name='homework'),
    path('update_homework/',views.update_homework,name='update_homework'),

    
]