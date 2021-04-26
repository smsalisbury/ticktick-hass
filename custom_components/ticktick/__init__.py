"""The TickTick integration."""
from __future__ import annotations

import asyncio
from ticktick import api

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

from .services import register_services


def setup(hass: HomeAssistant, config):
    """Set up the TickTick integration."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up TickTick from a config entry."""

    client = api.TickTickClient(entry.data.get("email"), entry.data.get("password"))
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN][entry.entry_id] = client

    register_services(DOMAIN, hass, client)

    return True
