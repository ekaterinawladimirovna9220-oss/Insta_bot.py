import time
import os
from instagrapi import Client
from concurrent.futures import ThreadPoolExecutor

# Load credentials from GitHub Secrets
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")

cl = Client()
session_file = "session.json"

# Session-safe login
if os.path.exists(session_file):
    cl.load_settings(session_file)
else:
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings(session_file)

REPLY_TEXT = "@{} TESTING H BHAI"

print("ЁЯПн INDUSTRIAL SCALE BOT STARTED")
print("тЪб Ready for multiple groups")

class GroupManager:
    def __init__(self):
        self.thread_data = {}
        self.seen_messages = {}
        self.my_user_id = cl.user_id_from_username(USERNAME)
        self.load_all_groups()

    def load_all_groups(self):
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
        try:
            current_time = time.time()
            if current_time - self.thread_data[thread_id]['last_checked'] < 5:  # 5 sec for safety
                return
            self.thread_data[thread_id]['last_checked'] = current_time

            thread = cl.direct_thread(thread_id)
            if thread.messages:
                latest_msg = thread.messages[0]
                if (latest_msg.id not in self.seen_messages[thread_id] and
                    hasattr(latest_msg, 'user_id') and
                    latest_msg.user_id != self.my_user_id):
                    user_info = cl.user_info(latest_msg.user_id)
                    cl.direct_send(REPLY_TEXT.format(user_info.username), thread_ids=[thread_id])
                    self.seen_messages[thread_id].add(latest_msg.id)
                    print(f"ЁЯЪА @{user_info.username} тЖТ {self.thread_data[thread_id]['name']}")
        except Exception as e:
            print("Error:", e)

    def process_all_groups_parallel(self):
        with ThreadPoolExecutor(max_workers=5) as executor:  # safer for GitHub Actions
            futures = [executor.submit(self.process_single_group, thread_id)
                       for thread_id in self.thread_data.keys()]
            for future in futures:
                future.result()

# Bot start
manager = GroupManager()
print(f"\nЁЯОп Monitoring {len(manager.thread_data)} groups simultaneously")
print("тЪб Bot ready!")

# Main loop
while True:
    start_time = time.time()
    manager.process_all_groups_parallel()
    elapsed = time.time() - start_time
    if elapsed < 5:  # maintain minimum loop interval
        time.sleep(5 - elapsed)
