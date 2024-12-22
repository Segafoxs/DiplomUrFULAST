from .models import Employee


def select_in_db(name):
    query = Employee.objects.filter(name=name)
    if len(query) != 0:
        return query
    return None