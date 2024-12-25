import pandas as pd
from django.http import HttpResponse, JsonResponse, FileResponse
from django.urls import resolve
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from base_app.models import Contracts, Filial

from base_app.forms import AddOrderForm, ReportsForm

from base_app.contract_models import standart
from base_app.contract_models.krd import (toshev, tander, konditery_kubani, agro)
from base_app.contract_models.vlg import (atm, dzhokej, smit, sady)

from loguru import logger

from wms.models import WmsStocks

dict_module = {
    'toshev': toshev,
    'kzvs': standart,
    'agrokompleks': agro,
    # 'ok': ok,
    'tander': tander,
    'smit': smit,
    'dzhokej': dzhokej,
    'konditery-kubani': konditery_kubani,
    'atm': atm,
    # 'zelandiya': zelandiya,
    'sady': sady,
}


@login_required
def index(request):
    request.session['user'] = request.user.username
    request.session['filial'] = request.user.profile.filial
    if request.user.is_superuser:
        return render(request, 'base_app/admin.html', context={'session': request.session})
    else:
        request.session['filial'] = request.user.profile.filial.slug
        return render(request, 'base_app/home.html')


def show_add_orders(request):
    _filial_slug = request.GET.get('filial', None)
    context = {'selected': 'add_orders'}
    if _filial_slug:
        form = AddOrderForm(filial_slug=_filial_slug)
        context['form'] = form
        return render(request, 'base_app/add_orders.html', context=context)
    else:
        return render(request, 'base_app/add_orders.html', context=context)


def show_reports(request):
    for k, v in request.session.items():
        print(f'{k}={v}')

    _filial_slug = request.GET.get('filial', None)
    context = {'selected': 'reports'}
    if _filial_slug:
        form = ReportsForm(filial_slug=_filial_slug)
        context['form'] = form
        return render(request, 'base_app/reports.html', context=context)
    else:
        return render(request, 'base_app/reports.html', context=context)


@csrf_exempt
def processing_add_orders(request):
    context = {}
    if request.method == 'POST':
        # print(request.POST)
        file = request.FILES.get('file', None)
        print(file)
        # filial = request.GET.get('filial', None)
        filial = request.POST.get('filial', None)
        print(filial)
        contract = request.POST.get('contract', None)
        print(contract)

        if not contract:
            contract = request.GET.get('contract', None)
        context['contract'] = Contracts.objects.get(slug=contract)
        context['filial'] = Filial.objects.get(slug=filial)
        res, error_valid = dict_module[context['contract'].slug].start(file, context['contract'], context['filial'])
        if not error_valid:
            if isinstance(res, dict):
                context = {'result': res}
            else:
                context = {'result': {'error': f'Ошибка обработки\n{res}'}}
            return JsonResponse(context)
            # return render(request, 'base_app/show_result.html', context=context)
        context = {'result': res}
        return JsonResponse(context)
        # return render(request, f'base_app/show_result.html', context=context)
    else:
        return JsonResponse(context)
        # return render(request, 'base_app/show_result.html')


def get_stock_wms(request):
    operation = request.GET.get('slug_operation', None)
    context = {}
    context['selected'] = operation
    context['filial'] = Filial.objects.get(slug=request.GET.get('filial', None))
    context['contract'] = Contracts.objects.get(slug=request.GET.get('contract', None))
    context['result'] = (WmsStocks(_contract=context['contract'], _filial=context['filial']).get_goods_by_guid_group_guid_store(_contract=context['contract'], _filial=context['filial']))
    # context['result'] = (WmsStocks(_contract=context['contract'], _filial=context['filial']).get_store_guid(
    #     _contract=context['contract'], _filial=context['filial']))
    # df = pd.read_excel(context['result'])
    # context['result'] = df.to_json(orient='records')
    # from rest_framework.response import Response
    # return Response(df.to_json(orient="records"))
    # return FileResponse(open(context['result'], 'rb'))
    return JsonResponse({'id_store':context['result']})
    # return render(request, 'base_app/reports.html', context=context)


def get_stock_pg(request):
    operation = request.GET.get('slug_operation', None)
    context = {'selected': operation}
    return render(request, 'base_app/reports.html', context=context)


def get_sverka(request):
    operation = request.GET.get('slug_operation', None)
    context = {'selected': operation}
    return render(request, 'base_app/reports.html', context=context)


def get_sverka_ka(request):
    operation = request.GET.get('slug_operation', None)
    context = {'selected': operation}
    return render(request, 'base_app/reports.html', context=context)
