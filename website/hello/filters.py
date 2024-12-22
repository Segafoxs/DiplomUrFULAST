import django_filters
from .models import Permit

class MyFilter(django_filters.FilterSet):


    class Meta:
        model = Permit
        fields = {'status': ["contains"]}