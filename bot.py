#    This file is part of the ChannelAutoForwarder distribution (https://github.com/xditya/ChannelAutoForwarder).
#    Copyright (c) 2021 Adiya
#    
#    This program is free software: you can redistribute it and/or modify  
#    it under the terms of the GNU General Public License as published by  
#    the Free Software Foundation, version 3.
# 
#    This program is distributed in the hope that it will be useful, but 
#    WITHOUT ANY WARRANTY; without even the implied warranty of 
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
#    General Public License for more details.
# 
#    License can be found in < https://github.com/xditya/ChannelAutoForwarder/blob/main/License> .

import logging
import asyncio
from telethon import TelegramClient, events, Button
from decouple import config
from telethon.tl.functions.users import GetFullUserRequest

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

# start the bot
print("Iniciando...")
try:
    apiid = config("APP_ID", cast=int)
    apihash = config("API_HASH")
    bottoken = config("BOT_TOKEN")
    frm = config("FROM_CHANNEL", cast=int)
    tochnl = config("TO_CHANNEL", cast=int)
    datgbot = TelegramClient('bot', apiid, apihash).start(bot_token=bottoken)
except:
    print("¡Faltan variables de entorno! Por favor, vuelva a comprobar.")
    print("Bot está saliendo...")
    exit()


@datgbot.on(events.NewMessage(pattern="/start"))
async def _(event):
    ok = await datgbot(GetFullUserRequest(event.sender_id))
    await event.reply(f"¡Hola `{ok.user.first_name}`!\n\n¡Soy un bot de publicación automática de canales! ¡Lea /help para saber más!\n\nPuedo usar solo dos canales (un bot) a la vez para reenviar las publicaciones.\n\nBot creado y gestionado por [Skueletor](https://t.me/DKzippO)...", buttons=[Button.url("🍃 AsAEcos", url="http://t.me/AsAEcos"), Button.url("👤 Soporte", url="https://t.me/DKzippO")], link_preview=False)


@datgbot.on(events.NewMessage(pattern="/help"))
async def helpp(event):
    await event.reply("**¡Bienvenido al apartado de ayuda!**\n\nEste bot enviará todas las publicaciones nuevas en un canal al otro canal. (¡Sin que aparezca que fue reenviado!)\nSolo se puede usar en dos canales a la vez, así que puede conseguir otro bot comprándolo [aquí](https:/t.me/DKzippO).\n\n¡Agrégame a ambos canales y hazme administrador en ambos, y todos los mensajes nuevos se publicarán automáticamente en el canal vinculado!\n\n ¿Te gustó el bot? Suelta un ♥ a @skueletor_bot :)")

@datgbot.on(events.NewMessage(incoming=True, chats=frm)) 
async def _(event): 
    if not event.is_private:
        try:
            if event.poll:
                return
            if event.photo:
                photo = event.media.photo
                await datgbot.send_file(tochnl, photo, caption = event.text, link_preview = False)
            elif event.media:
                try:
                    if event.media.webpage:
                        await datgbot.send_message(tochnl, event.text, link_preview = False)
                        return
                except:
                    media = event.media.document
                    await datgbot.send_file(tochnl, media, caption = event.text, link_preview = False)
                    return
            else:
                await datgbot.send_message(tochnl, event.text, link_preview = False)
        except:
            print("TO_CHANNEL ID está mal o no puedo enviar mensajes allí (hazme administrador).")


print("El bot ha sido iniciado correctamente.")
print("Hecho con ❤️ por Skueletor")
print("Visite 🍃 AsAEcos")
datgbot.run_until_disconnected()
