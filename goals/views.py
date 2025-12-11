from django.shortcuts import render, redirect, get_object_or_404
from . import models
from .models import FinancialTracker
from .forms import GoalForm, UpdateSavingsForm
from django.contrib.auth.decorators import login_required
from django.db.models import F

@login_required
def goal_list(request):
    filter_option = request.GET.get("filter", "all")

    if filter_option == "completed":
        goals = FinancialTracker.objects.filter(user=request.user, current_amount__gte=F('target_amount'))
    elif filter_option == "in progress":
        goals = FinancialTracker.objects.filter(user=request.user, current_amount__lt=F('target_amount'))
    else:
        goals = FinancialTracker.objects.filter(user=request.user)

    return render(request, "goals/goal_list.html", {"goals": goals})

@login_required
def create_goal(request):
    if request.method == "POST":
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect("goal-list")
    else:
        form = GoalForm()
    return render(request, "goals/create_goal.html", {"form": form})

@login_required
def update_savings(request, pk):
    goal = get_object_or_404(FinancialTracker, pk=pk, user=request.user)
    if request.method == "POST":
        form = UpdateSavingsForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect("goal-list")
    else:
        form = UpdateSavingsForm(instance=goal)
    return render(request, "goals/update_savings.html", {"form": form, "goal": goal})