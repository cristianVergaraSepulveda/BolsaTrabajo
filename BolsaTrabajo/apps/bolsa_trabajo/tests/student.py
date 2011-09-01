# coding: utf-8

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from ..utils import generate_user_digest
from ..models.student import Student


class NewStudentTestCase(TestCase):
    fixtures = ['users.json', 'student_level.json', 'student.json']

    def assert_and_check_messages(self, user, email_assertion, approval_assertion):
        self.assertTrue(self.client.login(username='test-student', password='test-student'))
        resp = self.client.get('/account/')
        self.assertEqual(user.profile.validated_email, email_assertion)
        self.assertEqual(user.profile.approved, approval_assertion)
        if not email_assertion:
            self.assertTrue('no ha sido verificado' in resp.content)
        else:
            self.assertTrue('Cuenta de correo activada correctamente' in resp.content)
            if not approval_assertion:
                self.assertTrue(
                    'no ha sido validada personalmente por un encargado, por favor espere hasta ser contactado.' in resp.content)
        self.client.logout()

    def test_new_student_view(self):
        resp = self.client.get('/account/register/student/')
        self.assertEqual(200, resp.status_code)

    def test_new_student_register_with_accepted_email(self):
        # create dictionary with new student info
        new_student_data = {'first_name': 'Test', 'last_name': 'Student', 'email': 'dleytonddd@dcc.uchile.cl',
                            'level': 1, 'resume': 'resumen alumno test 1', 'username': 'test-student',
                            'password': 'test-student', 'repeat_password': 'test-student'}

        # do a POST request including the new enterprise to be registered
        resp = self.client.post('/account/register/student/', new_student_data)

        # get the new student object from the database
        new_student = Student.objects.get(username='test-student')

        # assert that the student object has the expected username
        self.assertEqual(new_student.first_name, 'Test')

        # assert that the account hasn't been approved yet
        self.assert_and_check_messages(new_student, email_assertion=False, approval_assertion=False)

        # login
        self.assertTrue(self.client.login(username='test-student', password='test-student'))

        # go to the validation mail url
        key = generate_user_digest(new_student.username, new_student.email)
        resp2 = self.client.get('/account/validate_email/', {'validation_key': key})

        # get the new student object from the database (again to reflect db changes)
        new_student = Student.objects.get(username='test-student')

        # assert that the user's email has been validated and his/her account approved
        self.assert_and_check_messages(new_student, email_assertion=True, approval_assertion=True)

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
        new_student_data = {'first_name': 'Test', 'last_name': 'Student', 'email': 'dleytonddd@gmail.com', 'level': 1,
                            'resume': 'resumen alumno test 1', 'username': 'test-student', 'password': 'test-student',
                            'repeat_password': 'test-student'}

        # do a POST request including the new enterprise to be registered
        resp = self.client.post('/account/register/student/', new_student_data)

        # get the new student object from the database
        new_student = Student.objects.get(username='test-student')

        # assert that the student object has the expected username
        self.assertEqual(new_student.first_name, 'Test')

        # assert that the account hasn't been approved yet
        self.assert_and_check_messages(new_student, email_assertion=False, approval_assertion=False)

        # login
        self.assertTrue(self.client.login(username='test-student', password='test-student'))

        # go to the validation mail url
        key = generate_user_digest(new_student.username, new_student.email)
        resp2 = self.client.get('/account/validate_email/', {'validation_key': key})

        # get the new student object from the database
        new_student = Student.objects.get(username='test-student')

        # assert that the user's email has been validated and his/her account approved
        self.assert_and_check_messages(new_student, email_assertion=True, approval_assertion=False)

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

    def admin_registration_manage(self, pending_student):
        # get the user staff record
        sandra = User.objects.get(username='sandra')

        # get the user record within a pending registration
        accepted_student = Student.objects.get(username='pedrito')

        # check the integrity of that records
        self.assertEqual(sandra.username, 'sandra')
        self.assertEqual(accepted_student.username, 'pedrito')

        pending_student.profile.validated_email = True
        pending_student.profile.approved = False
        pending_student.profile.save()

        accepted_student.profile.validated_email = True
        accepted_student.profile.approved = True
        accepted_student.profile.save()

        self.assertEqual(pending_student.profile.validated_email, True)
        self.assertEqual(pending_student.profile.approved, False)
        self.assertTrue(pending_student.profile.is_student())

        # log in as staff user
        self.assertTrue(self.client.login(username='sandra', password='test'))

        # check the content of the staff user account page
        resp = self.client.get('/account/')
        self.assertTrue('Solicitudes de registro' in resp.content)

        # check the pending user is listed in the pending registrations
        resp2 = self.client.get('/account/pending_registration_request/')
        self.assertTrue('malito' in resp2.content)
        self.assertTrue('malito@gmail.com' in resp2.content)
        self.assertFalse('pedrito' in resp2.content)
        self.assertFalse('@dcc.uchile.cl' in resp2.content)

        # check the details of the pending registration
        resp3 = self.client.get('/account/pending_registration_request/' + str(pending_student.id) + '/')
        self.assertTrue('malito' in resp3.content)
        self.assertTrue('Aceptar la solicitud de registro' in resp3.content)
        self.assertTrue('Rechazar la solicitud de registro' in resp3.content)

    def test_admin_accept_new_registration_with_not_accepted_email(self):
        pending_student = Student.objects.get(username='malito')
        self.assertEqual(pending_student.username, 'malito')

        self.admin_registration_manage(pending_student)

        # accept pending registration
        self.client.get('/account/pending_registration_request/' + str(pending_student.id) + '/accept/')

        # get the updated pending student record
        old_pending_student = Student.objects.get(username='malito')

        # check that the pending student is now accepted
        self.assertEqual(old_pending_student.profile.validated_email, True)
        self.assertEqual(old_pending_student.profile.approved, True)

    def test_admin_reject_new_registration_with_not_accepted_email(self):
        pending_student = Student.objects.get(username='malito')
        self.assertEqual(pending_student.username, 'malito')

        self.admin_registration_manage(pending_student)

        # reject pending registration
        self.client.get('/account/pending_registration_request/' + str(pending_student.id) + '/reject/')
        # check that the record was deleted
        self.assertRaises(ObjectDoesNotExist, Student.objects.get, username='malito')
