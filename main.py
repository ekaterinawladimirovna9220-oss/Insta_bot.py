import time
import threading
from instagrapi import Client
from concurrent.futures import ThreadPoolExecutor

USERNAME = "x0a6l"
PASSWORD = "Guru@123"

cl = Client()
cl.login(USERNAME, PASSWORD)

REPLY_TEXT = "@{} 𝐌sɢ 𝐌ᴀᴛ 𝐊ᴀʀ 𝐖ᴀʀɴᴀ 𝐄sᴘᴀᴅᴀ/𝐀ɴᴜʀᴀɢ 𝐊ɪ 𝐌ᴀᴀ 𝐂ᴏᴅ 𝐃ᴜɴɢᴀ🤪🤪"

print("🏭 INDUSTRIAL SCALE BOT STARTED")
print("⚡ Ready for 500+ groups")
print("🎯 0.1 second response time")

class GroupManager:
    def __init__(self):
        self.thread_data = {}
        self.seen_messages = {}
        self.my_user_id = cl.user_id_from_username(USERNAME)
        self.load_all_groups()
        
    def load_all_groups(self):
        """सभी groups load करता है"""
        threads = cl.direct_threads()
        print(f"📊 Loaded {len(threads)} groups")
        
        for thread in threads:
            thread_id = thread.id
            thread_name = getattr(thread, 'title', getattr(thread, 'name', f'Group-{thread_id}'))
            
            self.thread_data[thread_id] = {
                'name': thread_name,
                'last_checked': 0
            }
            self.seen_messages[thread_id] = set()
            
            print(f"   ✅ {thread_name}")
    
    def process_single_group(self, thread_id):
        """एक group process करता है"""
        try:
            current_time = time.time()
            
            # हर 0.1 seconds में check करो
            if current_time - self.thread_data[thread_id]['last_checked'] < 0.1:
                return
                
            self.thread_data[thread_id]['last_checked'] = current_time
            
            # Group messages fetch करो
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
                    
                    print(f"🚀 @{user_info.username} → {self.thread_data[thread_id]['name']}")
                    
        except Exception as e:
            # Errors ignore करो - continue processing
            pass
    
    def process_all_groups_parallel(self):
        """सभी groups को parallel process करता है"""
        with ThreadPoolExecutor(max_workers=50) as executor:  # 50 parallel threads
            futures = []
            for thread_id in self.thread_data.keys():
                future = executor.submit(self.process_single_group, thread_id)
                futures.append(future)
            
            # Wait for all to complete
            for future in futures:
                future.result()

# Bot start करो
manager = GroupManager()

print(f"\n🎯 Monitoring {len(manager.thread_data)} groups simultaneously")
print("⚡ 0.1 second response time")
print("🏭 Industrial scale ready!")

# Main loop
while True:
    start_time = time.time()
    
    # सभी groups parallel process करो
    manager.process_all_groups_parallel()
    
    # Loop timing maintain करो
    elapsed = time.time() - start_time
    if elapsed < 0.1:
        time.sleep(0.1 - elapsed)
