from app.models.drugs import FilteredDrugRequest, FilteredDrugsResponse, DrugResponse
from app.models.mongo import MongoQuery
from app.services.mongo_service import MongoService
from typing import List, Dict, Any

class DrugsService:
    def __init__(self, mongo_service: MongoService):
        self.mongo_service = mongo_service

    def get_unique_drugs(self) -> List[DrugResponse]:
        query = MongoQuery(
            db="health",
            collection="drugs",
            aggregation=[
                {"$group": {
                    "_id": {
                        "searchTerm": "$searchTerm",
                        "concent": "$producto.concent",
                        "nombreFormaFarmaceutica": "$producto.nombreFormaFarmaceutica"
                    }}},
                {"$sort": {
                    "_id.searchTerm": 1,
                    "_id.concent": 1,
                    "_id.nombreFormaFarmaceutica": 1
                }},
                {"$project": {
                    "_id": 0,
                    "searchTerm": "$_id.searchTerm",
                    "concent": "$_id.concent",
                    "nombreFormaFarmaceutica": "$_id.nombreFormaFarmaceutica"
                }}
            ]
        )
        result = self.mongo_service.consult_mongo(query)
        return [DrugResponse(**drug, dropdown=self._create_dropdown(drug)) for drug in result.documents]

    def get_filtered_drugs(self, request: FilteredDrugRequest) -> FilteredDrugsResponse:
        match_stage = {
            '$match': {
                "searchTerm": request.selected_drug,
                "producto.concent": request.concent,
                "producto.nombreFormaFarmaceutica": request.nombreFormaFarmaceutica,
                "comercio.locacion.distrito": request.selected_distrito
            }
        }

        count_query = MongoQuery(
            db="health",
            collection="drugs",
            aggregation=[match_stage, {'$count': 'total'}]
        )
        count_result = self.mongo_service.consult_mongo(count_query)
        total_count = count_result.documents[0]['total'] if count_result.documents else 0

        results_query = MongoQuery(
            db="health",
            collection="drugs",
            aggregation=[
                match_stage,
                {'$sort': {'producto.precios.precio2': 1}},
                {'$limit': 3},
                {'$lookup': {
                    'from': 'pharmacies',
                    'localField': 'comercio.pharmacyId',
                    'foreignField': '_id',
                    'as': 'pharmacyInfo'
                }},
                {'$project': {
                    '_id': 1,
                    'nombreProducto': '$producto.nombreProducto',
                    'concent': '$producto.concent',
                    'nombreFormaFarmaceutica': '$producto.nombreFormaFarmaceutica',
                    'precio2': '$producto.precios.precio2',
                    'nombreComercial': {'$arrayElemAt': ['$pharmacyInfo.nombreComercial', 0]},
                    'direccion': {'$arrayElemAt': ['$pharmacyInfo.locacion.direccion', 0]},
                    'googleMaps_search_url': {'$arrayElemAt': ['$pharmacyInfo.google_maps.googleMaps_search_url', 0]},
                    'googleMapsUri': {'$arrayElemAt': ['$pharmacyInfo.google_maps.googleMapsUri', 0]}
                }}
            ]
        )
        results = self.mongo_service.consult_mongo(results_query)

        return FilteredDrugsResponse(totalCount=total_count, drugs=results.documents)

    def get_unique_districts(self) -> List[Dict[str, Any]]:
        query = MongoQuery(
            db="peru",
            collection="districts",
            aggregation=[
                {"$project": {"_id": 0, "descripcion": 1}},
                {"$sort": {"descripcion": 1}}
            ]
        )
        result = self.mongo_service.consult_mongo(query)
        return result.documents

    def _create_dropdown(self, drug):
        return f"{drug['searchTerm']} {drug['concent']} [{drug['nombreFormaFarmaceutica']}]"