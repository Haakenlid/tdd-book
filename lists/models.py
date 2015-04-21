from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import get_user_model

class List(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
    )
    shared_with = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='shared_lists',
    )

    @property
    def name(self):
        if self.item_set:
            return self.item_set.first().text
        else:
            return 'empty list {pk}'.format(self.pk)

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])

    def share(self, email):
        User = get_user_model()
        recipient, _ = User.objects.get_or_create(email=email)
        self.shared_with.add(recipient)


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')
