from django.urls import path

from scraper.views import LeadGeneratorView, ScrapingTaskListView, ScrapingTaskDetailsView, LeadsByTaskView, ExportLeadsView

app_name = 'scraper'

urlpatterns = [
    path('generate/', LeadGeneratorView.as_view(), name="generate"),
    path('scraping-tasks/<str:type>', ScrapingTaskListView.as_view(), name='scraping-tasks'),
    path('tasks/<int:pk>/', ScrapingTaskDetailsView.as_view(), name='scraping-tasks'),
    path('tasks/<int:pk>/leads', LeadsByTaskView.as_view(), name='task-leads'),
    path('tasks/<int:pk>/leads/export', ExportLeadsView.as_view(), name='export-leads'),
]