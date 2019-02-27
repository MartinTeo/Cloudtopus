import os
import csv
import logging
import datetime
import traceback
from zipfile import ZipFile
from django.shortcuts import render, get_object_or_404
from Module_TeamManagement.src import bootstrap, utilities
from Module_CommunicationManagement.src import tele_util
from Module_TeamManagement.models import *
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from django.utils.encoding import smart_str
from random import randint
from django.views.generic import TemplateView
from formtools.wizard.views import SessionWizardView
from django.http import HttpResponse, HttpResponseRedirect
from Module_Account.src import processLogin
from django.contrib.auth import logout, login
from Module_TeamManagement import forms
from Module_TeamManagement.forms import *
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import FormView
from Module_TeamManagement.mixins import AjaxFormMixin
from telethon.errors import PhoneNumberUnoccupiedError
from telethon.tl.types import Channel

logr = logging.getLogger(__name__)

# Student Home Page
#
def home(requests):
    context = {}
    # Redirect user to login page if not authorized and student
    try:
        processLogin.studentVerification(requests)
    except:
        logout(requests)
        return render(requests,'Module_Account/login.html',context)
    context["home"] = "active"
    requests.session['userType'] = "Student"

    student_email = requests.user.email
    all_SocialAccount = SocialAccount.objects.all()

    for each_SocialAccount in all_SocialAccount:
        data = each_SocialAccount.extra_data
        if data['email'] == student_email:
            requests.session['user_picture'] = data['picture']
            requests.session['user_name'] = data['name'].replace('_','').strip()

    # Populates the info for the side nav bar for instructor
    utilities.populateRelevantCourses(requests, studentEmail=student_email)

    # Reads web scrapper results
    trailResults = utilities.populateTrailheadInformation(requests, student_email)
    context.update(trailResults)

    # Get number of weeks since school term start and reamining weeks till school term ends
    past_weeks, remaining_weeks = utilities.getRemainingWeeks()

    if past_weeks != None and remaining_weeks != None:
        context['past_weeks'] = past_weeks
        context['remaining_weeks'] = remaining_weeks
        context['progress'] =  (past_weeks/(past_weeks+remaining_weeks)) * 100
    else:
        context['past_weeks'] = 0
        context['remaining_weeks'] = 0
        context['progress'] = 0

    return render(requests,"Module_TeamManagement/Student/studentHome.html",context)

def aboutCloudtopus(requests):
    context={}
    userEmail = requests.user.email

    try:
        processLogin.studentVerification(requests)
        context['userTypeExtension'] = "Module_TeamManagement/Student/studentBase.html"
    except:
        try:
            processLogin.InstructorVerification(requests)
            context['userTypeExtension'] = "Module_TeamManagement/Instructor/instructorBase.html"
        except:
            logout(requests)
            return render(requests, 'Module_Account/login.html', response)
    
    return render(requests,"Module_TeamManagement/aboutCloudtopus.html",context)


# Admin homepage
#
def CLEAdmin(requests):
    context = {}
    if not requests.user.is_authenticated:
        return render(requests,'Module_Account/login.html',context)
    else:
        context["home_page"] = "active"
        return render(requests,"Administrator/admindashboard.html",context)
    # return render(requests,"Module_TeamManagement/Instructor/instructorOverview.html",context)


# Faculty Home Page
#
def faculty_HomePage(requests):
    context = {'faculty_DashboardPage': "active"}

    # Redirect user to login page if not authorized and faculty
    try:
        processLogin.InstructorVerification(requests)
    except:
        logout(requests)
        return render(requests,'Module_Account/login.html',context)

    requests.session['userType'] = "Instructor"
    faculty_username = requests.user.email.split('@')[0]
    all_SocialAccount = SocialAccount.objects.all()

    for each_SocialAccount in all_SocialAccount:
        data = each_SocialAccount.extra_data
        if data['email'] == requests.user.email:
            requests.session['user_picture'] = data['picture']
            requests.session['user_name'] = data['name'].replace('_','').strip()

    try:
        #Populates the info for the side nav bar for instructor
        utilities.populateRelevantCourses(requests, instructorEmail=requests.user.email)
    except Exception as e:
        traceback.print_exc()
        context['error_message'] = e.args[0]

    context['course_section_count'] = len(requests.session['courseList_updated'])
    context['ITOpsLab_count'] = len(requests.session['courseList_ITOpsLab'])
    return render(requests, 'Module_TeamManagement/Instructor/instructorDashboard.html', context)


