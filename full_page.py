from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import streamlit as st
import time

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Path to your chromedriver executable
chromedriver_path = "/path/to/chromedriver"  # Adjust this to your actual path

# Streamlit UI
st.title("Screenshot & HTML Downloader with Selenium")

# Get URL input from user
url = st.text_input("Enter the URL to capture", "https://example.com")

if st.button("Capture Screenshot and Download HTML"):
    if url:
        try:
            # Create a new instance of the Chrome driver
            service = Service(chromedriver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)

            # Navigate to the provided URL
            driver.get(url)

            # Wait for the page to load
            time.sleep(3)  # You can adjust this based on your needs

            # Take screenshot
            screenshot_path = "screenshot.png"
            driver.save_screenshot(screenshot_path)

            # Get the HTML content of the page
            html_content = driver.page_source
            
            # Save the HTML to a file
            with open("page.html", "w", encoding="utf-8") as f:
                f.write(html_content)

            st.success("Screenshot and HTML saved.")
            st.image(screenshot_path)
            with open("page.html", "rb") as file:
                st.download_button(label="Download HTML", data=file, file_name="page.html", mime="text/html")

            # Close the browser
            driver.quit()
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please enter a valid URL.")
