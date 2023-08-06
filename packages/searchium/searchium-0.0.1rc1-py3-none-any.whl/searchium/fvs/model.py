from typing import List, Optional

from pydantic import BaseModel


class LoadedDataset(BaseModel):
    datasetId: str = None
    datasetNumOfRecords: int = None
    _hammingK: str = None
    _maxNQueries: str = None
    _neuralMatrixId: str = None
    _normalize: bool = None
    _rerankTopK: int = None
    searchType: str = None
    _typicalNQueries: int = None
    _inMemNumOfRecords: int
    _isLoaded: bool
    _pendingTransactionsInd: bool
    _removedIndexes: List
    _shiftMap: str


class EncodingDetails(BaseModel):
    binDatasetSizeInBytes: str = None
    binFilePath: str = None
    isActive: str = None
    nbits: str = None
    id: str = None


class Dataset(BaseModel):
    _datasetCopyFilePath: str = None
    _datasetFileType: str = None
    datasetName: str = None
    datasetStatus: str = None
    datasetType: str = None
    id: str = None
    _encodingDetails: List[EncodingDetails] = None


class SearchResponse(BaseModel):
    distance: List[List[float]] = None
    indices: List[List[int]] = None
    metadata: Optional[str] = None
    search: float
    total: float


class LoadedDatasets(LoadedDataset):
    __loaded_datasets: List[LoadedDataset] = None

    def get_loaded_datasets_list(self):
        return self.__loaded_datasets
