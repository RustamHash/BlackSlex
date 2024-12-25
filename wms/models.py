import datetime
import json
import locale
import os

import pandas as pd
import requests


class SaveFileWms:
    def __init__(self):
        super(SaveFileWms, self).__init__()
        self.json_stocks_wms = None
        self.contract_wms = None
        self.filial_wms = None

    def save_reports_stock(self):
        _path_files = self.__exists_create_folder()
        _f_name = f'{_path_files}\\{self.__create_date_file_name()}_{self.contract_wms}_wms.xlsx'
        _df = pd.json_normalize(self.json_stocks_wms)
        for col in _df.columns:
            if 'navigationLinkUrl' in col:
                _df.drop([col], axis=1, inplace=True)
        _df = self.__date_reformat(_df)
        _df.to_excel(f'{_f_name}', index=False)
        return _f_name

    @staticmethod
    def __date_reformat(_df):
        for col in _df.columns:
            if 'СерияНоменклатуры.ДатаПроизводства' == col or 'СерияНоменклатуры.ГоденДо' == col:
                _df[col] = pd.to_datetime(_df[col])
                _df[col] = _df[col].dt.date
        return _df

    @staticmethod
    def __validate_file_name(file_name):
        file_name = str(file_name)
        file_name = file_name.replace('"', "").replace("'", "")
        file_name = file_name.lower()
        return file_name

    @staticmethod
    def __create_date_file_name():
        _dt = datetime.datetime.now()
        _dt = _dt.strftime("%d%m%y")
        _dt = str(_dt)
        return _dt

    @staticmethod
    def __create_date_folder_name():
        locale.setlocale(locale.LC_TIME, 'ru')
        _dt = datetime.datetime.now()
        _dt_mouth = _dt.strftime("%B")
        _dt_year = _dt.strftime("%Y")
        _dt_mouth = str(_dt_mouth)
        _dt_year = str(_dt_year)
        return _dt_mouth, _dt_year

    def __exists_create_folder(self):
        _dt_mouth, _dt_year = self.__create_date_folder_name()
        path_files = os.path.join(f'{self.filial_wms.path_saved_order}_wms', _dt_year, _dt_mouth)
        if not os.path.exists(path_files):
            os.makedirs(path_files)
        return path_files


class WmsKrd:
    def __init__(self, _contract, _filial):
        super(WmsKrd, self).__init__()
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Connection': 'keep-alive'
        }
        self.server = '172.172.185.67'
        # self.infobase = 'krd_itc_wms'
        self.infobase = str(_filial.url_wms)
        self.username = 'ODUser'
        self.password = 249981
        self.params = None
        self.contract_wms = None
        self.json_data = None
        # f"http://172.172.185.67/krd_itc_wms/odata/standard.odata/"
        self.full_url = f"http://{self.server}/{self.infobase}/odata/standard.odata/"
        self._auth = requests.auth.HTTPBasicAuth(self.username, self.password)

    def connect(self, _top=None):

        if _top is not None:
            if self.params is None:
                self.params = f"$top={_top}"
            else:
                self.params = f"{self.params}&$top={_top}"
        response = requests.get(url=self.full_url, headers=self.headers, auth=self._auth, params=self.params)
        print(response.url)
        return response


