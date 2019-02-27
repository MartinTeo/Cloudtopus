from datetime import datetime
from background_task import background
from telethon.tl.types import Channel, Chat
from Module_TeamManagement.models import Telegram_Chats
from Module_CommunicationManagement.src import tele_util

@background(schedule=0)
def test_tasks(message):
    print(message)


@background(schedule=0)
def getAllChatMembers(username,chat_type,chat_name):
    print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] Running background event: Get All Members')

    tele_chat_type = {
        'Channel':Channel,
        'Group':Chat,
    }

    telegram_chat = Telegram_Chats.objects.get(name=chat_name)
    client = tele_util.getClient(username)

    members, count = tele_util.getMembers(client,chat_name,tele_chat_type[chat_type])
    telegram_chat.members = '_'.join(members)
    telegram_chat.save()

    print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] Retreive all members for chat: ' + chat_name)
    tele_util.disconnectClient(client)

    print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] Ending background event: Get All Members')


@background(schedule=0)
def sendMessage(username,chat_type,chat_name,message):
    print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] Running background event: Sending Telegram Message')

    client = tele_util.getClient(username)

    if chat_type == 'Group':
        tele_util.sendGroupMessage(client,chat_name,message)
    elif chat_type == 'Channel':
        tele_util.sendChannelMessage(client,chat_name,message)

    print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] Sent message to ('+ chat_type +'): ' + chat_name)
    tele_util.disconnectClient(client)

    print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] Ending background event: Sending Telegram Message')


@background(schedule=0)
def createChannel(username,channel_name):
    print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] Running background event: Creating Telegram Channel')

    client = tele_util.getClient(username)

    results = tele_util.initialize_Channel(
        client=client,
        channel_name=channel_name,
    )

    telegram_chat = Telegram_Chats.objects.get(name=channel_name)
    telegram_chat.link = results['channel_link']
    telegram_chat.save()

    print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] Telegram Channel: ' + channel_name + ' create')
    # tele_util.disconnectClient(client)

    print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] Ending background event: Creating Telegram Channel')

    getAllChatMembers(
        username=username,
        chat_type=telegram_chat.type,
        chat_name=channel_name,
        schedule=0,
    )


@background(schedule=0)
def createGroup(username,group_name,additional_username):
    print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] Running background event: Creating Telegram Group')

    client = tele_util.getClient(username)

    results = tele_util.initialize_Group(
        username=additional_username,
        client=client,
        group_name=group_name,
    )

    telegram_chat = Telegram_Chats.objects.get(name=group_name)
    telegram_chat.link = results['group_link']
    telegram_chat.save()

    print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] Telegram Group: ' + group_name + ' create')
    tele_util.disconnectClient(client)

    print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] Ending background event: Creating Telegram Group')

    getAllChatMembers(
        username=username,
        chat_type=telegram_chat.type,
        chat_name=group_name,
        schedule=0,
    )


@background(schedule=0)
def deleteChat(username,telegram_username,chat_name,chat_type):
    print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] Running background event: Deleting Telegram Chat')

    client = tele_util.getClient(username)

    if chat_type == 'Group':
        tele_util.deleteGroup(client,chat_name,telegram_username)
    elif chat_type == 'Channel':
        tele_util.deleteChannel(client,chat_name)

    print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] Telegram Group: ' + chat_name + ' deleted')
    tele_util.disconnectClient(client)

    print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] Ending background event: Deleting Telegram Chat')
