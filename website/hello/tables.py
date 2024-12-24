from django_filters import FilterSet
import django_tables2 as tables
from .models import Permit
from django.utils.html import format_html

class PersonTable(tables.Table):
    signature_status = tables.Column(empty_values=(), verbose_name="Подпись")
    view_permit = tables.TemplateColumn(template_code='<a href="#" data-bs-toggle="modal" data-bs-target="#PermitModal"">Просмотр</a>',
                                        verbose_name="Информация")
    close_permit = tables.TemplateColumn(template_code='<button type="submit" class="btn btn-primary btn-sm">Закрыть</button>')
    class Meta:
        model = Permit
        template_name = "django_tables2/bootstrap.html"
        fields = ("number", "status", "department")

    def render_signature_status(self, record):

        signatures = []
        if record.signature_master:
            signatures.append("Подписано руководителем работ")
        if record.signature_director:
            signatures.append("Подписано начальником цеха")
        if record.signature_dailymanager:
            signatures.append("Подписано ДИС")
        if record.signature_stationengineer:
            signatures.append("Подписано начальником смены")
        
        if not signatures:
            return "Нет подписи"
        

        options = "".join([f'<option>{signature}</option>' for signature in signatures])
        dropdown_html = f'<select class="form-select">{options}</select>'
        
        return format_html(dropdown_html)
