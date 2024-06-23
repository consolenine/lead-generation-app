# Generated by Django 5.0.4 on 2024-06-23 04:07

import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapingTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('1', 'Queued'), ('2', 'In Progress'), ('3', 'Completed'), ('4', 'Failed')], default='1', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('config', models.JSONField(default=dict)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scraping_tasks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'scraping_tasks',
            },
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spotify_username', models.JSONField()),
                ('email', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), default=list, size=None)),
                ('phone', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), default=list, size=None)),
                ('related_playlists', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), default=list, size=None)),
                ('free_links', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), default=list, size=None)),
                ('paid_links', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), default=list, size=None)),
                ('others_links', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), default=list, size=None)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leads', to=settings.AUTH_USER_MODEL)),
                ('parent_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leads', to='scraper.scrapingtask')),
            ],
            options={
                'db_table': 'leads',
            },
        ),
    ]
