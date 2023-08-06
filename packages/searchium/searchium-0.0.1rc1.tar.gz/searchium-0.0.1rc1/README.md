## Clients of Searchium cloud platform
#### FVS - is fast vector search
##### get more info https://www.searchium.ai/

---
###### supported methods

- validate_allocation(self) -> bool
- get_loaded_dataset(self) -> List[LoadedDataset]:
- get_datasets -> List[Dataset]
- delete_dataset(dataset_id: str) -> bool
- load_dataset(self, dataset_id: str) -> bool
- unload_dataset(self, dataset_id: str) -> bool
- search(self, dataset_id: str, query: List[List[float]], topk: int = 5) -> SearchResponse
---

***example:***

***from searchium import fvs***

***client = fvs.get_client("your_allocation_id", "your_url")***

***dataset_id = 'your_dataset_id'***

***client.load_dataset(dataset_id)***

***client.search(dataset_id, query, 1)***

***client.unload_dataset(dataset_id)***

