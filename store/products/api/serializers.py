from datetime import datetime
from django.utils.timesince import timesince
from rest_framework import serializers

from products.models import Product, Category, Images, NotebookProduct


class CategorySerializer(serializers.ModelSerializer):

    # list of products in this category:
    products = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = "__all__"


class ImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = "__all__"

class NotebookProductSerializer(serializers.ModelSerializer):
    category_name = serializers.StringRelatedField(source='category',
                                                   read_only=True)
    images = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = NotebookProduct
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):

    # just for practice, has no sense:
    time_beetween_modified = serializers.SerializerMethodField()

    # display category name, not just id:
    category_name = serializers.StringRelatedField(source='category',
                read_only=True)  # опции source+read_only исправят ошибки с трудностями в POST

    # show full dict, instead of just 1 field
    # category_full_details = CategorySerializer(source='category', read_only=True)

    # shows images (id), that it has
    images = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_time_beetween_modified(self, object):
        time_delta = timesince(object.create_at, object.update_at)
        return time_delta


