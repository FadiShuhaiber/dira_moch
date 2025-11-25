from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


options = Options()
options.add_argument("--headless")  # Ensure Chrome runs in headless mode (without GUI)t
options.add_argument("--no-sandbox")  # Prevents errors on GitHub Actions
options.add_argument("--disable-dev-shm-usage")
                     
# Step 1: Open Chrome
driver = webdriver.Chrome(options=options)
driver.get("https://www.dira.moch.gov.il/ProjectsList")
#driver.maximize_window()

def wait_for_non_empty_text(by, value, timeout=15):
    return WebDriverWait(driver, timeout).until(
        lambda d: d.find_element(by, value).text.strip() != ""
    )

# Step 2: Click the "אישור" button
try:
    wait = WebDriverWait(driver, 15)
    confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'אישור')]")))
    confirm_button.click()
except Exception as e:
    print("Button click failed:", e)
    driver.quit()
    exit()

# Step 3: Get the number value
try:
    wait_for_non_empty_text(By.CSS_SELECTOR, "b.blue-label.col-md-1.count.ng-binding")
    count_element = driver.find_element(By.CSS_SELECTOR, "b.blue-label.col-md-1.count.ng-binding")
    number_value = count_element.text.strip()
    print(f"Number value found: {number_value}")
except TimeoutException:
    print("Timeout: Number value not found or empty.")
    driver.quit()
    exit()

# Step 4: Send value by email
def send_email(value):
    sender = "sotiris.automation@gmail.com"
    password = "aagx rgid mnow ljjh"

    #password = "Automation102030!#"  # Use an app-specific password
    #receiver = "fadi_sh11@hotmail.com, naief.espanioli@gmail.com"
    receiver = "fadi_sh11@hotmail.com"
    
    msg = MIMEMultipart("alternative")
    msg['Subject'] = "🟢 Project Update – Meher Lemishtaken"
    msg['From'] = "Sotiris Robot <your_email@gmail.com>"
    msg['To'] = receiver

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; }}
            .container {{
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: #f9f9f9;
                max-width: 600px;
                margin: auto;
            }}
            .footer {{
                font-size: 0.9em;
                color: #888;
                margin-top: 30px;
                border-top: 1px solid #ddd;
                padding-top: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>📢 Automated Project Alert</h2>
            <p>Hello,</p>
            <p>This is <strong>Sotiris Robot</strong> 🧠.</p>
            <p>I’d like to inform you that the current number of <strong>open projects</strong> at <strong>Meher Lemishtaken</strong> is:</p>
            <h1 style="color: #2a9d8f;">{value}</h1>
            <p>This message was generated and sent automatically by our monitoring system.</p>
            <div class="footer">
                Please do not reply to this email. If you have questions, contact the system administrator.<br>
                &copy; 2025 Sotiris Automation System
            </div>
        </div>
    </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
            print("Email sent successfully.")
    except Exception as e:
        print("Email sending failed:", e)

send_email(number_value)

# Step 5: Close browser
driver.quit()
