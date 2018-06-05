from django.db import models
from django.contrib.postgres.fields import JSONField

from mptt.models import MPTTModel, TreeForeignKey
from model_utils import FieldTracker

from .validators import validate_product_json_options


class OptionGroup(models.Model):
    name = models.CharField(max_length=64)

    fields_tracker = FieldTracker()

    def delete(self, using=None, keep_parents=False):
        products = Product.objects.filter(options__contains={'options': [{'option': self.name}]}).all()

        if products:
            return  # Revert deleting
        else:
            super(OptionGroup, self).delete(using, keep_parents)

    def save(self, *args, **kwargs):
        previous_option_group_name = self.fields_tracker.previous('name')

        products = Product.objects.filter(options__contains={'options': [{'option': previous_option_group_name}]}).all()
        for p in products:
            for o in p.options['options']:
                if o['option'] == previous_option_group_name:
                    o['option'] = self.name
            p.save()

        super(OptionGroup, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class OptionValue(models.Model):
    option_group = models.ForeignKey(OptionGroup, on_delete=models.CASCADE, related_name='values')
    name = models.CharField(max_length=64)

    fields_tracker = FieldTracker()

    class Meta:
        unique_together = ('option_group', 'name')

    def delete(self, using=None, keep_parents=False):
        products = Product.objects.filter(
            options__contains={'options': [
                {'option': self.option_group.name, 'values': [{'value': self.name}]}]}).all()

        if products:
            return  # Revert deleting
        else:
            super(OptionValue, self).delete(using, keep_parents)

    def save(self, *args, **kwargs):
        previous_option_value_name = self.fields_tracker.previous('name')

        products = Product.objects.filter(
            options__contains={'options': [
                {'option': self.option_group.name, 'values': [{'value': previous_option_value_name}]}]}).all()

        for p in products:
            for o in p.options['options']:
                if o['option'] == self.option_group.name:
                    for v in o['values']:
                        if v['value'] == previous_option_value_name:
                            v['value'] = self.name
            p.save()

        super(OptionValue, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(MPTTModel):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)

    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock_count = models.PositiveIntegerField(default=1)

    description = models.TextField(blank=True)

    options = JSONField(blank=True, default={})

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        validate_product_json_options(self.options)


def get_product_image_path(instance, filename):
    return 'products_images/{}/{}'.format(str(instance.product.slug), filename)


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to=get_product_image_path)

    def image_tag(self):
        return "<img src='%s' style='max-width: 200px; max-height: 200px;' />" % self.photo.url

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __str__(self):
        return 'Photo for "%s"' % self.product.name
