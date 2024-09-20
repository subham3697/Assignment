from django.db import models
from accounts.models import User
from django.urls import reverse


class Blog(models.Model):
    title = models.CharField(max_length=255,blank=True,null=True)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)

    class Meta:
        managed = True,
        db_table = "tbl_blog"

    @property
    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('blog:blog_detail', args=[self.id])

class BlogComment(models.Model):
    comment = models.CharField(max_length=255,blank=True,null=True)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    created_by  = models.ForeignKey(User,on_delete=models.CASCADE)


    class Meta:
        managed = True,
        db_table = "tbl_blog_comments"