# Generated by Django 2.2 on 2022-03-02 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='tag',
            field=models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='课程标签'),
        ),
    ]