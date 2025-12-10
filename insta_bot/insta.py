from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import threading
import time
import random
import os  
import openpyxl
from datetime import datetime

class InstaBot:
    def __init__(self, username, password, driver_path):
        self.username = username
        self.password = password
        self.driver_path = driver_path
        self.driver = None

    def start_driver(self):
        
        chrome_options = Options()
        #chrome_options.add_argument("--headless")  # Run in headless mode
        #chrome_options.add_argument("--no-sandbox")
        #chrome_options.add_argument("--disable-dev-shm-usage")
        #chrome_options.add_argument("--disable-gpu")  # Optional: Improves compatibility
        #chrome_options.add_argument("window-size=1920,1080")  # Set window size
        #chrome_options.add_argument("--disable-gpu")  # Disables GPU hardware acceleration
        #chrome_options.add_argument("--disable-software-rasterizer")  # Disables software-based rasterization
        #chrome_options.add_argument("--log-level=3") 
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get('https://www.instagram.com')
        time.sleep(3)
    def click(self, xpath):
        try:
            element = WebDriverWait(self.driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.click()
            print("Element",xpath,"clicked successfull")
        except Exception as e:
            print(f"Click error on {xpath}: {e}")

    def send(self, xpath, message):
        try:
            input_element = WebDriverWait(self.driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            input_element.clear()
            for char in message:
                input_element.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
        except Exception as e:
            print(f"Error sending message to {xpath}: {e}")
    def login(self):
        try:
            # Wait and accept cookies if the pop-up appears
            self.click("//button[text()='Decline optional cookies']")
            
            # Input username
            self.send("//input[@name='username']", self.username)
            
            # Input password
            self.send("//input[@name='password']", self.password)
            
            # Click the login button
            self.click("//button[@type='submit']")
            
            # Handle "Save Info?" and "Turn on Notifications" pop-ups after login
            self.click("/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div/div/div/div")
            self.click("/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div/div/div/div")
            time.sleep(5)  # Wait to complete login process
        except Exception as e:
            print(f"Login error: {e}")

    def move_to_profile(self, profile):
        profile = str(profile)
        self.driver.get(f'https://www.instagram.com/{profile}')
        time.sleep(5)
 

    def Follow(self):
        try:
            # Open followers list
            self.click("//a[contains(@href,'/followers/')]")
            random_follow_number = random.randint(7, 10)
            follow_done = 0
            
            while follow_done < random_follow_number:
                follow_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'button._acan._acap._acas')
                total_buttons = len(follow_buttons)
                
                print(f'Found {total_buttons} "Follow" buttons.')

                if total_buttons < random_follow_number:
                    self.scroll_and_get_followers()
                    print("Not enough buttons found...loading more followers")
                    continue
                
                for button in follow_buttons:
                    if follow_done >= random_follow_number:
                        print("Done succuessfull",follow_done)
                        break
                    if button.text.lower() == 'follow':
                        try:
                            button.click()
                            follow_done += 1
                            print(f"Followed {follow_done}")
                            time.sleep(random.uniform(60, 90))
                        except Exception as e:
                            print(f"Error clicking follow button: {e}")

        except Exception as e:
            print(f"Follow error: {e}")
           
    def scroll_and_get_followers(self):
        # Wait until the followers modal is present
            followers_modal = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".xyi19xy.x1ccrb07.xtf3nb5.x1pc53ja.x1lliihq.x1iyjqo2.xs83m0k.xz65tgg.x1rife3k"))
            )
            
            time.sleep(2)  # Give some time for the modal to load properly

            # Store the current number of followers
            previous_follower_count = 0
            followers = []
            follower_buttons = []
            
        
            # Get the follower elements (usernames) after scrolling
            follower_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                ".x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1")
            
            follower_buttons_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                ".x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x150jy0e.x1e558r4.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x6s0dn4.x1oa3qoh.xl56j7k")

            # Extract text from each element (usernames)
            followers = [element.text for element in follower_elements]
            follower_buttons = [button.text for button in follower_buttons_elements]

            # Check if the number of followers has increased
            current_follower_count = len(followers)
        
            if current_follower_count == previous_follower_count:
                # If no new followers are loaded, break the loop
                #break
                print("telos lista")
            # Update the previous count
            previous_follower_count = current_follower_count

            # Scroll to the bottom of the followers modal
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_modal)

            # Wait for more followers to load
            time.sleep(2)  # Adjust the wait time as needed

        # Combine followers and their buttons
            combined_list = list(zip(followers, follower_buttons))
            for sublist in combined_list:
                print(" ".join(map(str, sublist)))
        
    def check_who_followed(self,name):
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = "Followers"
            current_dateTime = datetime.now()

            sheet.append(["Username", "Button Text",current_dateTime])
            self.start_driver()
            self.login()
            self.move_to_profile(name)
            time.sleep(10)
                    # Δημιουργία αρχείου Excel
        

            # Πλοήγηση στο προφίλ του χρήστη
         
            time.sleep(3)

            # Άνοιγμα του followers modal
            followers_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "followers"))
            )
            followers_button.click()

            # Αναμονή για το modal
            followers_modal = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".xyi19xy.x1ccrb07.xtf3nb5.x1pc53ja.x1lliihq.x1iyjqo2.xs83m0k.xz65tgg.x1rife3k"))
            )

            time.sleep(2)  # Χρόνος για να φορτώσει πλήρως

            # Μεταβλητές για αποθήκευση followers
            followers = []
            follower_buttons = []
            previous_follower_count = 0

            while True:
                # Εύρεση στοιχείων followers
                follower_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                    ".x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1")
                follower_buttons_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                    ".x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x150jy0e.x1e558r4.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x6s0dn4.x1oa3qoh.xl56j7k")
                
                # Εξαγωγή δεδομένων
                new_followers = [element.text for element in follower_elements]
                new_buttons = [button.text for button in follower_buttons_elements]
                
                # Προσθήκη νέων δεδομένων στη λίστα
                for follower, button in zip(new_followers, new_buttons):
                    if follower not in followers:  # Αποφυγή διπλότυπων
                        followers.append(follower)
                        follower_buttons.append(button)
                        sheet.append([follower, button])  # Εισαγωγή στο Excel

                # Έλεγχος αν τελείωσε η φόρτωση
                current_follower_count = len(followers)
                if current_follower_count == previous_follower_count:
                    print(f"Τέλος! Συνολικοί followers: {current_follower_count}")
                    sheet.append([follower, button,current_follower_count])
                    break

                # Ενημέρωση προηγούμενης μέτρησης
                previous_follower_count = current_follower_count

              
                
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_modal)
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_modal)
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_modal)


                time.sleep(2)

            # Αποθήκευση στο Excel
            workbook.save(f"{name}_followers.xlsx")
            print(f"Οι followers αποθηκεύτηκαν στο αρχείο {name}_followers.xlsx")
            
    def check_who_got_followed(self):
            
        
            return 0
    def countdown(self,seconds):
        start_time = time.time()  # Αποθηκεύουμε τον χρόνο εκκίνησης
        end_time = start_time + seconds  # Ορίζουμε το χρόνο λήξης
        
        while seconds > 0:
            current_time = time.time()  # Παίρνουμε τον τρέχοντα χρόνο
            elapsed_time = current_time - start_time  # Υπολογίζουμε τον χρόνο που έχει περάσει
            remaining_time = max(0, int(end_time - current_time))  # Υπολογίζουμε τα υπόλοιπα δευτερόλεπτα

            # Εμφανίζουμε την αντίστροφη μέτρηση στην ίδια γραμμή
            print(f"Απομένουν {remaining_time} δευτερόλεπτα...", end='\r')
            
            if elapsed_time >= 1:  # Ενημέρωση κάθε 1 δευτερόλεπτο
                seconds -= 1
                start_time = current_time  # Ανανεώνουμε τον χρόνο εκκίνησης

        # Όταν τελειώσει η αντίστροφη μέτρηση, εμφανίζουμε το τελικό μήνυμα
        
        print("Η αντίστροφη μέτρηση τελείωσε!      ")
    def close_bot(self):
        self.driver.quit()
     
    def actions_follow(self):
        
        count = 0
        sleep=True
        while sleep==True:
       

            while count<16:
    
                self.start_driver()
                self.login()
                self.move_to_profile("sidaki.katerina1")
                time.sleep(10)
                self.Follow()
                self.close_bot()
                
                self.countdown(random.randint(6000,6500))
                count += 1
            
            
                print(f"Follow action count: {count}")
            self.countdown(random.randint(3*3600,4*3600))


 
 
   

