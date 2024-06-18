from rest_framework import serializers
from .models import ScrapingTask

class LeadRequestSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    tags = serializers.CharField(required=False, default="", allow_blank=True)
    date = serializers.CharField(required=False, default="2015-01-01")
    min_likes = serializers.IntegerField(required=False, default=0)
    max_likes = serializers.IntegerField(required=False, default=1000000)
    limit = serializers.IntegerField(required=False, default=20)
    searchAllTags = serializers.BooleanField(required=False, default=False)

class ScrapingTaskListRequestSerializer(serializers.Serializer):
    class Meta:
        model = ScrapingTask
        fields = ['id', 'status', 'created_at', 'updated_at', 'leads_count']

class ScrapingTaskDetailRequestSerializer(serializers.Serializer):
    class Meta:
        model = ScrapingTask
        fields = '__all__'
