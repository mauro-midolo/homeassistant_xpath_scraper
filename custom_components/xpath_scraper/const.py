DOMAIN = "xpath_scraper"

SENSOR = "sensor"
PLATFORMS = [SENSOR]

#Configuration 
CONF_ALIAS_VAR="xpath_scraper_name"
CONF_URL_VAR="xpath_scraper_url"
CONF_SLL_CHECK_VAR="xpath_scraper_ssl_check"
CONF_XPATH_VAR="xpath_scraper_xpath"
CONF_CLEAN_VAR="xpath_scraper_clean_check"
CONF_UNIT_OF_MEASUREMENT_VAR="xpath_scraper_unit_of_measurement"

#Update Inteval
CONF_SCAN_INTERVAL = "scan_interval"
DEFAULT_SCAN_INTERVAL = 60

from homeassistant.const import (
    UnitOfEnergy,
    UnitOfVolume,
    CURRENCY_EURO,
    CURRENCY_DOLLAR
)
from homeassistant.components.sensor import SensorDeviceClass
# Dizionario con le informazioni per diverse unità di misura
units = {
    "None": {
        "device_class": None, 
        "unit": None
    },
    "$": {
        "device_class": SensorDeviceClass.MONETARY, 
        "unit": CURRENCY_DOLLAR
    },
    "€": {
        "device_class": SensorDeviceClass.MONETARY,
        "unit": CURRENCY_EURO
    },
    "€/L": {
        "device_class": SensorDeviceClass.MONETARY,
        "unit": f"{CURRENCY_EURO}/{UnitOfVolume.LITERS}"
    },
    "$/gal": {
        "device_class": SensorDeviceClass.MONETARY,
        "unit": f"{CURRENCY_DOLLAR}/{UnitOfVolume.GALLONS}",
    },
    "L": {
        "device_class": SensorDeviceClass.VOLUME,
        "unit": UnitOfVolume.LITERS
    },
    "kWh": {
        "device_class": SensorDeviceClass.ENERGY,
        "unit": UnitOfEnergy.KILO_WATT_HOUR
    }
}