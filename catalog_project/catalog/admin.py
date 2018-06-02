from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin

from .models import OptionValue, OptionGroup, Category, ProductPhoto, Product


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


class PhotoInline(admin.StackedInline):
    fields = ('image_tag', 'photo',)
    readonly_fields = ('image_tag',)
    model = ProductPhoto
    extra = 1
    max_num = 5


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]
    prepopulated_fields = {'slug': ('name',)}
