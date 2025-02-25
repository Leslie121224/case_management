from django.contrib import admin
from .models import Case

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('case_number', 'department', 'customer', 'circuit_diagram', 'model_type', 'business_case_number', 'software_version', 'status', 'created_at')  # 顯示更多欄位
    search_fields = ('case_number', 'department', 'customer', 'business_case_number', 'software_version')  # 可搜尋欄位
    list_filter = ('status', 'department', 'created_at')  # 可篩選欄位
