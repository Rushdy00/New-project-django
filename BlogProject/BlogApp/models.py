from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    # variable = models.relation(tabel to create relation with,)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)
    STATUS =(
        ('Single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced',)
    )
    marital_status = models.CharField(choices=STATUS, max_length=50, default='Single')
    is_employed = models.BooleanField(default=False)
    profile_picture = models.ImageField(blank=True)

    def __str__(self):
        return self.user.username.title()

    class Meta:
        verbose_name_plural = 'Users Profiles'
        verbose_name = 'Profile'
class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    hashtags = models.ManyToManyField('Hashtag', related_name='ht_posts')

    def __str__(self):
        return self.title

class Hashtag(models.Model):
    name = models.CharField(max_length=255, unique=True)





