from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
# Create your models here.


class Project(models.Model):
    title = models.CharField(max_length=255)
    client_name = models.CharField(max_length=250)
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, related_name='project', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title

    def registered_time(self):
        minutes = 0
        entries = self.entries.all()

        for entry in entries:
            minutes = minutes + entry.minutes
        return minutes

    def num_of_task_runing(self):
        return self.task.filter(status=Task.RUNING).count()

    # def get_absolute_url(self):
    #     return reverse('project_detail', kwargs={'pk': self.pk})


class Task(models.Model):

    # choices
    #
    RUNING = 'runing'
    DONE = 'done'

    STATUS_CHOICES = [
        (RUNING, 'Runing'),
        (DONE, 'Done'),
    ]
    # Model
    #
    project = models.ForeignKey(
        Project, related_name='task', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(
        User, related_name='task', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=RUNING
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def registered_time(self):
        return sum(entry.minutes for entry in self.entries.all())


class Entry(models.Model):
    project = models.ForeignKey(
        Project, related_name='entries', on_delete=models.CASCADE)
    task = models.ForeignKey(
        Task, related_name='entries', on_delete=models.CASCADE)
    minutes = models.IntegerField(default=0)
    is_tracked = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, related_name='entries', on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        if self.task:
            return '%s - %s' % (self.task.name, self.created_at)

        return '%s' % self.created_at
