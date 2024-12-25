from django.urls import resolve
from base_app.models import Filial, Menu, Contracts


def get_app_name(request):
    app_name = resolve(request.path_info).view_name
    res = Filial.objects.filter(slug=app_name.split(':')[0]).first()
    if res:
        return {'get_filial': res}
    else:
        return {'get_filial': None}


def get_url_name(request):
    url_name = resolve(request.path_info).url_name
    return {
        'url_name': url_name
    }


def get_contract_list(request):
    app_name = resolve(request.path_info).view_name
    res = Contracts.objects.filter(menu__filial__slug=app_name.split(':')[0])
    if res:
        return {'contracts_list': res}
    else:
        return {'contracts_list': 'None'}


