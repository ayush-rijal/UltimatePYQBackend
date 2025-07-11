# Generated by Django 5.1.4 on 2025-03-25 10:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizAPI', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='questions_file',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='QuizResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz_id', models.CharField(max_length=36)),
                ('choices', models.JSONField()),
                ('score', models.IntegerField()),
                ('total_questions', models.IntegerField()),
                ('time_taken', models.CharField(blank=True, max_length=10, null=True)),
                ('completed_at', models.DateTimeField(auto_now_add=True)),
                ('questions_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizAPI.questions_file')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Quiz Result',
                'verbose_name_plural': 'Quiz Results',
            },
        ),
    ]
