from typing import Any
from django.core.mail import send_mail
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from agents.mixins import OrganisorAndLoginRequiredMixin
from .models import Lead, Agent, Category
from .forms import LeadForm, LeadModelForm, CustomUserForm, AssignAgentForm, LeadCategoryUpdateForm

class SignUpView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserForm

    def get_success_url(self):
        return reverse('login')

class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'
# Create your views here then call them in their respective app's urls.py.
# def home_page(request):
#     return render(request, "landing.html")

class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name="leads/leads_list.html"
    context_object_name="leads"

    def get_queryset(self):
        user = self.request.user

        #Initial queryset for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, 
                agent__isnull=False
                )
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # Filter Leads for current agent
            queryset =queryset.filter(agent__user=user)
        return queryset
    
    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, 
                agent__isnull=True
                )
            context.update({
                "unassigned_leads":queryset
                })
        return context



class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name="leads/lead_details.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset


# def lead_details(request, pk):
#     lead = Lead.objects.get(id=pk)
#     context={ 
#         "lead":lead
#         }
#     return render(request, "leads/lead_details.html", context)


class LeadCreateView(OrganisorAndLoginRequiredMixin, LoginRequiredMixin, generic.CreateView):
    template_name="leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse('leads:lead-list')
    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        send_mail(
            subject="A lead has been created",
            message= "Please go to the site to see the new lead",
            from_email="test@example.com",
            recipient_list=["test2@example.com"]
        )
        return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(OrganisorAndLoginRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    template_name="leads/lead_update.html"
    queryset = Lead.objects.all()
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user

        #Initial queryset for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # Filter Leads for current agent
            queryset =queryset.filter(agent__user=user)
        return queryset
    def get_success_url(self):
        return reverse("leads:lead-list")
    

class LeadDeleteView(OrganisorAndLoginRequiredMixin, LoginRequiredMixin, generic.DeleteView):
    template_name="leads/lead_delete.html"
    queryset = Lead.objects.all()

    def get_queryset(self):
        user = self.request.user

        #Initial queryset for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # Filter Leads for current agent
            queryset =queryset.filter(agent__user=user)
        return queryset


class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):
    template_name ="leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        agent = (form.cleaned_data["agent"])
        lead = Lead.objects.get(id=self.kwargs['pk'])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)
    
class CategoriesListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(CategoriesListView, self).get_context_data(**kwargs)
        
        #Filter unassigned liead to show also their categories in respective organization
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile
                )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation
                )
        context.update({
            "unassigned_lead_count":queryset.filter(category__isnull=True).count()
        })
        return context
    
    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset

class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_details.html"
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset
    
class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView): 
    template_name="leads/lead_category_update.html"
    queryset = Lead.objects.all()
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset
    
    def get_success_url(self):
        return reverse("leads:lead-details", kwargs={"pk":self.get_object().id})
    
