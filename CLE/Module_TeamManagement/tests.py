from django.test import TestCase

# Create your tests here.
from Module_TeamManagement.src import bootstrap, utilities, tele_util
from Module_TeamManagement.models import *

class DatabaseModelTest(TestCase):
    def test_clearDbTest(self):
        bootstrap.clear_Database()
        
        cltList = School_Term.objects.all()
        self.assertTrue(cltList.count()== 0)
        termList = School_Term.objects.all()
        self.assertTrue(termList.count()== 0)
        courseList = Course.objects.all()
        self.assertTrue(courseList.count()== 0)
        courseSectList = Course_Section.objects.all()
        self.assertTrue(courseSectList.count()== 0)
        classList = Class.objects.all()
        self.assertTrue(classList.count()== 0)
        facList = Faculty.objects.all()
        self.assertTrue(facList.count()== 0)
        stuList = Student.objects.all()
        self.assertTrue(stuList.count()== 0)


class CourseModelTest(TestCase):
    def create_Course(self, title="IS200", courseName = "Intro to Java", description = "Java"):
        return Course.objects.create(course_title = title, course_name= courseName, course_description=description)
    
    def create_courseSection(self, course="", sectionNum = "G5" ):
        return Course_Section.objects.create(course_section_id=course.course_title+sectionNum,
                    course=course,
                    section_number=sectionNum,
                    to_string=course.course_title+" "+sectionNum,
                )
    def test_course_creation(self):
        courseExample = self.create_Course()
        self.assertTrue(isinstance(courseExample, Course))
    
    def test_course_name(self):
        courseExample = self.create_Course(title="IS201")
        self.assertEqual(courseExample.course_title, "IS201")
    
    def test_course_section_creation(self):
        try:
            courseSection = self.create_courseSection() #No foreign key
        except:
            pass
        courseExample = self.create_Course(title="IS202")    
        courseSection = self.create_courseSection(course = courseExample)
        courseSectList = Course_Section.objects.all()
        self.assertTrue(courseSectList.count()== 1)
        for i in range(0,4):
            courseSection = self.create_courseSection(course = courseExample, sectionNum = "G" + str(i))
        courseSectList = Course_Section.objects.all()
        self.assertTrue(courseSectList.count()== 5)
        

class StudentModelTest(TestCase):
    def create_Student(self, stuEmail="debbielee.2016@smu.edu.sg", stuUsername = "debbielee.2016", firstName = "Debbie", lastName="Lee", telegramuser="@deblee"):
        return Student.objects.create(email = stuEmail, username= stuUsername, firstname=firstName, lastname =lastName , telegram_username=telegramuser)
    
    def test_student_creation(self):
        studentA = self.create_Student()
        self.assertTrue(isinstance(studentA, Student))
        self.assertFalse(isinstance(studentA, Course))

    def test_student_creationSameStudentError(self):
        try:
            studentB = self.create_Student(stuEmail="debbiElee.2016@smu.edu.sg", stuUsername = "debbielee.2016", firstName = "Debbie", lastName="Lee", telegramuser="@deblee")
        except:
            pass 

    def test_student_creationSecondStudent(self):
        studentB = self.create_Student(stuEmail="samlee.2017@smu.edu.sg", stuUsername = "samlee.2017", firstName = "Sam", lastName="Lee", telegramuser="@samlee")
        self.assertEqual(studentB.username, "samlee.2017")
        self.assertEqual(studentB.firstname, "Sam")

    def test_student_creationSecondStudentCount(self):
        sList = Student.objects.all()
        self.assertTrue(sList.count()== 2)