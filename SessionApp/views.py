from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Session

# Create your views here.

class SessionList(ListView):
    model = Session
    context_object_name = "sessions"
    ordering = ["start_time"]
    template_name = "session/session_list.html"
class SessionDetails(DetailView):
    model = Session
    template_name = "session/session_detail.html"
    context_object_name = "session"
class SessionCreate(CreateView):
    model = Session
    template_name = "session/session_form.html"
    fields = "__all__"
    success_url = reverse_lazy("session_list")
class SessionUpdate(UpdateView):
    model = Session
    template_name = "session/session_form.html"
    fields = "__all__"
    success_url = reverse_lazy("session_list")
class SessionDelete(DeleteView):
    model = Session
    success_url = reverse_lazy("session_list")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)