# Faculty Dashboard
#
def faculty_Dashboard(requests):
    context = {"faculty_Dashboard" : "active"}

    # Redirect user to login page if not authorized and faculty
    try:
        processLogin.InstructorVerification(requests)
    except:
        logout(requests)
        return render(requests,'Module_Account/login.html',context)

    requests.session['userType'] = "Instructor"
    faculty_username = requests.user.email.split('@')[0]
    all_SocialAccount = SocialAccount.objects.all()

    for each_SocialAccount in all_SocialAccount:
        data = each_SocialAccount.extra_data
        if data['email'] == requests.user.email:
            requests.session['user_picture'] = data['picture']
            requests.session['user_name'] = data['name'].replace('_','').strip()

    try:
        courseStudents = []

        #Populates the info for the side nav bar for instructor
        utilities.populateRelevantCourses(requests, instructorEmail=requests.user.email)
        facultyObj = Faculty.objects.get(email=requests.user.email)
        registered_course_section = facultyObj.course_section.all()
        courses = {}
        students = []
        tele_data = {}
        previouscourse = "a" #filler

        for course_section in registered_course_section:
            course_title = course_section.course.course_title

            if "G0" in (course_section.course_section_id):
                courses[course_title]= {"count" : 0, "sectionCount" : 0}
            else:
                if course_title not in courses:
                    courses[course_title]= {}
                    if previouscourse != "a":
                        courses[previouscourse]["count"] = len(courseStudents)
                        courses[previouscourse]["sectionCount"] = sectionCounter
                        courses[previouscourse]["toolImage_list"] = toolsList

                    courseStudents=[]
                    previoussection = "a"
                    previouscourse = course_title
                    sectionCounter = 0
                    toolsList=[]
                if previoussection != course_section:
                    sectionCounter += 1

                classObj = Class.objects.all().filter(course_section=course_section)

                for student in classObj:
                    students.append(student)
                    courseStudents.append(student)
                try:
                    currentCourseTools = course_section.learning_tools.split("_")
                    for tools in currentCourseTools:
                        if tools not in toolsList:
                            toolsList.append(tools)
                except:
                    pass
                previoussection = course_section

        if previouscourse != "a":
            courses[previouscourse]["count"] = len(courseStudents)
            courses[previouscourse]["sectionCount"] = sectionCounter
            courses[previouscourse]["toolImage_list"] = toolsList

        context['section_count'] = len(registered_course_section)
        context['course_count'] = len(courses)
        context['course_list'] = courses
        context['student_count'] = len(students)

    except:
        traceback.print_exc()
        context = {'messages' : ['Invalid user account']}
        return render(requests,'Module_Account/login.html',context)

    context["courses"] = requests.session['courseList_updated']

    # Get number of weeks since school term start and reamining weeks till school term ends
    past_weeks, remaining_weeks = utilities.getRemainingWeeks()

    if past_weeks != None and remaining_weeks != None:
        context['past_weeks'] = past_weeks
        context['remaining_weeks'] = remaining_weeks
        context['progress'] = (past_weeks/(past_weeks+remaining_weeks)) * 100
    else:
        context['past_weeks'] = 0
        context['remaining_weeks'] = 0
        context['progress'] = 0

    # Reads web scrapper results
    trailResults = utilities.populateTrailheadInformation(requests, instructorEmail=requests.user.email)
    context.update(trailResults)
    context['message'] = 'Successful retrieval of faculty\'s overview information'
    #print(context)
    return render(requests, "Module_TeamManagement/Instructor/instructorHome.html",context)

# Faculty force refresh trailhead page
#
#
def trailhead_refresh(requests):
    course_section = requests.GET.get("course_section")
    utilities.webScrapper(course_selected=course_section )
    return HttpResponseRedirect(requests.META.get('HTTP_REFERER'))

