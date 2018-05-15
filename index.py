#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import math
import requests

#estrutura do arquivo CSV de resultado, separador ","
#ITEM_ID,DOMAIN_ID,MISSING_ATTRIBUTES_PI,MISSING_ATTRIBUTES_FT


def findnth(haystack, needle, n):
    parts = haystack.split(needle, n+1)
    if len(parts) <= n+1:
        return -1
    return len(haystack) - len(parts[-1]) - len(needle)

def makeRequest(seller_id):
	#strReq = 'http://catalog-quality.adminml.com/catalog_quality/status/topitems?v=3&seller_id=' + str(seller_id)
	strReq = 'http://catalog-quality.adminml.com/catalog_quality/status/topitems?v=3&seller_id=' + str(seller_id) + '&limit=10000&offset=1'
	result = requests.get(strReq)
	return result

def limpaStr(entrada):
	result = entrada.replace('[u', '')
	result = result.replace(']', '')
	result = result.replace("u'", "")
	result = result.replace("'", "")
	result = result.replace(",", ";")
	return result

def main():
	print 'Consulta de atributos de sellers'

	objFile = open('cust_ids.txt', 'r')
	objResult = open('items.csv', 'w')
	#cabecalho do arquivo de resultado
	objResult.write('ITEM_ID,DOMAIN_ID,MISSING_ATTRIBUTES_PI,MISSING_ATTRIBUTES_FT\n')

	qtdLida = 0

	# Para cada linha de arquivo de sellers
	for line in objFile:
		
		#line contem o seller_id
		line = line.replace('\n', '')

		# faz o request, pega os Items
		response = makeRequest(line)
		nos = response.json()

		if (not nos) or (len(nos)==0):
			continue

		objResult.write(line + '\n')

		# Itera nos Items
		for item in nos:

			item_id = str(item['item_id'])
			domain_id = str(item['domain_id'])
			pi = limpaStr(str(item['adoption_status']['pi']['missing_attributes']))
			ft = limpaStr(str(item['adoption_status']['ft']['missing_attributes']))

			objResult.write( item_id + ',' + domain_id + ',' + pi + ',' + ft + '\n')

		
		qtdLida += 1
		
	print 'Total de logs = ' + str(qtdLida)
	objFile.close()
	objResult.close()


if __name__ == "__main__":
    main()
