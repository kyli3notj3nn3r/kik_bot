#!/usr/bin/env python3

# Import Python Libraries
import logging

# Import Installed Libraries
from colorama import Fore, Style

# Import KIK API
import kik_unofficial.datatypes.xmpp.chatting as chatting
from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
from kik_unofficial.datatypes.xmpp.errors import *
from kik_unofficial.datatypes.xmpp.login import *
from kik_unofficial.datatypes.xmpp.roster import *
from kik_unofficial.datatypes.xmpp.sign_up import *
from kik_unofficial.datatypes.xmpp.xiphias import *
from kik_unofficial.datatypes.xmpp.group_adminship import *

# Variables
username = ''  #  Put your bots username here
password = ''  # Put your bots password here
bot_admins = '' #  I would at least put your JID here, if you want to add more people, simply seperate each jid with a comma
listfr = ['a', 'b', 'c', 'd', 'e', 'f']
listfn = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
x = ''.join(random.choice(listfn + listfr) for _ in range(32))
y = ''.join(random.choice(listfn + listfr) for _ in range(16))
device_id = x
android_id = y


def main():
    # set up logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter(KikClient.log_format()))
    logger.addHandler(stream_handler)

    bot = KikBot()


def jid_to_username(jid):
    return jid.split('@')[0][0:-4]    
	
	
class KikBot(KikClientCallback):
    def __init__(self):
	    self.client = KikClient(self,
                                kik_username=username,
                                kik_password=password,
                                device_id_override=device_id,
                                android_id_override=android_id)
		thread = threading.Thread(target=self.keep_alive, args=())
        thread.daemon = True
        thread.start()
		
	    def on_authenticated(self):
            print(Fore.GREEN + Style.BRIGHT + "Now I'm Authenticated, let's request roster" + Style.RESET_ALL)
			self.client.request_roster()
			
		def on_login_ended(self, response: LoginResponse):
            print(Fore.RED + Style.BRIGHT + "Full name: {} {}".format(response.first_name, response.last_name) + Style.RESET_ALL)
			
		def keep_alive(self):  #  I added this into my code to constantly keep my bot connected to kiks servers, otherwise if groups are being quiet your bot will timeout
			time.sleep(120)
			while True:
				print("staying alive")
				self.client.send_chat_message("", "Staying alive")  #  Insert a random alts jid to dump into
				time.sleep(120)
				
		def on_chat_message_received(self, chat_message: chatting.IncomingChatMessage):
			print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "[+] '{}' says: {}".format(chat_message.from_jid, chat_message.body) + Style.RESET_ALL)
			self.client.request_info_of_users(chat_message.from_jid)
			
		def on_is_typing_event_received(self, response: chatting.IncomingIsTypingEvent):
			print(Fore.YELLOW + "[+] {} is now {}typing.".format(response.from_jid,
																 "not " if not response.is_typing else "") + Style.RESET_ALL)
																 
		def on_message_delivered(self, response: chatting.IncomingMessageDeliveredEvent):
			print(Fore.LIGHTMAGENTA_EX + "[+] Chat message with ID {} is delivered.".format(response.message_id) + Style.RESET_ALL)
			
		def on_message_read(self, response: chatting.IncomingMessageReadEvent):
			print(Fore.LIGHTMAGENTA_EX + "[+] Human has read the message with ID {}.".format(response.message_id) + Style.RESET_ALL)
			
		def on_group_receipts_received(self, response: chatting.IncomingGroupReceiptsEvent):
            print(Fore.LIGHTMAGENTA_EX + "[+] Message with ID {} has been {}".format(response.message_id, response.type) + Style.RESET_ALL)
            
        def on_group_message_received(self, chat_message: chatting.IncomingGroupChatMessage):
            print(Fore.LIGHTGREEN_EX + "[+] '{}' from group ID {} says: {}".format(chat_message.from_jid, chat_message.group_jid, chat_message.body) + Style.RESET_ALL)
        
        def on_group_is_typing_event_received(self, response: chatting.IncomingGroupIsTypingEvent):
            print(Fore.LIGHTYELLOW_EX + "[+] {} is now {}typing in group {}".format(response.from_jid, "not " if not response.is_typing else "", response.group_jid) + Style.RESET_ALL)
        
        def on_gif_received(self, response: chatting.IncomingGifMessage):
            print(Fore.RED + "GIF" + Style.RESET_ALL)
            
        def on_roster_received(self, response: FetchRosterResponse):
            print(Fore.YELLOW + "[+] Chat partners:\n" + '\n'.join([str(member) for member in response.peers]) + Style.RESET_ALL)
            
        def on_friend_attribution(self, response: chatting.IncomingFriendAttribution):
            print(Fore.LIGHTYELLOW_EX + "[+] Friend attribution request from " + response.referrer_jid + Style.RESET_ALL)
            
        def on_image_received(self, response: chatting.IncomingImageMessage):
            print(Fore.BLUE + "[+] Image message {} was received from {}".format(response.image_url, response.from_jid) + Style.RESET_ALL)
            
        def on_video_received(self, response: chatting.IncomingVideoMessage):
            print(Fore.BLUE + "[+] Video message {} was received from {}".format(response.video_url, response.from_jid) + Style.RESET_ALL)
            
        def on_peer_info_received(self, response: PeersInfoResponse):
            print(Fore.GREEN + "[+] Peer info: " + str(response.users) + Style.RESET_ALL)
            
        def on_xiphias_get_users_response(self, response: Union[UsersResponse, UsersByAliasResponse]):
            print(Fore.GREEN + " Users Response: " + str(response.users) + Style.RESET_ALL)
            
        def on_group_status_received(self, response: chatting.IncomingGroupStatus):
            print("status received")
            
        def on_group_sysmsg_received(self, response: chatting.IncomingGroupSysmsg):
            print(Fore.GREEN + Style.BRIGHT + "[+] System message in {}: {}".format(response.group_jid,
                                                                                    response.sysmsg) + Style.RESET_ALL)
                                                                                    
        def on_status_message_received(self, response: chatting.IncomingStatusResponse):
            print(Fore.YELLOW + "[+] Status message from {}: {}".format(response.from_jid, response.status) + Style.RESET_ALL)

        def on_username_uniqueness_received(self, response: UsernameUniquenessResponse):
            print("Is {} a unique username? {}".format(response.username, response.unique))

        def on_sign_up_ended(self, response: RegisterResponse):
            print("[+] Registered as " + response.kik_node)
            
        def on_disconnected(self):
            pass

        def on_connection_failed(self, response: ConnectionFailedResponse):
            print("[-] Connection failed: " + response.message)
        
        def on_login_error(self, login_error: LoginError):
            if login_error.is_captcha():
                login_error.solve_captcha_wizard(self.client)

        def on_register_error(self, response: SignUpError):
            print("[-] Register error: {}".format(response.message))


if __name__ == '__main__':
    main()
    logging.basicConfig(format=KikClient.log_format(), level=logging.INFO)




      



              
		
