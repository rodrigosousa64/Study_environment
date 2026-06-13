from django.http import request
from rest_framework.permissions import BasePermission, SAFE_METHODS


class Is_author_or_readonly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
