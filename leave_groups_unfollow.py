import time
import os
import signal
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Global flag for graceful shutdown
stop_flag = False

def signal_handler(sig, frame):
    global stop_flag
    print("\nNhận tín hiệu dừng. Đang thoát một cách an toàn...")
    stop_flag = True

def check_stop_condition():
    """Kiểm tra điều kiện dừng từ file stop.txt hoặc flag"""
    global stop_flag
    if stop_flag:
        return True
    if os.path.exists('stop.txt'):
        print("Phát hiện file stop.txt. Đang dừng...")
        return True
    return False

# Đăng ký signal handler cho Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Đọc danh sách profile
with open('profiles.txt') as f:
    profiles = [line.strip() for line in f if line.strip() and not line.startswith('#')]

def leave_all_groups(driver):
    if check_stop_condition():
        return False
        
    driver.get('https://www.facebook.com/groups/feed/')
    time.sleep(5)
    while True:
        if check_stop_condition():
            break
            
        groups = driver.find_elements(By.XPATH, "//a[contains(@href, '/groups/') and not(contains(@href, 'create'))]")
        group_links = list(set([g.get_attribute('href') for g in groups if g.get_attribute('href')]))
        if not group_links:
            break
        for link in group_links:
            if check_stop_condition():
                break
                
            driver.get(link)
            time.sleep(4)
            try:
                more_btn = driver.find_element(By.XPATH, "//span[contains(text(),'Thêm') or contains(text(),'More')] | //div[@aria-label='More']")
                more_btn.click()
                time.sleep(1)
            except:
                pass
            try:
                leave_btn = driver.find_element(By.XPATH, "//*[contains(text(),'Rời khỏi nhóm') or contains(text(),'Leave group')]")
                leave_btn.click()
                time.sleep(1)
                confirm_btn = driver.find_element(By.XPATH, "//div[@aria-label='Rời khỏi nhóm' or @aria-label='Leave group']")
                confirm_btn.click()
                time.sleep(2)
            except:
                continue
        break
    return not check_stop_condition()

def unfollow_everyone(driver):
    if check_stop_condition():
        return False
        
    driver.get('https://www.facebook.com/friends/list')
    time.sleep(5)
    # Lướt và hủy theo dõi bạn bè
    for i in range(10):
        if check_stop_condition():
            break
            
        unfollow_btns = driver.find_elements(By.XPATH, "//div[@aria-label='Bạn bè' or @aria-label='Friends']//span[contains(text(),'Bỏ theo dõi') or contains(text(),'Unfollow')]")
        for btn in unfollow_btns:
            if check_stop_condition():
                break
            try:
                btn.click()
                time.sleep(1)
            except:
                continue
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)
    return not check_stop_condition()

def main(profile_path):
    if check_stop_condition():
        return False
        
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

    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        time.sleep(3)
        
        success1 = leave_all_groups(driver)
        if success1 and not check_stop_condition():
            success2 = unfollow_everyone(driver)
            return success2
        return success1
        
    except Exception as e:
        print(f"Lỗi trong quá trình chạy: {e}")
        return False
    finally:
        if driver:
            driver.quit()
            
    return not check_stop_condition()

if __name__ == "__main__":
    try:
        for profile in profiles:
            if check_stop_condition():
                print("Đã dừng trước khi xử lý profile:", profile)
                break
                
            print(f"Đang chạy với profile: {profile}")
            success = main(profile)
            if not success:
                print("Đã dừng trong quá trình xử lý profile:", profile)
                break
                
            if not check_stop_condition():
                time.sleep(5)
                
        print("Đã hoàn thành hoặc dừng tất cả các profile.")
    except KeyboardInterrupt:
        print("\nĐã nhận Ctrl+C, đang thoát...")
    except Exception as e:
        print(f"Lỗi không mong muốn: {e}")
    finally:
        if os.path.exists('stop.txt'):
            os.remove('stop.txt')
            print("Đã xóa file stop.txt")
