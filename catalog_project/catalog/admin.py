from django.contrib import admin
from .models import OptionValue, OptionGroup


class OptionValueInline(admin.StackedInline):
    model = OptionValue
    extra = 1


@admin.register(OptionGroup)
class OptionGroupAdmin(admin.ModelAdmin):
    inlines = [OptionValueInline]
