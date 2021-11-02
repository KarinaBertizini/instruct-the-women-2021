import requests
import json
 
def version_exists(package_name, version):
   
     
#Variável ‘consulta’ vai receber o valor da requisição da API https://pypi.org/pypi/json
    consulta = requests.get(f"https://pypi.org/pypi/{package_name}/{version}/json")
     #response = r.json()
 
#O if vai receber o valor  da ‘consulta’ para retornar o código de status.  Se ele retornar
# 200 quer dizer que o servidor existe, caso contrário não
    if consulta.status_code == 200:
        return True
    else:
        return False
 
 
 
def latest_version(package_name):
 
 
#A request.get chamar a API e salva o valor em ‘achar’
    achar = requests.get(f"https://pypi.org/pypi/{package_name}/json")
 
#No if ela compara o valor em ‘achar’  com 404 e se ela for igual a 404 irá retornar
# ‘None’ que está vazio o que irá encerrar o processo
    if achar.status_code == 404:
        return None
 
#se ele der diferente ele vai retornar os valores das chaves em uma lista a última versão
    else:
        achar = achar.json()
        return achar['info']['version']