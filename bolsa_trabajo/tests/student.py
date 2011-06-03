from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import auth
from bolsa_trabajo.models.enterprise import Enterprise
from bolsa_trabajo.models.student import Student
from bolsa_trabajo.models.student_level import StudentLevel


class NewStudentTestCase(TestCase):

    fixtures = ['users.json','student_level.json','student.json']

    def test_new_student_view(self):
        resp = self.client.get('/account/register/student/')
        self.assertEqual(200,resp.status_code)

    def test_new_student_register(self):

        # create dictionary with new student info
        new_student_data = {'first_name':'Test', 'last_name':'Student', 'email':'dleytonddd@gmail.com', 'level':1, 'resume':'resumen alumno test 1', 'username':'test-student', 'password':'test-student', 'repeat_password':'test-student'}

        # do a POST request including the new enterprise to be registered
        resp = self.client.post('/account/register/student/',new_student_data)

        # get the new student object from the database
        new_student = Student.objects.get(username='test-student')

        # assert that the student object has the expected username
        self.assertEqual(new_student.first_name,'Test')

		# assert that the student object is not active, the new user should not logging in, so the login function should return False
        self.assertFalse(self.client.login(username='test-student',password='test-student'))

        #activate the new student object
        new_student.is_active = True
        new_student.save()

        # when logging in using the new student username and password, the login function should return True
        self.assertTrue(self.client.login(username='test-student',password='test-student'))


    def test_data_student_fixture(self):
        ent = Student.objects.get(first_name='testName1')
        self.assertEqual(ent.resume,'Lorem ipsumnderit')
