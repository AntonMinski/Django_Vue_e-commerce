from django.contrib import admin
from django import forms
from django.forms import ModelChoiceField

from .models import Category, Product, Images, NotebookProduct

from mptt.admin import DraggableMPTTAdmin


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'status']
    list_filter = ['status']


class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title', 'related_products_count',
                    'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}
    # inlines = [CategoryLangInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(
                 qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = \
        'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description =\
        'Related products (in tree)'


class ProductImageInLine(admin.TabularInline):
    model = Images
    extra = 5


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status']
    list_filter = ['status']
    readonly_fields = ['image_tag']
    inlines = [ProductImageInLine]
    prepopulated_fields = {'slug': ('title',)}


class NotebookProductAdmin(admin.ModelAdmin):
    final_price = ['fin_price']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='win'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category, CategoryAdmin2)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images)
admin.site.register(NotebookProduct, NotebookProductAdmin)
