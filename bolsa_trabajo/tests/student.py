# coding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import auth
from bolsa_trabajo.utils import generate_user_digest
from bolsa_trabajo.models.enterprise import Enterprise
from bolsa_trabajo.models.student import Student
from bolsa_trabajo.models.student_level import StudentLevel

class NewStudentTestCase(TestCase):

    fixtures = ['users.json','student_level.json','student.json']

    def assert_and_check_messages(self,user,email_assertion,approval_assertion):
        self.assertTrue(self.client.login(username='test-student',password='test-student'))
        resp = self.client.get('/account/')
        self.assertEqual(user.profile.validated_email,email_assertion)
        self.assertEqual(user.profile.approved,approval_assertion)
        if not email_assertion:
            self.assertTrue('no ha sido verificado' in resp.content)
        else:
            self.assertTrue('Cuenta de correo activada correctamente' in resp.content)
            if not approval_assertion:
                self.assertTrue('no ha sido validada personalmente por un encargado, por favor espere hasta ser contactado.' in resp.content)
        self.client.logout()

    def test_new_student_view(self):
        resp = self.client.get('/account/register/student/')
        self.assertEqual(200,resp.status_code)

    def test_new_student_register_with_accepted_email(self):
        # create dictionary with new student info
        new_student_data = {'first_name':'Test', 'last_name':'Student', 'email':'dleytonddd@dcc.uchile.cl', 'level':1, 'resume':'resumen alumno test 1', 'username':'test-student', 'password':'test-student', 'repeat_password':'test-student'}

        # do a POST request including the new enterprise to be registered
        resp = self.client.post('/account/register/student/',new_student_data)

        # get the new student object from the database
        new_student = Student.objects.get(username='test-student')

        # assert that the student object has the expected username
        self.assertEqual(new_student.first_name,'Test')

        # assert that the account hasn't been approved yet
        self.assert_and_check_messages(new_student,email_assertion=False,approval_assertion=False)

        # login
        self.assertTrue(self.client.login(username='test-student',password='test-student'))

        # go to the validation mail url
        key = generate_user_digest(new_student.username, new_student.email)
        resp2 = self.client.get('/account/validate_email/',{'validation_key' : key})

        # get the new student object from the database (again to reflect db changes)
        new_student = Student.objects.get(username='test-student')

        # assert that the user's email has been validated and his/her account approved
        self.assert_and_check_messages(new_student,email_assertion=True,approval_assertion=True)

        '''
        # the email account should be validated
        self.assertTrue(new_student.profile.validated_email)

        # message about email validation should be shown to the user
        self.client.login(username='test-student',password='test-student')
        resp = self.client.get('/account/')
        self.assertTrue('Cuenta de correo activada correctamente' in resp.content)
        '''

    def test_new_student_register_with_not_accepted_email(self):
        # create dictionary with new student info
        new_student_data = {'first_name':'Test', 'last_name':'Student', 'email':'dleytonddd@gmail.com', 'level':1, 'resume':'resumen alumno test 1', 'username':'test-student', 'password':'test-student', 'repeat_password':'test-student'}

        # do a POST request including the new enterprise to be registered
        resp = self.client.post('/account/register/student/',new_student_data)

        # get the new student object from the database
        new_student = Student.objects.get(username='test-student')

        # assert that the student object has the expected username
        self.assertEqual(new_student.first_name,'Test')

        # assert that the account hasn't been approved yet
        self.assert_and_check_messages(new_student,email_assertion=False,approval_assertion=False)

        # login
        self.assertTrue(self.client.login(username='test-student',password='test-student'))

        # go to the validation mail url
        key = generate_user_digest(new_student.username, new_student.email)
        resp2 = self.client.get('/account/validate_email/',{'validation_key' : key})

        # get the new student object from the database
        new_student = Student.objects.get(username='test-student')

        # assert that the user's email has been validated and his/her account approved
        self.assert_and_check_messages(new_student,email_assertion=True,approval_assertion=False)

        # finally the user must be on hold
        #self.assertTrue(new_student.accepted) #ESTO REALMENTE DEBE ESTAR ACÁ

        '''
        # the email account should be validated
        self.assertTrue(new_student.profile.validated_email)

        # message about email validation should be shown to the user
        self.client.login(username='test-enterprise',password='test-enterprise')
        resp = self.client.get('/account/')
        self.assertTrue('Cuenta de correo activada correctamente' in resp.content)

        # message about account approval should be shown to the user
        self.assertTrue('no ha sido validada personalmente por un encargado, por favor espere hasta ser contactado.' in resp.content)
        '''
