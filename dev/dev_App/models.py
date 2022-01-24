from django.db import IntegrityError, models
from django.utils import timezone
from django.utils.timezone import now
from datetime import timedelta





class Post(models.Model):
    title = models.CharField(max_length=155)
    url = models.URLField()
    creation_date = models.DateTimeField(default=timezone.now)
    amount_of_upvotes = models.IntegerField(default=1)
    author_name = models.CharField(max_length=155)

    class Meta:
        ordering = ['-creation_date']

    def __str__(self):
        return '%s' % self.title


class Vote(models.Model):
    post = models.ForeignKey(Post, related_name='votes', on_delete=models.CASCADE)

    def save(self, commit=True, *args, **kwargs):

        if commit:
            try:
                self.post.amount_of_upvotes += 1
                self.post.save()
                super(Vote, self).save(*args, **kwargs)

            except IntegrityError:
                self.post.amount_of_upvotes -= 1
                self.post.save()
                raise IntegrityError

        else:
            raise IntegrityError


    @property
    def deletes(self):
        time = self.created_at + timedelta(days=1)
        query = Vote.objects.get(pk=self.pk)
        
        while True:
           if time > now():
              query.delete()
              break    


    def __str__(self):
        return self.post.title


    

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author_name = models.CharField(max_length=155)
    content = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)



