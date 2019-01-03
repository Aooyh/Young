# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-01-03 06:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190103_0633'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateField(auto_now=True, verbose_name='创建时间')),
                ('update_time', models.DateField(default=datetime.datetime(2019, 1, 3, 6, 52, 26, 850523, tzinfo=utc), verbose_name='更新时间')),
            ],
            options={
                'verbose_name': 'article',
                'verbose_name_plural': 'articles',
                'db_table': 'tb_article',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='avatar_url',
            field=models.ImageField(null=True, upload_to='', verbose_name='用户头像'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(max_length=15, null=True, unique=True, verbose_name='昵称'),
        ),
        migrations.AddField(
            model_name='user',
            name='articles',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author', to='users.Article', verbose_name='帖子'),
        ),
    ]