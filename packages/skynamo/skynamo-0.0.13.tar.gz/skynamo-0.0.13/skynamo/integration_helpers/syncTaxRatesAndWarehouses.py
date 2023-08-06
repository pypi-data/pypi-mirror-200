from typing import List,Dict,Any
from skynamo.main.Reader import Reader
from skynamo.main.Writer import Writer
from skynamo.models.TaxRate import TaxRate
from skynamo.models.Warehouse import Warehouse

def syncErpTaxRatesWithSkynamo(erpTaxRates:List[Dict[str,Any]],taxIdField:str,taxNameField:str,rateField:str,taxRateIsActiveField:str='deleted_at',valueInTaxRateIsActiveFieldIndicatingActiveTaxRate:Any='',multiplyRateBy=1):
	erpTaxRateIdToSkynamoTaxRates=getDictOfErpTaxRateIdToSkynamoTaxRate()
	writer=Writer()
	for erpTaxRate in erpTaxRates:
		erpTaxRateId=erpTaxRate[taxIdField]
		name=erpTaxRate[taxNameField]+' ('+erpTaxRateId+')'
		newRate=float(erpTaxRate[rateField])*multiplyRateBy
		isActiveInErp=erpTaxRate[taxRateIsActiveField]==valueInTaxRateIsActiveFieldIndicatingActiveTaxRate
		if erpTaxRateId not in erpTaxRateIdToSkynamoTaxRates and isActiveInErp:# if tax rate is not in skynamo and is active in erp
			writer.addTaxRateCreate(name,newRate)
		else:# if tax rate is in skynamo
			skynamoTaxRate=erpTaxRateIdToSkynamoTaxRates[erpTaxRateId]
			if name!=skynamoTaxRate.name or newRate!=skynamoTaxRate.rate or isActiveInErp!=skynamoTaxRate.active:
				skynamoTaxRate.name=name
				skynamoTaxRate.rate=newRate
				skynamoTaxRate.active=isActiveInErp
				writer.addTaxRateUpdate(skynamoTaxRate,['name','rate','active'])
	errors=writer.apply()
	return errors

def syncErpWarehousesWithSkynamo(erpWarehouses:List[Dict[str,Any]],warehouseIdField:str,warehouseNameField:str,warehouseIsActiveField:str='deleted_at',valueInWarehouseIsActiveFieldIndicatingActiveWarehouse:Any=''):
	erpWarehouseIdToSkynamoWarehouse=getDictOfErpWarehouseIdToSkynamoWarehouse()
	writer=Writer()
	for erpWarehouse in erpWarehouses:
		erpWarehouseId=erpWarehouse[warehouseIdField]
		name=erpWarehouse[warehouseNameField]+' ('+erpWarehouseId+')'
		isActiveInErp=erpWarehouse[warehouseIsActiveField]==valueInWarehouseIsActiveFieldIndicatingActiveWarehouse
		if erpWarehouseId not in erpWarehouseIdToSkynamoWarehouse and isActiveInErp:# if warehouse is not in skynamo and is active in erp
			writer.addWarehouseCreate(name)
		else:
			skynamoWarehouse=erpWarehouseIdToSkynamoWarehouse[erpWarehouseId]
			if name!=skynamoWarehouse.name or isActiveInErp!=skynamoWarehouse.active:
				skynamoWarehouse.name=name
				skynamoWarehouse.active=isActiveInErp
				writer.addWarehouseUpdate(skynamoWarehouse,['name','active'])
	errors=writer.apply()
	return errors


def getDictOfErpTaxRateIdToSkynamoTaxRate():
	reader=Reader()
	result:Dict[str,TaxRate]={}
	existingTaxRates=reader.getTaxRates(forceRefresh=True)
	for taxRate in existingTaxRates:
		addTaxOrWarehouseObjectToResult(result,taxRate)
	return result

def getDictOfErpWarehouseIdToSkynamoWarehouse():
	reader=Reader()
	result:Dict[str,Warehouse]={}
	existingWarehouses=reader.getWarehouses(forceRefresh=True)
	for warehouse in existingWarehouses:
		addTaxOrWarehouseObjectToResult(result,warehouse)
	return result

def addTaxOrWarehouseObjectToResult(result:Dict[str,Any],object):
	firstBracketPos=object.name.find('(')
	lastBracketPos=object.name.find(')')
	if firstBracketPos!=-1 and lastBracketPos!=-1 and lastBracketPos>firstBracketPos:
		erpTaxRateId=object.name[firstBracketPos+1:lastBracketPos]
		result[erpTaxRateId]=object