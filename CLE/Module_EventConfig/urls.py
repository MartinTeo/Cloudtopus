from django.contrib import admin
from Module_EventConfig import views
from django.urls import path,re_path

urlpatterns = [
    path('background_tasks/test/',views.test,name='test'),
    path('instructor/ITOperationsLab/event/',views.faculty_Event_Base,name='itopslab_event'),
    path('instructor/ITOperationsLab/event/get/servers/',views.faculty_Event_GetServers,name='faculty_Event_GetServers'),
    path('instructor/ITOperationsLab/event/execute/',views.faculty_Event_Execute,name='itopslab_event_execute'),
    path('event/start/', views.serverCall), #Temp endpoint
    path('event/recovery/', views.serverRecoveryCall),

    # For events logs
    path('instructor/ITOperationsLab/eventslog/',views.events_list,name='events_list'),
    path('instructor/ITOperationsLab/eventslog/<str:pk>/update/', views.events_update, name='events_update'),
    path('instructor/ITOperationsLab/eventslog/<str:pk>/delete/', views.events_delete, name='events_delete'),
]
