# import unittest  # Note: this is 3.3's unittest2!

from django.test import TestCase

from trs import models


class PersonTestCase(TestCase):

    def test_smoke(self):
        person = models.Person()
        self.assertTrue(person)


class ProjectTestCase(TestCase):

    def test_smoke(self):
        project = models.Project()
        self.assertTrue(project)