# Faculty Student Management Page
#
def faculty_Overview(requests):

    context = {}
    # Redirect user to login page if not authorized and faculty
    try:
        processLogin.InstructorVerification(requests)
    except:
        logout(requests)
        return render(requests,'Module_Account/login.html',context)

    context = {"faculty_Overview" : "active", 'course' : {}}

    faculty_email = requests.user.email

    if requests.method == "GET":
        course_section = requests.GET.get('module')
        course_title = requests.GET.get('course_title')
        section_number = requests.GET.get('section_number')
    else:
        course_section = requests.POST.get('course_section')
        course_title = course_section[:-2]
        section_number = course_section[-2:]

    # Return sections that's related to the course
    courseList_updated = requests.session['courseList_updated']
    context['course_sectionList'] = courseList_updated[course_title]

    facultyObj = Faculty.objects.get(email=faculty_email)
    classObj_list = Class.objects.all().filter(course_section=course_section)

    trailResults = utilities.populateTrailheadInformation(requests, instructorEmail=requests.user.email)

    context.update(trailResults)
    if len(classObj_list) > 0:
        classList = [] # Containing student class objects
        for enrolled_class in classObj_list:
            studentInfo = {}
            studentInfo['team'] = enrolled_class.team_number
            studentInfo['info'] =  enrolled_class.student #Obtains student model from Foreign key
            studentUserName = enrolled_class.student.email.split("@")[0]
            try:
                studentInfo['link'] = Cloud_Learning_Tools.objects.get(id = studentUserName+"_Trailhead").website_link
                studentPointsPosition = trailResults['CourseTrailResults']['class']['Students_Information']['students'].index(studentUserName)
                studentInfo['points'] = trailResults['CourseTrailResults']['class']['Students_Information']['points'][studentPointsPosition]
                studentInfo['badges'] = trailResults['CourseTrailResults']['class']['Students_Information']['badges'][studentPointsPosition]
            except:
                studentInfo['link'] ="No link" #Exception which is caused by no cle linked
                studentInfo['points'] = 0
                studentInfo['badges'] = 0
            classList.append(studentInfo)
        context['course']['classList'] = classList

    course_section = Course_Section.objects.get(course_section_id=course_section)
    if course_section.section_number == 'G0':
        context['module'] = course_section.course.course_title
    else:
        context['module'] = course_section.course.course_title + " " + course_section.section_number

    context['course_section'] = Course_Section.objects.get(course=course_title, section_number = section_number)
    context['user'] = facultyObj
    context['message'] = 'Successful retrieval of faculty\'s profile'

    return render(requests,"Module_TeamManagement/Instructor/instructorOverview.html",context)


# TO-DO: update function
#
def student_Stats(requests):
    '''
        Check if user is authenticated aka session
    '''
    context = {}
    # Redirect user to login page if not authorized and student
    try:
        processLogin.studentVerification(requests)
    except:
        logout(requests)
        return render(requests,'Module_Account/login.html',context)
    context = {"stud_stats" : "active"}
    return render(requests,"Module_TeamManagement/Student/studentStatistics.html",context)


# Student Team Page
#
def student_Team(requests):
    context = {}
    # Redirect user to login page if not authorized and student
    try:
        processLogin.studentVerification(requests)
    except:
        logout(requests)
        return render(requests,'Module_Account/login.html',context)

    context = {"student_Team" : "active", 'course' : {}}
    studentList = []
    module = requests.GET.get('module')
    student_email =requests.user.email

    if student_email == None:
        context['message'] = 'Please specify a username'
        return render(requests,"Module_TeamManagement/Student/studentTeam.html", context)

    studentObj = Student.objects.get(email=student_email)
    classObj = Class.objects.all().filter(student=studentObj , course_section = module ) #Will return queryset containing 1 row unless has multiple teams in same class

    for enrolled_class in classObj: #Should contain 1 row
        if enrolled_class.team_number != None :
            team_list = Class.objects.all().filter(team_number=enrolled_class.team_number).filter(course_section=enrolled_class.course_section)
            for student_class_model in team_list:
                studentList.append(student_class_model.student) #List containing student models

            context['team'] = studentList
            context['teamno'] = enrolled_class.team_number

    # Reads web scrapper results
    trailResults = utilities.populateTrailheadInformation(requests, student_email)
    context.update(trailResults)

    context['module'] = classObj[0].course_section.course_section_id
    context['user'] = studentObj
    context['message'] = 'Successful retrieval of student\'s team'
    print(context)
    return render(requests,"Module_TeamManagement/Student/studentTeam.html",context)


