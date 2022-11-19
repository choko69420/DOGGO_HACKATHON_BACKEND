from django.core.management.base import BaseCommand, CommandError
from api.models import Report, User


class Command(BaseCommand):
    help = 'Updates the scores from the reports'

    def handle(self, *args, **options):
        reports = Report.objects.all()
        for report in reports:
            if report.valid == "valid":
                report.author.score += 10
                report.author.save()
            elif report.valid == "invalid":
                report.author.score -= 10
                report.author.save()
            else:
                continue

            self.stdout.write(self.style.SUCCESS(
                f'Successfully updated scores'))
