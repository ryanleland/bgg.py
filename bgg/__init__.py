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
        return f"{self.id}: {self.name} ({self.year})"
    
    def __repr__(self):
        return f"{self.id}: {self.name} ({self.year})"


class BGGClient:
    BASE_URL = "https://api.geekdo.com/xmlapi2"

    TYPE_BOARDGAME = 'boardgame'
    TYPE_BOARDGAME_PERSON = 'boardgameperson'
    TYPE_BOARDGAME_COMPANY = 'boardgamecompany'
    TYPE_RPG = 'rpg'
    TYPE_RPG_PERSON = 'rpgperson'
    TYPE_RPG_COMPANY = 'rpgcompany'
    TYPE_VIDEOGAME = 'videogame'
    TYPE_VIDEOGAME_COMPANY = 'videogamecompany'

    TYPES = [
        TYPE_BOARDGAME,
        TYPE_BOARDGAME_PERSON,
        TYPE_BOARDGAME_COMPANY,
        TYPE_RPG,
        TYPE_RPG_PERSON,
        TYPE_RPG_COMPANY,
        TYPE_VIDEOGAME,
        TYPE_VIDEOGAME_COMPANY
    ]

    def search(self, query: str, types: List[str] = None) -> List[Boardgame]:
        url = f"{self.BASE_URL}/search?query={query}"
        
        if types:
            url += f"&type={",".join(types)}"

        result = self._get_dict(url)

        for data in result.get("boardgames", {}).get("boardgame", []):
            yield Boardgame(data)

    def search_boardgame(self, query: str) -> List[Boardgame]:
        return self.search(query, types=[self.TYPE_BOARDGAME])

    def get(self, id: int) -> Boardgame:
        url = f"{self.BASE_URL}/thing?id={id}"
        result = self._get_dict(url)

        print(result)

    def _get_dict(self, url: str) -> dict:
        response = httpx.get(url)
        return xmltodict.parse(response.text, process_namespaces=True)
