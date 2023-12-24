from django.urls import path
from .views import AgentListView, AgentCreateView, AgentDetailsView, AgentUpdateView, AgentDeleteView

app_name ='agents'

urlpatterns = [
    path('', AgentListView.as_view(), name = 'agents'),
    path('create/', AgentCreateView.as_view(), name = 'add-agent'),
    path('<int:pk>/', AgentDetailsView.as_view(), name = 'agent-details'),
    path('<int:pk>/update', AgentUpdateView.as_view(), name = 'update-agent'),
    path('<int:pk>/delete', AgentDeleteView.as_view(), name = 'delete-agent'),
]
 