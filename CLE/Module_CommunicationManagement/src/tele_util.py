import os
import datetime
import traceback
from telethon import TelegramClient, sync, errors
from telethon.tl.functions import messages, channels
from telethon.tl.types import ChannelAdminRights, ChatInviteExported, Channel, Chat, ChannelParticipantsSearch
from Module_CommunicationManagement.src import tele_config

#-----------------------------------------------------------------------------#
#-------------------------- Telegram Functions -------------------------------#
#-----------------------------------------------------------------------------#

# Return telegram client object.
def getClient(username=None):
    if username == None:
        raise Exception('Please specify a username.')

    if tele_config.CLIENT == None:
        session_file = username + '.session'
        tele_config.CLIENT = TelegramClient(os.path.join(SESSION_FOLDER,session_file), API_ID, API_HASH)
        print("Client is none")

    tele_config.CLIENT.connect()
    print(tele_config.CLIENT)
    return tele_config.CLIENT


# Return True if name already exists within telegram. Else False
def dialogExists(client=None,dialog_name=None,type=None):
    if client == None:
        raise Exception('Please specify a client.')

    if dialog_name == None:
        raise Exception('Please specify a group/channel name.')

    if type == None:
        raise Exception('Please specify a type; Chat/Channel.')

    dialogs = client.get_dialogs()
    for dialog in dialogs:
        if dialog.name == dialog_name and isinstance(dialog.entity,type):
            return True

    return False


# Return dialog object if name exists within telegram. Else None
def getDialog(client,dialog_name,type):
    if dialogExists(client,dialog_name,type):
        dialogs = client.get_dialogs()
        for dialog in dialogs:
            if dialog.name == dialog_name and isinstance(dialog.entity,type):
                return dialog

    return None


# Return entity object if name exists within telegram. Else None
def getEntity(client,dialog_name,type):
    dialog = getDialog(client,dialog_name,type)
    if dialog != None:
        return dialog.entity

    return None


# Return members : list and number of memebers : int if name exists within telegram. Else empty list
def getMembers(client,dialog_name,type):
    offset = 0
    limit = 1000
    valid_members = []
    entity = getEntity(client,dialog_name,type)

    if entity == None:
        return [],0

    if type == Channel:
        members = client(channels.GetParticipantsRequest(
            channel=entity,
            filter=ChannelParticipantsSearch(''),
            offset=offset,
            limit=limit,
            hash=0
        ))
        for user in members.users:
            if not user.bot:
                valid_members.append(user.username)

    elif type == Chat:
        members = client.get_participants(entity)
        for member in members:
            if not member.bot:
                valid_members.append(member.username)

    return valid_members, len(valid_members)


# Return True if channel is succesfully create, ELSE False
# Valid for:
# 1. Course Channel
# 2. Section Channel
#
# Returns dict:
# - status
# - message
# - channel_name
# - channel_link
def initialize_Channel(client=None,course_title=None,section_number=None,channel_name=None):
    results = {'status' : False}
    title = ''

    if client == None:
        raise Exception('Client is invalid. Please connect to telegram client first.')

    if course_title != None and section_number != None:
        fin_year = getFinancialYear()
        title = (fin_year + ' ' + course_title + ' ' + section_number).strip()

    if channel_name != None:
        title = channel_name

    if title == '':
        raise Exception('Please specify a course tittle and section number OR a channel name.')

    # Create channel for specified user
    if dialogExists(client,title,Channel):
        results['status'] = True
        results['message'] = title + ' channel already exists within Telegram.'
    else:
        client(channels.CreateChannelRequest(title=title,about='This channel is for students in ' + title))

        channel_entity = getEntity(client,title,Channel)
        admin_rights = ChannelAdminRights(
            change_info=True,
            post_messages=True,
            edit_messages=True,
            delete_messages=True,
            ban_users=True,
            invite_users=True,
            invite_link=True,
            pin_messages=True,
            add_admins=True,
        )

        client(channels.EditAdminRequest(channel=channel_entity.id,user_id='@SMUCLEBot',admin_rights=admin_rights))
        results['status'] = True
        results['message'] = title + ' channel create.'

    invite_link = client(channels.ExportInviteRequest(getEntity(client,title,Channel).id))
    results['channel_name'] = title
    results['channel_link'] = invite_link.link

    return results


# Return True if groups are succesfully create, ELSE False
# Valid for:
# 1. Section Groups
# 2. Team Groups
#
# Returns dict:
# - status
# - message
# - group_name
# - group_link
def initialize_Group(username,client=None,course_title=None,section_number=None,team_number='',group_name=None):
    results = {'status' : False}
    title = ''

    if client == None:
        raise Exception('Client is invalid. Please connect to telegram client first.')

    if course_title != None and section_number != None:
        fin_year = getFinancialYear()
        title = (fin_year + ' ' + course_title + ' ' + section_number + team_number).strip()

    if group_name != None:
        title = group_name

    if title == '':
        raise Exception('Please specify a course tittle and section number OR a group name.')

    # Create groups for specified user
    if dialogExists(client,title,Chat):
        results['status'] = True
        results['message'] = title + ' group already exists within Telegram.'
    else:
        users = [username,'@SMUCLEBot']
        client(messages.CreateChatRequest(users=users,title=title))

        results['status'] = True
        results['message'] = title + ' group create.'

        # Remove that extra user after the group is created
        deleteUserFromGroup(client,title,username)

    invite_link = client(messages.ExportChatInviteRequest(getEntity(client,title,Chat).id))
    results['group_name'] = title
    results['group_link'] = invite_link.link

    return results


def deleteUserFromGroup(client,group_name,user_name):
    dialog = getDialog(client,group_name,Chat)
    chat_id = dialog.message.to_id.chat_id
    client(messages.DeleteChatUserRequest(
        chat_id=chat_id,
        user_id=user_name
    ))


def deleteGroup(client,group_name,username):
    dialog = getDialog(client,group_name,Chat)
    deleteUserFromGroup(client,group_name,username)


def deleteChannel(client,channel_name):
    channel_entity = getEntity(client,channel_name,Channel)
    client(channels.DeleteChannelRequest(
        channel=channel_entity.id,
    ))


def sendGroupMessage(client,group_name,message):
    dialog = getDialog(client,group_name,Chat)
    client(messages.SendMessageRequest(
        peer=dialog,
        message=message,
    ))


def sendChannelMessage(client,channel_name,message):
    channel_entity = getEntity(client,channel_name,Channel)
    client(messages.SendMessageRequest(
        peer=channel_entity.id,
        message=message,
    ))


def disconnectClient(client=None):
    if client == None:
        raise Exception('Please specify a client.')

    # tele_config.CLIENT = None
    client.disconnect()


# ============================================================================ #
# ============================================================================ #
# ============================================================================ #


if __name__ == "__main__":
    import tele_config
    from tele_config import *

    SESSION_FOLDER = os.path.abspath('telegram_sessions')

    try:
        client = getClient(ADMIN_USERNAME)
        client.connect()

        if not client.is_user_authorized():
            client.send_code_request(ADMIN_PHONE_NUMBER)
            try:
                client.sign_in(ADMIN_PHONE_NUMBER, input("Enter Code: "))
            except PhoneNumberUnoccupiedError:
                client.sign_up(ADMIN_PHONE_NUMBER, input("Enter Code: "))

        # RUN test methods here

        client.disconnect()


    except Exception as e:
        traceback.print_exc()
else:
    from Module_CommunicationManagement.src.tele_config import *
    from Module_CommunicationManagement.src import tele_config
    from Module_TeamManagement.src.utilities import getFinancialYear
