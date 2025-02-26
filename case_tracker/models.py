from django.contrib.auth.models import User
from django.db import models

class Case(models.Model):

    # 新增的欄位
    case_number = models.CharField(max_length=20, unique=True)  # 主要案號
    department = models.CharField(max_length=50)  # 所屬部門
    related_case_number = models.CharField(max_length=20, blank=True, null=True)  # 對應案號
    customer = models.CharField(max_length=100, blank=True, null=True)  # 客戶名稱
    created_at = models.DateTimeField(auto_now_add=True)  # 案件建立時間
    circuit_diagram = models.CharField(max_length=50, blank=True, null=True)  # 電路圖編號
    model_type = models.CharField(max_length=50, blank=True, null=True)  # 機型
    business_case_number = models.CharField(max_length=50, blank=True, null=True)  # 業務案號
    software_version = models.CharField(max_length=50, blank=True, null=True)  # 軟體編號

    # 案件狀態（選單）
    STATUS_CHOICES = [
        ('pending', '待處理'),
        ('in_progress', '進行中'),
        ('completed', '已完成'),
        ('on_hold', '暫停'),
        ('canceled', '已取消'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # 案件狀態

    def __str__(self):
        return f"{self.case_number} ({self.department}) - {self.status}"

# 案件變更紀錄
class CaseHistory(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changes = models.TextField()

    def __str__(self):
        return f"{self.case.case_number} 修改於 {self.modified_at}"