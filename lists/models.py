from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings


class List(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
    )

    @property
    def name(self):
        if self.item_set:
            return self.item_set.first().text
        else:
            return 'empty list {pk}'.format(self.pk)

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')
