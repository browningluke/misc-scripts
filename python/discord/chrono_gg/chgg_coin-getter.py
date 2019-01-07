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

def chrono():
	ch_json = requests.get("https://api.chrono.gg/sale").json()
	
	# Ensure chrono API has pulled correctly
	try:
		game_id = dict(list(ch_json['items'])[0])['id']
	except KeyError as e:
		print("CHRONO API ERROR: game_id not found. {}".format(e))
		game_id = None

	if game_id is not None:
		st_json = requests.get("https://store.steampowered.com/api/appdetails?appids={}".format(game_id)).json()

		try:
			description = st_json[game_id]['data']['short_description']
		except KeyError as e:
			print("STEAM API ERROR: description not found. {}".format(e))
			description = "Description could not be found."
		else:
			# Description processing
			if "<strong>" in description:
				description = re.sub('<strong>|</strong>', "**", description)

		embed=discord.Embed(title="{}".format(ch_json['name']), url="{}".format(ch_json['unique_url']), description=description, color=discord.Color(0x35194A))
		embed.set_thumbnail(url="{}".format(ch_json['og_image']))
		embed.add_field(name="Sale Price", value="${}".format(ch_json['sale_price']), inline=True)
		embed.add_field(name="Discount", value="{}".format(ch_json['discount']), inline=True)
		embed.add_field(name="Normal Price", value="${}".format(ch_json['normal_price']), inline=True)
		embed.set_footer(text="{}".format(ch_json['steam_url']))

		config = load_json()

		if config['url'] is not None:
			webhook = Client(config['url'], name="Chrono.gg", tts="false", embed=embed.to_dict())
			webhook.send()

			print("{}: Message successfully sent. Name: {}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime()), ch_json['name']))
		else:
			print("Cannot find url. Skipping.")

def coin():
	config = load_json()

	for x in config['jwt']:
		res = requests.get("https://api.chrono.gg/quest/spin", headers={'Authorization': 'JWT {}'.format(x)})

		if res.status_code == 420:
			print("Coins already collected")
		
		elif res.status_code == 200:
			res_json = res.json()
			
			print("Coins collected: {}".format(res_json['quest']['value'] + res_json['quest']['bonus']))
			
			if res_json["chest"] != {}:
				print("Bonus chest: {} coins for a {} day streak.".format(res_json['chest']['base'] + res_json['chest']['bonus'], res_json['chest']['kind']))
			
			#print("Json:", res_json)
		
		elif res.status_code == 401:
			print("Status code 401: Unauthorised. Check your jwt. {}".format(x))
		else: 
			print("Coin error: status code = {}".format(res.status_code))

# Run at 12:30EST (4:30UTC)
schedule.every().day.at("17:30").do(chrono)
schedule.every().day.at("17:30").do(coin)


def main():
	chrono()
	coin()

	try:
		while True:
			schedule.run_pending()
			sleep(1)	
	except KeyboardInterrupt:
		pass

if __name__ == '__main__':
	main()