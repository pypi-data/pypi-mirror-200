import json
import logging
import os
from contextvars import ContextVar
from typing import Optional
from uuid import uuid4

import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler

# Keeps track of logger id in the Thread, across different modules.
_current_logger_id: ContextVar = ContextVar("Current logger id")


class LoggingManager:
    """Logging Manager

    A wrapper on Python built-in logging module. that handles GCP Cloud Logging
    According to importance there are 6 levels i.e Debug,Info,Warning
        ,Error,Exception,Critical
    """

    def __init__(
        self,
        name: str = __name__,
        logger_id: Optional[str] = None,
        gcp_env_variable: str = "GCP_SERVICE_KEY",
    ):
        """Initializing Logging Manager

        Args:
            name (str, optional): name of module/class which initialize
                logging. Defaults to __name__.
            level (int, optional): level to determine importance & up to what
                point capture logs. Defaults to logging.DEBUG.
            logger_id (str, optional): id of the logger.
            DEBUG : 10
            INFO : 20
            WARNING : 30
            ERROR : 40
            At time of initialization whatever the level is given below score
                levels will be ignored.
        """
        if logger_id:
            self._set_logger_id(logger_id)

        self._gcp_client = None
        try:
            if gcp_env_variable in os.environ:
                # Local testing
                self._gcp_client = (
                    google.cloud.logging.Client.from_service_account_json(
                        os.environ[gcp_env_variable]
                    )
                )
            else:
                self._gcp_client = google.cloud.logging.Client()
        except Exception:
            print("GCP Cloud Logging is not enabled.")

        self._logger = logging.getLogger(name)
        self._logger.handlers.clear()
        self._logger.setLevel(logging.INFO)

        if self._gcp_client:
            cloudlogging_formatter = logging.Formatter("%(name)s: %(message)s")
            cloud_handler = CloudLoggingHandler(self._gcp_client)
            cloud_handler.setFormatter(cloudlogging_formatter)
            self._logger.addHandler(cloud_handler)

        stream_handler = logging.StreamHandler()
        streamlog_format = "%(asctime)s [%(levelname)s] - %(name)s: %(message)s - JSON Payload: %(json_fields)s"  # noqa
        streamlog_formatter = logging.Formatter(fmt=streamlog_format)
        stream_handler.setFormatter(streamlog_formatter)
        self._logger.addHandler(stream_handler)

    @property
    def logger_id(self) -> str:
        """Get logger from Thread ContextVar if one exists or set it."""
        try:
            return _current_logger_id.get()
        except LookupError:
            self._set_logger_id(uuid4().hex)
            return _current_logger_id.get()

    def _set_logger_id(self, logger_id: str) -> None:
        _current_logger_id.set(logger_id)

    def _preprocess_json_payload(
        self, payload: Optional[dict]
    ) -> Optional[dict]:
        if not payload:
            return None

        payload["request_id"] = self.logger_id
        return payload

    def log(
        self,
        msg: str,
        level: int,
        json_params: Optional[dict] = None,
        skip_if_local: bool = False,
    ) -> None:
        if skip_if_local and not self._gcp_client:
            return

        json_params = self._preprocess_json_payload(json_params)
        if self._gcp_client:
            self._logger.log(level, msg, extra={"json_fields": json_params})
        else:
            self._logger.log(
                level,
                msg,
                extra={"json_fields": json.dumps(json_params, indent=2)},
            )

    def debug(
        self,
        msg: str,
        json_params: Optional[dict] = None,
        skip_if_local: bool = False,
    ) -> None:
        """Logs a debug message. Params: [msg] required"""
        self.log(
            msg,
            level=logging.DEBUG,
            json_params=json_params,
            skip_if_local=skip_if_local,
        )

    def info(
        self,
        msg: str,
        json_params: Optional[dict] = None,
        skip_if_local: bool = False,
    ) -> None:
        """Logs a info message. Params: [msg] required"""
        self.log(
            msg,
            level=logging.INFO,
            json_params=json_params,
            skip_if_local=skip_if_local,
        )

    def warning(
        self,
        msg: str,
        json_params: Optional[dict] = None,
        skip_if_local: bool = False,
    ) -> None:
        """Logs a warning message. Params: [msg] required"""
        self.log(
            msg,
            level=logging.WARNING,
            json_params=json_params,
            skip_if_local=skip_if_local,
        )

    def error(
        self,
        msg: str,
        json_params: Optional[dict] = None,
        skip_if_local: bool = False,
    ) -> None:
        """Logs an error message. Params: [msg] required"""
        self.log(
            msg,
            level=logging.ERROR,
            json_params=json_params,
            skip_if_local=skip_if_local,
        )

    def exception(
        self,
        msg: str,
        json_params: Optional[dict] = None,
        skip_if_local: bool = False,
    ) -> None:
        """Logs an exception. Params: [msg] required"""
        self.log(
            msg,
            level=logging.ERROR,
            json_params=json_params,
            skip_if_local=skip_if_local,
        )
