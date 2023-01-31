from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd


def scrap_just_dial(query, n):
    output = []
    DRIVER_PATH = r"YOUR DRIVER PATH"
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    q = query.split(' ')
    q = '-'.join(q)
    driver.get(f'https://www.justdial.com/Mumbai/search?q={q}')
    driver.maximize_window()
    # TODO: Check from here
    listing = driver.find_element_by_xpath('//*[@id="__next"]/section/section/div/div[5]/div[1]/div/div[1]')
    time.sleep(10)
        
    for i in range(1, n+1):
        print('====================================' + '\n' + str(i))
        textbox_xpath = '//*[@id="__next"]/section/section/div/div[5]/div[1]/div/div[1]/div[1]/div[1]/div[1]/div[2]'
        try:
            driver.implicitly_wait(10)
            elem = listing.find_element_by_xpath(f'//*[@id="__next"]/section/section/div/div[5]/div[1]/div/div[1]/div[{i}]/div[1]/div[1]')
            textbox = elem.find_element_by_xpath('.//div[2]')
            shop_name = textbox.find_element_by_xpath('.//div[1]/a').text
            print('shop_name: ', shop_name)
        except:
            break
        try:
            rating = textbox.find_element_by_xpath('.//div[2]/div').text
            print('rating: ', rating)
        except:
            rating = ''
        try:
            no_of_rating = textbox.find_element_by_xpath('.//div[2]/div[3]').text
            print('no_of_rating: ', no_of_rating)
        except:
            no_of_rating = ''
        try:
            address = textbox.find_element_by_xpath('.//div[3]/div').text
            print('address: ', address)
        except:
            address = ''
        try:
            opens_at = textbox.find_element_by_xpath('.//div[4]/div/div/span[2]').text
            print('opens_at: ', opens_at)
        except NoSuchElementException as e:
            opens_at = textbox.find_element_by_xpath('.//div[4]/div[1]/div[1]/span[1]').text
            print('opens_at: ', opens_at)
        except:
            opens_at = 'NA'
            print('opens_at: ', opens_at)
            
        try:
            years = textbox.find_element_by_xpath('.//div[4]/div[1]/div[3]/span').text
            print('years: ', years)
        except:
            years = 'NA'
        
        try:
            tags = ''
            tag_list = textbox.find_element_by_xpath('.//div[5]')
            x = 1
            while x <= 2:
                tags += tag_list.find_element_by_xpath(f'.//span[{x}]').text + ', '
                x += 1
            print('tags: ', tags[:-2])
        except:
            tags = ''
        output.append([shop_name, rating, no_of_rating, address, opens_at, years, tags])

    driver.close()
    return output


if __name__ == '__main__':
    search_query = input('Please input a Search Query: ')
    no_results = 0
    while no_results < 1 or no_results > 100:
        no_results = int(input('Please enter the number of results (between 1 and 100): '))
    elem_list = scrap_just_dial(search_query, no_results)
    my_df = pd.DataFrame(elem_list)
    headerList=['shop_name', 'rating', 'no_of_rating', 'address', 'opens_at', 'years', 'tags']	
    my_df.to_csv('my_csv.csv', index=False, header=headerList)
