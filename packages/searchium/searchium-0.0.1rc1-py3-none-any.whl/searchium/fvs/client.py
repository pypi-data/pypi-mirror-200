import requests
from pydantic.tools import parse_obj_as

from searchium.fvs.model import *


class ClientFVS(object):
    def __init__(self, allocation_id: str, url_searchium: str, port: int = 7760) -> None:
        self._allocation = allocation_id
        self._url_searchium = url_searchium
        self._port = port
        self._link = f"{self._url_searchium}:{self._port}/v1.0"
        self._headers = {'Content-Type': 'application/json', 'allocationToken': f'{self._allocation}'}

    def validate_allocation(self) -> bool:
        """
        Validate user allocation on cloud platform
        :return: bool
        """
        link = f"{self._link}/board/allocation/validate"
        body = {"allocationId": f"{self._allocation}"}
        get = requests.post(link, json=body)
        if get.status_code == 200:
            return True
        else:
            return False

    def get_loaded_dataset(self) -> List[LoadedDataset]:
        """
        Get list loaded datasets
        :return: List[LoadedDataset]
        """
        link = f"{self._link}/board/allocation/list"
        get = requests.get(link, headers=self._headers)
        if get.status_code == 200:
            loaded = get.json()['allocationsList'][f'{self._allocation}']['loadedDatasets']
            obj_as = parse_obj_as(List[LoadedDataset], loaded)
            return obj_as
        else:
            raise Exception(get.json())

    def get_datasets(self) -> List[Dataset]:
        """
        Get list imported datasets
        :return: List[Dataset]
        """
        link = f"{self._link}/dataset/list"
        get = requests.get(link, headers=self._headers)
        if get.status_code == 200:
            list_datasets = get.json()['datasetsList']
            obj_as = parse_obj_as(List[Dataset], list_datasets)
            return obj_as
        else:
            raise Exception(get.json())

    def delete_dataset(self, dataset_id: str) -> bool:
        """
        Delete dataset by dataset id
        :param dataset_id:
        :return: bool
        """
        link = f"{self._link}/dataset/remove/{dataset_id}"
        get = requests.delete(link, headers=self._headers)
        if get.status_code == 200:
            return True
        else:
            raise Exception(get.json())

    def load_dataset(self, dataset_id: str) -> bool:
        """
        load dataset by dataset id
        :param dataset_id: str
        :return: bool
        """
        link = f"{self._link}/dataset/load"
        body = {"allocationId": f"{self._allocation}", "datasetId": f"{dataset_id}", "normalize": True,
                "typicalNQueries": 1, "maxNQueries": 50, "hammingK": 3200}
        get = requests.post(link, json=body, headers=self._headers)
        if get.status_code == 200:
            return True
        else:
            raise Exception(get.json())

    def unload_dataset(self, dataset_id: str) -> bool:
        """
        unload dataset by dataset id
        :param dataset_id: str
        :return: bool
        """
        link = f"{self._link}/dataset/unload"
        body = {"allocationId": f"{self._allocation}", "datasetId": f"{dataset_id}"}
        get = requests.post(link, json=body, headers=self._headers)
        if get.status_code == 200:
            return True
        else:
            raise Exception(get.json())

    def search(self, dataset_id: str, query: List[List[float]], topk: int = 5) -> SearchResponse:
        """
        search query in dataset
        return result object SearchResponse
        where fields are:
        distance - distance
        indices - indices
        metadata - optional
        search - netto apu search time
        total - full search time FVS
        :return: search result
        """
        link = f"{self._link}/dataset/search"
        body = {"allocationId": f"{self._allocation}", "datasetId": f"{dataset_id}", "topk": topk,
                "queriesFilePath": query}
        get = requests.post(link, json=body, headers=self._headers)
        if get.status_code == 200:
            obj_as = parse_obj_as(SearchResponse, get.json())
            return obj_as.dict(exclude_none=True)
        else:
            raise Exception(get.json())

    def _train_dataset(self, dataset_id):
        # /dataset/train
        # {
        #     "datasetId": "",
        #     "trainType": "Regular"
        # }
        pass

    def _create_dataset(self) -> str:
        """
        :return: str dataset_id
        """
        pass

    def _add_chunk(self, dataset_id: str) -> None:
        pass

    def _check_connection(self) -> bool:
        # Alive
        # /alive
        pass


def get_client(allocation: str, url: str, port: int = 7760) -> ClientFVS:
    """
    Get client of FVS Searchium
    All these params as allocation & url you can receive
     on our cloud platform searchium.ai
    :param port: as default 7760
    :param allocation: str uuid
    :param url: str
    :return: client of FVS ClientFVS
    """
    return ClientFVS(allocation, url, port)
