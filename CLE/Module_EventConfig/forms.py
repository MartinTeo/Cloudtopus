from django import forms
from background_task.models_completed import CompletedTask
from background_task.models import Task

class PendingEventsForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('run_at',  )
        labels = {
            'run_at':'Date',
        }
