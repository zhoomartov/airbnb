from django_filters.rest_framework import FilterSet
from .models import Property


class PropertyFilter(FilterSet):
    class Meta:
       model = Property
       fields = {
           'price_per_night': ['gt', 'lt'],
           'property_type' : ['exact'],
           'max_guests' : ['exact']
       }