import pandas as pd
from base_app.contract_models.standart import start as start_standart


def start(file_name, contract, filial):
    res, error_valid = start_standart(file_name=file_name, contract=contract, filial=filial, create_product=True)
    return res, error_valid
