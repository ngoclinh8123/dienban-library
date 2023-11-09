from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import NotFound
from rest_framework import status
from service.framework.drf_class.custom_permission import CustomPermission
from rest_framework.permissions import AllowAny
from service.request_service import RequestService
from ..models import Category
from ..helper.sr import CategorySr


class CategoryViewSet(GenericViewSet):
    _name = "Category"
    serializer_class = CategorySr
    permission_classes = [AllowAny]
    search_fields = ("title",)

    def list(self, request):
        queryset = Category.objects.all()
        queryset = self.filter_queryset(queryset)
        serializer = CategorySr(queryset, many=True)
        return RequestService.res(serializer.data)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(Category, pk=pk)
        serializer = CategorySr(obj)
        return RequestService.res(serializer.data)

    @action(methods=["post"], detail=True)
    def add(self, request):
        serializer = CategorySr(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return RequestService.res(serializer.data)

    @action(methods=["put"], detail=True)
    def change(self, request, pk=None):
        obj = get_object_or_404(Category, pk=pk)
        serializer = CategorySr(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return RequestService.res(serializer.data)

    @action(methods=["delete"], detail=True)
    def delete(self, request, pk=None):
        obj = get_object_or_404(Category, pk=pk)
        obj.delete()
        return RequestService.res(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    @action(methods=["delete"], detail=False)
    def delete_list(self, request):
        pk = self.request.query_params.get("ids", "")
        ids = [int(pk)] if pk.isdigit() else [int(i) for i in pk.split(",")]
        queryset = Category.objects.filter(id__in=ids)
        if len(ids) != len(queryset):
            raise NotFound()
        queryset.delete()
        return RequestService.res(status=status.HTTP_204_NO_CONTENT)
