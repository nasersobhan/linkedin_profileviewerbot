from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pickle
import os

driver = webdriver.Chrome('D:\py\chromedriver_win32\chromedriver.exe')
link_list = []
link_list_v = []
#load profile links from file links.txt
if os.path.getsize('links.txt') > 0:  
	with open('links.txt', 'rb') as fp:
		link_list = pickle.load(fp)
#load Already Visited Links from file links_v.txt
if os.path.getsize('links_v.txt') > 0:  
	with open('links_v.txt', 'rb') as fp:
		link_list_v = pickle.load(fp)

def login_and_search():	
	#open login page for linkedin
	driver.get('https://www.linkedin.com/uas/login?goback=&trk=hb_signin')
	#maximize the window
	driver.maximize_window()
	#enter username
	email = driver.find_element_by_xpath('//*[@id="username"]')
	email.send_keys('YOUREMAIL') # change it to your username
	#enter password
	password = driver.find_element_by_xpath('//*[@id="password"]')
	password.send_keys('YOURPASSWORD') #change it to your password
	#click login
	login = driver.find_element_by_xpath('//*[@id="app__container"]/main/div/form/div[3]/button')
	login.click()


	return driver

def get_page_links(linkz):
		
	global link_list
	global link_list_v

	driver.get(linkz)
	soup = BeautifulSoup(driver.page_source, 'lxml')
	print ('OPEN: '+driver.current_url)
	link_list_v.append(linkz)

	
	ul = soup.find('ul', class_='results-list')
	if ul:
		for a in ul.find_all('a')[0:(len(ul.find_all('a'))-2)]:
			new_link='https://www.linkedin.com' + a['href']
			if new_link not in link_list and new_link not in link_list_v:
				link_list.append(new_link)
				print (new_link)	
	else:
		print('Not List found')

	ul = soup.find('ul', class_='mt4')
	if ul:
		for a in ul.find_all('a')[0:(len(ul.find_all('a'))-2)]:
			new_link='https://www.linkedin.com' + a['href']
			if new_link not in link_list and new_link not in link_list_v:
				link_list.append(new_link)
				print (new_link)	
	else:
		print('Not List found')
	
	with open('links.txt', 'wb') as fp:
		pickle.dump(link_list, fp)
	with open('links_v.txt', 'wb') as fp:
		pickle.dump(link_list_v, fp)
	print( str(len(link_list_v)) + ' Visited out of ' + str(len(link_list)))
	return link_list



########################################### MAIN ###################################

login_and_search()


if link_list:
	for linkz in link_list:
		if linkz not in link_list_v or not link_list_v:
			get_page_links(linkz)
			time.sleep(5)
else:
	get_page_links('https://www.linkedin.com/search/results/people/?keyword=python')
#driver.quit()

####################################################################################


