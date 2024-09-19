import asyncio
import streamlit as st
from pyppeteer import launch

# Function to take screenshot and save the HTML content
async def take_screenshot_and_save_html(url, width, height, screenshot_path, html_path, user_agent=None):
    # Launch headless browser
    browser = await launch()
    page = await browser.newPage()

    # Set custom viewport (resolution)
    await page.setViewport({'width': width, 'height': height})

    # Optionally set user-agent if provided
    if user_agent:
        await page.setUserAgent(user_agent)

    # Navigate to the provided URL
    await page.goto(url)

    # Get the HTML content of the page
    html_content = await page.content()

    # Save the HTML to a file
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Take full-page screenshot
    await page.screenshot({'path': screenshot_path, 'fullPage': True})

    # Close the browser
    await browser.close()

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
        # Run the screenshot and HTML download task asynchronously
        asyncio.get_event_loop().run_until_complete(
            take_screenshot_and_save_html(url, width, height, screenshot_path, html_path, googlebot_mobile_user_agent)
        )
        
        # Show success message
        st.success(f"Screenshot saved as {screenshot_path} and HTML saved as {html_path}")
        
        # Display screenshot
        st.image(screenshot_path)

        # Provide download link for HTML file
        with open(html_path, "rb") as file:
            btn = st.download_button(
                label="Download HTML",
                data=file,
                file_name="page.html",
                mime="text/html"
            )
    else:
        st.error("Please enter a valid URL.")