# This is for initial configuration by superadmin
# This function populates the database with the fauclty members and the courses
#
# Requests param: POST
# - file
#
# Models to populate:
# - Course
# - Faculty
# - School_Term
#
# Response (Succcess):
# - configureDB_faculty
# - results
# - message
#
def configureDB_faculty(requests):
    response = {"configureDB_faculty" : "active"}
    if requests.method == "GET":
        return render(requests, "Administrator/uploadcsv.html", response)

    bootstrapFile = {}
    try:
        file = requests.FILES.get("file", False)
        action = requests.POST.get("action")
        start_date = requests.POST.get("start_date")
        end_date = requests.POST.get("end_date")

        if not utilities.validateDate(start_date) or not utilities.validateDate(end_date):
            raise Exception("Incorrect date format, should be YYYY-MM-DD")

        bootstrapFile['start_date'] = start_date
        bootstrapFile['end_date'] = end_date

        if action != None:
            bootstrap.clear_Database()

        if file.name.endswith('.zip'):
            unzipped = ZipFile(file)
            unzipped.extractall(os.path.abspath('bootstrap_files'))
            bootstrapFile['file_type'] = 'zip'

            for fileName in unzipped.namelist():
                if fileName.lower() == 'faculty_information.xlsx':
                    bootstrapFile['faculty'] = os.path.abspath('bootstrap_files/' + fileName)
                elif fileName.lower() == 'course_information.xlsx':
                    bootstrapFile['course'] = os.path.abspath('bootstrap_files/' + fileName)

            if 'faculty' not in bootstrapFile.keys() or 'course' not in bootstrapFile.keys():
                raise Exception("Invalid file information within .zip file. Please upload faculty or course information only.")

        elif file.name.endswith('.xlsx'):
            if file.name.lower() == 'faculty_information.xlsx':
                bootstrapFile['file_path'] = file.temporary_file_path()
                bootstrapFile['file_type'] = 'excel'
                bootstrapFile['file_information'] = 'faculty'

            elif file.name.lower() == 'course_information.xlsx':
                bootstrapFile['file_path'] = file.temporary_file_path()
                bootstrapFile['file_type'] = 'excel'
                bootstrapFile['file_information'] = 'course'

            else:
                raise Exception("Invalid file information. Please upload faculty or course information only.")

        else:
            raise Exception("Invalid file type. Please upload .xlsx or .zip only")

        # If file is .xlsx or .zip then proceed with processing
        response['results'] =  bootstrap.bootstrap_Faculty(bootstrapFile)

    except Exception as e:
        # Uncomment for debugging - to print stack trace wihtout halting the process
        traceback.print_exc()
        response['error_message'] = e.args[0]
        return render(requests, "Administrator/uploadcsv.html", response)

    response['message'] = 'Successful Upload'
    return render(requests, "Administrator/uploadcsv.html", response)


