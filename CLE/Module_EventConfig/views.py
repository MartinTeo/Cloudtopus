import json
import time
import traceback
from django.shortcuts import render
from django.http import HttpResponse
from Module_EventConfig import tasks
from Module_EventConfig.src import utilities
from datetime import timedelta, datetime
from Module_TeamManagement.models import *
from Module_Account.src import processLogin
from Module_DeploymentMonitoring.models import *
from Module_DeploymentMonitoring import views as views_DM
from Module_DeploymentMonitoring.src import utilities as utilities_DM
from django.http import JsonResponse
from django.contrib.auth import logout
from Module_EventConfig.forms import *
from Module_EventConfig.models import *
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from background_task.models_completed import CompletedTask
from background_task.models import Task


# Test to see if django-background-tasks is wokring or not
#
def test(requests):
    value = requests.GET.get('message')
    period = requests.GET.get('period')

    if value == None:
        return HttpResponse('Please sepcify a message and a period (default 0 seconds).')

    if period == None:
        period = 0
    else:
        period = int(period)

    try:
        tasks.test_tasks(str(value), schedule=timedelta(seconds=period))

    except Exception as e:
        traceback.print_exc()
        return HttpResponse('Background tasks NOT successfully initiated')

    return HttpResponse('Background tasks successfully initiated')


# Main base function for event configuration page on faculty.
#
def faculty_Event_Base(requests,response=None):
    response = {"faculty_Event_Base" : "active"}

    # Redirect user to login page if not authorized and student
    try:
        processLogin.InstructorVerification(requests)
    except:
        logout(requests)
        return render(requests, 'Module_Account/login.html', response)

    try:
        course_title = requests.GET.get('course_title')
        course_sectionList = requests.session['courseList_ITOpsLab']

        response['course_sectionList'] = course_sectionList[course_title]
        response['course_title'] = course_title

        # faculty_email = requests.user.email
        # facultyObj = Faculty.objects.get(email=faculty_email)

    except Exception as e:
        traceback.print_exc()
        response['error_message'] = 'Error during event execution: ' + str(e.args[0])
        return render(requests, "Module_TeamManagement/Instructor/ITOpsLabEvent.html", response)

    return render(requests, "Module_TeamManagement/Instructor/ITOpsLabEvent.html", response)


# Supplementary - Experimental method
#
def faculty_Event_GetServers(requests):
    response = {"faculty_Event_GetServers" : "active"}

    # Redirect user to login page if not authorized and student
    try:
        processLogin.InstructorVerification(requests)
    except:
        logout(requests)
        return render(requests, 'Module_Account/login.html', response)

    section_numbers = requests.GET.get('section_number').split('_')
    course_title = requests.GET.get('course_title')

    try:
        courseList = requests.session['courseList_ITOpsLab']
        team_account_numberList = utilities_DM.getAllTeamDetails(courseList,course_title)

        servers = []
        parent = False
        slave = False
        for section_number in section_numbers:
            for team in team_account_numberList[section_number]:
                try:
                    serverObjs = Server_Details.objects.filter(account_number=team['account_number'])
                    for serverObj in serverObjs:
                        servers.append(serverObj)

                        if serverObj.type == 'Parent':
                            parent = True
                        elif serverObj.type == 'Slave':
                            slave = True
                except:
                    traceback.print_exc()

        response['server_count'] = len(servers)
        response['server_parent_check'] = parent
        response['server_slave_check'] = slave
    except:
        traceback.print_exc()

    return HttpResponse(json.dumps(response), content_type='application/json')


