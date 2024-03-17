from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, ProductLine, ProductCategorySerializer


class CategoryViewSet(viewsets.ViewSet):
    queryset = Category.objects.all().is_active()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)

    # @action(methods=['delete'], detail=False, url_path=r'category/(?P<slug>[\w-]+)')
    # def delete_cat(self, request, slug=None):
    #     category = get_object_or_404(self.queryset, slug=slug)
    #     category.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #
    # @action(methods=['post'], detail=False, url_path='category/(?P<category_name>[^/.]+)/(?P<slug>[^/.]+)')
    # def add_cat(self, request, category_name=None, slug=None):
    #     category_data = request.data
    #
    #     category_data['category_name'] = category_name
    #     category_data['slug'] = slug
    #     category_data['is_active'] = True
    #
    #     serializer = CategorySerializer(data=category_data)
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(viewsets.ViewSet):
    queryset = Product.objects.all().is_active()

    lookup_field = 'slug'

    def retrieve(self, request, slug=None):
        serializer = ProductSerializer(
            self.queryset.filter(slug=slug).prefetch_related(
                Prefetch('attribute_value__attribute')
            ).prefetch_related(
                Prefetch('product_line__product_image')).prefetch_related(
                Prefetch('product_line__attribute_value__attribute')
            ), many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path=r'category/(?P<slug>[\w-]+)')
    def list_product_by_category_slug(self, request, slug=None):
        serializer = ProductCategorySerializer(self.queryset.filter(category__slug=slug), many=True)
        return Response(serializer.data)
