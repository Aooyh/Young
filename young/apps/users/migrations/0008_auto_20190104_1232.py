# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-01-04 12:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20190104_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='son_comments', to='users.Comment', verbose_name='父评论'),
        ),
    ]
