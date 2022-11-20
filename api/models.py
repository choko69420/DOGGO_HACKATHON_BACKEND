from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    # choice field
    ANIMAL_CHOICES = [
        ('dog', 'dog'),
        ('cat', 'cat'),
        ('bird', 'bird'),
        ('fish', 'fish'),
        ('reptile', 'reptile'),
        ('other', 'other')
    ]
    animal = models.CharField(
        max_length=50, choices=ANIMAL_CHOICES, default='dog')
    score = models.IntegerField(default=0)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    friends = models.ManyToManyField("self", blank=True)
    friend_requests = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return f"{self.username} {self.email} {self.animal} {self.score}"


class Report(models.Model):
    CATEGORY_CHOICES = [
        ('sexism', 'sexism'),
        ('racism', 'racism'),
        ('homophobia', 'homophobia'),
        ('transphobia', 'transphobia'),
        ('ableism', 'ableism'),
        ('nsfw', 'nsfw'),
        ('other', 'other'),
    ]
    VALID_CHOICES = [
        ('valid', 'valid'),
        ('invalid', 'invalid'),
        ('pending', 'pending'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    reason = models.CharField(max_length=500, default="No reason given")
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reports')
    website_url = models.URLField(max_length=200)
    valid = models.CharField(
        max_length=50, default="pending", choices=VALID_CHOICES)

    def __str__(self):
        return f"{self.author} - {self.category} - {self.reason[:20]}..."