# This is for initial configuration by faculty
# This function associates the course with the faculty member
#
# Requests param: POST
# - course_title
# - file
#
# Models to populate:
# - Faculty_course_section
# - Course_Section
#
# Models to modify:
# - Faculty
# - Course_Section
#
# Response (Succcess):
# - configureDB_course
# - courses
# - message
#
def configureDB_course(requests):
    response = {"configureDB_course" : "active"}

    # Retrieve all the course
    courseObject = Course.objects.all()
    courseList = []

    for course in courseObject:
        courseList.append(course.course_title)
    response['courses'] = courseList

    if requests.method == "GET":
        return render(requests, "Module_TeamManagement/Instructor/uploadcsv.html", response)

    try:
        file = requests.FILES.get("file", False)
        if file:
            return configureDB_students(requests)

        course_title = requests.POST.get("course_title")
        facultyObj = Faculty.objects.get(email=requests.user.email)
        itOps_tool = requests.POST.get("add_tool")

        if course_title == None:
            raise Exception('Please enter a valid course title')

        courseObj = Course.objects.get(course_title=course_title)
        course_section_id = course_title + 'G0'

        if requests.session['configured_Tools'] == None:
            tools = [itOps_tool]
        else:
            tools = ['Telegram'] if 'Telegram' in requests.session['configured_Tools'] else []
            if itOps_tool != None:
                tools.append(itOps_tool)

        # Create/Retrieve (if exists) course_section object
        try:
            course_sectioObj = Course_Section.objects.get(course_section_id=course_section_id)
        except:
            course_sectioObj = Course_Section.objects.create(
                course_section_id=course_section_id,
                course=courseObj,
                section_number='G0',
                learning_tools='_'.join(tools) if len(tools) > 0 else None,
                to_string=course_title+' G0',
            )
            course_sectioObj.save()

        # Associate course with faculty
        facultyObj.course_section.add(course_sectioObj)

    except Exception as e:
        traceback.print_exc()
        response['error_message'] = e.args[0]
        return render(requests, "Module_TeamManagement/Instructor/uploadcsv.html", response)

    # Reflush the nav bar
    utilities.populateRelevantCourses(requests, instructorEmail=requests.user.email)

    response['message'] = 'Course created'
    return faculty_Dashboard(requests)


# This is for subsequent configuration by faculty
# This function populates the database with the students information
#
# Requests param: POST
# - file
# - course_title
#
# Models to populate:
# - Students
# - Course_Section
# - Class
#
# Models to modify:
# - Faculty
#
# Response (Succcess):
# - configureDB_students
# - results
# - message
#
def configureDB_students(requests):
    response = {"configureDB_students" : "active"}

    # Retrieve all the course
    courseObject = Course.objects.all()
    courseList = []

    for course in courseObject:
        courseList.append(course.course_title)
    response['courses'] = courseList

    if requests.method == "GET":
        return render(requests, "Module_TeamManagement/Instructor/uploadcsv.html", response)

    try:
        file = requests.FILES.get("file", False)
        faculty_username = requests.user.email.split('@')[0]
        course_title = requests.POST.get("course_title")
        bootstrapFile = {}

        if course_title == None:
            raise Exception('Please enter a valid course title')

        if not file:
            raise Exception('Please enter a valid file')

        if file.name.endswith('.xlsx'):
            if 'student_information' in file.name.lower():
                bootstrapFile['course_title'] = course_title
                bootstrapFile['faculty_username'] = faculty_username
                bootstrapFile['file_path'] = file.temporary_file_path()

            else:
                raise Exception("Invalid file information. Please upload students information only.")

        else:
            raise Exception("Invalid file type. Please upload .xlsx only")

        # If file is .xlsx then proceed with processing
        response['results'] =  bootstrap.bootstrap_Students(requests,bootstrapFile)

    except Exception as e:
        # Uncomment for debugging - to print stack trace wihtout halting the process
        # traceback.print_exc()
        response['error_message'] = e.args[0]
        return render(requests, "Module_TeamManagement/Instructor/uploadcsv.html", response)

    # Reflush the nav bar
    utilities.populateRelevantCourses(requests, instructorEmail=requests.user.email)

    response['message'] = 'Successful Upload'
    # return render(requests, "Module_TeamManagement/Instructor/uploadcsv.html", response)
    return faculty_Dashboard(requests)


