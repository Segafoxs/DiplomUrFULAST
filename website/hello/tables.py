from django_filters import FilterSet
import django_tables2 as tables
from .models import Permit
from django.utils.html import format_html
from django_tables2.utils import A
import itertools




class PermitTable(tables.Table):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.counter = itertools.count()
    #
    # def render_row_number(self):
    #     return {next(self.counter)}
    #
    # def render_id(self, value):
    #     return f"{value}"

    #row_number = tables.Column(empty_values=())
    number = tables.Column(verbose_name="Номер")
    action = tables.Column(verbose_name="Действие")
    status = tables.Column(verbose_name="Статус")
    signature_status = tables.Column(empty_values=(), verbose_name="Подпись", )
    view_permit = tables.TemplateColumn(
        template_code='<a href="#" data-bs-toggle="modal" data-bs-target="#PermitModal"">Просмотр</a>',
        verbose_name="Информация")
                                         


    #view_permit2 = tables.LinkColumn("view_permit", text="Просмотр")

    class Meta:
        model = Permit
        template_name = "django_tables2/bootstrap.html"

        fields = ("number", "action", "status", "department")
        # sequence =  ("number", "action", "status", "department" )



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
        if record.signature_executor:
            signatures.append("Подписано производителем работ")
        
        if not signatures:
            return "Нет подписи"
        

        options = "".join([f'<option>{signature}</option>' for signature in signatures])
        dropdown_html = f'<select class="form-select">{options}</select>'
        
        return format_html(dropdown_html)
