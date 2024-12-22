from django_filters import FilterSet
import django_tables2 as tables
from .models import Permit
from django.utils.html import format_html

class PersonTable(tables.Table):
    signature_status = tables.Column(empty_values=(), verbose_name="Подпись")

    class Meta:
        model = Permit
        template_name = "django_tables2/bootstrap.html"
        fields = ("number", "status", "department")

    def render_signature_status(self, record):

        signatures = []
        if record.signature_director:
            signatures.append("Подписано директором")
        if record.signature_dailymanager:
            signatures.append("Подписано DailyManager")
        if record.signature_stationengineer:
            signatures.append("Подписано StationEngineer")
        
        if not signatures:
            return "Нет подписи"
        

        options = "".join([f'<option>{signature}</option>' for signature in signatures])
        dropdown_html = f'<select class="form-select">{options}</select>'
        
        return format_html(dropdown_html)
