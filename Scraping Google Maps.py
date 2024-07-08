from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from seleniumbase import Driver
import csv
import os


def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)


def load_page(self, element):
    global myElem
    delay = 5
    try:
        myElem = WebDriverWait(self, delay).until(EC.presence_of_element_located((By.XPATH, element)))
    except TimeoutException:
        print('Loading page failed')

    return myElem


def get_text_with_class(self, element, default=""):
    global myElem
    delay = 2
    try:
        myElem = WebDriverWait(self, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, f".{element}")))
        return myElem.text
    except Exception:
        print('Loading text with class failed')
        return default


def get_text_with_xpath(self, element, default=""):
    global myElem
    delay = 5
    try:
        myElem = WebDriverWait(self, delay).until(EC.presence_of_element_located((By.XPATH, element)))
        return myElem.text
    except Exception:
        print('Loading text with xpath failed')
        return default
    

def save_to_csv(data):
    nama_rs = "GWK"
    csv_file_path = f"Wisata_{nama_rs}_Rating Terendah.csv"

    if os.path.exists(csv_file_path):
        with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for row in data:
                writer.writerow(row)
        print("Additional data has been added to", csv_file_path)
        
    else:
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            header = ["User", "Comment", "Rating"]
            writer.writerow(header)
            for row in data:
                writer.writerow(row)


def main():
    data = []
    driver = Driver(uc=True)
    driver.get('https://www.google.com/maps/place/Taman+Budaya+Garuda+Wisnu+Kencana/@-8.8104228,115.0151633,12z/data=!4m12!1m2!2m1!1sgaruda+wisnu!3m8!1s0x2dd244cf54e1dec7:0x1988663e064f5a51!8m2!3d-8.8104228!4d115.1675986!9m1!1b1!15sCgxnYXJ1ZGEgd2lzbnVaDiIMZ2FydWRhIHdpc251kgEEcGFya-ABAA!16zL20vMGRyenpx?authuser=0&entry=ttu')
    
    try:
        for i in range(1, 20000, 3):
            sleep(1)
            try:
                review_element = load_page(driver, f'//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]/div[9]/div[{i}]')
                scroll_to_element(driver, review_element)
                
                review = review_element.find_element(By.CSS_SELECTOR, '.jJc9Ad')
                
                try:
                    user_element = review.find_element(By.CSS_SELECTOR, '.GHT2ce.NsCY4')
                    user = user_element.find_element(By.CSS_SELECTOR, '.d4r55')
                    user_text = user.text
                except:
                    pass    
                print(user_text)
                
                try:
                    button_more = review.find_element(By.CSS_SELECTOR, '.w8nwRe.kyuRq')
                    button_more.click()
                except:
                    pass
                
                try:
                    rating_element = review.find_element(By.CSS_SELECTOR, '.DU9Pgb')
                    rating = rating_element.find_element(By.CSS_SELECTOR, '.kvMYJc').get_attribute('aria-label')
                except:
                    rating = ""
                print(rating)
                
                try:
                    review_element = review.find_element(By.CSS_SELECTOR, '.MyEned')
                    review_elements = review_element.find_elements(By.TAG_NAME, 'span')
                    
                    span_texts = [span.text for span in review_elements]
                    review_text = span_texts[0]
                except:
                    review_text = ""
                    
                print(review_text)

                data.append([user_text, review_text, rating])
            except:
                pass
            
            print(f'----------------Comment index ke-{i}----------------')
        
        save_to_csv(data)    
    except:
        print(f'Error')
        save_to_csv(data)
    
    print('Scrape done!!!')
    sleep(10)
    driver.quit()
            
            
if __name__ == "__main__":
    main()
