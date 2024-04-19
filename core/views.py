# views.py
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.apps import apps

from django.db.models import Q
from datetime import datetime
import re

date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
def is_date(string):
    return bool(date_pattern.match(string))

def filter_objects(queryset, filters):
    filtered_queryset = queryset

    for field, condition in filters.items():

        operator = condition[0]
        value = condition[1]
        if is_date(value):
            value = datetime.strptime(value, "%Y-%m-%d").date()


        if operator == "==":
            filtered_queryset = filtered_queryset.filter(**{field: value})
        elif operator == "!=":
            filtered_queryset = filtered_queryset.exclude(**{field: value})
        elif operator == ">":
            filtered_queryset = filtered_queryset.filter(**{f"{field}__gt": value})
        elif operator == ">=":
            filtered_queryset = filtered_queryset.filter(**{f"{field}__gte": value})
        elif operator == "<":
            filtered_queryset = filtered_queryset.filter(**{f"{field}__lt": value})
        elif operator == "<=":
            filtered_queryset = filtered_queryset.filter(**{f"{field}__lte": value})
        elif operator == "contains":
            filtered_queryset = filtered_queryset.filter(**{f"{field}__icontains": value})
        elif operator == "startswith":
            filtered_queryset = filtered_queryset.filter(**{f"{field}__istartswith": value})
        elif operator == "endswith":
            filtered_queryset = filtered_queryset.filter(**{f"{field}__iendswith": value})
        else:
            # Unsupported operator
            raise ValueError(f"Unsupported operator: {operator}")

    return filtered_queryset


class RetrieveDataAPIView(APIView):
    def post(self, request):
        data = request.data
        model_name = data.get('modelName')
        fields = data.get('fields', [])
        filters = data.get('filters', {})

        # Get the model class dynamically
        for app_config in apps.get_app_configs():
            try:
                model_class = apps.get_model(app_label=app_config.label, model_name=model_name)
                if model_class:
                    break
            except LookupError:
                # Model not found in this app, move to the next one
                pass
        else:
            return Response({'error': f'Model {model_name} not found in any installed apps.'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = model_class.objects.all()

        if filters:
            queryset = filter_objects(queryset, filters)

        # Select specific fields
        if fields and fields != ['*']:
            queryset = queryset.values(*fields)
        else:
            queryset = queryset.values()
        


        return Response({'data': queryset})

    def get(self, request):
        return Response({'error': 'Only POST requests are allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
