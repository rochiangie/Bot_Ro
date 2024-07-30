from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import random
import requests

# Funciones para los comandos
def start(update: Update, context: CallbackContext) -> None:
    # Creación del menú inline
    keyboard = [
        [InlineKeyboardButton("Opción 1", callback_data='1')],
        [InlineKeyboardButton("Opción 2", callback_data='2')],
        [InlineKeyboardButton("Opción 3", callback_data='3')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Selecciona una opción:', reply_markup=reply_markup)

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Aquí están los comandos disponibles: /start, /help, /saludar, /nombre, /chiste, /piropo')

def saludar(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('¡Hola! ¿Cómo estás?')

def pedir_nombre(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('¿Cuál es tu nombre?')
    context.user_data['esperando_nombre'] = True

def guardar_nombre(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('esperando_nombre'):
        nombre = update.message.text
        context.user_data['nombre'] = nombre
        context.user_data['esperando_nombre'] = False
        context.user_data['esperando_edad'] = True
        update.message.reply_text(f'¡Encantado de conocerte, {nombre}! ¿Cuántos años tienes?')
    elif context.user_data.get('esperando_edad'):
        edad = update.message.text
        context.user_data['edad'] = edad
        context.user_data['esperando_edad'] = False
        nombre = context.user_data.get('nombre', 'amigx')
        update.message.reply_text(f'¡Gracias, {nombre}! Ahora sé que tienes {edad} años.')
    else:
        responder_mensaje(update, context)

def responder_mensaje(update: Update, context: CallbackContext) -> None:
    texto = update.message.text.lower()
    nombre = context.user_data.get('nombre', 'amigx')
    
    # Lista de palabras clave para la misma respuesta
    saludos = ["hola", "holis", "buenas", "buenass", "holisss"]
    chistes = [
        "¿Por qué los pájaros no usan Facebook? Porque ya tienen Twitter.",
        "¿Qué hace una abeja en el gimnasio? ¡Zum-ba!",
        "¿Por qué los esqueletos no pelean entre ellos? Porque no tienen agallas."
    ]
    piropos = [
        "Si la belleza fuera un pecado, tú no tendrías perdón de Dios.",
        "¿Tienes un mapa? Porque me he perdido en tus ojos.",
        "Si fueras una lágrima, no lloraría por miedo a perderte."
    ]
    
    if any(saludo in texto for saludo in saludos):
        update.message.reply_text(f'Buenassss, {nombre}, ¿cómo va?')
    elif "adiós" in texto:
        update.message.reply_text(f'¡Hasta luego, {nombre}!')
    elif "como va?" in texto:
        update.message.reply_text(f'¡Bien! ¿Y tú, {nombre}?')
    elif "bien" in texto:
        update.message.reply_text(f'Me alegro, {nombre}')
    elif "cuentame un chiste" in texto or "chiste" in texto:
        update.message.reply_text(random.choice(chistes))
    elif "dime un piropo" in texto or "piropo" in texto:
        update.message.reply_text(random.choice(piropos))
    else:
        update.message.reply_text(f'Wtf?, {nombre}.')

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    option = query.data
    if option == '1':
        query.edit_message_text(text="Te daría un beso, pero soy un bot")
    elif option == '2':
        query.edit_message_text(text="Re está para unos mates")
    elif option == '3':
        query.edit_message_text(text="Te quiero")
    elif option == 'chiste1':
        query.edit_message_text(text="¿Por qué los pájaros no usan Facebook? Porque ya tienen Twitter.")
    elif option == 'chiste2':
        query.edit_message_text(text="¿Qué hace una abeja en el gimnasio? ¡Zum-ba!")
    elif option == 'chiste3':
        query.edit_message_text(text="¿Por qué los esqueletos no pelean entre ellos? Porque no tienen agallas.")
    elif option == 'piropo1':
        query.edit_message_text(text="Si la belleza fuera un pecado, tú no tendrías perdón de Dios.")
    elif option == 'piropo2':
        query.edit_message_text(text="¿Tienes un mapa? Porque me he perdido en tus ojos.")
    elif option == 'piropo3':
        query.edit_message_text(text="Si fueras una lágrima, no lloraría por miedo a perderte.")


def obtener_chiste():
    headers = {
        'Accept': 'application/json'
    }
    response = requests.get("https://icanhazdadjoke.com/", headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data['joke']
    else:
        return "No pude obtener un chiste en este momento, intenta de nuevo más tarde."

# Ejemplo de uso
print(obtener_chiste())


def piropo(update: Update, context: CallbackContext) -> None:
    # Creación del menú inline para piropos
    keyboard = [
        [InlineKeyboardButton("Piropo 1", callback_data='piropo1')],
        [InlineKeyboardButton("Piropo 2", callback_data='piropo2')],
        [InlineKeyboardButton("Piropo 3", callback_data='piropo3')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Selecciona un piropo:', reply_markup=reply_markup)

def main():
    # Configura tu token aquí
    updater = Updater("7462588816:AAGy1ypZmxsusKW0rHY8mzMDsAJKekiWPHk")

    dp = updater.dispatcher

    # Añade los handlers para los comandos
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("saludar", saludar))
    dp.add_handler(CommandHandler("nombre", pedir_nombre))
    dp.add_handler(CommandHandler("chiste", obtener_chiste))
    dp.add_handler(CommandHandler("piropo", piropo))

    # Añade el handler para guardar el nombre y la edad
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, guardar_nombre))

    # Añade el handler para los mensajes de texto
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, responder_mensaje))
    
    # Añade el handler para los botones inline
    dp.add_handler(CallbackQueryHandler(button))

    # Comienza a recibir actualizaciones
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
