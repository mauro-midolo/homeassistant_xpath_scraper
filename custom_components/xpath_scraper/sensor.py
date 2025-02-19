import logging
import asyncio
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorEntity
from .http.httpxpathclient import HttpXpathClient
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .sensorlist import sensors_binary
from homeassistant.helpers.update_coordinator import CoordinatorEntity

_LOGGER = logging.getLogger(__name__)
from .const import (
    CONF_ALIAS_VAR,
    CONF_CLEAN_VAR,
    CONF_SCAN_INTERVAL,
    CONF_SLL_CHECK_VAR,
    CONF_UNIT_OF_MEASUREMENT_VAR,
    CONF_XPATH_VAR,
    CONF_URL_VAR,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    units
)


class XPathScraperDataCoordinator(DataUpdateCoordinator):
    """Class to manage fetching WebServer data."""

    def __init__(self, hass, hostname, update_interval, ssl_checker, xpath, clean_checker, unit_of_measure):
        """Initialize the coordinator."""
        super().__init__(hass, _LOGGER, name=hostname, update_interval=update_interval)
        self._hostname = hostname
        self._ssl_checker = ssl_checker
        self._xpath = xpath
        self._clean_checker = clean_checker
        self._unit_of_measure = unit_of_measure
        

    async def _async_update_data(self):
        http_xpath_client: HttpXpathClient = HttpXpathClient()
        return await asyncio.to_thread(http_xpath_client.get_request, self._hostname, self._xpath, self._ssl_checker, self._clean_checker)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    webserver_url = entry.data.get(CONF_URL_VAR, "")
    xpath = entry.data.get(CONF_XPATH_VAR, "")
    if entry.options.get(CONF_SCAN_INTERVAL):
        update_interval = timedelta(seconds=entry.options[CONF_SCAN_INTERVAL])
    else:
        update_interval = timedelta(seconds=DEFAULT_SCAN_INTERVAL)
    ssl_checker = entry.data.get(CONF_SLL_CHECK_VAR, True)
    clean_checker = entry.data.get(CONF_CLEAN_VAR, False)
    unit_of_measure = entry.data.get(CONF_UNIT_OF_MEASUREMENT_VAR, None)
    coordinator = XPathScraperDataCoordinator(
        hass, webserver_url, update_interval, ssl_checker, xpath, clean_checker, unit_of_measure
    )
    await coordinator.async_config_entry_first_refresh()
    for sensor_name in sensors_binary:
        async_add_entities(
            [XPathScraperSensor(entry, sensor_name, coordinator)], True
        )


class XPathScraperEntity(CoordinatorEntity):
    def __init__(
        self,
        entry: ConfigEntry,
        sensor_name,
        coordinator: XPathScraperDataCoordinator,
    ):
        super().__init__(coordinator)
        self._entry = entry
        self._sensor_name = sensor_name

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{self._entry.data.get(CONF_ALIAS_VAR)}-{self._sensor_name}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._entry.data.get(CONF_ALIAS_VAR)}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data._data[self._sensor_name]

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return units[self.coordinator._unit_of_measure]["unit"]

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return units[self.coordinator._unit_of_measure]["device_class"]

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            name=self._entry.data.get(CONF_URL_VAR),
            identifiers={(DOMAIN, self._entry.data.get(CONF_URL_VAR))},
        )


class XPathScraperSensor(XPathScraperEntity, SensorEntity):
    """Representation of a WebServer Status sensor."""