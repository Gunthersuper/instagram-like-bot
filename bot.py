# Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
from threading import Thread
import config


class Instagram():
	def __init__(self, username, password):
		self.username = username
		self.password = password
		options = Options()
		options.add_experimental_option("excludeSwitches", ["enable-logging"])
		# options.add_argument("--headless")
		self.browser = webdriver.Chrome("chromedriver",options=options)
		self.browser.set_window_size(800, 900)

	def close_browser(self):
		self.browser.close()
		self.browser.quit()

	def login(self):
		browser = self.browser
		browser.get('https://www.instagram.com')
		time.sleep(random.randrange(3, 5))

		username_input = browser.find_element_by_name('username')
		username_input.clear()
		username_input.send_keys(self.username)

		time.sleep(random.randrange(2, 4))

		password_input = browser.find_element_by_name('password')
		password_input.clear()
		password_input.send_keys(self.password)
		time.sleep(random.randrange(1, 2))
		password_input.send_keys(Keys.ENTER)
		time.sleep(random.randrange(3, 5))

	def xpath_exists(self, url):
		browser = self.browser
		try:
			browser.find_element_by_xpath(url)
			exist = True
		except NoSuchElementException:
			exist = False
		return exist

	def get_posts_tag(self, tag, amount):
		browser = self.browser
		time.sleep(random.randrange(2, 3))
		browser.get('https://www.instagram.com/explore/tags/' + tag)
		time.sleep(random.randrange(3, 5))

		loops_count = int(amount / 12)
		post_box = browser.find_element_by_xpath('/html/body/div[1]/section/main/article')

		for i in range(1, loops_count + 1):
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(random.randrange(5, 7))
		all_div = post_box.find_elements_by_tag_name("a")
		posts_urls = [item.get_attribute('href') for item in all_div if "/p/" in item.get_attribute('href')]
		del posts_urls[amount:]
		
		return posts_urls

	def get_posts_locations(self, location, amount):
		browser = self.browser
		time.sleep(random.randrange(2, 3))
		browser.get('https://www.instagram.com/explore/locations/' + location)
		time.sleep(random.randrange(3, 5))

		loops_count = int(amount / 12)
		post_box = browser.find_element_by_xpath('/html/body/div[1]/section/main/article')

		for i in range(1, loops_count + 1):
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(random.randrange(5, 7))
		all_div = post_box.find_elements_by_tag_name("a")
		posts_urls = [item.get_attribute('href') for item in all_div if "/p/" in item.get_attribute('href')]
		del posts_urls[amount:]
		
		return posts_urls

	def like_post(self, post):
		browser = self.browser
		try:
			browser.get(post)
			time.sleep(random.randrange(1, 2))
			browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div[2]/section[1]/span[1]/button').click()
			time.sleep(random.randrange(1, 2))
			browser.get(post)
			time.sleep(random.randrange(1, 2))
			print(f'Post - {post} successfully liked')
			time.sleep(random.randrange(3, 4))
		except ElementNotInteractableException:
			print('not interactable error')
		except Exception as ex:
			print(ex)
			

	def like_by_tags(self, tags = list(), amount = 10, delay = 600):
		browser = self.browser
		if len(tags) == 0:
			print(f'Please enter atleast 1 tag')
			self.close_browser()
		if len(tags) == 1:
			print(f'There is only one tag: {tags}\n and {amount} posts')
		if len(tags) > 1:
			print(f'There are {len(tags)} tags: {tags}\n and {amount} posts for each tag, so {len(tags)*amount} total posts')	
		n = 0
		for tag in tags:
			posts = self.get_posts_tag(tag, amount)
			time.sleep(random.randrange(1, 2))
			n = n + 1
			print(f'{n} - tag: {tag}')
			for post in posts:
				self.like_post(post)
				time.sleep(delay)


	def like_by_locations(self, locations = list(), amount = 10, delay = 600):
		browser = self.browser
		if len(locations) == 0:
			print(f'Please enter atleast 1 location')
			self.close_browser()
		if len(locations) == 1:
			print(f'There is only one location: {locations}\n and {amount} posts')
		if len(locations) > 1:
			print(f'There are {len(locations)} locations: {locations}\n and {amount} posts for each location, so {len(locations)*amount} total posts')
		n = 0
		for location in locations:
			posts = self.get_posts_locations(location, amount)
			time.sleep(random.randrange(1, 2))
			n = n + 1
			print(f'{n} - location: {location}')
			for post in posts:
				self.like_post(post)
				time.sleep(delay)


bot = Instagram(config.username, config.password)
bot.login()
if config.type_like == 'tag':
	bot.like_by_tags(config.tags, config.amount, config.delay)

if config.type_like == 'location':
	bot.like_by_locations(config.locations, config.amount, config.delay)
