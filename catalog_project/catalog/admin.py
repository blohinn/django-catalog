from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin

from .models import OptionValue, OptionGroup, Category


class OptionValueInline(admin.StackedInline):
    model = OptionValue
    extra = 1


@admin.register(OptionGroup)
class OptionGroupAdmin(admin.ModelAdmin):
    inlines = [OptionValueInline]


class CategoryAdmin(DraggableMPTTAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(
    Category,
    CategoryAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
    ),
    list_display_links=(
        'indented_title',
    ),
)
