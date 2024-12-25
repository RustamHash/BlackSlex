# -*- coding: utf-8 -*-
# base_app\contract_models\neo_stroy_krd.py
import pandas as pd
import datetime

from base_app.contract_models.utils import data_to_dict, save_to_xml, dic_log_return, generator_bar_code, DIC_NUM_ART

dic_num_art = DIC_NUM_ART


def start(file_name, contract, filial, create_product=False, create_client=False):
    try:
        for i in dic_log_return:
            dic_log_return[i] = 0
        _df_order, _df_porder = __load_parse_file(file_name)
        if len(_df_order) > 0:
            __create_order(_df=_df_order, contract=contract, filial=filial)
        if len(_df_porder) > 0:
            __create_porder(_df=_df_porder, contract=contract, filial=filial)
            if create_product:
                __create_product(_df=_df_porder, contract=contract, filial=filial)
        return dic_log_return, True
    except Exception as e:
        return {'error': str(e)}, False


def __load_parse_file(_wb_file):
    _df = pd.read_excel(_wb_file, dtype=object)
    _df_order = _df[_df['ВидНакладной'] == 'Расход'].copy()
    _df_porder = _df[_df['ВидНакладной'] == 'Приход'].copy()
    return _df_order, _df_porder


def __create_order(_df, contract, filial, _dic_num_art=None, ):
    df_order = pd.DataFrame()
    global dic_num_art
    if _dic_num_art is not None:
        dic_num_art = _dic_num_art
    df_order['Itemid'] = _df[_df.columns[dic_num_art['NUM_ART_PRODUCT']]]
    df_order['Qty'] = _df[_df.columns[dic_num_art['NUM_QTY_PRODUCT']]]
    df_order['SalesId'] = _df[_df.columns[dic_num_art['NUM_ORDER']]]
    df_order['InventLocationId'] = contract.id_sklad
    df_order['ConsigneeAccount'] = contract.id_client
    df_order['DeliveryDate'] = _df[_df.columns[dic_num_art['NUM_DATE']]]
    df_order['ManDate'] = ''
    df_order['SalesUnit'] = 'шт'
    df_order['Delivery'] = 2
    df_order['Redelivery'] = 1
    df_order['OrderType'] = 1
    df_order['Comment'] = _df[_df.columns[dic_num_art['NUM_COMMENT']]]
    dic_order = data_to_dict(df_order)
    save_to_xml(dic_order, 'CustPicking', contract=contract, filial=filial)
    dic_log_return['Расход'] += len(dic_order)


def __create_porder(_df, contract, filial, _dic_num_art=None):
    df_porder = pd.DataFrame()
    global dic_num_art
    if _dic_num_art is not None:
        dic_num_art = _dic_num_art
    df_porder['Itemid'] = _df[_df.columns[dic_num_art['NUM_ART_PRODUCT']]]
    df_porder['Qty'] = _df[_df.columns[dic_num_art['NUM_QTY_PRODUCT']]]
    df_porder['PurchId'] = _df[_df.columns[dic_num_art['NUM_ORDER']]]
    df_porder['VendAccount'] = contract.id_postav
    df_porder['DeliveryDate'] = _df[_df.columns[dic_num_art['NUM_DATE']]]
    df_porder['InventLocationId'] = contract.id_sklad
    df_porder['ProductionDate'] = '01.01.2023'
    df_porder['PurchUnit'] = 'шт'
    df_porder['PurchTTN'] = 1
    df_porder['Price'] = 0
    dic_order = data_to_dict(df_porder)
    save_to_xml(dic_order, 'VendReceipt', contract=contract, filial=filial)
    dic_log_return['Приход'] += len(dic_order)


def __create_product(_df, contract, filial, _dic_num_art=None):
    global dic_num_art
    if _dic_num_art is not None:
        dic_num_art = _dic_num_art
    bar_code_list = _df[_df.columns[1]].apply(lambda x: generator_bar_code()).to_list()
    df_product = pd.DataFrame()
    df_product['ItemId'] = _df[_df.columns[dic_num_art['NUM_ART_PRODUCT']]]
    df_product['ItemName'] = _df[_df.columns[dic_num_art['NUM_NAME_PRODUCT']]]
    df_product['NetWeight'] = 500
    df_product['NetWeightBox'] = 500
    df_product['NetWeightPack'] = 500
    df_product['BruttoWeight'] = 500
    df_product['BruttoWeightBox'] = 500
    df_product['BruttoWeightPack'] = 500
    df_product['Quantity'] = 1
    df_product['standardShowBoxQuantity'] = 1
    df_product['UnitId'] = 'шт'
    df_product['Depth'] = 1200
    df_product['Height'] = 1800
    df_product['Width'] = 800
    df_product['BoxDepth'] = 1200
    df_product['BoxHeight'] = 1800
    df_product['BoxWidth'] = 800
    df_product['BlockDepth'] = 1200
    df_product['BlockHeight'] = 1800
    df_product['BlockWidth'] = 800
    df_product['StandardPalletQuantity'] = 1
    df_product['QtyPerLayer'] = 1
    df_product['Price'] = 1
    df_product['ShelfLife'] = 1095
    df_product['EanBarcode'] = bar_code_list
    df_product['EanBarcodeBox'] = bar_code_list
    df_product['EanBarcodePack'] = bar_code_list
    df_product['Gs1Barcode'] = bar_code_list
    df_product['Gs1BarcodeBox'] = bar_code_list
    df_product['Gs1BarcodePack'] = bar_code_list
    dic_product = data_to_dict(df_product)
    save_to_xml(dic_product, 'InventTable', contract=contract, filial=filial)
    dic_log_return['Справочник товаров'] += len(dic_product)
