import dataclasses
import datetime
import logging
import time
from typing import Any, Optional, cast

import requests

logger = logging.getLogger(__name__)


class AzureApiCall:
    def __init__(self, azure_requests, method, url):
        self.azure_requests = azure_requests
        self.method = method
        self.url = url

    def request(self, *args, **kwargs):
        return self.azure_requests.request(self.method, self.url, *args, **kwargs)


class AzureRequests:
    def __init__(
        self,
        pat: str,
        organization: str,
        project: Optional[str] = None,
        team: Optional[str] = None,
    ):
        self.auth = (pat, pat)
        self.organization = organization
        self.project = project
        self.team = team
        self.rate_info: Optional[RateLimit] = None

    def api(self, azure_url, **url_params):
        params = dict(
            organization=self.organization,
            project=self.project or "",
            team=self.team or "",
        )
        params.update(url_params)
        method, _, raw_url = azure_url.partition(" ")
        url = raw_url.format(**params)
        return AzureApiCall(self, method, url)

    def get(self, url: str, *args, **kwargs) -> Any:
        return self.request("get", url, *args, **kwargs)

    def post(self, url: str, *args, **kwargs) -> Any:
        return self.request("post", url, *args, **kwargs)

    def put(self, url: str, *args, **kwargs) -> Any:
        return self.request("put", url, *args, **kwargs)

    def patch(self, url: str, *args, **kwargs) -> Any:
        return self.request("patch", url, *args, **kwargs)

    def delete(self, url: str, *args, **kwargs) -> Any:
        return self.request("delete", url, *args, **kwargs)

    def request(self, method: str, url: str, *args, **kwargs) -> Any:
        kwargs.setdefault("headers", {})
        if method.lower() == "patch":
            kwargs["headers"]["Content-type"] = "application/json-patch+json"
        if method.lower() in ("post", "put"):
            kwargs["headers"]["Content-type"] = "application/json"

        url_params = {
            "organization": self.organization,
            "project": self.project,
            "team": self.team,
        }
        url_params.update(kwargs.pop("url_params", {}))
        for key, value in url_params.items():
            to_replace = str(value or "")
            url = url.replace("{" + key + "}", to_replace)

        kwargs["auth"] = self.auth

        if self.rate_info:
            if self.rate_info.remaining:
                waiting = max(0, 30 - self.rate_info.remaining)
            else:
                waiting = self.rate_info.retry_after
            if waiting:
                log_level = logging.WARNING
            else:
                log_level = logging.DEBUG
            logger.log(
                log_level,
                "Rate limit info: "
                + f"remaining={self.rate_info.remaining} "
                + f"delay={self.rate_info.delay:.2f} "
                + f"retry={self.rate_info.retry_after} "
                + f"limit={self.rate_info.limit} "
                + f"reset={self.rate_info.to_sleep.total_seconds()/60:.1f}min "
                + f"resource={self.rate_info.resource}. "
                + f"Waiting {waiting} sec.",
            )
            if waiting:
                time.sleep(waiting)
        response = requests.request(method, url, *args, **kwargs)
        if not response.ok:
            if response.status_code // 100 == 5:
                logger.warning(
                    f"Azure DevOps server error ({response.status_code}). Retrying later..."
                )
                time.sleep(15)
                return self.request(method, url, *args, **kwargs)
            logger.error("Azure DevOps API error: " + response.text)
            response.raise_for_status()
        if "X-RateLimit-Remaining" in response.headers:
            self.rate_info = RateLimit(
                resource=cast(str, response.headers.get("X-RateLimit-Resource")),
                delay=float(response.headers.get("X-RateLimit-Delay", "0")),
                remaining=int(cast(str, response.headers.get("X-RateLimit-Remaining"))),
                limit=int(cast(str, response.headers.get("X-RateLimit-Limit"))),
                reset=datetime.datetime.fromtimestamp(
                    int(cast(str, response.headers.get("X-RateLimit-Reset")))
                ),
                retry_after=int(response.headers.get("Retry-After", "0")),
            )
        else:
            self.rate_info = None
        return response.json()


@dataclasses.dataclass
class RateLimit:
    resource: str
    remaining: int
    delay: float
    retry_after: int
    limit: int
    reset: datetime.datetime

    @property
    def to_sleep(self) -> datetime.timedelta:
        return self.reset - datetime.datetime.now()
