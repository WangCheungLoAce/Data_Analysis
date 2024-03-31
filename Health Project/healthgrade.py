import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def scrape_health_data(specialty, location):
    try:
        options = Options()
        options.headless = True  
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # Your target URL
        URL = "https://www.healthgrades.com/"
        driver.get(URL)  

        specialty_input = driver.find_element(By.CSS_SELECTOR, 'input[name="term-input-group"]')
        specialty_input.clear()
        specialty_input.send_keys(specialty)
        clean_button = driver.find_element(By.CSS_SELECTOR, 'button[data-qa-target="location-input-clear"]')
        time.sleep(5)
        clean_button.click()

        time.sleep(5)

        location_input = driver.find_element(By.CSS_SELECTOR, 'input[name="location-input-group"]')
        location_input.clear()
        location_input.send_keys(location)
        search_button = driver.find_element(By.CSS_SELECTOR, 'button[data-qa-target="hero-search-bar-search-btn"]')
        time.sleep(5)
        search_button.click()

        

        all_data = []
        current_page = 1
        # Stop if the next page button is not found
        while True:
            time.sleep(5)  
            all_data.extend(parse_doctor_info(driver)) 
            if not navigate_next_page(driver):
                break  
            current_page += 1

    finally:
        if driver is not None:
            driver.quit()

    return all_data

def parse_doctor_info(driver):
    doctors = driver.find_elements(By.CSS_SELECTOR, '.results-card--pro')
    data = []
    for doctor in doctors:
        try:
            name = doctor.find_element(By.CSS_SELECTOR, 'h3.card-name').text
            specialty = doctor.find_element(By.CSS_SELECTOR, "div.provider-info__specialty span:not(.sr-only)").text
            rating = doctor.find_element(By.CSS_SELECTOR, 'span.star-rating__score').text
            num_ratings = doctor.find_element(By.CSS_SELECTOR, 'span.star-rating__reviews').text
            address = doctor.find_element(By.CSS_SELECTOR, 'div.location-info.location-info--right-align address.location-info__address span.location-info-address__address').text
            feedback_items = doctor.find_elements(By.CSS_SELECTOR, 'li.provider-strengths__strength-item')
            feedback = [item.text for item in feedback_items]
            city_state_zip = doctor.find_element(By.CSS_SELECTOR, "div.location-info.location-info--right-align address.location-info__address span.location-info-address__city-state").text
            data.append({
                'Name': name,
                'Specialty': specialty,
                'Rating': rating,
                'Address': address,
                'City_State_Zip': city_state_zip,
                'Number_of_Ratings': num_ratings,
                'Patient_Feedback': feedback
            })
        except NoSuchElementException:
            continue
    return data

# Function to navigate to the next page
def navigate_next_page(driver):
    try:
        next_page_button = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Next Page"]')
        driver.execute_script("arguments[0].click();", next_page_button)
    except NoSuchElementException:
        print("Next page button not found or last page reached.")
        return False
    return True

if __name__ == "__main__":
    scrape_health_data()
