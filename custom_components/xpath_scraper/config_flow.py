import voluptuous as vol
from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv
from lxml import etree
from .const import (
    CONF_UNIT_OF_MEASUREMENT_VAR,
    DOMAIN,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    CONF_ALIAS_VAR,
    CONF_URL_VAR,
    CONF_SLL_CHECK_VAR,
    CONF_XPATH_VAR,
    CONF_CLEAN_VAR
)

def is_valid_xpath(xpath):
    try:
        etree.XPath(xpath)  # Prova a creare un oggetto XPath
        return True
    except (etree.XMLSyntaxError, etree.XPathEvalError):
        return False

class XPathScraperConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    async def async_step_user(self, user_input=None):
        self._errors = {}
        if user_input is not None:
            # Controlla l'URL
            if not vol.Url()(user_input[CONF_URL_VAR]):
                self._errors["base"] = "invalid_url"
                return await self._show_config_form(user_input)

            # Controlla l'XPath
            if not is_valid_xpath(user_input[CONF_XPATH_VAR]):
                self._errors["base"] = "invalid_xpath"
                return await self._show_config_form(user_input)

            return self.async_create_entry(
                title=user_input[CONF_ALIAS_VAR],
                data={
                    CONF_ALIAS_VAR: user_input[CONF_ALIAS_VAR],
                    CONF_URL_VAR: user_input[CONF_URL_VAR],
                    CONF_SLL_CHECK_VAR: user_input[CONF_SLL_CHECK_VAR],
                    CONF_XPATH_VAR: user_input[CONF_XPATH_VAR],
                    CONF_CLEAN_VAR:user_input[CONF_CLEAN_VAR],
                    CONF_UNIT_OF_MEASUREMENT_VAR:user_input[CONF_UNIT_OF_MEASUREMENT_VAR]
                },
            )

        # Show the form to the user
        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input):
        unit_choices = [
        ("None","None"),
        ("€", "EUR"), 
        ("$", "USD"),
        ("€/L", "EUR/l"), 
        ("$/gal", "$/gal"),
        ("L", "Litre"),
        ("kWh", "kWh"),  
    ]
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_ALIAS_VAR, default=""): str,
                    vol.Required(CONF_URL_VAR, default=""): str,
                    vol.Required(CONF_SLL_CHECK_VAR, default=True): bool,
                    vol.Required(CONF_XPATH_VAR, default=""): str,
                    vol.Required(CONF_CLEAN_VAR, default=False): bool,
                    vol.Required(CONF_UNIT_OF_MEASUREMENT_VAR, default="None"): vol.In([unit[0] for unit in unit_choices]),

                }
            ),
            errors=self._errors,
        )
    @staticmethod
    def async_get_options_flow(config_entry):
        return XPathScraperOptionsFlow(config_entry)

class XPathScraperOptionsFlow(config_entries.OptionsFlow):

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Recupera il valore corrente di scan_interval, oppure usa il default
        current_interval = self.config_entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        schema = vol.Schema({
            vol.Optional(CONF_SCAN_INTERVAL, default=current_interval): cv.positive_int
        })
        return self.async_show_form(step_id="init", data_schema=schema)