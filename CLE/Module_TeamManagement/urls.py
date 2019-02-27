from Module_TeamManagement import views
from django.contrib import admin
from django.urls import path
from Module_TeamManagement.forms import PhoneNumberForm, VerificationCodeForm,TrailheadForm
from Module_TeamManagement.views import TelegramWizard, PhoneNumberFormView

urlpatterns = [
    path('home/', views.home, name='home'),
    path('home/aboutCloudtopus/', views.aboutCloudtopus, name='aboutCloudtopus'),
    path('student/configTools/', views.configureDB_clt, name='uploadtoolStudent'),
    path('instructor/configTools/', views.configureDB_clt, name='uploadtools'),
    path('instructor/configStudents/', views.configureDB_course, name='uploadcsv'),
    path('instructor/configTeams/', views.configureDB_teams, name='uploadteam'),
    path('student/team/', views.student_Team, name='sTeam'),
    path('student/stats/', views.student_Stats, name='sStats'),
    path('instructor/overview/', views.faculty_Overview, name='instOverview'),
    path('instructor/home/', views.faculty_Dashboard, name='instHome'),
    path('instructor/home2/', views.faculty_HomePage, name='instHome2'),
    path('CLEAdmin/',views.CLEAdmin, name = 'cleAdmin'),
    path('CLEAdmin/moduleSetup',views.configureDB_faculty, name = 'modSu'),
    path('charts/',views.line_chart, name = 'charts_view'),
    # path('instructor/telegram_setup/', TelegramWizard.as_view(FORMS, condition_dict={'verificationcode': views.enter_phonenumber}), name='telegram_setup'),
    # path('instructor/telegram_setup/', TelegramWizard.as_view([PhoneNumberForm, VerificationCodeForm]), name='telegram_setup'),
    path('instructor/telegram_setup/', views.configureDB_telegram, name='telegram_setup'),
    path('join/', PhoneNumberFormView.as_view(), name='phone_number_form'),
    path('csv/clt_file', views.clt_file_download),
    path('admin/csv/clt_file.csv', views.clt_file_ouput, name = "clt_file"),
    path('celery/trailhead/refresh', views.trailhead_refresh, name = 'trailhead_refresh'),
    #trailmixes
    path('instructor/trailmix/',views.trailhead_list,name='trailhead_list'),
    path('instructor/trailmix/create/', views.trailhead_create, name='trailhead_create'),
    path('instructor/trailmix/<str:pk>/delete/', views.trailhead_delete, name='trailhead_delete'),
]