# This is for subsequent configuration by faculty
# This function configures the students team based on a excel file
#
# Requests param: POST
# - file
#
# Models to populate:
# - NONE
#
# Models to modify:
# - Class
#
# Response (Succcess):
# - configureDB_teams
# - results
# - message
#
def configureDB_teams(requests):
    response = {"configureDB_teams" : "active"}
    if requests.method == "GET":
        utilities.populateRelevantCourses(requests,instructorEmail=requests.user.email)
        response['courses'] = requests.session['courseList_updated']
        return render(requests, "Module_TeamManagement/Instructor/instructorTeams.html", response)

    try:
        file = requests.FILES.get("file", False)
        faculty_email = requests.user.email
        course_section = requests.POST.get("course_section")
        bootstrapFile = {}

        if course_section == None:
            raise Exception('Please enter a valid course section number')

        if not file:
            raise Exception('Please enter a valid file')

        if file.name.endswith('.xlsx'):
            if 'team_information' in file.name.lower():
                bootstrapFile['faculty_email'] = faculty_email
                bootstrapFile['course_section'] = course_section
                bootstrapFile['file_path'] = file.temporary_file_path()

            else:
                raise Exception("Invalid file information. Please upload teams information only.")

        else:
            raise Exception("Invalid file type. Please upload .xlsx only")

        # If file is .xlsx then proceed with processing
        response['results'] = bootstrap.update_Teams(bootstrapFile)

    except Exception as e:
        traceback.print_exc()
        response['error_message'] = e.args[0]
        response['courses'] = requests.session['courseList_updated']
        return render(requests, "Module_TeamManagement/Instructor/instructorTeams.html", response)

    response['message'] = 'Teams Configured'
    return faculty_Overview(requests)


# This is for subsequent configuration by faculty
# This function configures the CLT with the associate student
#
# Requests param: POST
# - file
# - course_title
#
# Models to populate:
# - Cloud_Learning_Tools
#
# Models to modify:
# - Class
#
# Response (Succcess):
# - configureDB_clt
# - results
# - message
#
def configureDB_clt(requests):
    response = {"configureDB_clt" : "active"}

    if requests.method == "GET" and requests.GET.get("user") == "faculty":
        utilities.populateRelevantCourses(requests,instructorEmail=requests.user.email)
        response['courses'] = requests.session['courseList_updated']
        return render(requests, "Module_TeamManagement/Instructor/instructorTools.html", response)

    elif requests.method == "GET" and (requests.GET.get("user") == "student" or requests.POST.get("user") == "student"):
        utilities.populateRelevantCourses(requests,studentEmail=requests.user.email)
        response['courses'] = requests.session['courseList_updated']
        return render(requests, "Module_TeamManagement/Student/studentTools.html", response)

    try:
        user = requests.POST.get("user")

        if user == "student":
            student_email = requests.user.email
            type = requests.POST.get("type")
            link = requests.POST.get("link")
            course = requests.POST.get("course_title")

            if course == None:
                raise Exception('Please specify a course.')
            elif type == None:
                raise Exception('Please specify a learning tool type.')
            elif len(link) == 0:
                raise Exception('Please specify a learning tool link.')
            elif "https://trailhead.salesforce.com/en/me/" not in link:
                raise Exception('Please specify a valid learning tool link.')

            id = student_email.split('@')[0] + "_" + type
            class_studentObj = Class.objects.filter(student=student_email).filter(course_section=course)
            try:
                # Update
                cltObj = Cloud_Learning_Tools.objects.get(id=id)
                cltObj.website_link = link
                cltObj.save()
            except:
                # Create
                cltObj = Cloud_Learning_Tools.objects.create(
                    id=id,
                    type=type,
                    website_link=link,
                )
                cltObj.save()

            for student in class_studentObj:
                student.clt_id.add(cltObj)

            utilities.webScrapper_SingleLink(student_email,link,course_section=course.replace(' ',''))
            return home(requests)

        file = requests.FILES.get("file", False)
        faculty_email = requests.user.email
        action = requests.POST.get("action")
        bootstrapFile = {}
        cleToolName = requests.POST.get("type")
        print(cleToolName)

        if action == 'batch':
            course = requests.POST.get("course_title")
        else:
            course = requests.POST.get("course_section")
        bootstrap.configureCourseToolsList(course,cleToolName) #Configures the course section database to include list of tools into the course section for display on dashboard

        if file:
            if file.name.endswith('.xlsx'):
                if 'learning_tools' in file.name.lower():
                    bootstrapFile['faculty_email'] = faculty_email
                    bootstrapFile['course'] = course
                    bootstrapFile['action'] = action
                    bootstrapFile['file_path'] = file.temporary_file_path()

                else:
                    raise Exception("Invalid file information. Please upload tools information only.")

            else:
                raise Exception("Invalid file type. Please upload .xlsx only")
        else:
            raise Exception("Please upload an excel file")

        # If file is .xlsx then proceed with processing
        response['results'] = bootstrap.update_CLT(bootstrapFile,course)
        utilities.webScrapper(course_selected=course )

    except Exception as e:
        traceback.print_exc()
        response['error_message'] = e.args[0]
        if requests.POST.get("user") == "student":
            utilities.populateRelevantCourses(requests,studentEmail=requests.user.email)
            response['courses'] = requests.session['courseList_updated']
            return render(requests, "Module_TeamManagement/Student/studentTools.html", response)

        if action == 'batch':
            utilities.populateRelevantCourses(requests,instructorEmail=requests.user.email)
            response['courses'] = requests.session['courseList_updated']
            return render(requests, "Module_TeamManagement/Instructor/instructorTools.html", response)

        else:
            return faculty_Overview(requests)

    response['message'] = 'Learning Tools Configured'

    if action == 'batch':
        utilities.populateRelevantCourses(requests,instructorEmail=requests.user.email)
        response['courses'] = requests.session['courseList_updated']
        return render(requests, "Module_TeamManagement/Instructor/instructorTools.html", response)
    else:
        return faculty_Overview(requests)


