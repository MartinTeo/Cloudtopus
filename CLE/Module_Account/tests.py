from django.test import  RequestFactory,TestCase
# Create your tests here.
from Module_Account.src import processLogin
from django.contrib.auth.models import User

from Module_TeamManagement.models import *

class AccountModuleTest(TestCase):
    def test_login(self):
        a = processLogin.validate("admin","admin")
        self.assertTrue(isinstance(a, User))
        
        b = processLogin.validate("admin","admi2n")
        self.assertFalse(isinstance(b, User))

class AccountVerificationTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
                
    def test_student_verification(self):
        self.student = Student.objects.create(email="martin.teo.2016@smu.edu.sg",username ="martin.teo.2016",firstname="Martin",lastname="Teo")        
        request = self.factory.get('/home/')
        request.user = self.student
        try:
            processLogin.studentVerification(request)
            response = True
        except: 
            response = False
        self.assertTrue(response)

        request.user = None
        try:
            processLogin.studentVerification(request)
            response = True
        except: 
            response = False
        self.assertFalse(response)
        Student.objects.all().delete()

    def test_instructor_verification(self):
        self.instructor = Faculty.objects.create(email="ch.lee@smu.edu.sg",username ="ch.lee",firstname="ChuanHui",lastname="Lee")
        request = self.factory.get('/instructor/home/')
        request.user = self.instructor
        try:
            processLogin.InstructorVerification(request)
            response = True
        except: 
            response = False
        self.assertTrue(response)

        request.user = None
        try:
            processLogin.InstructorVerification(request)
            response = True
        except: 
            response = False
        self.assertFalse(response)
        Faculty.objects.all().delete()



