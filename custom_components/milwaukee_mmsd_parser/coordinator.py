import logging
from dataclasses import dataclass
from datetime import timedelta
from typing import override

from milwaukee_mmsd_parser import get_mmsd_information, MMSDInformation

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


@dataclass
class MilwaukeeMMSDRuntimeData:
    coordinator: MilwaukeeMMSDCoordinator


type MilwaukeeMMSDConfigEntry = ConfigEntry[MilwaukeeMMSDRuntimeData]


class MilwaukeeMMSDCoordinator(DataUpdateCoordinator[MMSDInformation]):

    def __init__(self, hass: HomeAssistant, config: ConfigEntry):
        super().__init__(
            hass,
            _LOGGER,
            config_entry=config,
            name=DOMAIN,
            update_interval=timedelta(minutes=10))

    @override
    async def _async_update_data(self) -> MMSDInformation:
        try:
            return await get_mmsd_information()
        except Exception as e:
            _LOGGER.exception("Failed to fetch data from Milwaukee MMSD")
            raise UpdateFailed(translation_domain=DOMAIN, translation_key="cannot_connect") from e
