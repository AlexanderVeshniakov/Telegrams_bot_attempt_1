import requests
import json
from typing import List, Dict, Any

class NASA:
    def __init__(self, start_date: str, end_date: str, api_key: str) -> None:
        self.base_url = f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}'
        self.data = self.get_asteroids()

    def get_asteroids(self) -> Dict[str, Any]:
        url = self.base_url
        r = requests.get(url)
        data = json.loads(r.text)
        return data

    def get_hazardous_asteroids(self) -> List[Dict[str, Any]]:
        
        neo = self.data['near_earth_objects']
        hazardous_asteroids: List[Dict[str, Any]] = []

        for date in neo:
            for near in neo[date]:
                if near.get('is_potentially_hazardous_asteroid', False):
                    close_approach_data = near.get('close_approach_data', [{}])[0]
                    asteroid_info: Dict[str, Any] = {
                        'ID астероида': near.get('id', ''),
                        'Имя': near.get('name', ''),
                        'Предполагаемый диаметр (км)': near["estimated_diameter"]["kilometers"].get('estimated_diameter_max', ''),
                        'Потенциальная опасность': True,
                        'Скорость (км/с)': float(close_approach_data.get('relative_velocity', {}).get('kilometers_per_second', 0))
                    }
                    hazardous_asteroids.append(asteroid_info)
        return hazardous_asteroids