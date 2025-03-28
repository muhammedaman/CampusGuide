from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def fetch_etlab_data(username, password):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background (no browser window)
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # Open login page
        driver.get("https://kmctce.etlab.app/user/login")
        time.sleep(2)
        
        # Enter login credentials
        driver.find_element(By.ID, "LoginForm_username").send_keys(username)
        driver.find_element(By.ID, "LoginForm_password").send_keys(password)
        
        # Click login button
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)
        
        # Check if login was successful
        if "login" in driver.current_url:
            driver.quit()
            return {"error": "Invalid username or password"}

        data = {"attendance": [], "assignments": [], "sessional_exams": [], "module_tests": []}

        # ✅ Fetch Attendance Data
        try:
            driver.get("https://kmctce.etlab.app/ktuacademics/student/viewattendancesubject/37")
            time.sleep(3)
            attendance_table = driver.find_element(By.CLASS_NAME, "items")
            headers = [th.text.strip() for th in attendance_table.find_elements(By.TAG_NAME, "th")]
            rows = [[td.text.strip() for td in tr.find_elements(By.TAG_NAME, "td")] for tr in attendance_table.find_elements(By.TAG_NAME, "tr")[1:]]
            data["attendance"] = pd.DataFrame(rows, columns=headers).to_dict(orient="records")
        except Exception as e:
            print("Error fetching attendance:", str(e))
            data["attendance"] = []

        # ✅ Fetch Assignment Data
        try:
            driver.get("https://kmctce.etlab.app/student/assignments")
            time.sleep(3)
            assignment_table = driver.find_element(By.CLASS_NAME, "items")
            headers = [th.text.strip() for th in assignment_table.find_elements(By.TAG_NAME, "th")]
            rows = [[td.text.strip() for td in tr.find_elements(By.TAG_NAME, "td")] for tr in assignment_table.find_elements(By.TAG_NAME, "tr")[1:]]
            data["assignments"] = pd.DataFrame(rows, columns=headers).to_dict(orient="records")
        except Exception as e:
            print("Error fetching assignments:", str(e))
            data["assignments"] = []

        # ✅ Fetch Sessional Exams Data
        try:
            driver.get("https://kmctce.etlab.app/ktuacademics/student/results")
            time.sleep(3)
            sessional_table = driver.find_element(By.ID, "yw0")
            headers = [th.text.strip() for th in sessional_table.find_elements(By.TAG_NAME, "th")]
            rows = [[td.text.strip() for td in tr.find_elements(By.TAG_NAME, "td")] for tr in sessional_table.find_elements(By.TAG_NAME, "tr")[1:]]
            data["sessional_exams"] = pd.DataFrame(rows, columns=headers).to_dict(orient="records")
        except Exception as e:
            print("Error fetching sessional exams:", str(e))
            data["sessional_exams"] = []

        # ✅ Fetch Module Test Data
        try:
            module_test_table = driver.find_element(By.ID, "yw1")
            headers = [th.text.strip() for th in module_test_table.find_elements(By.TAG_NAME, "th")]
            rows = [[td.text.strip() for td in tr.find_elements(By.TAG_NAME, "td")] for tr in module_test_table.find_elements(By.TAG_NAME, "tr")[1:]]
            data["module_tests"] = pd.DataFrame(rows, columns=headers).to_dict(orient="records")
        except Exception as e:
            print("Error fetching module tests:", str(e))
            data["module_tests"] = []

    except Exception as e:
        print("Unexpected error:", str(e))
        return {"error": str(e)}

    finally:
        driver.quit()
    
    return data
