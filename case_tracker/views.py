from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Case, CaseHistory
from django.contrib.auth.decorators import login_required
from .forms import CaseForm
from django.db.models import Q  # 🔹 支援模糊搜尋
import datetime
import calendar  # 🔹 用來取得該月份最後一天
from django.utils.html import format_html  # 🔹 確保 `format_html()` 可用

    
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
    query = request.GET.get("q", "").strip()  # 取得搜尋關鍵字，去除前後空格
    sort_order = request.GET.get("sort_order", "-created_at")  # 依案件建立日期排序，預設「最新優先」
    department_filter = request.GET.get("department", "")  # 部門篩選
    status_filter = request.GET.get("status", "")  # 狀態篩選
    
    # 取得年、月、日
    start_year = request.GET.get("start_year", "")
    start_month = request.GET.get("start_month", "")
    start_day = request.GET.get("start_day", "")
    end_year = request.GET.get("end_year", "")
    end_month = request.GET.get("end_month", "")
    end_day = request.GET.get("end_day", "")
    
    cases = Case.objects.all().order_by(sort_order)  # 🔹 依照使用者選擇排序
    search_results = {}
    
    if query:
        for case in cases:
            match_reasons = []  # 存放匹配原因
            if query.lower() in case.case_number.lower():
                match_reasons.append(f"案件號碼：{highlight_text(case.case_number, query)}")
            if query.lower() in case.department.lower():
                match_reasons.append(f"部門名稱：{highlight_text(case.department, query)}")
            if query.lower() in case.circuit_diagram.lower():
                match_reasons.append(f"電路圖：{highlight_text(case.circuit_diagram, query)}")
            if query.lower() in case.model_type.lower():
                match_reasons.append(f"機型：{highlight_text(case.model_type, query)}")
            if query.lower() in case.business_case_number.lower():
                match_reasons.append(f"客戶編號：{highlight_text(case.business_case_number, query)}")
            if query.lower() in case.software_version.lower():
                match_reasons.append(f"軟體版本：{highlight_text(case.software_version, query)}")
            if query.lower() in case.status.lower():
                match_reasons.append(f"狀態：{highlight_text(case.status, query)}")

            if match_reasons:
                search_results[case.id] = match_reasons
                
        cases = cases.filter(
            Q(case_number__icontains=query) |
            Q(department__icontains=query) |
            Q(circuit_diagram__icontains=query) |
            Q(model_type__icontains=query) |
            Q(business_case_number__icontains=query) |
            Q(software_version__icontains=query) |
            Q(status__icontains=query)
        )

    # 部門篩選
    if department_filter:
        cases = cases.filter(department=department_filter)

    # 狀態篩選
    if status_filter:
        cases = cases.filter(status=status_filter)

     # 日期範圍篩選
 # 日期範圍篩選
    try:
        if start_year:
            start_year = int(start_year)
            start_month = int(start_month) if start_month else 1  # 預設 1 月
            start_day = int(start_day) if start_day else 1  # 預設 1 日

            start_date = datetime.date(start_year, start_month, start_day)
            cases = cases.filter(created_at__gte=start_date)

        if end_year:
            end_year = int(end_year)
            end_month = int(end_month) if end_month else 12  # 預設 12 月

            # 🔹 如果沒有選擇 end_day，就自動取得該年該月的最後一天
            if not end_day:
                _, last_day = calendar.monthrange(end_year, end_month)
                end_day = last_day  # 🔹 設定為該月份的最後一天
            else:
                end_day = int(end_day)

            end_date = datetime.date(end_year, end_month, end_day)
            cases = cases.filter(created_at__lte=end_date)

    except ValueError:
        pass  # 避免錯誤日期導致崩潰

    # 產生年份、月份、日期選項
    current_year = datetime.date.today().year
    years = range(current_year - 10, current_year + 1)  # 最近 10 年
    months = range(1, 13)
    days = range(1, 32)



    # 取得所有部門 & 狀態（讓篩選選單可用）
    all_departments = Case.objects.values_list("department", flat=True).distinct()
    all_statuses = Case.objects.values_list("status", flat=True).distinct()

    return render(request, "case_list.html", {
        "cases": cases,
        "query": query,
        "search_results": search_results,
        "sort_order": sort_order,
        "department_filter": department_filter,
        "status_filter": status_filter,
        "start_year": str(start_year),
        "start_month": str(start_month),
        "start_day": str(start_day),
        "end_year": str(end_year),
        "end_month": str(end_month),
        "end_day": str(end_day),
        "years": years,
        "months": months,
        "days": days,
        "all_departments": all_departments,
        "all_statuses": all_statuses,
    })

# 🔹 標記匹配的關鍵字為紅色
def highlight_text(text, query):
    return format_html(text.replace(query, f'<span style="color: red; font-weight: bold;">{query}</span>'))

    
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