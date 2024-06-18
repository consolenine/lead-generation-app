import re
import asyncio
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import LeadRequestSerializer
from .models import ScrapingTask, Lead
from .leadgen import leadGenerator
from django.http import JsonResponse
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
                status="running",
                owner=request.user,
                config = {
                    "users": users,
                    "tags": tags,
                    "all_tags": all_tags,
                    "last_updated": last_updated,
                    "min_likes": min_likes,
                    "max_likes": max_likes,
                    "max_leads": max_leads,
                }
            )
            
            async def main():
                return await leadGenerator(
                    users,
                    filters={
                        "min_likes": int(min_likes),
                        "max_likes": int(max_likes),
                        "last_updated": last_updated,
                        "tags": tags,
                        "all_tags": all_tags,
                        "search_title": True,
                        "max_leads": int(max_leads),
                    },
                )

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(self.run_with_disconnect_check(main))
                if result:
                    task.status = "Completed"
                    task.save()
            except asyncio.CancelledError:
                task.status = "Failed"
                task.save()
                return Response({"detail": "Client disconnected"}, status=status.HTTP_410_GONE)
            except Exception as e:
                task.status = "Failed"
                task.save()
                print(e)
                return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            data = []
            for item in result:
                data.append(
                    {
                        "user": item["user"],
                        "links": {
                            "free": list(item["links"]["free"]),
                            "paid": list(item["links"]["paid"]),
                            "others": list(item["links"]["others"]),
                        },
                        "email": list(item["email"]),
                        "phone": list(item["phone"]),
                        "related_playlists": list(item["related_playlists"]),
                    }
                )
            csv_file_path = settings.BASE_DIR / "static/files/spotify_leads.csv"
            with open(csv_file_path, "w") as file:
                writer = csv.writer(file)
                writer.writerow(["User ID", "Email", "Phone", "Free Links", "Paid Links", "Others", "Related Playlists"])
                for item in data:
                    writer.writerow([
                        item["user"]["id"],
                        ",".join(item["email"]),
                        ",".join(item["phone"]),
                        ",".join(item["links"]["free"]),
                        ",".join(item["links"]["paid"]),
                        ",".join(item["links"]["others"]),
                        ",".join(item["related_playlists"][0]),
                    ])
            
            Lead.objects.bulk_create(
                [
                    Lead(
                        spotify_username=item["user"] or "Placeholder",
                        email=item["email"],
                        phone=item["phone"],
                        related_playlists=item["related_playlists"],
                        free_links=item["links"]["free"],
                        paid_links=item["links"]["paid"],
                        others_links=item["links"]["others"],
                        owner=request.user,
                        parent_task=task,
                    )
                    for item in data
                ]
            )

            return JsonResponse(data, safe=False)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    async def run_with_disconnect_check(self, coro, timeout=60):
        task = asyncio.create_task(coro())
        while not task.done():
            await asyncio.sleep(1)
            timeout = timeout - 1
            if timeout <= 0:
                task.cancel()
                break
        return await task

class ScrapingTaskListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        tasks = ScrapingTask.objects.filter(owner=request.user)
        return JsonResponse(
            {
                "data": [
                    {
                        "id": task.id,
                        "status": task.status,
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