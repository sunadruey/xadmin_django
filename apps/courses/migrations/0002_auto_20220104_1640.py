# Generated by Django 2.2 on 2022-01-04 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='degree',
            field=models.CharField(choices=[('cj', '初级'), ('zj', '中级'), ('gj', '高级')], max_length=2, verbose_name='难度'),
        ),
        migrations.AlterField(
            model_name='course',
            name='detail',
            field=models.TextField(verbose_name='课程详情'),
        ),
    ]
