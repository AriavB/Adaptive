from functools import lru_cache

import geoip2.database


class CountryResolver:

    def __init__(self, database_path: str):
        self._reader = geoip2.database.Reader(database_path)

    @lru_cache(maxsize=4096)
    def resolve(self, ip: str) -> str:
        try:
            response = self._reader.country(ip)
            return response.country.name or "Other"
        except Exception:
            return "Other"