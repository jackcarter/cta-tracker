from django.db import models
from django.utils import timezone


class Stop(models.Model):
    id = models.IntegerField(unique=True)

    def __unicode__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    pub_date = models.DateTimeField('date published', default=timezone.now())
    slug = models.SlugField(max_length=100, unique=True)
    category = models.ManyToManyField(Category)

    def save(self, *args, **kwargs):
        if not self.id:
            #only create a slug the first time it's saved, so as not to break links
            unique_slugify(self, self.title)
        super(Post, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post)
    content = models.TextField(max_length=500)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        data = self.content
        max_length = 20
        ellipsis = '...'
        return (data[:max_length] + ellipsis) if len(data) > (max_length + len(ellipsis)) else data


class PostCategorization(models.Model):
    post = models.ForeignKey(Post)
    category = models.ForeignKey(Category)