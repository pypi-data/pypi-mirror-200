import logging.config
from datetime import datetime

import requests

from .consts import LOGGING_CONFIG, DEFAULT_TIMEOUT

logging.config.dictConfig(LOGGING_CONFIG)
LOGGER = logging.getLogger("cscwrapper")


class APIHandler:
    def __init__(
        self,
        host: str,
        headers: dict,
        logging: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        self._host = host
        self._headers = headers
        self.__logging = logging
        self.REQUEST_TIMEOUT = timeout  # Note: online searches take some time

    @property
    def host(self):
        return self._host

    def _send_request(self, method, payload=None, log_config: dict = None):
        if self.__logging:
            LOGGER.info("Sending [%s] API call to [%s]", method, self._host)

        log_entry = None

        if log_config:
            if (
                "model" not in log_config
                or "user" not in log_config
                or "timezone" not in log_config
            ):
                raise Exception("Invalid log dict")

            logging_model = log_config.pop("model")
            requested_by = log_config.pop("user")
            request_time = log_config.pop("timezone", datetime)

            log_entry = logging_model(
                requested_by=requested_by,
                request_url=f"{method}: {self._host}",
                request_headers=self._headers,
                request_body=payload,
                request_time=request_time.now(),
                **log_config,
            )

        try:

            response = requests.request(
                method,
                self._host,
                headers=self._headers,
                timeout=self.REQUEST_TIMEOUT,
                data=payload,
            )

            if self.__logging:
                LOGGER.info(
                    "Received [%s] response for [%s: %s]",
                    response.status_code,
                    method,
                    self._host,
                )

            if log_entry:
                log_entry.response_code = response.status_code
                log_entry.response_body = response.text
                log_entry.response_time = log_entry.request_time + response.elapsed
                log_entry.save()

            response.raise_for_status()

            response = response.text

            if self.__logging:
                LOGGER.info(
                    "CSC UCC Response for [%s: %s] -- [%s]",
                    method,
                    self._host,
                    response,
                )

            return response
        except requests.HTTPError as excp:
            if self.__logging:
                LOGGER.error(
                    "CSC UCC API Failed. Received [%s] response for [%s: %s]",
                    response.status_code,
                    method,
                    self._host,
                )

            raise Exception(
                f"Failed to get success response from CSC. Response: [{response.text}]"
            ) from excp
