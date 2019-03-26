import django_filters
from app import models


class domainFilter(django_filters.FilterSet):
    class Meta:
        model = models.domain
        fields = {
            'name':['exact','regex','contains'],
            'account':['exact'],
        }
