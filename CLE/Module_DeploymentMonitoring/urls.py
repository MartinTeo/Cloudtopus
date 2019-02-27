from django.contrib import admin
from Module_DeploymentMonitoring import views
from django.urls import path,re_path

urlpatterns = [
    path('instructor/ITOperationsLab/setup/awskeys/',views.faculty_Setup_GetAWSKeys,name='itopslab_setup_AWSKeys'),
    path('instructor/ITOperationsLab/monitor/',views.faculty_Monitor_Base,name='itopslab_monitor'),
    path('student/ITOperationsLab/deploy/',views.student_Deploy_Base,name='itopslab_studeploy'),
    path('student/ITOperationsLab/deploy/<str:course_title>/2',views.student_Deploy_Upload,name='itopslab_studeployUpload'),
    path('student/ITOperationsLab/monitor/',views.student_Monitor_Base,name='itopslab_stumonitor'),

    # For adding deployment packages into system
    path('instructor/ITOperationsLab/setup/deployment_package/',views.faculty_Setup_GetGitHubLinks,name='dp_list'),
    path('instructor/ITOperationsLab/setup/deployment_package/create/', views.faculty_Setup_AddGitHubLinks, name='dp_create'),
    path('instructor/ITOperationsLab/setup/deployment_package/<str:course_title>/<str:pk>/update/', views.faculty_Setup_UpdateGitHubLinks, name='dp_update'),
    path('instructor/ITOperationsLab/setup/deployment_package/<str:course_title>/<str:pk>/delete/', views.faculty_Setup_DeleteGitHubLinks, name='dp_delete'),
    path('instructor/ITOperationsLab/setup/deployment_package/<str:course_title>/delete/all/', views.faculty_Setup_DeleteAllGitHubLinks, name='dp_delete_all'),

    # For retrieving and sharing of AMI
    path('instructor/ITOperationsLab/setup/',views.faculty_Setup_Base,name='itopslab_setup'),
    path('instructor/ITOperationsLab/setup/ami/get/',views.faculty_Setup_GetAMI,name='itopslab_setup_AMI_get'),
    path('instructor/ITOperationsLab/setup/ami/accounts/get/',views.faculty_Setup_GetAMIAccounts,name='itopslab_setup_AMI_Accounts_get'),
    path('instructor/ITOperationsLab/setup/ami/accounts/share/',views.faculty_Setup_ShareAMI,name='itopslab_setup_AMI_Accounts_share'),

    # For standard student deployment page
    path('student/ITOperationsLab/deploy/standard/',views.student_Deploy_Standard_Base,name='itopslab_studeploy_standard'),
    path('student/ITOperationsLab/deploy/standard/deployment_package/',views.student_Deploy_Standard_GetDeploymentPackages,name='dp_list_student'),
    path('student/ITOperationsLab/deploy/standard/account/',views.student_Deploy_Standard_AddAccount,name='itopslab_studeploy_standard_AddAccount'),
    path('student/ITOperationsLab/deploy/standard/server/',views.student_Deploy_Standard_GetIPs,name='server_list'),
    path('student/ITOperationsLab/deploy/standard/server/create/',views.student_Deploy_Standard_AddIPs,name='server_create'),
    path('student/ITOperationsLab/deploy/standard/server/<str:course_title>/<str:pk>/update/',views.student_Deploy_Standard_UpdateIPs,name='server_update'),
    path('student/ITOperationsLab/deploy/standard/server/<str:course_title>/<str:pk>/delete/',views.student_Deploy_Standard_DeleteIPs,name='server_delete'),
    path('student/ITOperationsLab/deploy/standard/server/<str:course_title>/delete/all/',views.student_Deploy_Standard_DeleteAllIPs,name='server_delete_all'),
]
