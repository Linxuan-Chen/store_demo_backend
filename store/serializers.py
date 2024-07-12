from rest_framework import serializers
from .models import Product, Collection


class SimpleProductSerializer(serializers.ModelSerializer):
    """A simple product serializer

        The serializer only displays basic meta data of a product
    """
    class Meta:
        model = Product
        fields = ['title', 'inventory', 'unit_price']


class CollectionRetrieveSerializer(serializers.ModelSerializer):
    """A serializer to retrieve collection data

        featured_product_names returns simple data of featured products of the collection
    """

    featured_products = serializers.SerializerMethodField(
        method_name='get_featured_products')

    class Meta:
        model = Collection
        fields = ['id', 'title', 'featured_products']

    def get_featured_products(self, collection):
        products = collection.featured_product
        return SimpleProductSerializer(products, many=True).data


class CollectionModifySerializer(serializers.ModelSerializer):
    """A serialzier to modify collection data"""
    class Meta:
        model = Collection
        fields = ['title']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'collection', 'title', 'slug',
                  'description', 'inventory', 'promotions', 'unit_price']
