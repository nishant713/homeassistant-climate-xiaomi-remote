from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, DEFAULT_SLOT, DEFAULT_TIMEOUT
from .remote_handler import async_learn_command

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Xiaomi IR Climate UI", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("remote_entity_id"): str,
            }),
            description_placeholders={}
        )

class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            entity_id = self.config_entry.data["remote_entity_id"]
            await async_learn_command(
                self.hass,
                entity_id,
                user_input["slot"],
                user_input["timeout"]
            )
            return self.async_create_entry(title="Learned IR", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("label", default="Power"): str,
                vol.Optional("slot", default=DEFAULT_SLOT): int,
                vol.Optional("timeout", default=DEFAULT_TIMEOUT): int
            }),
            description_placeholders={
                "entity_id": self.config_entry.data.get("remote_entity_id", "unknown")
            }
        )
