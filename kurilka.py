from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time, os
class BaseSel():
	def __init__(self, driver, link):
		self.driver=driver
		self.link=link
	def open(self):
		self.driver.get(self.link)
	def element_active(self, selector, time=10):
		try:
			result=WebDriverWait(self.driver, time).until(
				EC.element_to_be_clickable(selector)
			)
		except:
			result=False
		finally:
			return result
	def visibility_of_element(self, selector, time=10):
		try:
			result=WebDriverWait(self.driver, time).until(
				EC.visibility_of_element_located(selector)
			)
		except:
			result=False
		finally:
			return result
def code(data):
	res_data=''
	n=1
	for i in range(len(data)):
		res_data+=chr(ord(data[i])+n)
		n+=1
		if n==5:
			n=1
	return res_data
def decode(data):
	res_data=''
	n=1
	for i in range(len(data)):
		res_data+=chr(ord(data[i])-n)
		n+=1
		if n==5:
			n=1
	return res_data
def choosing_link():
	link='https://workite.ru/afk/guid/bb7b0040-9637-41e3-a604-2eecf6e1e389/'
	print('По умолчанию ссылка на курилку розницы, если требуется другая нажми 1')
	choose_kurilka=int(input())
	if choose_kurilka==1:
		link=input('Вставь ссылку на нужную курилку')
	return link
def collect_data():
	data=[]
	answer=0
	if os.path.exists('data.txt'):
		print('Использовать данные из прошлого раза?(1-Да, 0-Нет)')
		answer=int(input())
	if answer==0:
		login=input('Логин:')
		password=input('Пароль:')
		f=open('data.txt', 'w')
		f.write(code(login)+'\n'+code(password))
		f.close()
		data.append(code(login))
		data.append(code(password))
	elif answer==1:
		f=open('data.txt', 'r')
		for line in f:
			data.append(line)
		data[0]=data[0][:-1]
		f.close()
	else:
		assert False
	return data
def check_authorisation(kurilka):
	return kurilka.visibility_of_element(selectors.error, 2)
def check_fields_available(field1, field2):
	assert field1!=False, 'Недоступно поле логина'
	assert field2!=False, 'Недоступно поле пароля'
def clicker(kurilka):
	start=int(input('Начинаем?(1-Да, 0-Нет)'))
	if start==1:
		flag=0
		i=0
		main_butt=kurilka.driver.find_element(By.ID, "but_long")
		while(flag==0):
			i+=1
			print(str(i)+' раз кликнул')
			try:    
				main_butt.click()
			except:
				pass
			if main_butt.text=='Ушел' and main_butt.get_attribute('disabled')=='true':
				print('Еще?(1-Да, 0-Нет)')
				answer=int(input())
				if answer!=1:
					flag=1
class selectors():
	login_field=(By.ID, "username")
	password_field=(By.ID, "password")
	log_button=(By.CSS_SELECTOR, "input[type='submit']")
	error=(By.CSS_SELECTOR, "label.errors")
	main_button=(By.ID, "but_long")
link=choosing_link()
data=collect_data()
browser=webdriver.Chrome()
kurilka=BaseSel(browser, link)
kurilka.open()
log_input=kurilka.element_active(selectors.login_field)
pass_input=kurilka.element_active(selectors.password_field)
check_fields_available(log_input, pass_input)
log_input.send_keys(decode(data[0]))
pass_input.send_keys(decode(data[1]))
subm=kurilka.element_active(selectors.log_button)
subm.click()
assert check_authorisation(kurilka)==False, 'Неверный логин или пароль'
kurilka.visibility_of_element(selectors.main_button)
clicker(kurilka)
browser.quit()
