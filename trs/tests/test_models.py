# import unittest  # Note: this is 3.3's unittest2!
from django.test import TestCase

from trs import models
from trs.tests import factories


class PersonTestCase(TestCase):

    def test_smoke(self):
        person = factories.PersonFactory.create()
        self.assertTrue(person)

    def test_representation(self):
        person = factories.PersonFactory.build(name='Pietje')
        self.assertEqual(str(person), 'Pietje')

    def test_get_absolute_url(self):
        person = factories.PersonFactory.build(slug='reinout')
        self.assertEqual(person.get_absolute_url(), '/persons/reinout/')

    def test_as_widget(self):
        person = factories.PersonFactory.build()
        self.assertTrue(person.as_widget())

    def test_sorting(self):
        factories.PersonFactory.create(name='Reinout')
        factories.PersonFactory.create(name='Maurits')
        self.assertEqual(models.Person.objects.all()[0].name,
                         'Maurits')


class ProjectTestCase(TestCase):

    def test_smoke(self):
        project = models.Project()
        project.save()
        self.assertTrue(project)

    def test_representation(self):
        project = models.Project(code='P1234')
        self.assertEqual(str(project), 'P1234')

    def test_get_absolute_url(self):
        project = models.Project(code='P1234', slug='P1234')
        self.assertEqual(project.get_absolute_url(), '/projects/P1234/')

    def test_as_widget(self):
        project = models.Project(code='P1234', slug='P1234')
        self.assertTrue(project.as_widget())

    def test_sorting(self):
        project1 = models.Project(code='P1234')
        project1.save()
        project2 = models.Project(code='P0123')
        project2.save()
        self.assertEqual(models.Project.objects.all()[0].code,
                         'P0123')


class PersonChangeTestCase(TestCase):

    def test_smoke(self):
        person_change = models.PersonChange()
        person_change.save()
        self.assertTrue(person_change)


class BookingTestCase(TestCase):

    def test_smoke(self):
        booking = models.Booking()
        booking.save()
        self.assertTrue(booking)


class WorkAssignmentTestCase(TestCase):

    def test_smoke(self):
        work_assignment = models.WorkAssignment()
        work_assignment.save()
        self.assertTrue(work_assignment)


class BudgetAssignmentTestCase(TestCase):

    def test_smoke(self):
        budget_assignment = models.BudgetAssignment()
        budget_assignment.save()
        self.assertTrue(budget_assignment)
