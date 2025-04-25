from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

schedule, created = IntervalSchedule.objects.get_or_create(
    every=1,
    period=IntervalSchedule.DAYS,
)

PeriodicTask.objects.get_or_create(
    interval=schedule,
    name="Block inactive users",
    task="users.tasks.block_inactive_users",
    defaults={"kwargs": json.dumps({})}
)
