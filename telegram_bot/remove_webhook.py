from telegram import Bot
import asyncio

async def main():
    bot = Bot(token="2007814209:AAEfgXKP3vRb3czgExrYUik0G0iIZxsX40w")
    await bot.delete_webhook()
    print("Webhook снят!")

asyncio.run(main())