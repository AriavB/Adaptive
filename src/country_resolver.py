from __future__ import annotations

from collections import OrderedDict
from pathlib import Path
from threading import RLock

import geoip2.database
from geoip2.errors import AddressNotFoundError


class CountryResolver:
    """Resolve client IPs via a GeoIP database using a bounded cache."""

    def __init__(self, database_path: str | Path, cache_size: int = 4096) -> None:
        if cache_size < 0:
            raise ValueError("cache_size must be non-negative")

        self._database_path = Path(database_path)
        self._reader = geoip2.database.Reader(str(self._database_path))
        self._cache_size = cache_size
        self._cache: OrderedDict[str, str] = OrderedDict()
        self._lock = RLock()
        self._closed = False

    def resolve(self, ip: str) -> str:
        """Return the ISO-like country name or ``Other`` if it cannot be resolved."""
        with self._lock:
            if self._closed:
                raise RuntimeError("CountryResolver is closed")

            cached = self._cache.get(ip)
            if cached is not None:
                self._cache.move_to_end(ip)
                return cached

            try:
                result = self._reader.country(ip)
                country = result.country.name or "Other"
            except (AddressNotFoundError, ValueError):
                country = "Other"
            except Exception:
                country = "Other"

            if self._cache_size:
                self._cache[ip] = country
                self._cache.move_to_end(ip)
                if len(self._cache) > self._cache_size:
                    self._cache.popitem(last=False)

            return country

    def close(self) -> None:
        """Close the GeoIP database handle and clear the cache."""
        with self._lock:
            if self._closed:
                return
            self._reader.close()
            self._closed = True
            self._cache.clear()

    def __enter__(self) -> "CountryResolver":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
