from django.contrib import admin, messages

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
    actions = None

    def save_model(self, request, obj, form, change):
        messages.add_message(request, messages.ERROR,
                             "If option value wasn't deleted it mean that exist product(s) with attached option value.")
        super(OptionGroupAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        messages.add_message(request, messages.ERROR,
                             "If option group wasn't deleted it mean that exist product(s) with attached option group.")
        super(OptionGroupAdmin, self).delete_model(request, obj)


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
