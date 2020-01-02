from django.db import models
from accounts.models import Blogger
# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length = 200)
    pub_date = models.DateTimeField()
    # Count number of objects with votes
    image = models.ImageField(upload_to = 'blogs/images')
    body = models.TextField()
    blogger = models.ForeignKey(Blogger, on_delete=models.CASCADE)
    banner = models.BooleanField(default = False)

    def __str__(self):
        return self.title

    def summary(self):
        sentenceList = self.body.split()
        if len(sentenceList) > 20:
            return ' '.join(sentenceList[:20]) + ' ...'
        else:
            return self.body
    
    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')

    def getVotes(self):
        return Vote.objects.filter(blog = self).count()
    
    def getUsers(self):
        return [vote.blogger.user.get_username() for vote in Vote.objects.filter(blog = self)]
    
    votes_total = property(getVotes)

class Vote(models.Model):
    vote_date = models.DateTimeField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    blogger = models.ForeignKey(Blogger, on_delete=models.CASCADE)