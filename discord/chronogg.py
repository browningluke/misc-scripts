import requests
import discord
import schedule
import time

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

		embed=discord.Embed(title="{}".format(ch_json['name']), url="{}".format(ch_json['unique_url']), description=description)
		embed.set_thumbnail(url="{}".format(ch_json['og_image']))
		embed.add_field(name="Sale Price", value="${}".format(ch_json['sale_price']), inline=True)
		embed.add_field(name="Discount", value="{}".format(ch_json['discount']), inline=True)
		embed.add_field(name="Normal Price", value="${}".format(ch_json['normal_price']), inline=True)
		embed.set_footer(text="{}".format(ch_json['steam_url']))


		webhook = Client('https://discordapp.com/api/webhooks/469032213930049558/VINTvU7qIJ3int-UR2LLPqsxIemCxUhkb4V-sLnUP1rhHCMyJ_BL0oBCdrc4QuZrjWW4',
			embed=embed.to_dict())
		webhook.send()

# Run at 12:30EST (4:30UTC)
schedule.every().day.at("16:30").do(chrono)

try:
	while True:
		schedule.run_pending()
		time.sleep(1)	
except KeyboardInterrupt:
	pass