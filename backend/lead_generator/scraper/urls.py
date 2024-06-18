from django.urls import path

from scraper.views import LeadGeneratorView, ScrapingTaskListView, ScrapingTaskDetailsView, LeadsByTaskView

app_name = 'scraper'

urlpatterns = [
    path('generate/', LeadGeneratorView.as_view(), name="generate"),
    path('scraping-tasks/', ScrapingTaskListView.as_view(), name='scraping-tasks'),
    path('tasks/<int:pk>/', ScrapingTaskDetailsView.as_view(), name='scraping-tasks'),
    path('tasks/<int:pk>/leads', LeadsByTaskView.as_view(), name='task-leads'),
]