from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Case, CaseHistory
from django.contrib.auth.decorators import login_required
from .forms import CaseForm
from django.db.models import Q  # 🔹 支援模糊搜尋

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
    query = request.GET.get("q", "")  # 取得搜尋關鍵字
    sort_order = request.GET.get("sort_order", "-created_at")  # 依案件建立日期排序，預設「最新優先」
    cases = Case.objects.all().order_by(sort_order)  # 🔹 依照使用者選擇排序

    if query:
        cases = cases.filter(
            Q(case_number__icontains=query) |
            Q(department__icontains=query) |
            Q(circuit_diagram__icontains=query) |
            Q(model_type__icontains=query) |
            Q(business_case_number__icontains=query) |
            Q(software_version__icontains=query) |
            Q(status__icontains=query)
        )

    return render(request, "case_list.html", {
        "cases": cases, 
        "query": query, 
        "sort_order": sort_order  # 🔹 把 sort_order 傳回模板
    })
    
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

# 編輯案件
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
    
# 查看案件細節
@login_required
def case_detail(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    history = CaseHistory.objects.filter(case=case).order_by("-modified_at")  # 依修改時間排序
    return render(request, "case_detail.html", {"case": case, "history": history})