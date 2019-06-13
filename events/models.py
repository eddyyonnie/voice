from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import numpy as np

class Profile(models.Model):
    avatar = models.ImageField(default='empty.png',blank=True ,upload_to='avatar/')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f'{self.user.username}'


    @classmethod
    def get_profiles(cls):
        return cls.objects.all()


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Project(models.Model):
    title = models.CharField(max_length=30)
    image = models.ImageField(upload_to='projects/')
    description = models.TextField(max_length=500)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    url = models.CharField(max_length=100)
     
    def __str__(self):
        return self.title

    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()

    def update_description(self,desc):
        self.description = desc
        self.save()

    @classmethod
    def search_projects(cls, title):
        projects = Project.objects.filter(title__icontains = title)
        return projects

    @classmethod
    def get_project_id(cls, id):
        project = Project.objects.get(pk=id)
        return project

    @classmethod
    def get_projects(cls):
        return cls.objects.all()

    @classmethod
    def filter_by_user(cls,owner):
        the_user = User.objects(username=owner)
        return cls.objects.filter(owner__id = the_user.id)

    def average_design(self):
        design_ratings = list(map(lambda x: x.design, self.ratings.all()))
        return np.mean(design_ratings)

    def average_usability(self):
        usability_ratings = list(map(lambda x: x.usability, self.ratings.all()))
        return np.mean(usability_ratings)

    def average_content(self):
        content_ratings = list(map(lambda x: x.content, self.ratings.all()))
        return np.mean(content_ratings)

    
class Ratings(models.Model):
    RATING = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),

    )
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='ratings')
    review = models.TextField()
    design = models.IntegerField(choices=RATING, default=0)
    usability= models.IntegerField(choices=RATING, default=0)
    content = models.IntegerField(choices=RATING, default=0)


    @classmethod
    def get_rating_by_projects(cls, id):
        ratings = Ratings.objects.filter(project__pk = id)
        return ratings

    @classmethod
    def get_reviews(cls,review):
        review = Ratings.objects.get(review=review)