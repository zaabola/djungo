from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Conference , Submission
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here.
def all_conferences(req):
    conferences=Conference.objects.all()
    return render(req, 'conference/liste.html', {"liste":conferences})

class ConferenceList(ListView):
    model = Conference
    context_object_name ="liste"
    ordering =["start_date"]
    template_name ="conference/liste.html"

class ConferenceDetails(DetailView):
    model =Conference
    template_name ="conference/detail.html"
    context_object_name ="conference"

class ConferenceCreate(CreateView):
    model=Conference
    template_name ="conference/conference_form.html"
    fields ="__all__"
    success_url = reverse_lazy("conference_liste")

class ConferenceUpdate(UpdateView):
    model=Conference
    template_name ="conference/conference_form.html"
    fields ="__all__"
    success_url = reverse_lazy("conference_liste")

class ConferenceDelete(DeleteView):
    model = Conference
    success_url = reverse_lazy("conference_liste")
    
    def get(self, request, *args, **kwargs):

        return self.delete(request, *args, **kwargs)
    
# Add to your existing ConferenceApp/views.py

class SubmissionList(ListView):
    model = Submission
    context_object_name = "submissions"
    ordering = ["submission_date"]
    template_name = "conference/submission_list.html"

class SubmissionDetails(DetailView):
    model = Submission
    template_name = "conference/submission_detail.html"
    context_object_name = "submission"

class SubmissionCreate(CreateView):
    model = Submission
    template_name = "conference/submission_form.html"
    fields = "__all__"
    success_url = reverse_lazy("submission_list")

class SubmissionUpdate(UpdateView):
    model = Submission
    template_name = "conference/submission_form.html"
    fields = "__all__"
    success_url = reverse_lazy("submission_list")

class SubmissionDelete(DeleteView):
    model = Submission
    success_url = reverse_lazy("submission_list")
    
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)