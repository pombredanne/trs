import datetime

from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser
import mock

from trs import views
from trs.tests import factories

REINOUTS_BIRTHDATE = datetime.date(year=1972, month=12, day=25)


class BaseMixinTestCase(TestCase):

    def setUp(self):
        self.view = views.BaseMixin()
        self.view.request = RequestFactory().get('/')

    def test_today(self):
        self.assertTrue(self.view.today)

    def test_active_projects_is_iterable(self):
        # if no one is logged in, we should be iterable, too.
        self.view.request = RequestFactory().get('/')
        self.view.request.user = AnonymousUser()
        self.assertEqual(self.view.active_projects, [])

    def test_active_person(self):
        # if no one is logged in, we should be iterable, too.
        person = factories.PersonFactory.create()
        self.view.request.user = person.user
        self.assertEqual(self.view.active_person, person)

    def test_active_projects(self):
        person = factories.PersonFactory.create()
        project1 = factories.ProjectFactory.create(code='p1')
        project2 = factories.ProjectFactory.create(code='p2')
        factories.WorkAssignmentFactory(assigned_to=person,
                                        assigned_on=project1)
        factories.WorkAssignmentFactory(assigned_to=person,
                                        assigned_on=project2)
        self.view.request.user = person.user
        self.assertEqual(list(self.view.active_projects),
                         [project1, project2])


class PersonsViewTestCase(TestCase):

    def setUp(self):
        self.person1 = factories.PersonFactory.create(slug='person1')
        self.person2 = factories.PersonFactory.create(slug='person2')

    def test_smoke(self):
        view = views.PersonsView()
        self.assertEqual(list(view.persons), [self.person1, self.person2])


class PersonViewTestCase(TestCase):

    def setUp(self):
        self.person = factories.PersonFactory.create()

    def test_smoke(self):
        view = views.PersonView(kwargs={'slug': self.person.slug})
        self.assertEqual(view.person, self.person)


class ProjectsViewTestCase(TestCase):

    def setUp(self):
        self.project1 = factories.ProjectFactory.create(slug='project1')
        self.project2 = factories.ProjectFactory.create(slug='project2')

    def test_smoke(self):
        view = views.ProjectsView()
        self.assertEqual(list(view.projects), [self.project1, self.project2])


class ProjectViewTestCase(TestCase):

    def setUp(self):
        self.project = factories.ProjectFactory.create()

    def test_smoke(self):
        view = views.ProjectView(kwargs={'slug': self.project.slug})
        self.assertEqual(view.project, self.project)


class BookingViewTestCase(TestCase):

    def test_active_year_week_explicit(self):
        year = 1972
        week = 51
        year_week = factories.YearWeekFactory.create(year=year, week=week)
        view = views.BookingView(kwargs={'year': year, 'week': week})
        self.assertEqual(view.active_year_week, year_week)

    def test_active_year_week_implicit(self):
        year_week = factories.YearWeekFactory.create(
            year=1972,
            week=51,
            first_day=REINOUTS_BIRTHDATE)

        def _mock_date(self):
            return REINOUTS_BIRTHDATE

        with mock.patch('trs.views.BaseMixin.today', _mock_date):
            view = views.BookingView(kwargs={})
            self.assertEqual(view.active_year_week, year_week)

    def test_active_first_day(self):
        factories.YearWeekFactory.create(
            year=1972,
            week=51,
            first_day=REINOUTS_BIRTHDATE)
        view = views.BookingView(kwargs={'year': 1972, 'week': 51})
        self.assertEqual(view.active_first_day, REINOUTS_BIRTHDATE)

    def test_year_weeks_to_display(self):
        factories.YearWeekFactory.create()  # week 1
        year_week2 = factories.YearWeekFactory.create()
        year_week3 = factories.YearWeekFactory.create()
        year_week4 = factories.YearWeekFactory.create()
        year_week5 = factories.YearWeekFactory.create()
        factories.YearWeekFactory.create()  # week 6
        current_year_week = year_week4
        # So we want 2 and 3 before, 4 itself and 5 as the next one.
        view = views.BookingView(kwargs={'year': current_year_week.year,
                                         'week': current_year_week.week})
        self.assertEqual(list(view.year_weeks_to_display),
                              [year_week2, year_week3, year_week4, year_week5])
