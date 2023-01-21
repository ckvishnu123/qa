from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Questions(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to="images", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)

    # using property decorator we can call a method of class as an attribute without brackets
    @property
    def question_answers(self):
        # - for descending order
        return self.answers_set.all().annotate(u_count=models.Count('up_vote')).order_by('-u_count')

    def __str__(self):
        return self.title


class Answers(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 2 times relation to same model then related_name should be added
    up_vote = models.ManyToManyField(User, related_name="upvote")
    created_date = models.DateField(auto_now_add=True)

    @property
    def upvote_count(self):
        return self.up_vote.all().count()

    def __str__(self):
        return self.answer