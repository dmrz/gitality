from django.core.urlresolvers import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    ListView,
    DeleteView
)

from core.mixins import (
    ExcludeFormMixin,
    LoginRequiredMixin,
    UserFormMixin,
    UserOwnerMixin
)

from .forms import ProjectForm
from .models import Project


class ProjectListView(ListView):

    model = Project

project_list = ProjectListView.as_view()


class ProjectDetailView(DetailView):

    model = Project

project_detail = ProjectDetailView.as_view()


class ProjectCreateView(LoginRequiredMixin, UserFormMixin, CreateView):

    form_class = ProjectForm
    model = Project

project_create = ProjectCreateView.as_view()


class ProjectUpdateView(LoginRequiredMixin, UserFormMixin, UpdateView):

    form_class = ProjectForm
    model = Project

project_update = ProjectUpdateView.as_view()
