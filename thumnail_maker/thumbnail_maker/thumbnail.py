from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import base64
from urllib.parse import urlencode, quote_plus

# URL for the thumbnail
def prepare_url(text="Nextjs vs Laravel", g1="#ff5f6d", g2="#ffc371", g3="#705df2"):
    base_url = "https://tycon.dreamjim.xyz/thumbnail.html"
    params = {
        "text": text,
        "g1": g1,
        "g2": g2,
        "g3": g3
    }
    return f"{base_url}?{urlencode(params, quote_via=quote_plus)}"


def download_image_from_canvas(url, file_name="thumbnail.png"):
    # Output file name
    output_file = file_name

    # Directory to save downloads
    download_dir = os.path.abspath("downloads")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    driver = None  # Initialize driver to None
    try:
        # Set up Chrome options for headless browsing
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        print("Setting up Chrome options...")

        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        print("Chrome options configured.")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        print("WebDriver initialized.")
        driver.get(url)
        print(f"Navigating to {url}...")
        print("Canvas element found, proceeding to download...")
        time.sleep(3)
        print(f"Image successfully downloaded as {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up
        if driver:
            driver.quit()

if __name__ == "__main__":
    title = "TensorFlow Basics"

    g1 = "#6100ff"
    g2 = "#cd70ff"
    g3 = "#f25fb5"
    
    for i in range(1, 11):
        text = f"{title} - {i}"
        url = prepare_url(text=text, g1=g1, g2=g2, g3=g3)
        print(f"Downloading thumbnail {i}...")
        download_image_from_canvas(url)
        print(f"Thumbnail {i} downloaded.")
        time.sleep(2)