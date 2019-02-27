import os
import xlrd
import time
import traceback
import datetime
from django.core.files import File
from Module_TeamManagement.src import utilities
from Module_TeamManagement.models import *
from Module_DeploymentMonitoring.models import *
from Module_CommunicationManagement.src import tele_config

#-----------------------------------------------------------------------------#
#-------------------------- Bootstrap Function -------------------------------#
#-----------------------------------------------------------------------------#

def clear_Database():
    Deployment_Package.objects.all().delete()
    Server_Details.objects.all().delete()
    AWS_Credentials.objects.all().delete()
    Image_Details.objects.all().delete()
    Class.objects.all().delete()
    School_Term.objects.all().delete()
    Cloud_Learning_Tools.objects.all().delete()
    Faculty.objects.all().delete()
    Course_Section.objects.all().delete()
    Student.objects.all().delete()
    Course.objects.all().delete()
    Telegram_Chats.objects.all().delete()

    session_folder = tele_config.SESSION_FOLDER
    for session_file in os.listdir(session_folder):
        file_path = os.path.join(session_folder,session_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            raise e


def parse_File_Student(filePath,bootstrapInfo={}):

    # Create a workbook object from the filePath
    workbook = xlrd.open_workbook(filePath)

    # Get first worksheet
    sheet = workbook.sheet_by_index(0)

    # Get headers
    headers = sheet.row_values(0)

    # Get header indexes of each column
    index_username = headers.index('Username')
    index_lastname = headers.index('Last Name')
    index_firstname = headers.index('First Name')
    index_email = headers.index('Email')
    index_section = headers.index('Section')

    # Start with '1' instead of '0' to clear header buffer
    for row in range(1,sheet.nrows):
        student = []
        rowData = sheet.row_values(row)

        # Declare variables
        username = rowData[index_username].strip()
        if '\\' in username:
            username = username.split("\\")[1]

        section_number = rowData[index_section].strip()
        if ',' in section_number:
            section_number = section_number.split(",")[1]

        teamList = rowData[index_section+1:]
        if len(teamList) > 0:
            if 'Team' in list(filter(None,teamList))[0]:
                team_number = 'T' + list(filter(None,teamList))[0].split()[-1]
            else:
                team_number = list(filter(None,teamList))[0]
            student.append(team_number)

        email = rowData[index_email].strip()
        firstname = rowData[index_firstname].strip()
        lastname = rowData[index_lastname].strip()

        # Create student : list
        student = [email,username,firstname,lastname] + student

        # Store in dict with section_number as key and student : list as value
        try:
            bootstrapInfo[section_number]['students'].append(student)
        except Exception as ex:
            if ex.args[0] == section_number:
                bootstrapInfo[section_number] = {'students':[student]}
            elif ex.args[0] == 'student':
                bootstrapInfo[section_number].update({'students':[student]})

    return bootstrapInfo


def parse_File_Faculty(filePath,bootstrapInfo={}):

    # Create a workbook object from the filePath
    workbook = xlrd.open_workbook(filePath)

    # Get first worksheet
    sheet = workbook.sheet_by_index(0)

    # Get headers
    headers = sheet.row_values(0)

    # Get header indexes of each column
    index_username = headers.index('Username')
    index_lastname = headers.index('Last Name')
    index_firstname = headers.index('First Name')
    index_email = headers.index('Email')

    # Start with '1' instead of '0' to clear header buffer
    for row in range(1,sheet.nrows):
        faculty = []
        rowData = sheet.row_values(row)

        # Declare variables
        username = rowData[index_username].strip()
        if '\\' in username:
            username = username.split("\\")[1]

        email = rowData[index_email].strip()
        firstname = rowData[index_firstname].strip()
        lastname = rowData[index_lastname].strip()

        if 'Phone Number' in headers:
            phoneNumber = str(int(rowData[headers.index('Phone Number')])).strip()
            if len(phoneNumber) == 8:
                phoneNumber = str('+65') + phoneNumber

            encrypt_phoneNumber = utilities.encode(phoneNumber)
            faculty.append(encrypt_phoneNumber)

        # Create faculty : list
        faculty = [email,username,firstname,lastname] + faculty

        # Store in dict with faculty as key and faculty : list as value
        try:
            bootstrapInfo['faculty'].append(faculty)
        except:
            bootstrapInfo['faculty'] = [faculty]

    return bootstrapInfo


def parse_File_Course(filePath,bootstrapInfo={}):

    # Create a workbook object from the classFile
    workbook = xlrd.open_workbook(filePath)

    # Get first worksheet
    sheet = workbook.sheet_by_index(0)

    # Get headers
    headers = sheet.row_values(0)

    # Get header indexes of each column
    index_title = headers.index('Title')
    index_name = headers.index('Name')
    index_desc = headers.index('Description')

    # Start with '1' instead of '0' to clear header buffer
    for row in range(1,sheet.nrows):
        rowData = sheet.row_values(row)

        # Declare variables
        course_Title = rowData[index_title].strip()
        course_Name = rowData[index_name].strip()
        course_Desc = rowData[index_desc].strip()

        # Create course : list
        course = [course_Title,course_Name,course_Desc]

        # Store in dict with course as key and course : list as value
        try:
            bootstrapInfo['course'].append(course)
        except:
            bootstrapInfo['course'] = [course]

    return bootstrapInfo


def parse_File_Team(filePath,bootstrapInfo={}):

    # Create a workbook object from the filePath
    workbook = xlrd.open_workbook(filePath)

    # Get first worksheet
    sheet = workbook.sheet_by_index(0)

    # Get headers
    headers = sheet.row_values(0)

    # Get header indexes of each column
    index_email = headers.index('Email')
    index_section = headers.index('Section')

    # Start with '1' instead of '0' to clear header buffer
    for row in range(1,sheet.nrows):
        rowData = sheet.row_values(row)

        # Declare variables
        email = rowData[index_email].strip()

        teamList = rowData[index_section+1:]
        if len(teamList) > 0:
            if 'Team' in list(filter(None,teamList))[0]:
                team_number = 'T' + list(filter(None,teamList))[0].split()[-1]
            else:
                team_number = list(filter(None,teamList))[0]
            bootstrapInfo[email] = team_number

    return bootstrapInfo


def parse_File_CLT(filePath,bootstrapInfo={}):

    # Create a workbook object from the filePath
    workbook = xlrd.open_workbook(filePath)

    # Get first worksheet
    sheet = workbook.sheet_by_index(0)

    # Get headers
    headers = sheet.row_values(0)

    # Get header indexes of each column
    index_email = headers.index('Email')
    index_type = headers.index('Type')
    index_link = headers.index('Link')

    # Start with '1' instead of '0' to clear header buffer
    for row in range(1,sheet.nrows):
        rowData = sheet.row_values(row)

        # Declare variables
        email = rowData[index_email].strip()
        type = rowData[index_type].strip()
        link = rowData[index_link]
        id = email.lower().split('@')[0] + '_' + type

        # Create clt : list
        clt = [id,type,link]

        # Store in dict with email as key and clt : list as value
        try:
            bootstrapInfo[email].append(clt)
        except:
            bootstrapInfo[email] = [clt]

    return bootstrapInfo


def bootstrap_Faculty(fileDict):
    bootstrapInfo = {}
    results = {}

    if fileDict['file_type'] == 'zip':
        bootstrapInfo = parse_File_Faculty(fileDict['faculty'], bootstrapInfo)
        bootstrapInfo = parse_File_Course(fileDict['course'], bootstrapInfo)

    elif fileDict['file_type'] == 'excel' and fileDict['file_information'] == 'course':
        bootstrapInfo = parse_File_Course(fileDict['file_path'], bootstrapInfo)

    elif fileDict['file_type'] == 'excel' and fileDict['file_information'] == 'faculty':
        bootstrapInfo = parse_File_Faculty(fileDict['file_path'], bootstrapInfo)

    try:
        if len(bootstrapInfo) == 0:
            raise Exception

        start_date = fileDict['start_date']
        end_date = fileDict['end_date']
        financial_year = utilities.getFinancialYear()
        school_term_number = utilities.getSchoolTerm()
        school_term_id = financial_year + 'T' + str(school_term_number)

        try:
            School_Term.objects.get(school_term_id=school_term_id)
        except:
            school_temrObj = School_Term.objects.create(
                school_term_id=school_term_id,
                term=school_term_number,
                financial_year=financial_year,
                start_date=start_date,
                end_date=end_date if end_date != None else start_date + datetime.timedelta(weeks=16),
            )
            school_temrObj.save()

        for user,data in bootstrapInfo.items():
            if user == 'course':
                results['course_count'] = len(data)
                for course in data:
                    try:
                        Course.objects.get(course_title=course[0])
                    except:
                        courseObj = Course.objects.create(
                            course_title=course[0],
                            course_name=course[1],
                            course_description=course[2],
                        )
                        courseObj.save()
            else:
                results['faculty_count'] = len(data)
                for faculty in data:
                    try:
                        Faculty.objects.get(email=faculty[0])
                    except:
                        facultyObj = Faculty.objects.create(
                            email=faculty[0],
                            username=faculty[1],
                            firstname=faculty[2],
                            lastname=faculty[3],
                            phone_number=faculty[4] if len(faculty) == 5 else None,
                        )
                        facultyObj.save()

    except Exception as e:
        # Uncomment for debugging - to print stack trace wihtout halting the process
        #traceback.print_exc()
        raise Exception('Unsuccessful Upload. There was an error during the inserting of data into the database')

    return results


def bootstrap_Students(requests,fileDict):
    bootstrapInfo = {}
    results = {}

    bootstrapInfo = parse_File_Student(fileDict['file_path'],bootstrapInfo)

    course_title = fileDict['course_title']
    faculty_username = fileDict['faculty_username']

    facultyObj = Faculty.objects.get(username=faculty_username)
    courseObj = Course.objects.get(course_title=course_title)

    # Clear info from database =================================================
    try:
        section_numbers = bootstrapInfo.keys()
        course_section_ids = [course_title + section_number for section_number in section_numbers]

        for course_section_id in course_section_ids:
            if Class.objects.all().filter(course_section=course_section_id).exists():
                Class.objects.all().filter(course_section=course_section_id).delete()
            if Course_Section.objects.all().filter(course_section_id=course_section_id).exists():
                course_sectionObj = Course_Section.objects.get(course_section_id=course_section_id)
                facultyObj.course_section.remove(course_sectionObj)
                #course_sectionObj.delete()

    except Exception as e:
        # Uncomment for debugging - to print stack trace wihtout halting the process
        traceback.print_exc()
        raise Exception('Unsuccessful Upload. There was an error during the purging of the database')
    # ==========================================================================

    # If faculty previously initialize a course without adding student, he will be associated to a section G0
    # This try,catch is to remove that section G0 before associating a true section
    try:
        existing_course_sectionObj = Course_Section.objects.get(course_section_id=course_title+'G0')
        facultyObj.course_section.all().filter(course_section_id=existing_course_sectionObj)
        facultyObj.course_section.remove(existing_course_sectionObj)
    except:
        pass

    # Get school term object
    school_term_id = utilities.getFinancialYear() + 'T' + str(utilities.getSchoolTerm())
    school_termObj = School_Term.objects.get(school_term_id=school_term_id)

    # Bootstrap info into database =============================================
    try:
        if len(bootstrapInfo) == 0:
            raise Exception

        student_count = 0
        for section_number,section_Data in bootstrapInfo.items():
            try:
                course_sectionObj = Course_Section.objects.get(course_section_id=course_title+section_number)
            except:
                course_sectionObj = Course_Section.objects.create(
                    course_section_id=course_title+section_number,
                    course=courseObj,
                    section_number=section_number,
                    to_string=course_title+" "+section_number,
                )
                course_sectionObj.save()

            itOps_tool = requests.POST.get("add_tool")
            if requests.session['configured_Tools'] == None:
                tools = [itOps_tool]
            else:
                tools = ['Telegram'] if 'Telegram' in requests.session['configured_Tools'] else []
                if itOps_tool != None:
                    tools.append(itOps_tool)

            course_sectionObj.learning_tools = '_'.join(tools) if len(tools) > 0 else None
            course_sectionObj.save()

            facultyObj.course_section.add(course_sectionObj)

            for user,data in section_Data.items():
                if user == 'students':
                    student_count += len(data)
                    for student in data:
                        stuEmail = (student[0].split("@")[0]+ "@smu.edu.sg").lower()
                        try:
                            studentObj = Student.objects.get(email=stuEmail)
                            studentObj.email=stuEmail
                            studentObj.username=student[1]
                            studentObj.firstname=student[2]
                            studentObj.lastname=student[3]
                            studentObj.save()
                        except:
                            studentObj = Student.objects.create(
                                email=stuEmail,
                                username=student[1],
                                firstname=student[2],
                                lastname=student[3],
                            )
                            studentObj.save()

                        try:
                            classObj = Class.objects.get(student=studentObj)
                            classObj.course_section=course_sectionObj
                            classObj.team_number=student[4] if len(student) == 5 else None
                            classObj.save()
                        except:
                            classObj = Class.objects.create(
                                student=studentObj,
                                course_section=course_sectionObj,
                                team_number=student[4] if len(student) == 5 else None,
                                school_term=school_termObj,
                            )
                            classObj.save()

        results['section_count'] = len(bootstrapInfo)
        results['student_count'] = student_count

    except Exception as e:
        # Uncomment for debugging - to print stack trace wihtout halting the process
        traceback.print_exc()
        raise Exception('Unsuccessful Upload. There was an error during the inserting of data into the database')
    # ==========================================================================

    return results

'''
Configures the course section database to include list of tools into the course section for display on dashboard
Does not create the list of tools associated in the database
'''
def configureCourseToolsList(course_section, toolName):
    course_sectionObj = Course_Section.objects.get(course_section_id=course_section)

    if course_sectionObj.learning_tools == None:
        course_sectionObj.learning_tools = toolName
    else:
        if toolName not in course_sectionObj.learning_tools:
            course_sectionObj.learning_tools = course_sectionObj.learning_tools + "_" + toolName

    course_sectionObj.save()
    return


def update_Teams(fileDict):
    bootstrapInfo = {}
    results = {}

    bootstrapInfo = parse_File_Team(fileDict['file_path'],bootstrapInfo)
    faculty_email = fileDict['faculty_email']
    course_section = fileDict['course_section']

    try:
        if len(bootstrapInfo) == 0:
            raise Exception

        facultyObj = Faculty.objects.get(email=faculty_email)

        # For each student that falls under that specific course_section, update their team_number
        for student_email,team_number in bootstrapInfo.items():
            classObj = Class.objects.filter(student=student_email).filter(course_section=course_section)
            for student in classObj:
                student.team_number = team_number
                student.save()

        results['student_count'] = len(bootstrapInfo)

    except Exception as e:
        # Uncomment for debugging - to print stack trace wihtout halting the process
        traceback.print_exc()
        raise Exception('Unsuccessful Upload. There was an error during the inserting of data into the database')

    return results


def update_CLT(fileDict, course):
    bootstrapInfo = {}
    results = {}
    course_section_selected =  Course_Section.objects.get(course_section_id=course)
    bootstrapInfo = parse_File_CLT(fileDict['file_path'],bootstrapInfo)
    faculty_email = fileDict['faculty_email']
    course = fileDict['course']
    action = fileDict['action']

    try:
        if len(bootstrapInfo) == 0:
            raise Exception

        facultyObj = Faculty.objects.get(email=faculty_email)

        # For each student that falls under that specific course_section, create the CLT object and update their CLT
        for student_email,clt_list in bootstrapInfo.items():
            for clt in clt_list:
                try:
                    # Update link
                    cltObj = Cloud_Learning_Tools.objects.get(id=clt[0])
                    cltObj.website_link = clt[2]
                    cltObj.save()
                except:
                    # Create new object
                    cltObj = Cloud_Learning_Tools.objects.create(
                        id=clt[0],
                        type=clt[1],
                        website_link=clt[2]
                    )
                    cltObj.save()
                print(course_section_selected)
                print(course_section_selected not in cltObj.course_section.all())
                if course_section_selected not in cltObj.course_section.all():
                    cltObj.course_section.add(course_section_selected)
                    print(course_section_selected not in cltObj.course_section.all())

                if action == 'batch':
                    course_sections = facultyObj.course_section.all()
                    for course_section in course_sections:
                        if course in course_section.course_section_id:
                            classObj = Class.objects.filter(student=student_email).filter(course_section=course_section)
                            for student in classObj:
                                student.clt_id.add(cltObj)
                else:
                    classObj = Class.objects.filter(student=student_email).filter(course_section=course)
                    for student in classObj:
                        student.clt_id.add(cltObj)

        results['student_count'] = len(bootstrapInfo)

    except Exception as e:
        # Uncomment for debugging - to print stack trace wihtout halting the process
        traceback.print_exc()
        raise Exception('Unsuccessful Upload. There was an error during the inserting of data into the database')

    return results
