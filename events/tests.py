from django.test import TestCase
from .models import Profile,Project,Ratings
from django.contrib.auth.models import User


class ProfileTestCase(TestCase):
    def setUp(self):
        '''
        Profile set up method
        '''
        self.user = User.objects.create_user(username='test', password='079053')
        self.profile = Profile(id=1,avatar='path/to/photo',user = self.user,bio='test bio')

    def test_instance(self):
        '''
        Tests for profile instance
        '''
        self.assertTrue(isinstance(self.profile,Profile))

    # Error
    def test_save_profile(self):
        '''
        Testing saving method
        '''
        self.profile.save_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) > 0)

    def test_delete_profile(self):
        '''
        Testing profile deleting
        '''
        self.profile.delete_profile()
        self.assertTrue(len(Profile.objects.all()) == 0)


class ProjectTestCase(TestCase):
    def setUp(self):
        '''
        Project set up
        '''
        self.user = User.objects.create_user(username='test', password='079053')
        self.profile = Profile(id=1, avatar='path/to/photo',user = self.user,bio='test bio')
        self.project = Project(id=1,title='test title',image='path/to/image',description='test description',owner=self.profile,url='https://something.com')

    def test_project_instance(self):
        '''
        Tests for project instance
        '''
        self.assertTrue(isinstance(self.project,Project))

    def test_delete_project(self):
        '''
        Testing project deleting
        '''
        self.project.delete_project()
        self.assertTrue(len(Project.objects.all()) == 0)


class RatingsTestCase(TestCase):
    def setup(self):
        '''
        Ratings set up
        '''
        self.user = User.objects.create_user(username='test', password='079053')
        self.profile = Profile(id=1,avatar='path/to/photo',user = self.user,bio='test bio')
        self.project = Project(id=1,title='test title',image='path/to/image',description='test description',owner=self.profile,url='https://something.com')
        self.rating= Ratings(id=1,project=self.project,user=self.user,review='test review',design=10,usability=10,content=10)

    # Error
    def test_rating_instance(self):
        '''
        Tests for ratings instance
        '''
        self.assertTrue(isinstance(self.rating,Ratings))

