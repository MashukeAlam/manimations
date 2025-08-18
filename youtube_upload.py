from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import traceback

# Path to your Chrome profile
profile_path = r'C:\Users\MashukJim\YoutubeProfile'
profile_directory = 'Default'

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument(f'user-data-dir={profile_path}')
options.add_argument(f'profile-directory={profile_directory}')
options.add_argument('--disable-extensions')  # Disable extensions for a cleaner profile
options.add_argument('--no-sandbox')  # Bypass OS security
options.add_experimental_option("detach", True)


# Initialize the Chrome driver
driver = None
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
print("WebDriver initialized successfully. Browser should open with the specified profile.")

time.sleep(5)  # Wait for the browser to open

# Navigate to the YouTube upload page
upload_url = "https://studio.youtube.com/channel/UCWPJ-VHUywWsTo6Bix1PM_Q/videos/upload?d=ud&filter=%5B%5D&sort=%7B%22columnType%22%3A%22date%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D"

driver.get(upload_url)
print(f"Navigating to: {upload_url}")

# Keep the browser open for a while to see the result
# time.sleep(20) 