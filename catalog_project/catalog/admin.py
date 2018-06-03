from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin
from django_admin_json_editor import JSONEditorWidget

from .models import OptionValue, OptionGroup, Category, ProductPhoto, Product
from .product_options_editor_schema import get_product_option_json_editor_schema


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

    def get_form(self, request, obj=None, **kwargs):
        widget = JSONEditorWidget(get_product_option_json_editor_schema, collapsed=False)
        form = super().get_form(request, obj, widgets={'options': widget}, **kwargs)
        return form
