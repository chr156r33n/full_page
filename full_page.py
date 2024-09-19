from playwright.sync_api import sync_playwright
import streamlit as st
import nest_asyncio

# Allow nested asyncio event loops
nest_asyncio.apply()

# Function to take screenshot and save the HTML content
def take_screenshot_and_save_html(url, width, height, screenshot_path, html_path, user_agent=None):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False if you want to see the browser
        page = browser.new_page()

        # Set custom viewport (resolution)
        page.set_viewport_size({'width': width, 'height': height})

        # Optionally set user-agent if provided
        if user_agent:
            page.set_user_agent(user_agent)

        # Navigate to the provided URL
        page.goto(url)

        # Get the HTML content of the page
        html_content = page.content()

        # Save the HTML to a file
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Take full-page screenshot
        page.screenshot({'path': screenshot_path, 'full_page': True})

        # Close the browser
        browser.close()

# Streamlit UI
st.title("Mobile Googlebot Screenshot & HTML Downloader")

# Get URL input from user
url = st.text_input("Enter the URL to capture", "https://example.com")

# Set default resolution for mobile Googlebot
st.write("Resolution is preset to mobile Googlebot:")
width = 412  # Example: Google Pixel 4 width in pixels
height = 869  # Example: Similar height Googlebot Mobile uses for rendering

# Predefined Googlebot mobile user-agent string
googlebot_mobile_user_agent = ("Mozilla/5.0 (Linux; Android 10; Pixel 4 XL Build/QQ3A.200805.001)"
                               " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.135 Mobile Safari/537.36"
                               " (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")

# Path to save screenshot and HTML (you can modify these if needed)
screenshot_path = 'screenshot.png'
html_path = 'page.html'

# Button to trigger screenshot and HTML download
if st.button("Capture Screenshot and Download HTML as Mobile Googlebot"):
    if url:
        try:
            take_screenshot_and_save_html(url, width, height, screenshot_path, html_path, googlebot_mobile_user_agent)
            st.success(f"Screenshot saved as {screenshot_path} and HTML saved as {html_path}")
            st.image(screenshot_path)
            with open(html_path, "rb") as file:
                st.download_button(label="Download HTML", data=file, file_name="page.html", mime="text/html")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please enter a valid URL.")
