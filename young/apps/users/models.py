from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    mobile = models.CharField(max_length=11, verbose_name='用户手机号', unique=True)
    nickname = models.CharField(max_length=15, unique=True, verbose_name='昵称', null=True)
    avatar_url = models.ImageField(verbose_name='用户头像', null=True)
    collect_articles = models.ForeignKey('Article', verbose_name='收藏文臧', null=True)
    # read_articles = models.ManyToManyField('Article', related_name='read_users', verbose_name='阅读文章', null=True)
    like_articles = models.ManyToManyField('Article', related_name='like_users', verbose_name='点赞文章', null=True)
    like_comments = models.ManyToManyField('Comment', related_name='like_users', verbose_name='点赞评论', null=True)

    class Meta:
        db_table = 'tb_user'
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Article(models.Model):
    create_time = models.DateField(auto_now=True, verbose_name='创建时间')
    update_time = models.DateField(default=timezone.now, verbose_name='更新时间')
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='articles', verbose_name='作者', null=True)
    headline = models.CharField(max_length=100, verbose_name='标题', null=True)
    content = models.TextField(verbose_name='文章内容', null=True)
    read_count = models.IntegerField(default=0, verbose_name='阅读量')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    trans_count = models.IntegerField(default=0, verbose_name='转发数')
    focus_url = models.ImageField(null=True, verbose_name='缩略图')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        db_table = 'tb_article'
        verbose_name = 'article'
        verbose_name_plural = 'articles'


class Comment(models.Model):
    create_time = models.DateField(auto_now=True, verbose_name='创建时间')
    update_time = models.DateField(default=timezone.now, verbose_name='更新时间')
    content = models.CharField(max_length=500, verbose_name='评论内容', null=True)
    article = models.ForeignKey('Article', on_delete=models.CASCADE, verbose_name='所属文章', related_name='comments')
    author = models.ForeignKey('User', verbose_name='评论者', related_name='comments', null=True)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, verbose_name='父评论',
                               related_name='son_comments', null=True)
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        db_table = 'tb_comment'
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
