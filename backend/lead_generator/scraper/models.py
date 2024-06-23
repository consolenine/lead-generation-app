from django.contrib.postgres.fields import ArrayField
from django.db import models

class Lead(models.Model):
    spotify_username = models.JSONField()
    email = ArrayField(
        models.CharField(max_length=255, blank=True),
        default=list
    )
    phone = ArrayField(
        models.CharField(max_length=255, blank=True),
        default=list
    )
    related_playlists = ArrayField(
        models.CharField(max_length=255, blank=True),
        default=list
    )
    free_links = ArrayField(
        models.CharField(max_length=255, blank=True),
        default=list
    )
    paid_links = ArrayField(
        models.CharField(max_length=255, blank=True),
        default=list
    )
    others_links = ArrayField(
        models.CharField(max_length=255, blank=True),
        default=list
    )
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='leads', on_delete=models.CASCADE)
    parent_task = models.ForeignKey('scraper.ScrapingTask', related_name='leads', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'leads'

class ScrapingTask(models.Model):
    class StatusChoices(models.TextChoices):
        QUEUED = '1', 'Queued'
        IN_PROGRESS = '2', 'In Progress'
        COMPLETED = '3', 'Completed'
        FAILED = '4', 'Failed'

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.QUEUED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    config = models.JSONField(default=dict)
    owner = models.ForeignKey('auth.User', related_name='scraping_tasks', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'scraping_tasks'
    
    @property
    def leads_count(self):
        return Lead.objects.filter(parent_task=self).count()
    