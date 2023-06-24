BUTTON: dict[str, dict[str, str]] = {
    "es": {
        "inline_location": "Enviar ubicación",
        "inline_forecast": "Eliminar datos",
    },
    "en": {"inline_location": "Send location"},
}

COMMAND: dict[str, dict[str, str]] = {
    "es": {
        "start": "🌤️ Puedo obtener información del clima basado en tu ubicación como 🌡️ temperatura aparente, ☁️ nubosidad, 🌧️ probabilidad de lluvia, etc.\n\n🛠️ Por ahora solo trabajo con tu ubicación actual, en actualizaciones futuras podré usar nombres de cuidades.\n\n📍 Por favor, comparta su ubicación actual para guardarla.",  # noqa
        "location_saved": "💾 Su ubicación ha sido guardada!\n\n✏️ Puede cambiarla con el comando /new_location.\n\n📓 Puede usar los comandos /forecast_hour y /forecast_day para obtener la información del clima por día o horas del día.",  # noqa
        "location_not_found": "⚠️ No se encontró una ubicación. Por favor, use el comando /start para agregar una nueva ubicación.",  # noqa
        "remove": "🔄 Estos datos han expirado, use el comando /forecast_hour o /forecast_day para obtener nuevos datos.",  # noqa
        "cancel": "❌ Operación cancelada, puede reanudarla usando el comando /start.",  # noqa
    },
    "en": {
        "start": "🌤️ I can get the weather info based on your location by day and hour like 🌡️ apparent temperature, ☁️ cloudcover, 🌧️ precipitation probability, etc.\n\n🛠️ For now it works with your location, later I will update to search by city.\n\n📍 Please send me your currect location to save it.",  # noqa
        "location_saved": "💾 This location has been saved!\n\n✏️ You can change your location in any moment.\n\n📓 Open the menu and use /forecast_hour to get data of all day or /forecast_day to get general data.",  # noqa
        "location_not_found": "❌ No location found. Please, use the command /start to add a new location.",  # noqa
    },
}

CONTENT: dict[str, dict[str, str]] = {
    "es": {
        "forecast_hour_head": "Para el día {} el clima por horas es:\n\n",
        "forecast_hour_body": "{} -> {} {}° ~ {}° - ☔️ {}%\n",
        "forecast_day": "Para el día {} el clima es:\n\nLa temperatura mínima es de {}° ~ {}° y máxima de {}° ~ {}°.\n\nCon un ☔️ {}% de probabilidad de lluvia.",  # noqa
    },
    "en": {},
}

CLOUD_STATUS: dict[str, str] = {
    "clear": "☀️",
    "partly_cloudy": "⛅",
    "cloudy": "☁️",
}
