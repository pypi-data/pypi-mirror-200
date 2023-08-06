from . import Configuration, ApiClient
from .apis import (
    GroupsApi,
    DevicesApi,
    SitesApi,
    RoomsApi,
    PartsApi,
    PartFamiliesApi,
    LabelsApi,
    LogsApi,
    SchemaApi,
    ReservationsApi,
)
from .models import ReservationRequest, ReservationSessionSerializerReadOnly
from urllib3.util.retry import Retry
from typing import Optional
from threading import Thread
from time import sleep
from datetime import datetime, timezone
import logging

__all__ = [
    "HwMuxApi",
    "ReservationNotSatisfiedException",
    "SatisfiedReservationWatchdog",
]


class ReservationNotSatisfiedException(Exception):
    """
    Raised from HwMuxApicreate_reservation() when a reservation is not
    satisfied and raise_error_if_not_satisfied=True
    """


def ApiDecorator(apiClass):
    class NewApiClass(apiClass):
        @classmethod
        def list_all(cls, method, *args, **kwargs):
            return HwMuxApi.list_all(method, *args, **kwargs)

    return NewApiClass


class HwMuxApi:
    """
    HwMuxApi is a wrapper around the hwmux_client library that provides access to all public APIs.
    """

    def __init__(
        self,
        user_token: Optional[str] = None,
        server_url: Optional[str] = None,
        retries: Optional[Retry] = None,
    ):
        config = Configuration(host=server_url)
        if user_token is not None:
            config = Configuration(
                host=server_url,
                api_key={"tokenAuth": user_token},
                api_key_prefix={"tokenAuth": "Token"},
                discard_unknown_keys=True,
            )
        config.retries = retries
        self.client = ApiClient(config)
        self.apis = {}
        for api in [
            GroupsApi,
            DevicesApi,
            SitesApi,
            RoomsApi,
            PartsApi,
            PartFamiliesApi,
            LabelsApi,
            LogsApi,
            SchemaApi,
            ReservationsApi,
        ]:
            self.apis[api.__name__] = ApiDecorator(api)(self.client)

    @classmethod
    def list_all(cls, method, *args, **kwargs):
        all_items = []
        page = 0
        while True:
            page += 1
            kwargs["page"] = page
            items = method(*args, **kwargs)
            all_items.extend(items.results)
            if items.next is None:
                break
        return all_items

    def get_location_url(self, site, room, location_id):
        url = f"{self.client.configuration.host}/api/sites/{site}/rooms/{room}/locations/{location_id}/".replace(
            "https", "http"
        )
        return url

    @property
    def groups_api(self) -> GroupsApi:
        return self.apis["GroupsApi"]

    @property
    def devices_api(self) -> DevicesApi:
        return self.apis["DevicesApi"]

    @property
    def sites_api(self) -> SitesApi:
        return self.apis["SitesApi"]

    @property
    def rooms_api(self) -> RoomsApi:
        return self.apis["RoomsApi"]

    @property
    def parts_api(self) -> PartsApi:
        return self.apis["PartsApi"]

    @property
    def part_families_api(self) -> PartFamiliesApi:
        return self.apis["PartFamiliesApi"]

    @property
    def labels_api(self) -> LabelsApi:
        return self.apis["LabelsApi"]

    @property
    def logs_api(self) -> LogsApi:
        return self.apis["LogsApi"]

    @property
    def schema_api(self) -> SchemaApi:
        return self.apis["SchemaApi"]

    @property
    def reservations_api(self) -> ReservationsApi:
        return self.apis["ReservationsApi"]

    def create_reservation(
        self, request: ReservationRequest, raise_error_if_not_satisfied=False
    ):
        """
        Create a reservation and wait until it is satisfied.
        Args:
            request: reservation request
            raise_error_if_not_satisfied: if True, raise ReservationNotSatisfiedException if reservation is not satisfied

        Returns:
            SatisfiedReservationWatchdog object that periodically renews the
            reservation lease in a background thread and can be used to release the reservation.

        """
        logger = logging.getLogger(__name__)
        reservation: ReservationSessionSerializerReadOnly = (
            self.reservations_api.reservations_create(reservation_request=request)
        )
        while not reservation.is_satisfied:
            if raise_error_if_not_satisfied:
                self.reservations_api.reservations_cancel_update(reservation.id)
                raise ReservationNotSatisfiedException("Reservation not satisfied")
            interval = min(
                30,
                int(seconds_until_lease_expires(reservation) / 2),
            )
            logger.info(f"Reservation not satisfied, waiting {interval} seconds...")
            sleep(interval)
            reservation = self.reservations_api.reservations_update(reservation.id)
        return SatisfiedReservationWatchdog(self, reservation)


class SatisfiedReservationWatchdog:
    """
    A SatisfiedReservationWatchdog object is returned from HwMuxApi.create_reservation()
    It contains a background thread that periodically renews the reservation lease and a
    release() method that cancels the background thread and releases the reservation.
    """

    default_watchdog_max_interval = 30

    def __init__(
        self, hwmux_api: HwMuxApi, reservation: ReservationSessionSerializerReadOnly
    ):
        """
        Creates a new SatisfiedReservationWatchdog object and starts the background thread.
        Args:
            hwmux_api: instance of HwMuxApi
            reservation_id: reservation id
        """
        self.stop_watchdog = False
        self.reservation = reservation
        self.hwmux_api = hwmux_api
        self.watchdog_thread = Thread(target=self.watchdog_thread)
        self.watchdog_thread.daemon = True
        self.watchdog_thread.start()

    @property
    def reservation_id(self):
        return self.reservation.id

    def release(self):
        """
        Releases the reservation and stops the background thread.
        """
        self.stop_watchdog = True
        self.watchdog_thread.join()
        self.hwmux_api.reservations_api.reservations_release_update(self.reservation_id)

    def wait_for_watchdog_interval(self, interval: int):
        """
        Waits for the watchdog interval to expire or until stop_watchdog is set to True.
        """
        start = datetime.now()
        while (
            datetime.now() - start
        ).total_seconds() < interval and not self.stop_watchdog:
            sleep(0.1)

    def watchdog_thread(self):
        """
        Background thread that periodically renews the reservation lease.
        """
        logger = logging.getLogger(__name__)
        while not self.stop_watchdog:
            interval = min(
                self.default_watchdog_max_interval,
                int(seconds_until_lease_expires(self.reservation) / 2),
            )
            self.wait_for_watchdog_interval(interval)
            if not self.stop_watchdog:
                logger.debug("Renewing reservation lease")
                self.reservation = self.hwmux_api.reservations_api.reservations_update(
                    self.reservation_id
                )


def seconds_until_lease_expires(reservation: ReservationSessionSerializerReadOnly):
    return (reservation.t_lease_expires - datetime.now(timezone.utc)).total_seconds()
