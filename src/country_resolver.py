from __future__ import annotations

from functools import lru_cache

import geoip2.database


class CountryResolver:
    def __init__(self, database_path: str, cache_size: int = 4096):
        self._reader = geoip2.database.Reader(database_path)
        self._cache_size = cache_size

    @lru_cache(maxsize=4096)
    def resolve(self, ip: str) -> str:
        try:
            response = self._reader.country(ip)
        except geoip2.Error:
            return "Other"

        return response.country.name or "Other"
