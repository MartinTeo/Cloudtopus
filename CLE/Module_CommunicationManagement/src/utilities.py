from Module_TeamManagement.models import Telegram_Chats

def getTelegramChatJSON(chat_obj=None,chat_name=None):
    telegram_chat = {}

    if chat_obj == None and chat_name == None:
        raise Exception('Please specify at least a chat_obj or a chat_name.')

    if chat_obj == None and chat_name != None:
        chat_obj = Telegram_Chats.objects.get(name=chat_name)

    telegram_chat = {
        'name': chat_obj.name,
        'link': chat_obj.link,
        'type': chat_obj.type,
        'members': chat_obj.members.split('_') if chat_obj.members != None else [],
        'members_count': len(chat_obj.members.split('_')) if chat_obj.members != None else 0,
        'name_join': chat_obj.name.replace(' ','_'),
    }

    return telegram_chat
