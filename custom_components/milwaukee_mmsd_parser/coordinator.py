from typing import override, List

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import logging
from homeassistant.core import HomeAssistant
from datetime import date, timedelta
from dataclasses import dataclass
from .const import DOMAIN
from homeassistant.config_entries import ConfigEntry
from milwaukee_mmsd_parser import get_facilities, MMSDFacilityInformation

_LOGGER = logging.getLogger(__name__)


@dataclass
class MilwaukeeMMSDData:
    facilities: List[MMSDFacilityInformation]

@dataclass
class MilwaukeeMMSDRuntimeData:
    coordinator: MilwaukeeMMSDCoordinator

type MilwaukeeMMSDConfigEntry = ConfigEntry[MilwaukeeMMSDRuntimeData]

class MilwaukeeMMSDCoordinator(DataUpdateCoordinator[MilwaukeeMMSDData]):

    def __init__(self, hass: HomeAssistant, config: ConfigEntry):
        super().__init__(
            hass,
            _LOGGER,
            config_entry=config,
            name=DOMAIN,
            update_interval=timedelta(minutes=10))

    @override
    async def _async_update_data(self) -> MilwaukeeMMSDData:
        try:
            _LOGGER.info(f"Gathering MMSD facilities")
            facilities = await get_facilities()
            return MilwaukeeMMSDData(facilities=facilities)
        except Exception as e:
            _LOGGER.exception("Failed to fetch data from Milwaukee MMSD")
            raise UpdateFailed(translation_domain=DOMAIN, translation_key="cannot_connect") from e