# This is for subsequent configuration by faculty
# This function authenticates the faculty and creates the channels/groups
#
# Requests param: GET
# - phone_number
#
# Models to modify:
# - Class
#
# Response (Succcess):
# - configure_telegram
# - results
# - message
#
def configureDB_telegram(requests):
    response = {"configure_telegram" : "active"}
    utilities.populateRelevantCourses(requests,instructorEmail=requests.user.email)
    response['courses'] = requests.session['courseList_updated']

    if requests.method == "GET":
        return render(requests, "Module_TeamManagement/Instructor/instructorTools.html", response)

    try:
        username = requests.user.email.split('@')[0]
        phone_number = requests.POST.get('phone_number')
        login_code = requests.POST.get('login_code')
        toolType = 'Telegram' if requests.POST.get('type') == None else requests.POST.get('type')

        facultyObj = Faculty.objects.get(username=username)
        registered_course = facultyObj.course_section.all()

        if len(phone_number) == 8:
            phone_number = str('+65') + phone_number

        client = tele_util.getClient(username)

        if not client.is_user_authorized():
            if phone_number != None and login_code == None:
                client.send_code_request(phone_number)

                encrypt_phone_number = utilities.encode(phone_number)
                facultyObj.phone_number = encrypt_phone_number
                facultyObj.save()

                return HttpResponse('')

            elif phone_number != None and login_code != None:
                try:
                    client.sign_in(phone=phone_number, code=login_code)
                except PhoneNumberUnoccupiedError:
                    client.sign_up(phone=phone_number, code=login_code)
        print(toolType)
        for course_section in registered_course:
            bootstrap.configureCourseToolsList(course_section.course_section_id,toolType)

        # Add faculty telegram username into DB
        # myself = client.get_me()
        # facultyObj.telegram_username = '@' + str(myself.username)
        # facultyObj.save()

        tele_util.disconnectClient(client)

    except Exception as e:
        traceback.print_exc()
        response['error_message'] = e.args[0]
        return render(requests, "Module_TeamManagement/Instructor/instructorTools.html", response)

    response['message'] = 'Telegram Account Configured'
    # return render(requests, "Module_TeamManagement/Instructor/instructorTools.html", response)
    return faculty_HomePage(requests)


line_chart = TemplateView.as_view(template_name='Module_TeamManagement\line_chart.html')


# <description>
#
class PhoneNumberFormView(AjaxFormMixin, FormView):
    form_class = PhoneNumberForm
    template_name  = 'Module_TeamManagement/Instructor/instructorTools.html'
    success_url = '/form-success/'


# Multistep form for telegram Setup
#
class TelegramWizard(SessionWizardView):
    template_name = "Module_TeamManagement/Instructor/telegram.html"

    def done(self, form_list, **kwargs):
        form_data = process_form_data(form_list)

        return render(self.request, 'Module_TeamManagement/Instructor/done.html', {'form_data': form_data})


