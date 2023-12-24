from django.urls import path
from.views import(
    LeadListView, 
    LeadDetailView, 
    LeadCreateView, 
    LeadUpdateView, 
    LeadDeleteView, 
    AssignAgentView, 
    CategoriesListView, 
    CategoryDetailView, 
    LeadCategoryUpdateView,
    )
app_name = 'leads'

urlpatterns = [
    path('', LeadListView.as_view(), name = 'lead-list'),
    #path ('create/', lead_create, name = 'create-lead'),
    path ('create/', LeadCreateView.as_view(), name = 'create-lead'),
    path ('categories/', CategoriesListView.as_view(), name = 'categories'),
    path ('<int:pk>/categories/', CategoryDetailView.as_view(), name = 'category-details'),
    #path('<pk>/', lead_details, name = 'lead-details'),
    path ('<int:pk>/assign/', AssignAgentView.as_view(), name = 'assign-agent'),
    path('<int:pk>/', LeadDetailView.as_view(), name = 'lead-details'),
    #path('<pk>/update', lead_update, name = 'update-lead'),
    path('<int:pk>/update', LeadUpdateView.as_view(), name = 'update-lead'),
    path('<int:pk>/lead-category-update', LeadCategoryUpdateView.as_view(), name = 'lead-category-update'),
    #path('<pk>/delete', lead_delete, name = 'delete-lead'),
    path('<int:pk>/delete', LeadDeleteView.as_view(), name = 'delete-lead'),
]

#Next, include the path in project urls.py using include function
