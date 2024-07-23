from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
def scrape(reg):
    retry=3
    data={"REGISTER":reg,"NAME":None,"CGPA":None}
    while retry>0:
        try:
            s=Service(r"C:\Users\PRAVEEN\OneDrive\Desktop\NEW_PRA\PYTHONSELENIUM\chromedriver-win64\chromedriver.exe")
            driver=webdriver.Chrome(service=s)
            driver.get('http://www.srkrexams.in/Login.aspx')
            
            user_xpath="/html/body/form/div[4]/div/div/div[2]/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div/input"
            user_keys=driver.find_element(By.XPATH, user_xpath)
            user_keys.send_keys(reg)
            
            password_xpath = "/html/body/form/div[4]/div/div/div[2]/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/input"
            pass_key=driver.find_element(By.XPATH, password_xpath)
            pass_key.send_keys(reg)
            
            login_xpath="/html/body/form/div[4]/div/div/div[2]/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[3]/div/input"
            login_click=driver.find_element(By.XPATH,login_xpath)
            webpage=login_click.click()
            
            driver.implicitly_wait(3)
            
            cgpa_xpath="/html/body/form/div[5]/div[3]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div[1]/div[2]/div/div/table/tbody/tr[7]/td[3]/span"
            cgpa=driver.find_element(By.XPATH, cgpa_xpath)
            data['CGPA']=cgpa.text
            
            name_xpath="/html/body/form/div[5]/div[3]/div/div/div/div[1]/div/div/div/div/div/div[1]/div/div[2]/label"
            name=driver.find_element(By.XPATH, name_xpath)
            data['NAME']=name.text
    
            break
            
        except NoSuchElementException:
            print(f"No such element found for {reg}. Retrying...")
            retry -=1
        except Exception as e:
            print(e)
        finally:
            driver.quit()
    return data
        
def generate_codes():
    codes = []
    prefix = "21B91A12"
    for i in range(90,100):
        if i<10:
            codes.append(prefix+"0"+str(i))
        else:
            codes.append(prefix+str(i))
    for letter in range(ord('A'), ord('D') + 1):
        for number in range(10):
            codes.append(prefix+chr(letter)+str(number))    
    return codes
if __name__=="__main__":
    regids=generate_codes()
    results=[]
    for i in regids:
        result=scrape(i)
        results.append(result)
    df=pd.DataFrame(results)
    df.to_csv('it.csv',index=False)
