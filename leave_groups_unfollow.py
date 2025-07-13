import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Đọc danh sách profile
with open('profiles.txt') as f:
    profiles = [line.strip() for line in f if line.strip() and not line.startswith('#')]

def leave_all_groups(driver):
    driver.get('https://www.facebook.com/groups/feed/')
    time.sleep(5)
    while True:
        groups = driver.find_elements(By.XPATH, "//a[contains(@href, '/groups/') and not(contains(@href, 'create'))]")
        group_links = list(set([g.get_attribute('href') for g in groups if g.get_attribute('href')]))
        if not group_links:
            break
        for link in group_links:
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

def unfollow_everyone(driver):
    driver.get('https://www.facebook.com/friends/list')
    time.sleep(5)
    # Lướt và hủy theo dõi bạn bè
    for _ in range(10):
        unfollow_btns = driver.find_elements(By.XPATH, "//div[@aria-label='Bạn bè' or @aria-label='Friends']//span[contains(text(),'Bỏ theo dõi') or contains(text(),'Unfollow')]")
        for btn in unfollow_btns:
            try:
                btn.click()
                time.sleep(1)
            except:
                continue
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)

def main(profile_path):
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
    time.sleep(3)
    leave_all_groups(driver)
    unfollow_everyone(driver)
    driver.quit()

if __name__ == "__main__":
    for profile in profiles:
        print(f"Đang chạy với profile: {profile}")
        main(profile)
        time.sleep(5)
