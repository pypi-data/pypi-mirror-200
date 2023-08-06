from random import choice, randint
from re import findall
from websocket import create_connection
from json import dumps, loads
from urllib3 import PoolManager
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode as b64e, urlsafe_b64decode as b64d
from Crypto.Cipher import AES

class Bot:

    def __init__(self, auth):
        self._auth = auth

    def CheckNewMessages(self):
        for recv in self._handler():
            yield recv


    def GetChatType(self, chat_id):
        if chat_id.startswith('u'):
            return 'User'
        elif chat_id.startswith('g'):
            return 'Group'
        elif chat_id.startswith('c'):
            return 'Channel'

    def SendMessage(self, chat_id, text, message_id = None):
        metadata = self._MetaData(text)
        data = {'object_guid': chat_id, 'rnd': str(randint(10000000, 999999999)), 'text': metadata[1].strip(),'reply_to_message_id': message_id}
        if metadata[0] != []:
            data['metadata'] = {'meta_data_parts': metadata[0]}
        return self._M('sendMessage', data)

    def EditMessage(self, chat_id, new_text, message_id):
        metadata = self._MetaData(new_text)
        data = {'object_guid': chat_id, 'text': metadata[1].strip(), 'message_id': message_id}
        if metadata[0] != []:
            data['metadata'] = {'meta_data_parts': metadata[0]}
        return self._M('editMessage', data)['message_update']

    def ForwardMessage(self, from_chat_id, message_ids, to_chat_id):
        return self._M('forwardMessages', {'from_object_guid': from_chat_id, 'message_ids': message_ids, 'rnd': str(randint(100000,999999999)), 'to_object_guid': to_chat_id})

    def PinMessage(self, chat_id, message_id):
        return self._M('setPinMessage', {'object_guid': chat_id, 'message_id': message_id, 'action': 'Pin'})

    def UnpinMessage(self, chat_id, message_id):
        return self._M('setPinMessage', {'object_guid': chat_id, 'message_id': message_id, 'action': 'Unpin'})

    def DeleteMessage(self, chat_id, message_ids):
        return self._M('deleteMessages', {'object_guid': chat_id, 'message_ids': message_ids, 'type': 'Global'})['message_updates']

    def GetMessagesInfo(self, chat_id, messages_ids):
        return self._M('getMessagesByID', {'object_guid': chat_id, 'message_ids': messages_ids})['messages']

    def GetLinkInfo(self, url):
        return self._M('getLinkFromAppUrl', {'app_url': url})['link']['open_chat_data']

    def GetChats(self):
        return self._M('getChats', {})

    def GetChatInfo(self, chat_id):
        data = self.GetChatType(chat_id)
        return self._M(f'get{data}Info',{f'{data.lower()}_guid': chat_id})

    def GetChatInfo_ID(self, username):
        return self._M('getObjectByUsername', {'username': username})

    def GetLastMessage(self, chat_id):
        return self.GetChatInfo(chat_id)['chat'].get('last_message', None)

    def GetLastMessageID(self, chat_id):
        return self.GetChatInfo(chat_id)['chat'].get('last_message_id', None)

    def DeleteChatHistory(self, chat_id):
        return self._M('deleteChatHistory', { 'object_guid': chat_id, 'last_message_id': self.GetLastMessageID(chat_id)})['chat_update']

    def DeleteChat(self, chat_id):
        return self._M('deleteUserChat', { 'user_guid': chat_id, 'last_deleted_message_id': self.GetLastMessageID(chat_id)})

    def BanMember(self, chat_id, user_id):
        return self._M(f'ban{self.GetChatType(chat_id)}Member', {f'{self.GetChatType(chat_id).lower()}_guid': chat_id, 'member_guid': user_id, 'action': 'Set'})

    def GetBannedMembers(self, chat_id):
        return self._M(f'getBanned{self.GetChatType(chat_id)}Members', {f'{self.GetChatType(chat_id).lower()}_guid': chat_id})['in_chat_members']

    def SetGroupAccess(self, chat_id, access):
        return self._M('setGroupDefaultAccess', {'access_list': access, 'group_guid': chat_id})

    def GetGroupAdmins(self, chat_id):
        return self._M('getGroupAdminMembers', {'group_guid': chat_id})['in_chat_members']

    def SetGroupTimer(self, chat_id, time):
        return self._M('editGroupInfo', {'group_guid': chat_id, 'slow_mode': int(time), 'updated_parameters': ['slow_mode']})['group']

    def AddAdmin(self, chat_id, user_id, access):
        return self._M(f'set{self.GetChatType(chat_id)}Admin', {f'{self.GetChatType(chat_id).lower()}_guid': chat_id, 'member_guid': user_id, 'access_list': access, 'action': 'SetAdmin'})['in_chat_member']
    
    def DeleteAdmin(self, chat_id, user_id):
        return self._M(f'set{self.GetChatType(chat_id)}Admin', {f'{self.GetChatType(chat_id).lower()}_guid': chat_id, 'member_guid': user_id, 'action': 'UnsetAdmin'})['in_chat_member']

    def JoinGroup(self, link):
        return self._M('joinGroup', {'hash_link': link.split('/')[-1]})

    def LeaveGroup(self, chat_id):
        return self._M('leaveGroup', {'group_guid': chat_id})

    def EditGroup(self, chat_id, title = None, bio = None):
        data = self.GetChatInfo(chat_id)['group']
        return self._M('editGroupInfo', {'group_guid': chat_id, 'title': title or data.get('group_title', None), 'description': bio or data.get('description', None), 'updated_parameters': ['title', 'description']})

    def GetChatLink(self, chat_id):
        return self._M(f'get{self.GetChatType(chat_id)}Link', {f'{self.GetChatType(chat_id).lower()}_guid': chat_id})['join_link']

    def JoinChannel(self, chat_id):
        return self._M('joinChannelAction', {'action': 'Join', 'channel_guid': chat_id})

    def JoinChannel_Link(self, link):
        return self._M('joinChannelByLink', {'hash_link': link.split('/')[-1]})

    def LeaveChannel(self, chat_id):
        return self._M('joinChannelAction', {'action': 'Leave', 'channel_guid': chat_id})

    def Block(self, chat_id):
        return self._M('setBlockUser', {'user_guid': chat_id, 'action': 'Block'})['chat_update']

    def Unblock(self, chat_id):
        return self._M('setBlockUser', {'user_guid': chat_id, 'action': 'Unblock'})['chat_update']

    def GetLoginedDevices(self):
        return self._M('getMySessions', {})

    def EditUser(self, fn, ln, bio = None):
        return self._M("updateProfile", {"first_name": fn, "last_name": ln, "bio": bio, "updated_parameters": ["first_name", "last_name", "bio"]})

    def logout(self):
        return self._M('logout', {})
    


    def _MetaData(self, text):
        g = 0
        results = []
        if text is None:
            return ([], text)
        real_text = text.replace('**', '').replace('__', '').replace('``', '').replace('@@', '')
        bolds = findall(r'\*\*(.*?)\*\*' , text)
        italics = findall(r'\_\_(.*?)\_\_' , text)
        monos = findall(r'\`\`(.*?)\`\`' , text)
        mentions = findall(r'\@\@(.*?)\@\@' , text)
        mention_ids = findall(r'\@\@\((.*?)\)' , text)
        for bold_index , bold_word in zip([real_text.index(i) for i in bolds] , bolds):
            results.append({'from_index' : bold_index, 'length' : len(bold_word), 'type' : 'Bold'})
        for italic_index , italic_word in zip([real_text.index(i) for i in italics] , italics):
            results.append({'from_index' : italic_index, 'length' : len(italic_word), 'type' : 'Italic'})
        for mono_Index , mono_word in zip([real_text.index(i) for i in monos] , monos):
            results.append({'from_index' : mono_Index, 'length' : len(mono_word), 'type' : 'Mono'})
        for mention_index , mention_word in zip([real_text.index(i) for i in mentions] , mentions):
            results.append({'type': 'MentionText', 'from_index': mention_index, 'length': len(mention_word), 'mention_text_object_guid': mention_ids[g] if '@(' in text else '@'})
            if '@(' in text:
                real_text = real_text.replace(f'({mention_ids[g]})', '') 
            g += 1
        return (results, real_text)

    def _handler(self):
        try:
            ws = create_connection(choice(list(loads(PoolManager().request('GET', 'https://getdcmess.iranlms.ir/').data.decode())['data']['socket'].values())))
            ws.send(dumps({'api_version': '5', 'auth': self._auth, 'method': 'handShake'}))
            print('Connected !')
            while True:
                try:
                    recv = loads(ws.recv())
                    if recv != {"status":"OK","status_det":"OK"}:
                        if recv['type'] == 'messenger':
                            yield loads(self._decrypt(recv['data_enc']))
                except:
                    print('ErroR! Reconnecting...')
                    create_connection(choice(list(loads(PoolManager().request('GET', 'https://getdcmess.iranlms.ir/').data.decode())['data']['socket'].values()))).send(dumps({'api_version': '5', 'auth': self._auth, 'method': 'handShake'}))
                    print('Connected Again!')
                    continue
        except:
            print("Check Your Internet Connection")

    def _M(self, met, data):
        try:
        	data = {'api_version': '5', 'auth': self._auth, 'data_enc': self._encrypt(dumps({'method': met, 'input': data, 'client': {'app_name': 'Main', 'app_version': '4.1.7', 'platform': 'Web', 'package': 'web.rubika.ir', 'lang_code': 'fa'}}))}
        	result = PoolManager().request('POST', 'https://messengerg2c2.iranlms.ir/', body = dumps(data).encode())
        	result = loads(self._decrypt(loads(result.data.decode('utf-8'))['data_enc']))
	        if result['status'] == 'OK':
 	           return result['data']
        except:
        	print("ErroR")

    def _replaceCharAt(self, e, t, i):
        return e[0:t] + i + e[t + len(i):]

    def _secret(self, e):
        t, n, s = e[0:8], e[16:24] + e[0:8] + e[24:32] + e[8:16], 0
        while s < len(n):
            e = n[s]
            if e >= '0' and e <= '9':
                t = chr((ord(e[0]) - ord('0') + 5) %10 + ord('0'))
                n = self._replaceCharAt(n, s, t)
            else:
                t = chr((ord(e[0]) - ord('a') + 9) %26 + ord('a'))
                n = self._replaceCharAt(n, s, t)
            s += 1
        return n

    def _encrypt(self, text):
        return b64e(AES.new(bytearray(self._secret(self._auth), 'UTF-8'), AES.MODE_CBC, bytearray.fromhex('0' * 32)).encrypt(pad(text.encode('UTF-8'), AES.block_size))).decode('UTF-8')

    def _decrypt(self, text):
        return unpad(AES.new(bytearray(self._secret(self._auth), 'UTF-8'), AES.MODE_CBC, bytearray.fromhex('0' * 32)).decrypt(b64d(text.encode('UTF-8'))), AES.block_size).decode('UTF-8')



class GetMessagesInfo:

    def __init__(self, data):
        self._data = data

    def Text(self):
        return self._data['message_updates'][0]['message'].get('text', 'None')

    def MessageID(self):
        return self._data['message_updates'][0]['message_id']

    def RepliedMessageID(self):
        return self._data['message_updates'][0]['message'].get('reply_to_message_id', None)

    def ChatGuid(self):
        return self._data['message_updates'][0]['object_guid']

    def AuthorGuid(self):
        return self._data['message_updates'][0]['message']['author_object_guid']

    def ChatType(self):
        return self._data['message_updates'][0]['type']

    def ChatTitle(self):
        return self._data['show_notifications'][0]['title']

    def AuthorTitle(self):
        return self._data['chat_updates'][0]['chat']['last_message']['author_title']

