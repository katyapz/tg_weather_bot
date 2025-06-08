import time
import aiohttp
from aiohttp import ClientError, ClientTimeout

class ApiInteractionClient:
    def __init__(self, api_key: str, cache_ttl: int = 300, timeout: int = 10):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.timeout = timeout  # Таймаут запроса

        self.api_cache: dict[str, tuple[float, dict]] = {}  # place -> (timestamp, data)
        self.cache_ttl = cache_ttl  # Время жизни кэша

    async def get_weather(self, place: str) -> dict:
        # Проверка кэша
        now = time.time()
        if place in self.api_cache:
            ts, data = self.api_cache[place]
            if now - ts < self.cache_ttl:
                return data

        try:
            timeout = ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                try:
                    async with session.get(
                        f"{self.base_url}/weather?q={place}&appid={self.api_key}"
                    ) as response:
                        data = await response.json()
                        
                        # Сохраняем в кэш
                        self.api_cache[place] = (now, data)
                        return data
                        
                except ClientError as e:
                    raise Exception(f"Failed to get data: {str(e)}")
                    
        except Exception as e:
            raise Exception(f"Unexpected error occurred: {str(e)}")
