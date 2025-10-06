import asyncio
import base64
import time
from typing import Optional

import httpx


class SpotifyAuthService:
    """Manages an app-level Spotify access token with background refresh."""

    def __init__(self, client_id: str, client_secret: str) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._access_token: Optional[str] = None
        self._expires_at_epoch: float = 0.0
        self._refresh_task: Optional[asyncio.Task] = None
        self._lock = asyncio.Lock()
        self._stop_event = asyncio.Event()

    @property
    def access_token(self) -> Optional[str]:
        return self._access_token

    async def start(self) -> None:
        """Start background refresh loop."""
        # Ensure any previous loop is stopped
        await self.stop()
        self._stop_event = asyncio.Event()
        self._refresh_task = asyncio.create_task(self._run_refresh_loop())

    async def stop(self) -> None:
        """Stop background refresh loop."""
        if self._refresh_task and not self._refresh_task.done():
            self._stop_event.set()
            self._refresh_task.cancel()
            try:
                await self._refresh_task
            except asyncio.CancelledError:
                pass
        self._refresh_task = None

    async def _run_refresh_loop(self) -> None:
        """Fetch token immediately, then refresh before expiry in a loop."""
        try:
            # Fetch immediately on startup
            await self._fetch_and_store_token()
            while not self._stop_event.is_set():
                # Compute sleep until refresh (60s buffer)
                now = time.time()
                refresh_in = max(5.0, self._expires_at_epoch - now - 60.0)
                try:
                    await asyncio.wait_for(self._stop_event.wait(), timeout=refresh_in)
                    # If stop event set, break
                    if self._stop_event.is_set():
                        break
                except asyncio.TimeoutError:
                    # Timeout means it's time to refresh
                    pass
                await self._fetch_and_store_token()
        except asyncio.CancelledError:
            # Normal shutdown path
            raise

    async def _fetch_and_store_token(self) -> None:
        """Fetch a new client-credentials token and store it."""
        async with self._lock:
            auth_url = "https://accounts.spotify.com/api/token"
            basic = base64.b64encode(f"{self._client_id}:{self._client_secret}".encode()).decode()
            headers = {
                "Authorization": f"Basic {basic}",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            data = {"grant_type": "client_credentials"}
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(auth_url, headers=headers, data=data)
                resp.raise_for_status()
                payload = resp.json()
                self._access_token = payload.get("access_token")
                expires_in = float(payload.get("expires_in", 3600))
                self._expires_at_epoch = time.time() + expires_in


# Singleton holder to be initialized in app startup
spotify_auth_service: Optional[SpotifyAuthService] = None


