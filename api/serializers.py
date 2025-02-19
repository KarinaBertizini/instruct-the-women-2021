from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import PackageRelease, Project
from .pypi import version_exists, latest_version
import json
from rest_framework.renderers import JSONRenderer


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageRelease
        fields = ["name", "version"]
        extra_kwargs = {"version": {"required": False}}

#A função validate irá receber a ‘version’ que irá validar as os valores para achar
# a última versão para apresentar na pypi.py
    def validate(self, data):
  
        found = False
        for i in data:
            if i == 'version':
                pack_ver = data[i]
                found = True

        if found == True:
            v_exist = version_exists(data["name"], pack_ver)
            if v_exist == True:
                return data
            else:
                raise serializers.ValidationError({"error": "One or more packages doesn't exist"})
        else:
            last = latest_version(data["name"])
            if last == None:
                raise serializers.ValidationError({"error": "One or more packages doesn't exist"})
            else:
                data['version'] = last
                return data

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "packages"]

    packages = PackageSerializer(many=True)

#A função create irá criar um projeto de acordo coma a configuração dentro do
# models.py que pede um nome que é criado no ‘projeto’ os valores que estão
# chegando vem da função anterior e o ‘packages’ que pode receber mais de um valor
    def create(self, validated_data):        
        
        packages = validated_data["packages"]
        projeto = Project.objects.create(name=validated_data["name"])       
        dic_pack = {}

#O ‘leng_pack’ irá receber o len(packages) que dá o tamanho do package que pode ser um ou mais        
        leng_pack = len(packages)
        i = 0

#O ‘while’ irá funcionar enquanto o leng_pack for menor que o contador que é ‘i’. O if ira comparar 
# o 'name' e a 'version' com a biblioteca 'dic_pack.item' e se eles forem iguais seram deletados.
# Se o if for falso, ele mandara os dados para o else e a adicionar na api  
        while i < leng_pack:
            if (packages[i]['name'], packages[i]['version']) in dic_pack.items():
                projeto.delete()
                raise serializers.ValidationError("Pacote com o mesmo nome")
            else:
                package = PackageRelease.objects.create(name=packages[i]['name'], version=packages[i]['version'], project=projeto)
                dic_pack[packages[i]['name']] = packages[i]['version']
                i += 1
        
        projeto.save()
        #print(packages[0]['version'])
        #[{'name': 'Django', 'version': '3.2.8'}, {'name': graphene, 'version': 2}]

        return projeto