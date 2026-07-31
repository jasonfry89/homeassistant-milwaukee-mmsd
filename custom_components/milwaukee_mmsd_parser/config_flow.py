from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult

from .const import DOMAIN

class EmptyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle an empty config flow for a zero-input integration."""

    VERSION = 1

    async def async_step_user(
            self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step where no input is required."""

        # Abort if the integration is already configured to prevent duplicates
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            # Create the entry immediately when the user clicks 'Submit'
            return self.async_create_entry(
                title="Milwaukee Metropolitan Sewerage District",
                data={}
            )

        # Show an empty form with no fields, just a 'Submit' button
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({})
        )