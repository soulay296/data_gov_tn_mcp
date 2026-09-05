import httpx

from config import settings


class DataGovClient:
    def __init__(self) -> None:
        self.base_url = settings.DATAGOV_API_BASE_URL
        self.timeout = settings.REQUEST_TIMEOUT
        self.verify_ssl = settings.DATAGOV_VERIFY_SSL

    async def get(self, path: str, params: dict | None = None) -> dict:
        url = f"{self.base_url}{path}"
        try:
            async with httpx.AsyncClient(
                timeout=self.timeout, verify=self.verify_ssl
            ) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as exc:
            raise DataGovError(f"Erreur API data.gov.tn ({url}): {exc}") from exc


class DataGovError(Exception):
    """Erreur d'accès à l'API data.gov.tn."""


datagov_client = DataGovClient()
