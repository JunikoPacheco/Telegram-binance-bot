import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from binance.client import Client
import logging

# Configuración de logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Claves de la API de Binance
BINANCE_API_KEY = 'tu_binance_api_key'
BINANCE_API_SECRET = 'tu_binance_api_secret'

# Token de Telegram (lo obtuviste de BotFather)
TELEGRAM_TOKEN = 'tu_telegram_bot_token'

# Inicializa el cliente de Binance
binance_client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

# Función que verifica el precio
def verificar_precio(update: Update, context: CallbackContext):
    try:
        # Extraer el par y el precio objetivo del mensaje
        par = context.args[0].upper()
        precio_objetivo = float(context.args[1])

        # Obtener el precio actual de Binance
        ticker = binance_client.get_symbol_ticker(symbol=par)
        precio_actual = float(ticker['price'])

        # Verificar si el precio actual alcanza el objetivo
        if precio_actual >= precio_objetivo:
            mensaje = f"Alerta: {par} ha alcanzado el precio objetivo de {precio_objetivo}. Precio actual: {precio_actual}."
        else:
            mensaje = f"{par} está a {precio_actual}, aún no alcanza el precio objetivo de {precio_objetivo}."

        update.message.reply_text(mensaje)
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

# Función que inicia el bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text("¡Hola! Usa el comando /alertar para configurar una alerta de precio. Ejemplo: /alertar BTCUSDT 35000")

# Función principal para configurar el bot de Telegram
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Comandos del bot
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("alertar", verificar_precio))

    # Comienza a escuchar los mensajes
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
