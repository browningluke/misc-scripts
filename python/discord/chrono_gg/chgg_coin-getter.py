import requests
import discord
import schedule
from time import gmtime, strftime, sleep
import os
import json
import re

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

class Chrono:

	def __init__(self):
		self.sale_url = "https://api.chrono.gg/sale"
		self.steam_url = "https://store.steampowered.com/api/appdetails?appids={}"

		# Embed properties
		self.name = "Chrono.gg"
		self.tts = "false"
		self.avatar_url = "https://pbs.twimg.com/profile_images/705158228959748096/OPCXSf4V_400x400.jpg"


	@staticmethod
	def load_json():
		try:
			with open("{}/{}".format(os.path.dirname(os.path.abspath(__file__)), "config.json"), 'r+') as f:
				_c = json.load(f)
				f.close()
			return _c
		except (OSError, IOError) as e:
			return None
		except Exception as e:
			raise e

	def get_sale(self):
		chrono_json = requests.get(self.sale_url).json()
		
		# Ensure chrono API has pulled correctly
		try:
			game_id = dict(list(chrono_json['items'])[0])['id']
		except KeyError as e:
			print("CHRONO API ERROR: game_id not found. {}".format(e))
			return None

		steam_json = requests.get(self.steam_url.format(game_id)).json()

		try:
			description = steam_json[game_id]['data']['short_description']
		except KeyError as e:
			print("STEAM API ERROR: description not found. {}".format(e))
			description = "Description could not be found."
		else:
			# Description processing
			if "<strong>" in description:
				description = re.sub('<strong>|</strong>', "**", description)
			if "&quot;" in description:
				description = re.sub('&quot;', "'", description)

		embed=discord.Embed(title="{}".format(chrono_json['name']), url="{}".format(chrono_json['unique_url']), description=description, color=discord.Color(0x420677))
		
		embed.set_image(url="{}".format(chrono_json['promo_image']))
		embed.set_thumbnail(url=self.avatar_url)
		
		embed.add_field(name="Sale Price", value="${}".format(chrono_json['sale_price']), inline=True)
		embed.add_field(name="Discount", value="{}".format(chrono_json['discount']), inline=True)
		embed.add_field(name="Normal Price", value="${}".format(chrono_json['normal_price']), inline=True)
		embed.add_field(name="Rating", value="[{}]({})".format(steam_json[game_id]["data"]["metacritic"]["score"], steam_json[game_id]["data"]["metacritic"]["url"]), inline=True)
		
		embed.set_footer(text="({}/{}) | {}".format("{}", "{}", chrono_json['steam_url']))

		return embed

	def get_coins(self):
		config = self.load_json()

		success = 0
		total = 0

		for x in config['jwt']:
			res = requests.get("https://api.chrono.gg/quest/spin", headers={'Authorization': 'JWT {}'.format(x["token"])})

			if res.status_code == 420:
				print("Coins already collected")
			
			elif res.status_code == 200:
				res_json = res.json()
				
				print("Coins collected: {}".format(res_json['quest']['value'] + res_json['quest']['bonus']))
				
				if res_json["chest"] != {}:
					print("Bonus chest: {} coins for a {} day streak.".format(res_json['chest']['base'] + res_json['chest']['bonus'], res_json['chest']['kind']))
				
				#print("Json:", res_json)

				success += 1
			
			elif res.status_code == 401:
				print("Status code 401: Unauthorised. Check your jwt. ({})".format(x["name"]))
			else: 
				print("Coin error: status code = {}".format(res.status_code))

			total += 1

		return success, total

	def run_check(self):
		embed = self.get_sale()
		coins_success, coins_total = self.get_coins()
		
		if embed is None:
			return None
		
		embed.set_footer(text = embed.footer.text.format(coins_success, coins_total))
		config = self.load_json()
		
		if config['url'] is not None:
			webhook = Client(config['url'], name=self.name, tts=self.tts, embed=embed.to_dict(), avatar_url=self.avatar_url)
			webhook.send()

			print("{}: Message successfully sent. Name: {}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime()), embed.title))
		else:
			print("Cannot find url. Skipping.")


def main():
	chrono = Chrono()
	
	# Run at 12:30EST (4:30UTC)
	schedule.every().day.at("17:30").do(chrono.run_check)
	chrono.run_check()
	
	try:
		while True:
			schedule.run_pending()
			sleep(1)	
	except KeyboardInterrupt:
		pass

if __name__ == '__main__':
	main()