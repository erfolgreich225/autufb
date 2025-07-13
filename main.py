import time
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Đọc danh sách profile
with open('profiles.txt') as f:
    profiles = [line.strip() for line in f if line.strip() and not line.startswith('#')]


# Đọc nội dung comment mẫu
with open('comments.txt') as f:
    comments = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Đọc danh sách ảnh mẫu
try:
    with open('images.txt') as f:
        images = [line.strip() for line in f if line.strip() and not line.startswith('#')]
except FileNotFoundError:
    images = []


# Random chọn comment text hoặc ảnh
def random_comment_or_image():
    options = []
    if comments:
        options.append('text')
    if images:
        options.append('image')
    if not options:
        return ('text', 'No comment')
    choice = random.choice(options)
    if choice == 'text':
        cmt = random.choice(comments)
        rand_chars = ''.join(random.choices(string.ascii_letters, k=2))
        return ('text', f"{cmt} {rand_chars}")
    else:
        img_path = random.choice(images)
        return ('image', img_path)

def load_posted_ids():
    try:
        with open('posted_ids.txt') as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return set()

def save_posted_id(post_id):
    with open('posted_ids.txt', 'a') as f:
        f.write(post_id + '\n')

def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))

def is_ad(post):
    # Tùy chỉnh điều kiện nhận diện quảng cáo
    try:
        ad_label = post.find_element(By.XPATH, ".//*[contains(text(),'Được tài trợ') or contains(text(),'Sponsored')]")
        return ad_label is not None
    except:
        return False


def comment_in_groups(profile_path):
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={profile_path}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--lang=vi")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    driver = webdriver.Chrome(options=chrome_options)
    time.sleep(2)

    # Đọc danh sách link nhóm từ file groups.txt
    with open('groups.txt') as f:
        group_links = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    posted_ids = load_posted_ids()
    for group_url in group_links:
        driver.get(group_url)
        time.sleep(5)
        scroll_count = 0
        while True:
            posts = driver.find_elements(By.XPATH, "//div[@role='article']")
            for post in posts:
                try:
                    if is_ad(post):
                        continue
                    post_id = post.get_attribute('data-ft') or post.get_attribute('id')
                    if not post_id or post_id in posted_ids:
                        continue
                    # Tìm ô comment
                    try:
                        comment_box = post.find_element(By.XPATH, ".//form//div[@aria-label='Viết bình luận...']")
                    except:
                        continue
                    cmt_type, cmt_content = random_comment_or_image()
                    comment_box.click()
                    time.sleep(random.uniform(0.5, 1.5))
                    if cmt_type == 'text':
                        human_typing(comment_box, cmt_content)
                        comment_box.send_keys(Keys.ENTER)
                    elif cmt_type == 'image':
                        try:
                            attach_btn = post.find_element(By.XPATH, ".//input[@type='file' and @accept='image/*']")
                            attach_btn.send_keys(cmt_content)
                            time.sleep(random.uniform(1.5, 2.5))
                            comment_box.send_keys(Keys.ENTER)
                        except Exception as e:
                            continue
                    save_posted_id(post_id)
                    posted_ids.add(post_id)
                    time.sleep(random.uniform(3, 6))
                except Exception as e:
                    continue
            driver.execute_script("window.scrollBy(0, 1000);")
            scroll_count += 1
            time.sleep(random.uniform(2, 4))
            if scroll_count > 20:
                break
    driver.quit()

if __name__ == "__main__":
    for profile in profiles:
        print(f"Đang chạy với profile: {profile}")
        comment_in_groups(profile)
        time.sleep(random.uniform(10, 30))
