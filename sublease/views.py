from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView, View
from django.urls import reverse_lazy
from .models import Sublease
from .forms import SubleaseForm, SubleasePhotoForm


class SubleaseCreateView(LoginRequiredMixin, CreateView):
    model = Sublease
    form_class = SubleaseForm
    template_name = "sublease/sublease_create.html"
    success_url = reverse_lazy("sublease-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SubleaseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Sublease
    form_class = SubleaseForm
    template_name = "sublease/sublease_edit.html"

    def test_func(self):
        sublease = self.get_object()
        return sublease.user == self.request.user


class SubleaseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Sublease
    template_name = "sublease/sublease_confirm_delete.html"
    success_url = reverse_lazy("sublease-list")

    def test_func(self):
        sublease = self.get_object()
        return sublease.user == self.request.user


class SubleaseDetailView(DetailView):
    model = Sublease
    template_name = "sublease/sublease_detail.html"


class SubleaseListView(ListView):
    model = Sublease
    template_name = "sublease/sublease_list.html"
    ordering = ['-id']


class SubleasePhotoUploadView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "sublease/sublease_add_photo.html"

    def test_func(self):
        sublease = get_object_or_404(Sublease, pk=self.kwargs["pk"])
        return sublease.user == self.request.user

    def get(self, request, pk):
        form = SubleasePhotoForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        sublease = get_object_or_404(Sublease, pk=pk)
        form = SubleasePhotoForm(request.POST, request.FILES)

        if form.is_valid():
            photo = form.save(commit=False)
            photo.sublease = sublease
            photo.save()
            return redirect("sublease-detail", pk=pk)

        return render(request, self.template_name, {"form": form})