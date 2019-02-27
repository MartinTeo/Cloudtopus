import os

# telethon configuration values
API_ID = '367454'
API_HASH = '1bf84fb9cec9b739bc9dc2a5fe97ee10'
if 'posix' in os.name:
    SESSION_FOLDER = os.path.join(os.getcwd(),'Module_CommunicationManagement/src/telegram_sessions')
else:
    SESSION_FOLDER = os.path.join(os.getcwd(),'Module_CommunicationManagement\\src\\telegram_sessions')
ADMIN_SESSION_FILE = 'admin_login.session'
ADMIN_USERNAME = 'admin_login'

# telegram-bot configuration values
BOT_TOKEN = '661877002:AAGwwd3zN0ZLObDAObV6FqRGCQkmphEkrus'
ADMIN_CHAT_ID = '-1001296496624'

# admin credentials
ADMIN_PHONE_NUMBER = '6591169096'
ADMIN_GROUP = 'Thunderhead Monkeys'

# Runtime variables
CLIENT = None