class WmsStocks(WmsKrd, SaveFileWms):
    def __init__(self, _contract=None, _filial=None):
        super(WmsStocks, self).__init__(_contract=_contract, _filial=_filial)
        super().__init__(_contract, _filial)
        self._filial = _filial
        self.cat_name = 'ОстаткиВПоллетах'
        self.params = (f"$select="
                       # f"*"
                       f"Номенклатура/Code,"
                       f"Номенклатура/Description,"
                       f"Номенклатура/Артикул,"
                       f"Номенклатура/Parent/Description,"
                       f"КоличествоBalance,"
                       f"СерияНоменклатуры/ДатаПроизводства,"
                       f"СерияНоменклатуры/ГоденДо,"
                       f"ЯчейкаХранения/Склад/Ref_Key, "
                       f"ЯчейкаХранения/Склад/Description"
                       f"&$orderby=Номенклатура/Артикул"
                       )
        self.full_url = (f'{self.full_url}/AccumulationRegister_{self.cat_name}/Balance?'
                         f'$format=json&'
                         f'$expand=Номенклатура/Parent, ЯчейкаХранения/Склад, СерияНоменклатуры'
                         )

    def get_good_by_art(self, good_art, _contract):
        self.infobase = self._filial.url_wms
        self.contract_wms = _contract
        self.params = f"{self.params}&$filter=Номенклатура/Артикул eq'{good_art}'"
        response = self.connect()
        if response.status_code != 200:
            return response.text
        self.json_stocks_wms = json.loads(response.text).get('value', None)
        _file_name = self.save_reports_stock()
        return _file_name

    def get_goods_by_guid_group(self, _contract, _filial, top=None):
        self.infobase = _filial.url_wms
        self.contract_wms = _contract
        self.filial_wms = _filial
        self.params = (f"{self.params}&$filter="
                       f"Номенклатура/Parent/Code eq '{str(self.contract_wms.id_groups_goods)}'"
                       )
        if top is not None:
            self.params = f"{self.params}&$top={top}"
        response = self.connect()
        if response.status_code != 200:
            return response.text
        self.json_stocks_wms = json.loads(response.text).get('value', None)
        _file_name = self.save_reports_stock()
        return _file_name

    def get_goods_by_guid_group_guid_store(self, _contract, _filial, top=None):
        _guid = 'ff0af2e0-39a8-11ed-b63d-d3de6462aa6d'
        self.infobase = _filial.url_wms
        self.contract_wms = _contract
        self.filial_wms = _filial
        self.params = (f"{self.params}&$filter="
                       f"Номенклатура/Parent/Code eq '{str(self.contract_wms.id_groups_goods)}'"
                       f"and "
                       f"ЯчейкаХранения/Склад/Ref_Key eq guid'{str(_guid)}'")
        if top is not None:
            self.params = f"{self.params}&$top={top}"
        response = self.connect()
        if response.status_code != 200:
            return response.text
        self.json_stocks_wms = json.loads(response.text).get('value', None)
        _file_name = self.save_reports_stock()
        return _file_name

    def get_store_guid(self, _contract, _filial, top=None):
        self.infobase = _filial.url_wms
        self.contract_wms = _contract
        self.cat_name = 'Catalog_Склады'
        self.full_url = 'http://172.172.185.67/krd_itc_wms/odata/standard.odata//Catalog_Склады?$format=json&$select=ОбщийСклад_Key'
        self.params = f"&$filter=Code eq '{str(_contract.id_sklad)}'"
        response = self.connect()
        result = json.loads(response.text).get('value', None)
        store_guid = result[0]['ОбщийСклад_Key']
        return store_guid


class WmsGoods(WmsKrd, SaveFileWms):
    def __init__(self):
        super(WmsGoods, self).__init__()
        self.cat_name = 'Номенклатура'
        self.params = f"$select=Ref_Key,Parent_Key,Code,Description,Артикул"
        self.full_url = f'{self.full_url}/Catalog_{self.cat_name}'

    def get_good_by_art(self, good_art, _contract):
        self.infobase = _contract.filial.url_wms
        self.contract_wms = _contract
        self.params = f"{self.params}&$filter=Артикул eq'{good_art}'"
        response = self.connect()
        if response.status_code != 200:
            return response.text
        self.json_stocks_wms = json.loads(response.text).get('value', None)
        _file_name = self.save_reports_stock()
        return _file_name

    def get_goods_by_guid_group(self, _contract, _filial, top=None):
        self.infobase = _filial.url_wms
        self.contract_wms = _contract
        self.params = f"{self.params}&$filter=Parent_Key eq '{str(self.contract_wms.id_groups_goods)}'"
        if top is not None:
            self.params = f"{self.params}&$top={top}"
        response = self.connect()
        if response.status_code != 200:
            return response.text
        self.json_stocks_wms = json.loads(response.text).get('value', None)
        _file_name = self.save_reports_stock()
        return _file_name
