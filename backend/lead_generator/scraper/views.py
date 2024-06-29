import re
import asyncio
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import LeadRequestSerializer
from .models import ScrapingTask, Lead
from django.http import JsonResponse, HttpResponse
import csv
from django.conf import settings

class LeadGeneratorView(APIView):
    permission_classes = [IsAuthenticated]
    
    def extract_user_id(self, url):
        pattern = r"user\/([a-zA-Z0-9]+)[\/\?]?"
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        else:
            return url

    def post(self, request):
        serializer = LeadRequestSerializer(data=request.data)
        if serializer.is_valid():
            raw_users = serializer.validated_data.get("username")
            users = [self.extract_user_id(user_url) for user_url in raw_users.split("&")]

            tags = serializer.validated_data.get("tags").split("&")
            tags = [tag.strip() for tag in tags if tag.strip()]

            last_updated = serializer.validated_data.get("date")
            min_likes = serializer.validated_data.get("min_likes")
            max_likes = serializer.validated_data.get("max_likes")
            max_leads = serializer.validated_data.get("limit")
            all_tags = serializer.validated_data.get("searchAllTags")
            
    
            task = ScrapingTask.objects.create(
                owner=request.user,
                config = {
                    "users": users,
                    "tags": tags,
                    "all_tags": all_tags,
                    "last_updated": last_updated,
                    "min_likes": min_likes,
                    "max_likes": max_likes,
                    "run_limit": max_leads,
                }
            )
            
            return Response({"task_id": task.id}, status=status.HTTP_201_CREATED)
            
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScrapingTaskListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, type):
        tasks = None

        # Filter tasks based on the 'type' parameter
        if type == 'queued':
            tasks = ScrapingTask.objects.filter(owner=request.user, status=ScrapingTask.StatusChoices.QUEUED)
        elif type == 'failed':
            tasks = ScrapingTask.objects.filter(owner=request.user, status=ScrapingTask.StatusChoices.FAILED)
        elif type == 'completed':
            tasks = ScrapingTask.objects.filter(owner=request.user, status=ScrapingTask.StatusChoices.COMPLETED)
        else:
            tasks = ScrapingTask.objects.filter(owner=request.user)
        
        return JsonResponse(
            {
                "data": [
                    {
                        "id": task.id,
                        "status": task.StatusChoices(task.status).label,
                        "created_at": task.created_at,
                        "updated_at": task.updated_at,
                        "leads_count": task.leads_count,
                    }
                    for task in tasks
                ]
            }
        )

class ScrapingTaskDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        task = ScrapingTask.objects.get(owner=request.user, id=pk)
        leads = Lead.objects.filter(owner=request.user, parent_task_id=task)
        return JsonResponse(
            {
                "task": {
                    "id": task.id,
                    "status": task.status,
                    "created_at": task.created_at,
                    "updated_at": task.updated_at,
                    "leads_count": task.leads_count,
                    "config": task.config,
                },
                "leads": [
                    {
                        "id": lead.id,
                        "spotify_username": lead.spotify_username,
                        "email": lead.email,
                        "phone": lead.phone,
                        "related_playlists": lead.related_playlists,
                        "free_links": lead.free_links,
                        "paid_links": lead.paid_links,
                        "others_links": lead.others_links,
                    }
                    for lead in leads
                ]
            }
        )

class LeadsByTaskView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        task = ScrapingTask.objects.get(owner=request.user, id=pk)
        leads = Lead.objects.filter(owner=request.user, parent_task_id=task)
        return JsonResponse(
            {
                "data": [
                    {
                        "id": lead.id,
                        "spotify_username": lead.spotify_username,
                        "email": lead.email,
                        "phone": lead.phone,
                        "related_playlists": lead.related_playlists,
                        "free_links": lead.free_links,
                        "paid_links": lead.paid_links,
                        "others_links": lead.others_links,
                    }
                    for lead in leads
                ]
            }
        )

class ExportLeadsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        task = ScrapingTask.objects.get(owner=request.user, id=pk)
        if not task:
            return Response({"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        
        leads = Lead.objects.filter(owner=request.user, parent_task_id=task)

        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="leads.csv"'

        writer = csv.writer(response)
        # Write the header
        writer.writerow(['Lead ID', 'Playlist Owner', 'Emails', 'Phone Numbers', 'Related Playlists', 'Free Links', 'Paid Links', 'Others Links', 'Created At'])

        # Write data rows
        for lead in leads:
            writer.writerow([lead.id, lead.spotify_username, lead.email, lead.phone, lead.related_playlists, lead.free_links, lead.paid_links, lead.others_links, lead.created_at])

        return response