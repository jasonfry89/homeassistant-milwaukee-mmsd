"""Milwaukee Metropolitan Sewerage District integration."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN
from homeassistant.const import Platform
from .coordinator import MilwaukeeMMSDConfigEntry, MilwaukeeMMSDCoordinator, MilwaukeeMMSDRuntimeData

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.SENSOR
]

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True


async def async_setup_entry(hass: HomeAssistant, entry: MilwaukeeMMSDConfigEntry) -> bool:
    coordinator = MilwaukeeMMSDCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = MilwaukeeMMSDRuntimeData(coordinator)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True
