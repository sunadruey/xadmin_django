# Generated by Django 2.2 on 2022-03-03 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_course_theacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='teacher_tell',
            field=models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='教师告知'),
        ),
        migrations.AddField(
            model_name='course',
            name='youneed_know',
            field=models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='课程须知'),
        ),
    ]
