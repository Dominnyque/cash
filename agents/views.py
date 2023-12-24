import random
from django.shortcuts import render, reverse
from django.views import generic
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin

# Create your views here.
class AgentListView(OrganisorAndLoginRequiredMixin, LoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)

class AgentCreateView(OrganisorAndLoginRequiredMixin, LoginRequiredMixin, generic.CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agents")
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"{random.randint(0,1000000)}")
        user.save()

        Agent.objects.create(
            user = user,
            organisation = self.request.user.userprofile
        )

        send_mail(
            subject = "You are invited to be an agent",
            message = " You were added as an agent to Cas CRM. Please login to view your tas",
            from_email = "admin@test.net",
            recipient_list = [user.email]
        )
        
        return super(AgentCreateView, self).form_valid(form)

class AgentDetailsView(OrganisorAndLoginRequiredMixin, LoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_details.html"
    queryset = Agent.objects.all()
    context_object_name = "agent"

class AgentUpdateView(OrganisorAndLoginRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    template_name = 'agents/agent_update.html'
    form_class = AgentModelForm

    queryset = Agent.objects.all()
    context_object_name = "agent"

    def get_success_url(self):
        return reverse("agents:agents")
    
class AgentDeleteView(OrganisorAndLoginRequiredMixin, LoginRequiredMixin, generic.DeleteView):
    template_name="agents/agent_delete.html"
    queryset = Agent.objects.all()

    def get_success_url(self):
        return reverse('agents:agents')