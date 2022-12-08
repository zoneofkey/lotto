from django.db import models

# Create your models here.
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Post(models.Model):
    postname = models.CharField(max_length=200)
    contents = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now=True)
    contents2 = models.TextField(default="")
    mainphoto = models.ImageField(blank=True, null=True)
    wishnote = models.CharField(max_length=200, default="")
    pub_date_k = models.CharField(max_length=200, default="")
    color_k = models.CharField(max_length=200, default="lucky.png")

    def __str__(self):
        return self.postname

# 삭제시 미디어 파일도 같이 삭제 오버 라이딩 함
@receiver(post_delete, sender=Post)
def deleteAttFile(sender, **kwargs):
    attFile = kwargs.get("instance")
    attFile.mainphoto.delete(save=False)

