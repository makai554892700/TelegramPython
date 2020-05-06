from telethon import TelegramClient
import asyncio

# 定义telegram相关参数
api_id_1 = 0
api_hash_1 = ''  # Your api_hash
phone_number_1 = ''  # Your phone number
user_1 = TelegramClient(phone_number_1, api_id_1, api_hash_1)
user_1.session.report_errors = False


async def init():
    await user_1.connect()
    if not await user_1.is_user_authorized():
        await user_1.send_code_request(phone_number_1)
        await user_1.sign_in(phone_number_1, input('Enter the code: '))


loop = asyncio.get_event_loop()
loop.run_until_complete(init())
# api_id_2 = 1
# api_hash_2 = ''  # Your api_hash
# phone_number_2 = ''  # Your phone number
# user_2 = TelegramClient(phone_number_2, api_id_2, api_hash_2)
# user_2.session.report_errors = False
# user_2.connect()
# if not user_2.is_user_authorized():
#     user_2.send_code_request(phone_number_2)
#     user_2.sign_in(phone_number_2, input('Enter the code: '))
#
# api_id_3 = 2
# api_hash_3 = ''  # Your api_hash
# phone_number_3 = ''  # Your phone number
# user_3 = TelegramClient(phone_number_3, api_id_3, api_hash_3)
# user_3.session.report_errors = False
# user_3.connect()
# if not user_3.is_user_authorized():
#     user_3.send_code_request(phone_number_3)
#     user_3.sign_in(phone_number_3, input('Enter the code: '))
#
# api_id_4 = 3
# api_hash_4 = ''  # Your api_hash
# phone_number_4 = ''  # Your phone number
# user_4 = TelegramClient(phone_number_4, api_id_4, api_hash_4)
# user_4.session.report_errors = False
# user_4.connect()
# if not user_4.is_user_authorized():
#     user_4.send_code_request(phone_number_4)
#     user_4.sign_in(phone_number_4, input('Enter the code: '))
