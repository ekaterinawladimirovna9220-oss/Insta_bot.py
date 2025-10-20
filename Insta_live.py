import time
import threading
from instagrapi import Client
from concurrent.futures import ThreadPoolExecutor

USERNAME = "x0a6l"
PASSWORD = "Guru@123"

cl = Client()
cl.login(USERNAME, PASSWORD)

REPLY_TEXT = "@{} ЁЭРМs╔в ЁЭРМс┤Ас┤Ы ЁЭРКс┤А╩А ЁЭРЦс┤А╩А╔┤с┤А ЁЭРДsс┤Шс┤Ас┤Ес┤А/ЁЭРА╔┤с┤Ь╩Ас┤А╔в ЁЭРК╔к ЁЭРМс┤Ас┤А ЁЭРВс┤Пс┤Е ЁЭРГс┤Ь╔┤╔вс┤АЁЯдкЁЯдк"

print("ЁЯПн INDUSTRIAL SCALE BOT STARTED")
print("тЪб Ready for 500+ groups")
print("ЁЯОп 0.1 second response time")

class GroupManager:
    def __init__(self):
        self.thread_data = {}
        self.seen_messages = {}
        self.my_user_id = cl.user_id_from_username(USERNAME)
        self.load_all_groups()
        
    def load_all_groups(self):
        """рд╕рднреА groups load рдХрд░рддрд╛ рд╣реИ"""
        threads = cl.direct_threads()
        print(f"ЁЯУК Loaded {len(threads)} groups")
        
        for thread in threads:
            thread_id = thread.id
            thread_name = getattr(thread, 'title', getattr(thread, 'name', f'Group-{thread_id}'))
            
            self.thread_data[thread_id] = {
                'name': thread_name,
                'last_checked': 0
            }
            self.seen_messages[thread_id] = set()
            
            print(f"   тЬЕ {thread_name}")
    
    def process_single_group(self, thread_id):
        """рдПрдХ group process рдХрд░рддрд╛ рд╣реИ"""
        try:
            current_time = time.time()
            
            # рд╣рд░ 0.1 seconds рдореЗрдВ check рдХрд░реЛ
            if current_time - self.thread_data[thread_id]['last_checked'] < 0.1:
                return
                
            self.thread_data[thread_id]['last_checked'] = current_time
            
            # Group messages fetch рдХрд░реЛ
            thread = cl.direct_thread(thread_id)
            
            if thread.messages:
                latest_msg = thread.messages[0]
                
                if (latest_msg.id not in self.seen_messages[thread_id] and 
                    hasattr(latest_msg, 'user_id') and 
                    latest_msg.user_id != self.my_user_id):
                    
                    user_info = cl.user_info(latest_msg.user_id)
                    
                    # Instant reply
                    cl.direct_send(REPLY_TEXT.format(user_info.username), thread_ids=[thread_id])
                    self.seen_messages[thread_id].add(latest_msg.id)
                    
                    print(f"ЁЯЪА @{user_info.username} тЖТ {self.thread_data[thread_id]['name']}")
                    
        except Exception as e:
            # Errors ignore рдХрд░реЛ - continue processing
            pass
    
    def process_all_groups_parallel(self):
        """рд╕рднреА groups рдХреЛ parallel process рдХрд░рддрд╛ рд╣реИ"""
        with ThreadPoolExecutor(max_workers=50) as executor:  # 50 parallel threads
            futures = []
            for thread_id in self.thread_data.keys():
                future = executor.submit(self.process_single_group, thread_id)
                futures.append(future)
            
            # Wait for all to complete
            for future in futures:
                future.result()

# Bot start рдХрд░реЛ
manager = GroupManager()

print(f"\nЁЯОп Monitoring {len(manager.thread_data)} groups simultaneously")
print("тЪб 0.1 second response time")
print("ЁЯПн Industrial scale ready!")

# Main loop
while True:
    start_time = time.time()
    
    # рд╕рднреА groups parallel process рдХрд░реЛ
    manager.process_all_groups_parallel()
    
    # Loop timing maintain рдХрд░реЛ
    elapsed = time.time() - start_time
    if elapsed < 0.1:
        time.sleep(0.1 - elapsed)
