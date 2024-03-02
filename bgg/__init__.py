import httpx
import xmltodict

from typing import List, Optional


class Boardgame:
    def __init__(self, data: dict):
        self.data: dict = data

    @property
    def id(self) -> int:
        return int(self.data["@objectid"])
    
    @property
    def name(self) -> str:
        name = self.data["name"]
        if isinstance(name, dict):
            name = name.get("#text")
        return name

    @property
    def year(self) -> Optional[int]:
        if "yearpublished" in self.data:
            return int(self.data["yearpublished"])
    
    def __str__(self):
        return f"{self.name} ({self.year})"


class BGGClient:
    BASE_URL = "https://api.geekdo.com/xmlapi"

    def search(self, query: str) -> List[Boardgame]:
        url = f"{self.BASE_URL}/search?search={query}"
        result = self._get_dict(url)

        for data in result.get("boardgames", {}).get("boardgame", []):
            print(Boardgame(data))

    def get(self, id: int) -> Boardgame:
        ...

    def _get_dict(self, url: str) -> dict:
        response = httpx.get(url)
        return xmltodict.parse(response.text, process_namespaces=True)


if __name__ == "__main__":
    client = BGGClient()
    client.search("carca")