from django.db import models
from apps.approved.models import Approved
from apps.applications.models import InternshipApplication

class ProgressView(Approved):
    class Meta:
        proxy = True
        verbose_name = "Progress"
        verbose_name_plural = "Progress"
class Progress(models.Model):
    application = models.ForeignKey(InternshipApplication, on_delete=models.CASCADE, null=True, blank=True)
    #
    # other fields...
    @property
    def start_date(self):
        return self.application.start_date if self.application else None

    @property
    def end_date(self):
        return self.application.end_date if self.application else None
