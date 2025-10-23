from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import pandas as pd
import time

#  SETUP
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
service = Service(r"C:\Users\jagdi\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")  # <-- CHANGE THIS
driver = webdriver.Chrome(service=service, options=options)

# Loading all the URLs
urls_df = pd.read_csv(r"C:\Users\jagdi\Desktop\HUBLET\prop_urls.txt", header=None, names=['url']).head()

property_data = []

# SCRAPING LOOP 
for idx, row in urls_df.iterrows():
    url = row['url']
    print(f"Scraping {idx+1}/600: {url}")
    driver.get(url)
    time.sleep(2)

    # Try to expand sections
    try:
        view_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'View all details')]")
        driver.execute_script("arguments[0].click();", view_btn)
        time.sleep(2)
    except NoSuchElementException:
        pass

    try:
        read_more = driver.find_element(By.XPATH, "//a[contains(text(),'Read More') or contains(text(),'Read less')]")
        driver.execute_script("arguments[0].click();", read_more)
        time.sleep(1)
    except NoSuchElementException:
        pass

        
    data = {
        "source": "magicbricks",
        "city": "Pune",
        "category": None,
        "url": url,
        "id": None,
        "description": None,
        "cityName": "Pune",
        "addressLocality": None,
        "Floor": None,
        "furnshingstatus": None,
        "agentName": None,
        "agentCompanyName": None,
        "agentMaskedmobilenumber": None,
        "rentalValue": None,
        "securityDeposit": None,
        "landmarks": None,
        "furnishing": None,
        "flooring": None,
        "Lift":None,
        "Age of Construction":None,
        "Area_sqft":None,
        
    }

    # Property ID
    try:
        data["id"] = driver.find_element(By.XPATH, "//span[contains(text(),'Property ID')]").text.split(":")[1].strip()
    except:
        pass

    # Name of the Property (usually the title)
    # try:
    #     data["name"] = driver.find_element(By.CSS_SELECTOR, "h1").text.strip()
    # except:
    #     pass

    # Rental Value and Security Deposit
    try:
        rental_value = driver.find_element(By.XPATH, "//li[contains(., 'Rental Value')]//div[@class='mb-ldp__more-dtl__list--value']").text
        data["rentalValue"] = rental_value
    except:
        pass

    try:
        security_deposit = driver.find_element(By.XPATH, "//li[contains(., 'Security Deposit')]//div[@class='mb-ldp__more-dtl__list--value']").text
        data["securityDeposit"] = security_deposit
    except:
        pass

    # Address and Landmarks
    try:
        address = driver.find_element(By.XPATH, "//li[contains(., 'Address')]//div[@class='mb-ldp__more-dtl__list--value']").text
        data["addressLocality"] = address
    except:
        pass

    try:
        landmarks = driver.find_element(By.XPATH, "//li[contains(., 'Landmarks')]//div[@class='mb-ldp__more-dtl__list--value']").text
        data["landmarks"] = landmarks
    except:
        pass

    # Furnishing and Flooring
    try:
        furnishing = driver.find_element(By.XPATH, "//li[contains(., 'Furnishing')]//div[@class='mb-ldp__more-dtl__list--value']").text
        data["furnishing"] = furnishing
    except:
        pass

    try:
        flooring = driver.find_element(By.XPATH, "//li[contains(., 'Flooring')]//div[@class='mb-ldp__more-dtl__list--value']").text
        data["flooring"] = flooring
    except:
        pass

    # Overlooking details
    # try:
    #     overlooking = driver.find_element(By.XPATH, "//li[contains(., 'Overlooking')]//div[@class='mb-ldp__more-dtl__list--value']").text
    #     data["overlooking"] = overlooking
    # except:
    #     pass
    
    
    # Age of construction 
    try:
        Age = driver.find_element(By.XPATH, "//li[contains(., 'Age of Construction')]//div[@class='mb-ldp__more-dtl__list--value']").text
        data["Age of Construction"] = Age
    except:
        pass

    # Area 
   # Try to extract Carpet Area or Super Built-up Area
    try:
        # Find the element containing the area value
        area_element = driver.find_element(By.XPATH, 
            "//div[@class='mb-ldp__dtls__body__list--value mb-ldp__dtls__body__list--flex mb-ldp__dtls__body__list--flex-column']/div[@class='mb-ldp__dtls__body__list']")
        
        area_value = area_element.text.strip()
        
        area_number = ''.join(filter(str.isdigit, area_value))
        data["Area_sqft"] = area_number
    except Exception as e:
        area_number = "N/A"
    # Floor no 
    try:
        floor_element = driver.find_element(By.XPATH, 
            "//li[div[contains(text(), 'Floor')]]//div[@class='mb-ldp__dtls__body__list--value']")
        
        floor_number = floor_element.text.split('(')[0].strip()
        
        print(f"Floor Number: {floor_number}")
        data["Floor"] = floor_number
    except Exception as e:
        floor_info = "N/A"
        
    # Lift
    try:
        lift_element = driver.find_element(By.XPATH, "//li[contains(., 'Lift')]//div[@class='mb-ldp__more-dtl__list--value']").text
        
        data["Lift"] = lift_element
        # print(f"Extracted Lift Count: {lift_element}")

    except:
        lift_info = "N/A"


    # Description
    try:
        description = driver.find_element(By.XPATH, "//span[contains(@class,'mb-ldp__more-dtl__description--content')]").text
        data["description"] = description
    except:
        pass

    # Agent Details
    try:
        agent_name = driver.find_element(By.XPATH, "//span[contains(@class, 'mb-ldp__contact-info--name')]").text
        data["agentName"] = agent_name
    except:
        pass

    try:
        agent_phone = driver.find_element(By.XPATH, "//span[contains(@class,'mb-ldp__contact-info--mobile')]").text
        data["agentMaskedmobilenumber"] = agent_phone
    except:
        pass

    # try:
    #     agent_company = driver.find_element(By.XPATH, "//div[contains(@class, 'mb-ldp__contact-info__company')]").text
    #     data["agentCompanyName"] = agent_company
    # except:
    #     pass
    print(f"DATA - {data} \n\n")
    property_data.append(data)

# --------------- SAVE TO CSV -----------------
df = pd.DataFrame(property_data)

df.to_csv("pune_pune6.csv", index=False)
print("Data saved to pune_pune6.csv")

driver.quit()
