from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Case, CaseHistory

@receiver(pre_save, sender=Case)
def track_case_changes(sender, instance, **kwargs):
    if instance.pk:  # 只有更新時才記錄
        old_case = Case.objects.get(pk=instance.pk)
        changes = []
        for field in instance._meta.fields:
            field_name = field.name
            old_value = getattr(old_case, field_name)
            new_value = getattr(instance, field_name)
            if old_value != new_value:
                changes.append(f"{field_name}: {old_value} → {new_value}")

        if changes:
            CaseHistory.objects.create(
                case=instance,
                modified_by=instance.modified_by if hasattr(instance, 'modified_by') else None,
                changes=", ".join(changes)
            )
