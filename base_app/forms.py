from django import forms

from base_app.models import Contracts


# contracts_all = Contracts.objects.all()


def append_contract_choices(filial_slug, menu_slug):
    contract_choice = []
    contract_all_filial = Contracts.objects.filter(filial__slug=filial_slug, menu__slug=menu_slug)
    for contract in contract_all_filial:
        _ = (contract.slug, contract.name)
        contract_choice.append(_)
    return contract_choice


class AddOrderForm(forms.Form):
    def __init__(self, filial_slug, *args, **kwargs):
        super(AddOrderForm, self).__init__(*args, **kwargs)
        self.menu_slug = 'add_orders'
        self.fields['contract'] = forms.ChoiceField(label='Контракт',
                                                    choices=append_contract_choices(filial_slug=filial_slug, menu_slug=self.menu_slug))
        self.fields['file'] = forms.FileField(label='Файл')

        self.fields['contract'].widget.attrs.update({'class': 'inp_open_file'})
        self.fields['file'].widget.attrs.update({'class': 'inp_open_file', 'accept': '.xls, .xlsx'})


class ReportsForm(forms.Form):
    def __init__(self, filial_slug, *args, **kwargs):
        super(ReportsForm, self).__init__(*args, **kwargs)
        self.menu_slug = 'reports'
        self.fields['contract'] = forms.ChoiceField(label='Контракт',
                                                    choices=append_contract_choices(filial_slug=filial_slug, menu_slug=self.menu_slug))
        # self.fields['file'] = forms.FileField(label='Файл')

        self.fields['contract'].widget.attrs.update({'class': 'inp_open_file'})
        # self.fields['file'].widget.attrs.update({'class': 'inp_open_file', 'accept': '.xls, .xlsx'})
