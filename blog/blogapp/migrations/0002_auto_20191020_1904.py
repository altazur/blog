# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-10-20 19:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment_text',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='post_text',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='user_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='comment_id',
        ),
        migrations.RemoveField(
            model_name='post',
            name='post_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_id',
        ),
    ]
