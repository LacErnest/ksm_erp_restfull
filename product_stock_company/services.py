import requests
from rest_framework.renderers import JSONRenderer
import json
from django.apps import apps

def get_shops_with_positive_stock():
    """Permet d'obtenir la liste des articles magasins ayant un stock positif"""
    if apps.is_installed('store'):
        from store.models import ArticleStore
        return ArticleStore.objects.filter(physical_stock__gt=0, theoric_stock__gt=0)
    else:
        url = 'https://wiconet-company-api.herokuapp.com/company_partnership_types/' 
        headers =  {'content-type' : 'application/json'}
        try: 
            r = requests.post(url, auth=('wiconet', 'w1c0net@app'), data=json.dumps(data), headers=headers)
            print(repr(r))
        except Exception as err :
            print(repr(err))

def get_shops():
    """Permet d'obtenir la liste des boutiques"""
    if apps.is_installed('company'):
        from store.models import Structure
        return Structure.objects.filter(type_structure='STORE')
    else:
        url = 'https://wiconet-company-api.herokuapp.com/company_partnership_types/' 
        headers =  {'content-type' : 'application/json'}
        try: 
            r = requests.post(url, auth=('wiconet', 'w1c0net@app'), data=json.dumps(data), headers=headers)
            print(repr(r))
        except Exception as err :
            print(repr(err))

def get_shop_products():
    """Permet d'obtenir la liste des produits dans une boutique"""
    if apps.is_installed('store') and apps.is_installed('company'):
        from store.models import Structure
        return Structure.objects.filter(type_structure='STORE')
    else:
        url = 'https://wiconet-company-api.herokuapp.com/company_partnership_types/' 
        headers =  {'content-type' : 'application/json'}
        try: 
            r = requests.post(url, auth=('wiconet', 'w1c0net@app'), data=json.dumps(data), headers=headers)
            print(repr(r))
        except Exception as err :
            print(repr(err))