from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Case, CaseHistory
from django.contrib.auth.decorators import login_required
from .forms import CaseForm

# 註冊帳號
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 註冊後自動登入
            return redirect("case_list")  # 跳轉到案件列表
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

# 案件列表
@login_required
def case_list(request):
    cases = Case.objects.all()
    return render(request, "case_list.html", {"cases": cases})

# 新增案件
@login_required
def add_case(request):
    if request.method == "POST":
        form = CaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("case_list")
    else:
        form = CaseForm()
    return render(request, "add_case.html", {"form": form})

@login_required
def edit_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    
    if request.method == "POST":
        form = CaseForm(request.POST, instance=case)
        if form.is_valid():
            updated_case = form.save(commit=False)
            updated_case.modified_by = request.user  # 記錄修改者
            updated_case.save()
            return redirect("case_list")
    else:
        form = CaseForm(instance=case)
    
    return render(request, "edit_case.html", {"form": form, "case": case})
    
@login_required
def case_detail(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    history = CaseHistory.objects.filter(case=case).order_by("-modified_at")  # 依修改時間排序
    return render(request, "case_detail.html", {"case": case, "history": history})