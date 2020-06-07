from django_cron import CronJobBase, Schedule
from django.utils import timezone
from datetime import timedelta
from postman.models import Email


class CleanEmails(CronJobBase):
    RUN_EVERY_MINS = 43200

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'postman.clean_emails'

    def do(self):
        half_year = timezone.now() - timedelta(days=180)
        emails = Email.objects.filter(received_on__lte=half_year)
        for email in emails:
            email.delete()

