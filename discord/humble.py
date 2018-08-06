from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import discord
import time

class Scraper:

	def __init__(self, url, **kwargs):
		self.options = webdriver.ChromeOptions()
		self.options.add_argument('headless')
		
		self.browser = webdriver.Chrome(chrome_options=self.options)
		self.browser.get('https://www.humblebundle.com/games/cigames-bundle')
		time.sleep(1)
		self.html = self.browser.page_source
		self.browser.quit()

		self.soup = BeautifulSoup(self.html, 'html.parser')


	def getLogo(self):
		logo = self.soup.find('div', class_="hero-section-logo")
		logo_url = logo["style"].split("'")[1]
		return logo_url

	def getDescription(self):
		desc = self.soup.find('p', class_="detailed-marketing-blurb")
		return desc.text.strip()

	def getDaysLeft(self):
		t_days = self.soup.find('span', class_="js-days timer-field")
		
		print(t_days)

		t_days_formatted = t_days.text.strip().split(' ')[0]
		return t_days_formatted

	def getHoursLeft(self):
		t_hrs = self.soup.find('span', class_="js-hours timer-field")
		print(t_hrs)
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


def humble():
	hb_json = requests.get("https://hr-humblebundle.appspot.com/androidapp/v2/service_check").json()

	for i in hb_json:
		if i['bundle_machine_name'] in open('bundles.log'):
			print("Bundle already posted")
		else:
			print(i['url'])
			hb = Scraper(i['url'])

			embed=discord.Embed(title="{}".format(i['bundle_name']), url="{}".format(i['url']), description="{}".format(hb.getDescription()))
			embed.set_thumbnail(url="{}".format(hb.getLogo()))
			embed.add_field(name="Time Left:", value="{} Days, {} Hours".format(hb.getDaysLeft(), hb.getHoursLeft()), inline=False)
			webhook = Client('https://discordapp.com/api/webhooks/469032302832517131/8BP8fktZhfSUG86Uf3h66OYj2ceAQ2d8FcuKztifO_OTc0sPvXJt2v1vv19neFlIaneN',
				embed=embed.to_dict())
			webhook.send()

			with open('bundles.log', 'w+') as f:
				f.write(i['bundle_machine_name'])
				f.close()


# Run at 12:30EST (4:30UTC)
schedule.every().day.at("16:30").do(humble)

try:
	while True:
		schedule.run_pending()
		time.sleep(1)	
except KeyboardInterrupt:
	pass