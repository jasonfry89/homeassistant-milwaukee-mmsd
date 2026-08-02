import logging
from typing import override

from milwaukee_mmsd_parser import MMSDFacility

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorEntityDescription
from homeassistant.const import UnitOfRatio, UnitOfVolume
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, SHORT_NAME, API_NAME
from .coordinator import MilwaukeeMMSDCoordinator, MilwaukeeMMSDConfigEntry

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = [
    SensorEntityDescription(
        key="current usage",
        device_class=SensorDeviceClass.VOLUME,
        native_unit_of_measurement=UnitOfVolume.GALLONS,
        icon="mdi:water-opacity",
        suggested_display_precision=0,
    ),
    SensorEntityDescription(
        key="maximum capacity",
        device_class=SensorDeviceClass.VOLUME,
        native_unit_of_measurement=UnitOfVolume.GALLONS,
        icon="mdi:water",
        suggested_display_precision=0,
    ),
    SensorEntityDescription(
        key="percent used",
        native_unit_of_measurement=UnitOfRatio.PERCENTAGE,
        icon="mdi:percent",
        suggested_display_precision=2,
    ),
]


async def async_setup_entry(
        hass: HomeAssistant,
        config: MilwaukeeMMSDConfigEntry,
        async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    coordinator = config.runtime_data.coordinator
    sensors = [
        MilwaukeeMMSDSensor(
            config,
            entity_description,
            facility.name,
        )
        for facility in coordinator.data.facilities
        for entity_description in SENSOR_TYPES
    ]
    async_add_entities(sensors)


class MilwaukeeMMSDSensor(CoordinatorEntity[MilwaukeeMMSDCoordinator], SensorEntity):

    def __init__(
            self,
            config: MilwaukeeMMSDConfigEntry,
            entity_description: SensorEntityDescription,
            facility_name: str):

        super().__init__(coordinator=config.runtime_data.coordinator)
        self.entity_description = entity_description
        self._attr_name = f"{facility_name} {entity_description.key}"
        self._attr_unique_id = self._attr_name
        self._facility_name = facility_name

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, f"{self._facility_name}")},
            name=f"{self._facility_name}",
            manufacturer=SHORT_NAME,
            model=API_NAME,
        )

    @property
    def _facility(self) -> MMSDFacility:
        facilities = [facility for facility in self.coordinator.data.facilities if facility.name == self._facility_name]
        if not facilities:
            raise Exception(f"_facility - Missing facility for {self._facility_name}")
        facility = facilities[0]
        if facility.current_million_gallons is None or facility.maximum_million_gallons is None:
            raise Exception(f"_facility - Facility does not have both current and maximum for {self._facility_name}")
        return facility

    @property
    @override
    def native_value(self) -> int | float | bool:
        if self.entity_description.key == "maximum capacity":
            return self._facility.maximum_million_gallons * 1_000_000
        elif self.entity_description.key == "current usage":
            return self._facility.current_million_gallons * 1_000_000
        elif self.entity_description.key == "percent used":
            return 100.0 * self._facility.current_million_gallons / self._facility.maximum_million_gallons
        else:
            raise Exception(f"native_value - Invalid key: {self.entity_description.key}")
