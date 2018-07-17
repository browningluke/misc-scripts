import sys

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']
morse = ['.-', '-...', '-.-.', '-..', '.', '..-.', '--.', '....', '..', '.---', '-.-', '.-..', '--', '-.', '---', '.--.', '--.-', '.-.', '...', '-', '..-', '...-', '.--', '-.--', '-.--', '--..', '/']

ma_conv = dict(zip(morse, alphabet))
am_conv = dict(zip(alphabet, morse))

def to_english():

	string = input("Enter morse code: ")
	s = string.split()

	for i in s:
		print(ma_conv[i], end='', flush=True)

def to_morse():

	string = input("Enter english: ")
	s = list(string)

	for i in s:
		i = i.lower()
		print("{} ".format(am_conv[i]), end='', flush=True)

def main():
	c = input("1) Morse to english\n2) English to morse\n")

	if c == '1':
		to_english()
	elif c == '2':
		to_morse()
	else:
		print('please enter a valid number')
		main()

if __name__ == "__main__":
	main()
