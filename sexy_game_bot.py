
import random
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ParseMode

API_TOKEN = 'BURAYA_TOKEN_YERLEŞDİR'
ADMIN_ID = 123456789  # Buraya öz Telegram ID-ni yaz

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

users = []
points = {}
hearts = {}
coins = {}
premium_users = set()
truths = [
    "Ən böyük sirrin nədir?", "İlk öpüşün neçə yaşında olub?", 
    "Ən çox kimə simpatiyan var burda?", "Qısqanclıq edirsənmi?"
]
dares = [
    "Bir nəfərə 3 şirin söz yaz", "Bir istifadəçiyə virtual öpüş göndər", 
    "Adını 10 dəqiqə ərzində 'Sexy King/Queen' et", "Səsini yaz və 'Səni istəyirəm' de"
]

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.reply("**Sexy Oyuna xoş gəldin!**
Əmr siyahısı üçün: /help", parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=['help'])
async def help_cmd(message: types.Message):
    await message.reply("/play — Oyuna başla
/kiss @istifadəçi — Öpüş
/gift @istifadəçi — Hədiyyə
/truth — Həqiqət sualı
/dare — Cəsarət tapşırığı
/private @istifadəçi — Şəxsi otaq
/heart @istifadəçi — Qəlb göndər
/coins — Coin bax
/premium — Premium ver (admin)
/goldroom — Qızıl otaq (premium)")

@dp.message_handler(commands=['play'])
async def play(message: types.Message):
    if message.from_user.id not in users:
        users.append(message.from_user.id)
    if len(users) < 2:
        await message.reply("Ən azı 2 nəfər lazımdır.")
        return
    chosen = random.sample(users, 2)
    await message.reply(f"Şüşə fırlandı! Seçildi:
❤️ <a href='tg://user?id={chosen[0]}'>İstifadəçi 1</a> və <a href='tg://user?id={chosen[1]}'>İstifadəçi 2</a>", parse_mode="HTML")

@dp.message_handler(commands=['kiss'])
async def kiss(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Öpüş göndərmək üçün kimisə reply et.")
        return
    user_id = message.reply_to_message.from_user.id
    await message.answer(f"<a href='tg://user?id={message.from_user.id}'>Sən</a> ➤ 💋 ➤ <a href='tg://user?id={user_id}'>Ona öpdü!</a>", parse_mode="HTML")
    points[message.from_user.id] = points.get(message.from_user.id, 0) + 1
    coins[message.from_user.id] = coins.get(message.from_user.id, 0) + 1

@dp.message_handler(commands=['gift'])
async def gift(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Hədiyyə göndərmək üçün kimisə reply et.")
        return
    await message.reply("🎁 Hədiyyə göndərildi!")
    points[message.from_user.id] = points.get(message.from_user.id, 0) + 1
    coins[message.from_user.id] = coins.get(message.from_user.id, 0) + 2

@dp.message_handler(commands=['truth'])
async def truth(message: types.Message):
    await message.reply("Həqiqət sualın:
" + random.choice(truths))

@dp.message_handler(commands=['dare'])
async def dare(message: types.Message):
    await message.reply("Cəsarət tapşırığın:
" + random.choice(dares))

@dp.message_handler(commands=['private'])
async def private_room(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Şəxsi otağa dəvət üçün kimisə reply et.")
        return
    await message.reply("Gizli otaq təklifi göndərildi. Qarşı tərəf razı olsa, davam edin...")

@dp.message_handler(commands=['heart'])
async def send_heart(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Qəlb göndərmək üçün kimisə reply et.")
        return
    user_id = message.reply_to_message.from_user.id
    await message.answer(f"❤️ <a href='tg://user?id={message.from_user.id}'>Sən</a> qəlb göndərdi ➤ <a href='tg://user?id={user_id}'>Ona</a>", parse_mode="HTML")
    hearts[message.from_user.id] = hearts.get(message.from_user.id, 0) + 1
    coins[message.from_user.id] = coins.get(message.from_user.id, 0) + 2

@dp.message_handler(commands=['coins'])
async def check_coins(message: types.Message):
    coin = coins.get(message.from_user.id, 0)
    await message.reply(f"Coinlərin: {coin}")

@dp.message_handler(commands=['premium'])
async def make_premium(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("Sən bu əmri istifadə edə bilməzsən.")
        return
    if not message.reply_to_message:
        await message.reply("Premium vermək üçün kimisə reply et.")
        return
    user_id = message.reply_to_message.from_user.id
    premium_users.add(user_id)
    await message.reply("İstifadəçi artıq premiumdur.")

@dp.message_handler(commands=['goldroom'])
async def gold_room(message: types.Message):
    if message.from_user.id not in premium_users:
        await message.reply("Bu xüsusiyyət yalnız premium istifadəçilər üçündür.")
        return
    if not message.reply_to_message:
        await message.reply("Kimi qızıl otağa dəvət etmək istəyirsən?")
        return
    await message.reply("Qızıl otağa keçmək üçün qarşı tərəfin razılığı gözlənilir...")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
