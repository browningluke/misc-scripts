from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import discord
import time
import schedule
import os
from configparser import ConfigParser
from time import gmtime, strftime

class Scraper:

	def __init__(self, url, **kwargs):
		# Comment these lines
		self.options = webdriver.ChromeOptions()
		self.options.add_argument('headless')
		self.options.add_argument("disable-gpu")
		self.browser = webdriver.Chrome(chrome_options=self.options)
		# And uncomment this line to debug
		#self.browser = webdriver.Chrome()

		self.browser.get(url)
		time.sleep(1)
		self.html = self.browser.page_source
		self.browser.quit()

		self.soup = BeautifulSoup(self.html, 'html.parser')


	def getLogo(self):
		logo = self.soup.find('div', class_="hero-section-logo")
		try:
			logo_url = logo["style"].split("'")[1]
			return logo_url
		except TypeError:
			return None

	def getDescription(self):
		fore = self.soup.find('div', class_="hero-foreground")
		desc = fore.find('p', class_="detailed-marketing-blurb")
		#print(desc)
		return desc.text.strip()

	def getDaysLeft(self):
		t_days = self.soup.find('span', class_="js-days timer-field")
		
		#print(t_days)

		t_days_formatted = t_days.text.strip().split(' ')[0]
		return t_days_formatted

	def getHoursLeft(self):
		t_hrs = self.soup.find('span', class_="js-hours timer-field")
		#print(t_hrs)
		return t_hrs.text.strip()

class Client:

    def __init__(self, url, **kwargs):
        self.url = url
        self.message = kwargs.get('message')
        self.name = kwargs.get('name')
        self.avatar_url = kwargs.get('avatar_url')
        self.tts = kwargs.get('tts')
        self.embed = kwargs.get('embed')

    def send(self):
        data = {'content': self.message,
                'username': self.name,
                'avatar_url': self.avatar_url,
                'tts': self.tts,
                'embeds': [self.embed] if self.embed else None
                }
        r = requests.post(self.url, json=data)
        if r.status_code != 204:
            raise Exception('HTTP Error: Status Code {}'.format(r.status_code))
        else:
            return True

def load_url():

	try:
		with open("{}/{}".format(os.path.dirname(os.path.abspath(__file__)), "web_url.ini"), 'r+') as f:
			_c = ConfigParser()
			_c.read_file(f)
			f.close()
		return _c.get('Credentials', 'url')
	except (OSError, IOError) as e:
		return None
	except Exception as e:
		raise e

def humble():
	hb_json = requests.get("https://hr-humblebundle.appspot.com/androidapp/v2/service_check").json()

	for i in hb_json:
		if i['bundle_machine_name'] in open('bundles.log'):
			print("Bundle already posted")
		else:
			hb = Scraper(i['url'])

			embed=discord.Embed(title="{}".format(i['bundle_name']), url="{}".format(i['url']), description="{}".format(hb.getDescription()))
			logo = hb.getLogo()
			if logo is not None:
				embed.set_thumbnail(url="{}".format(logo))
			embed.add_field(name="Time Left:", value="{} Days, {} Hours".format(hb.getDaysLeft(), hb.getHoursLeft()), inline=False)
			

			url = load_url()
			if url is not None:
				webhook = Client(url, embed=embed.to_dict())
				webhook.send()

				print("{}: Message successfully sent. Name: {}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime()), i['bundle_name']))
			else:
				print("Cannot find url. Skipping.")

			with open('bundles.log', 'w+') as f:
				f.write("{}\n".format(i['bundle_machine_name']))
				f.close()


# Run at 12:30EST (4:30UTC)
schedule.every().day.at("16:30").do(humble)

humble()

try:
	while True:
		schedule.run_pending()
		time.sleep(1)	
except KeyboardInterrupt:
	pass