from django.db import models
from django.urls import reverse


class Actor(models.Model):
    csfd_id = models.TextField()
    name = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['csfd_id'],
                                    name='actor_unique_csfd_id')
        ]

    def get_absolute_url(self):
        return reverse('actor_detail', args=[str(self.pk)])


class Movie(models.Model):
    csfd_id = models.TextField()
    name = models.TextField()
    actors = models.ManyToManyField(Actor)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['csfd_id'],
                                    name='movie_unique_csfd_id')
        ]

    def get_absolute_url(self):
        return reverse('movie_detail', args=[str(self.pk)])
