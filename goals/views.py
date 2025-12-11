from django.shortcuts import render, redirect, get_object_or_404
from . import models
from .models import FinancialTracker
from .forms import GoalForm, UpdateSavingsForm
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum, Count, Avg, ExpressionWrapper, FloatField, Q
import csv
from django.http import HttpResponse
from django.http import JsonResponse

@login_required
def goal_list(request):
    filter_option = request.GET.get("filter", "all")

    # --- Goal Filtering ---
    if filter_option == "completed":
        goals = FinancialTracker.objects.filter(
            user=request.user,
            current_amount__gte=F('target_amount')
        )
    elif filter_option == "inprogress":
        goals = FinancialTracker.objects.filter(
            user=request.user,
            current_amount__lt=F('target_amount')
        )
    else:
        goals = FinancialTracker.objects.filter(user=request.user)

    user_goals = FinancialTracker.objects.filter(user=request.user)

    totals = user_goals.aggregate(
        total_saved=Sum("current_amount"),
        total_target=Sum("target_amount"),
        num_goals=Count("id"),
        completed_count=Count("id", filter=Q(current_amount__gte=F("target_amount"))),
    )

    goals = goals.annotate(
        progress_percent=ExpressionWrapper(
            (F("current_amount") * 100.0) / F("target_amount"),
            output_field=FloatField()
        )
    )

    avg_progress = user_goals.annotate(
        p=ExpressionWrapper((F("current_amount") * 100.0) / F("target_amount"), FloatField())
    ).aggregate(avg=Avg("p"))

    context = {
        "goals": goals,
        "totals": totals,
        "avg_progress": avg_progress["avg"],
    }

    return render(request, "goals/goal_list.html", context)


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


@login_required
def export_goals_csv(request):
    goals = FinancialTracker.objects.filter(user=request.user)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="financial_goals.csv"'

    writer = csv.writer(response)
    writer.writerow(["Goal Name", "Current Amount", "Target Amount", "Progress (%)"])

    for g in goals:
        progress = (g.current_amount / g.target_amount) * 100 if g.target_amount else 0
        writer.writerow([g.name, g.current_amount, g.target_amount, round(progress, 2)])

    return response


@login_required
def export_goals_json(request):
    goals = FinancialTracker.objects.filter(user=request.user).annotate(
        progress=ExpressionWrapper(
            (F("current_amount") * 100.0) / F("target_amount"),
            output_field=FloatField()
        )
    )

    data = [
        {
            "name": g.name,
            "current_amount": float(g.current_amount),
            "target_amount": float(g.target_amount),
            "progress_percent": round(g.progress, 2)
        }
        for g in goals
    ]

    return JsonResponse({"goals": data}, safe=False)