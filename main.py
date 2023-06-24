import logging
import os
from datetime import datetime

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    Update,
)
from telegram.error import TelegramError
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from api.api import weather_daily, weather_hourly
from utils.constants import BUTTON, CLOUD_STATUS, COMMAND, CONTENT

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

LOCATION = 0


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Start the bot, save user language and request current location.
    """

    assert context.user_data is not None
    assert update.effective_chat is not None
    assert update.effective_user is not None

    keyboard = [
        [
            KeyboardButton(
                text=BUTTON["es"]["inline_location"], request_location=True
            )
        ]
    ]

    try:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=COMMAND["es"]["start"],
            reply_markup=ReplyKeyboardMarkup(
                keyboard=keyboard, one_time_keyboard=True, resize_keyboard=True
            ),
        )
    except TelegramError as e:
        logging.error(e.message)
    else:
        return LOCATION


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Set the attached location to conversation user data.
    """

    assert context.user_data is not None
    assert update.effective_chat is not None
    assert update.effective_message is not None
    assert update.effective_message.location is not None

    context.user_data["location"] = {
        "latitude": update.effective_message.location.latitude,
        "longitude": update.effective_message.location.longitude,
    }

    try:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=COMMAND["es"]["location_saved"],
        )
    except TelegramError as e:
        logging.error(e.message)
    else:
        return ConversationHandler.END


async def forecast_hour(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Weather information by hour.
    """

    assert update.effective_chat is not None
    assert context.user_data is not None

    if "location" not in context.user_data:
        await location_not_found(update, context)

    weather_report = weather_hourly(
        lat=context.user_data["location"]["latitude"],
        lon=context.user_data["location"]["longitude"],
    )
    content = CONTENT["es"]["forecast_hour_head"].format(
        datetime.now().strftime("%d/%m/%Y")
    )

    for hour in range(len(weather_report.hourly.time)):
        time = datetime.strptime(
            weather_report.hourly.time[hour], "%Y-%m-%dT%H:%M"
        )
        temp = weather_report.hourly.temperature_2m[hour]
        app_temp = weather_report.hourly.apparent_temperature[hour]
        prec_prob = int(weather_report.hourly.precipitation_probability[hour])
        cloudcover = int(weather_report.hourly.cloudcover[hour])
        cloudcover_emoji = CLOUD_STATUS[
            "clear"
            if cloudcover <= 33
            else ("partly_cloudy" if cloudcover <= 66 else "cloudy")
        ]

        content += CONTENT["es"]["forecast_hour_body"].format(
            time.strftime("%H:%M"), cloudcover_emoji, temp, app_temp, prec_prob
        )

    keyboard = [
        [
            InlineKeyboardButton(
                BUTTON["es"]["inline_forecast"], callback_data=0
            )
        ]
    ]

    try:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=content,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    except TelegramError as e:
        logging.error(e.message)


async def forecast_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Daily forecast location based weather data.
    """

    assert update.effective_chat is not None
    assert context.user_data is not None

    if "location" not in context.user_data:
        await location_not_found(update, context)

    weather_report = weather_daily(
        lat=context.user_data["location"]["latitude"],
        lon=context.user_data["location"]["longitude"],
    )

    temp_min = weather_report.daily.temperature_2m_min[0]
    temp_max = weather_report.daily.temperature_2m_max[0]
    app_temp_min = weather_report.daily.apparent_temperature_min[0]
    app_temp_max = weather_report.daily.apparent_temperature_max[0]
    # uv_index_max = weather_report.daily.uv_index_max[0]
    # uv_index_clear_max = weather_report.daily.uv_index_clear_sky_max[0]
    # prec_hours = weather_report.daily.precipitation_hours[0]
    prec_prob_max = weather_report.daily.precipitation_probability_max[0]

    content = CONTENT["es"]["forecast_day"].format(
        datetime.now().strftime("%d/%m/%Y"),
        temp_min,
        app_temp_min,
        temp_max,
        app_temp_max,
        int(prec_prob_max),
    )
    keyboard = [
        [
            InlineKeyboardButton(
                BUTTON["es"]["inline_forecast"], callback_data=0
            )
        ]
    ]

    try:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=content,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    except TelegramError as e:
        logging.error(e.message)


async def location_not_found(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    assert update.effective_chat is not None

    try:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=COMMAND["es"]["location_not_found"],
        )
    except TelegramError as e:
        logging.error(e.message)
    else:
        return


async def remove_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    assert query is not None

    try:
        await query.answer()
        await query.edit_message_text(text=COMMAND["es"]["remove"])
    except TelegramError as e:
        logging.error(e.message)
    else:
        return


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.message is not None

    try:
        await update.message.reply_text(text=COMMAND["es"]["cancel"])
    except TelegramError as e:
        logging.error(e.message)
    else:
        return ConversationHandler.END


if __name__ == "__main__":
    app = ApplicationBuilder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()

    app.add_handlers(
        [
            ConversationHandler(
                entry_points=[CommandHandler("start", start)],
                states={
                    LOCATION: [MessageHandler(filters.LOCATION, location)]
                },
                fallbacks=[CommandHandler("cancel", cancel)],
            ),
            CommandHandler("forecast_hour", forecast_hour),
            CommandHandler("forecast_day", forecast_day),
            CallbackQueryHandler(remove_button),
        ]
    )

    app.run_polling()