# <description>
#
def process_form_data(form_list):
    form_data = [form.cleaned_data for form in form_list]

    logr.debug(form_data[0]['phone_number'])
    logr.debug(form_data[1]['login_code'])

    #add in method to return the validation Code
    return form_data


# For exporting the file
#
# Sample file dir would be clt_files\*School term*\*coursesection*
def clt_file_download(requests):
    schoolTerm = utilities.retrieve_school_term()
    course_section = requests.GET.get("module")
    output_file = os.path.join(os.getcwd(),'clt_files',schoolTerm.school_term_id.replace('/',""),course_section,'trailhead-points-log.csv')
    with open(output_file, 'rb') as myfile:
        response = HttpResponse(myfile, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=' + course_section+ 'trailhead-points.csv'
    return response


# <description>
#
def clt_file_ouput(requests):
    context ={}
    output_file = os.path.join(os.getcwd(),'clt_files','trailhead-points.csv')
    with open(output_file, 'r',encoding='utf-8') as myfile:
        fileValues = []
        csv_reader = csv.reader(myfile)
        for row in csv_reader:
            rowValue = ""
            for value in row:
                rowValue+= value+","

            fileValues.append(rowValue[:-1])
        context['csv_data'] = fileValues
    return render(requests, "Administrator/dummycsvpage.html", context)


# <description>
#
def trailhead_list(request):
    thm = Trailmix_Information.objects.all()
    return render(request, 'Module_TeamManagement/Instructor/instructorTrailmixes.html', {'thm': thm})


# <description>
#
def save_trailhead_form(request, form, template_name):
    from bs4 import BeautifulSoup
    import requests

    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            course_in_form = form.cleaned_data['course']
            link_in_form = form.cleaned_data['link']
            try:
                if_trailmix_exist = Trailmix_Information.objects.get(link=link_in_form, course = course_in_form) #If exist, do need to add more
            except: #if trailmix does not exist, create new entry
                newTrailMix = form.save()
                req = requests.get(newTrailMix.link)
                soup = BeautifulSoup(req.text, 'html.parser')
                title_broth = soup.find('div',attrs={'class': 'content-title'})
                description_broth = soup.find('div', attrs={'class': 'content-description'})
                newTrailMix.name = title_broth.text.strip()
                newTrailMix.description= (description_broth.text.strip())
                broth = soup.find_all('h3', attrs={'class': 'item-title'})
                badgeLinks = ""
                for broths in broth:
                    badgeLinks = badgeLinks + (broths.text.strip()) + " | "
                    #print(broths.a.get('href'))
                newTrailMix.badges = badgeLinks
                newTrailMix.save()
                facultyObj = Faculty.objects.get(email=request.user.email)
                courses = facultyObj.course_section.all()
                selected_course = newTrailMix.course
                course_sections = ""
                for course in courses:
                    if selected_course.course_title in course.course_section_id:
                        course_sections = course_sections + course.course_section_id +"_" #delimiter
                if course_sections == "":
                    newTrailMix.delete()  #No course selected, delete entry
                else:
                    newTrailMix.course_sections=course_sections
                    newTrailMix.save()
            data['form_is_valid'] = True
            thm = Trailmix_Information.objects.all()
            data['html_trailhead_list'] = render_to_string('dataforms/trailmixes/partial_trailhead_list.html', {
                'thm': thm
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


# <description>
#
def trailhead_create(request):
    if request.method == 'POST':
        form = TrailheadForm(request.POST)

    else:
        form = TrailheadForm()
    return save_trailhead_form(request, form, 'dataforms/trailmixes/partial_trailhead_create.html')


# <description>
#
def trailhead_delete(request, pk):
    trailhead = get_object_or_404(Trailmix_Information, pk=pk)
    data = dict()
    if request.method == 'POST':
        trailhead.delete()
        data['form_is_valid'] = True
        thm = Trailmix_Information.objects.all()
        data['html_trailhead_list'] = render_to_string('dataforms/trailmixes/partial_trailhead_list.html', {
            'thm': thm
        })
    else:
        context = {'trailhead': trailhead}
        data['html_form'] = render_to_string('dataforms/trailmixes/partial_trailhead_delete.html', context, request=request)
    return JsonResponse(data)
