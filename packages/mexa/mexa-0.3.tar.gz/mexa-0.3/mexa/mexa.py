# encoding: utf-8
# from datetime import datetime
from NssField import NssField


def fake(type_field, data):
    if type_field == 'nss':
        return NssField.generate(data)
    raise Exception(f"Tipo invalido: {type_field}")

def validate(type_field, value):
    if type_field == 'nss':
        return NssField.is_valid(value)
    raise Exception(f"Tipo invalido: {type_field}")


# i = 0
# while i < 10000000:
#    i += 1
#    # , 'f_afiliacion': '81',
#    nss = fake('nss', {'region_imss': '23', 'f_nacimiento': '83'})
#    if validate('nss', nss):
#        print(f"NSS valido '{nss}'")
#    else:
#        print(f"\t\tError NSS: {nss}")
#        print(NssField.error_msg)
#        break
