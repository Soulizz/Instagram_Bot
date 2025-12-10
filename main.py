# main.py
import threading
import time
from insta_bot.insta import InstaBot

class BotController:
    
    def __init__(self, username, password, driver_path):
        self.bot = InstaBot(username, password, driver_path)
        self.bot_thread = None
        self.running = False

    def auto_follow_control(self):
        if not self.running:
            self.running = True
            self.bot_thread = threading.Thread(target=self.bot.actions_follow)
            self.bot_thread.start()
            print("Bot started.")
        else:
            print("Bot is already running.")
    def check_who_followed_control(self,name):
            if not self.running:
                
                self.running = True
                self.bot_thread = threading.Thread(target=self.bot.check_who_followed,args=(name,))
                self.bot_thread.start()
                print("Bot started.")
            else:
                print("Bot is already running.")
    def check_who_got_followed_control(self,name):
        if not self.running:
            self.running = True
            self.bot_thread = threading.Thread(target=self.bot.check_who_got_followed,args=(name,))
            self.bot_thread.start()
            print("Bot started.")
        else:
            print("Bot is already running.")
    def stop_bot(self):
        if self.running:
            self.bot.close_bot()
            self.running = False
            print("Bot stopped.")
        else:
            print("Bot is not running.")

    def control_loop(self):
        while True:
            print("\n--- Menu ---")
            print("1: Auto Follow")
            print("2: Who Followed an Account")
            print("3: Who Got Followed")
            print("4: Exit")
            print("-----------------\n")
            
            command = input("Enter your choice: ").strip()
            
            if command == '1':
                print("Starting Auto Follow...")
                self.auto_follow_control()
            elif command == '2':
                print("Checking who followed an account...")
                name=input("Give name of user you want to see who followed:")
                self.check_who_followed_control(name)
            elif command == '3':
                print("Checking who got followed...")
                self.check_who_got_followed_control(name)
            elif command == '4':
                if self.running:
                    self.stop_bot()
                print("Exiting...")
                break
            else:
                print("Unknown command. Please select a valid option.")
if __name__ == "__main__":
    print("--Insert Your Instagram Username--")
    username=input("Username:")
    print("--Insert Your Instagram Password--")
    password=input("Password:")
    driver_path = r'C:\Users\kapamapa\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'

    controller = BotController(username, password, driver_path)
    controller.control_loop()