# Execute event function after base is called
#
def faculty_Event_Execute(requests):
    response = {"faculty_Event_Execute" : "active"}

    events = {
        'stop':{
            'method':tasks.stopServer,
            'message':'Successfully stopped ',
            'message_scheduled':'Successfully scheduled "STOP" event for ',
        },
        'dos':{
            'method':tasks.dosAttack,
            'message':'Successfully triggered DoS attack to',
            'message_scheduled':'Successfully scheduled "DoS" event for ',
        },
        'stopapp':{
            'method':tasks.stopWebApplication,
            'message':'Successfully killed the web application of ',
            'message_scheduled':'Successfully scheduled "STOP WEB APP" event for ',
        },
    }

    # Redirect user to login page if not authorized and student
    try:
        processLogin.InstructorVerification(requests)
    except:
        logout(requests)
        return render(requests, 'Module_Account/login.html', response)

    faculty_email = requests.user.email
    facultyObj = Faculty.objects.get(email=faculty_email)
    course_sectionList = requests.session['courseList_ITOpsLab']

    course_title = requests.POST.get('course_title')
    section_numberList = requests.POST.getlist('section_number')
    server_type = requests.POST.get('server_type')
    event_type = requests.POST.get('event_type')

    if requests.POST.get('datetime') == 'now' or requests.POST.get('setDate') == None:
        scheduled_datetime = datetime.now()
    else:
        scheduled_datetime = (datetime.strptime(requests.POST.get('setDate'),'%Y-%m-%dT%H:%M'))

    print('Course Title: ' + course_title)
    print('Section Numbers: ' + '_'.join(section_numberList))
    print('Server Type: ' + server_type)
    print('Event Type: ' + event_type)
    print('Schedule Datatime: ' + str(scheduled_datetime))

    try:
        serverList = []
        team_details = utilities_DM.getAllTeamDetails(course_sectionList,course_title)
        for section_number in section_numberList:
            for details in team_details[section_number]:
                querySet_serverList = Server_Details.objects.filter(account_number=details["account_number"])
                for server in querySet_serverList:
                    if server.type == server_type and server.state == 'Live':
                        serverList.append(
                            {
                                'server_ip':server.IP_address,
                                'server_id':server.instanceid,
                                'server_account':server.account_number.account_number
                            }
                        )

        if len(serverList) > 0:
            period = scheduled_datetime - datetime.now()
            events[event_type]['method'](server_list=serverList, schedule=period, section_numbers=section_numberList, server_type=server_type)

    except Exception as e:
        traceback.print_exc()
        response['error_message'] = 'Error during event execution: ' + str(e.args[0])
        return render(requests, "Module_TeamManagement/Instructor/ITOpsLabEvent.html", response)

    requests.section_number = course_sectionList[course_title][0]['section_number']

    if len(serverList) > 0:
        if requests.POST.get('datetime') == 'now':
            response['message'] = events[event_type]['message'] + str(len(serverList)) + ' ' + str(server_type) + ' servers.'
            time.sleep(6)
        else:
            response['message'] = events[event_type]['message_scheduled'] + str(len(serverList)) + ' ' + str(server_type) + ' servers.'
    else:
        response['error_message'] = 'All ' + str(server_type) + ' servers are currently down. Unable to send event to ' + str(server_type) + ' servers.'

    return views_DM.faculty_Monitor_Base(requests,response)


# Method to write the recovery time of the server that calls this
#
def serverRecoveryCall(request):
    secret_key = request.GET.get('secret_key')
    if utilities.validate(secret_key) == True:
        response = {'HTTPStatus':'OK', 'HTTPStatusCode':200}
        ipAddress= request.GET.get('ip')
        try:
            utilities.writeRecoveryTime(ipAddress)
        except:
            response = {'HTTPStatus':'No', 'HTTPStatusCode':404}
    else:
        response = {'HTTPStatus':'No', 'HTTPStatusCode':404}
    return JsonResponse(response)


# Method to call to log an event entry
#
def serverCall(request):
    secret_key = request.GET.get('secret_key')
    if utilities.validate(secret_key) == True:
        response = {'HTTPStatus':'OK', 'HTTPStatusCode':200}
        ipAddress= request.GET.get('ip')
        event_type=request.GET.get('event')
        factor = utilities.writeEventLog(event_type, ipAddress )
        print(factor)
    else:
        response = {'HTTPStatus':'No', 'HTTPStatusCode':404}
    return JsonResponse(response)


# <description>
#
def events_list(request):
    events = Task.objects.all()
    return render(request, 'dataforms/eventslog/events_list.html', {'events': events})


# <description>
#
def save_events_form(request, form, template_name, pk=None):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            if pk != None:
                data['message'] = 'Event successfully updated.'

            new_event = form.save()
            new_event.run_at = new_event.run_at - timedelta(hours=8)
            new_event.save()
            data['form_is_valid'] = True
            events = utilities_DM.getPendingTasksLogs(request.session['ESMCourseSection'])
            data['html_events_list'] = render_to_string('dataforms/eventslog/partial_events_list.html', {
                'pending_events': events
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


# <description>
#
def events_create(request):
    if request.method == 'POST':
        form = PendingEventsForm(request.POST)
    else:
        form = PendingEventsForm()
    return save_events_form(request, form, 'dataforms/eventslog/partial_events_create.html')


# <description>
#
def events_update(request, pk):
    eventsLog = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = PendingEventsForm(request.POST, instance=eventsLog)
    else:
        eventsLog.run_at = (eventsLog.run_at + timedelta(hours=8)) #.strftime("%Y-%m-%d %H:%M:%S")
        form = PendingEventsForm(instance=eventsLog)
    return save_events_form(request, form, 'dataforms/eventslog/partial_events_update.html', pk=pk)


# Delete function
#
def events_delete(request, pk):
    eventsLog = get_object_or_404(Task, pk=pk)
    data = dict()
    if request.method == 'POST':
        eventsLog.delete()
        data['form_is_valid'] = True
        data['message'] = 'Event successfully deleted'
        events = utilities_DM.getPendingTasksLogs(request.session['ESMCourseSection'])
        data['html_events_list'] = render_to_string('dataforms/eventslog/partial_events_list.html', {
            'pending_events': events
        })
    else:
        context = {'event': eventsLog}
        data['html_form'] = render_to_string('dataforms/eventslog/partial_events_delete.html', context, request=request)
    return JsonResponse(data)
