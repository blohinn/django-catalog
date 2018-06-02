from django.db import models


class OptionGroup(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class OptionValue(models.Model):
    option_group = models.ForeignKey(OptionGroup, on_delete=models.CASCADE, related_name='values')
    name = models.CharField(max_length=64)

    class Meta:
        unique_together = ('option_group', 'name')

    def __str__(self):
        return self.name
