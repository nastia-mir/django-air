from django.forms import ModelForm
from accounts.models import Staff, roles


class StaffRoleEditForm(ModelForm):
    class Meta:
        model = Staff
        fields = ['role']
