from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import LabeledPrice, PreCheckoutQuery, CallbackQuery, BotCommand
from aiogram.utils.callback_data import CallbackData
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from config import token, pay_token
import logging

bot = Bot(token=token)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

buy_laptop_cb = CallbackData('buy', 'item_id')

@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Купить ноутбук', callback_data=buy_laptop_cb.new(item_id = 'laptop')))
    await message.reply("Привет выбери товар для покупки", reply_markup=keyboard)
    
@dp.callback_query_handler(buy_laptop_cb.filter(item_id = 'laptop'))
async def process_payment(callback:CallbackQuery):
    price = [LabeledPrice(label='HP Victus', amount=7000000)]
    
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title='Ноутбук',
        payload='laptop',
        description='Ноутбук HP VICTUS 15-fa0031dx Intel Core i5-12450H(3.30-4.40GHz),8GB DDR4,512GB SSD m.2 NVMe,NVIDIA GTX 1650 4GB GDDR6,15.6" FHD(1920x1080)144Hz IPS,WiFi ac,BT 5.0,HD WC,CR,Win11,MicaSilv[68U87UA#ABA]',
        provider_token=pay_token,
        currency='KGS',
        prices=price,
        start_parameter='test_bot',
        photo_url='https://www.ultra.kg/upload/resize_cache/iblock/abb/1000_1000_1d0e97ea46f4438969ab06dd5b311ca67/abb3c7028d30f6d965fa949510ad6426.jpg',
        photo_height=512,
        photo_size=512,
        photo_width=512,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=False,
        is_flexible=False
    )
    await callback.answer()
    
@dp.pre_checkout_query_handler(lambda query : True)
async def pre(pre: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre.id, ok=True)
    
@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def suc(message: types.Message):
    await message.reply("Спасибо за покупку")
    
executor.start_polling(dp, skip_updates=True)
 
