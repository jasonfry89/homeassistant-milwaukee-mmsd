import logging
from typing import override

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, SHORT_NAME, API_NAME, SYSTEM_NAME
from .coordinator import MilwaukeeMMSDCoordinator, MilwaukeeMMSDConfigEntry

_LOGGER = logging.getLogger(__name__)

WATER_DROP_ALERT_DESCRIPTION = SensorEntityDescription(
    key="MMSD water drop alert",
    icon="mdi:water-alert",
    name="Water drop alert"
)


async def async_setup_entry(
        hass: HomeAssistant,
        config: MilwaukeeMMSDConfigEntry,
        async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    water_drop_alert_sensor = MilwaukeeMMSDWaterDropAlertSensor(config, WATER_DROP_ALERT_DESCRIPTION)
    async_add_entities([water_drop_alert_sensor])


class MilwaukeeMMSDWaterDropAlertSensor(CoordinatorEntity[MilwaukeeMMSDCoordinator], BinarySensorEntity):

    def __init__(
            self,
            config: MilwaukeeMMSDConfigEntry,
            entity_description: SensorEntityDescription):
        super().__init__(coordinator=config.runtime_data.coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, SYSTEM_NAME)},
            name=SYSTEM_NAME,
            manufacturer=SHORT_NAME,
            model=API_NAME,
        )

    @property
    @override
    def is_on(self) -> bool:
        return self.coordinator.data.water_drop_alert
