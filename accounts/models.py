from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timeFirstModification = models.DateTimeField(auto_now = True)
    displayName = models.CharField(max_length = 30)
    description = models.TextField()
    profilepic = models.ImageField(upload_to = 'users/profilepic')

    def summary(self):
        sentenceList = self.description.split()
        if len(sentenceList) > 20:
            return ' '.join(sentenceList[:20]) + ' ...'
        else:
            return self.description

    def __str__(self):
        return self.displayName