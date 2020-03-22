#!/usr/bin/python
#some_new_places.py
'''
Generates place and setting ideas.

To be done:
Poke into the WP page to see if it needs a "the" before naming it
e.g. "Barack Obama" vs. "the President"

Fix English silliness (e.g. "an universe", "an utopia")
 also plurals like "foxs"
Add a bit more variety to words and phrases.
Vary sentence structure (sentences are a bit run-on with all those mods

More than anything else, this needs to be cleaned up.
But it may never happen.
That's life I suppose.
'''

import os, random, re, string, sys, time, tweepy, wikipedia, webbrowser
from pathlib import Path

#Contants and Setup
tweeting = True
with open("tw.keys") as tw_api_file:
	tw_api_keys = []
	for line in tw_api_file:
		tw_api_keys.append(line.rstrip())
auth = tweepy.OAuthHandler(tw_api_keys[0], tw_api_keys[1])
auth.secure = True

res = Path('resources')

#Methods
def get_words():
	words = {}
	wordtypes = []
	
	wordtypefiles = res.glob('*.txt')
	for filename in wordtypefiles:
		wordtype = os.path.splitext(os.path.basename(filename))[0]
		wordtypes.append(wordtype)
		words[wordtype] = []
		with open(filename) as wordfile:
			head = wordfile.readline().rstrip()
			for line in wordfile:
				splitline = (line.rstrip()).split("\t")
				words[head].append(splitline[0])
			
	return words
	
def get_templates():
	'''Template files include both text and denotation of word types to be
	 included.'''
	 
	templates = {}
	templatetypes = []
	
	templatetypefiles = res.glob('*.tsv')
	for filename in templatetypefiles:
		templatetype = os.path.splitext(os.path.basename(filename))[0]
		templatetypes.append(templatetype)
		templates[templatetype] = []
		with open(filename) as templatefile:
			head = templatefile.readline().rstrip()
			for line in templatefile:
				splitline = (line.rstrip()).split("\t")
				templates[head].append(splitline)
	
	return templates
	
def get_wp_pages():
	#Returns a list of Wikipedia page titles, to be used as concepts
	pagenames = []
	for item in wikipedia.random(pages=8):
		if len(item) < 18:
			pagenames.append(item)
	
	return pagenames
		
def title_this(s):
	return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
		lambda mo: mo.group(0)[0].upper() +
			mo.group(0)[1:].lower(), s)

def check_strings(s1, s2):
	#Compares two strings to see if they match any words.
	#Returns True if any words are shared
	a_match = False
	s1_elems = [x for x in s1.split()]
	s2_elems = [x for x in s2.split()]
	
	for elem in s1_elems:
		if elem in s2_elems:
			a_match = True
	
	return a_match

def make_place():
	
	makeplace = True
	
	words = get_words()
	
	'''These conversions really shouldn't be necessary.'''
	
	places = words['places']
	materials = words['materials']
	descriptors = words['descriptors']
	emotions = words['emotions']
	colors = words['colors']
	smells = words['smells']
	geoareas = words['geoareas']
	sounds = words['sounds']
	clothing = words['clothing']
	concepts = words['concepts']
	animals = words['animals']
	names = words['names']
	residents = words['residents']
	magic_types = words['magic_types']
	light_mods = words['light_mods']
	
	templates = get_templates()
	
	while makeplace == True:
		linechoice = random.randint(0,3)
		
		adj1 = random.choice(descriptors)
		place1 = random.choice(places)
		geo = random.choice(geoareas)
		
		if adj1[0].lower() in ["a","e","i","o","u","y"]:
			part1 = "An"
		else:
			part1 = "A"	
			
		if linechoice == 0:
			lineout = "%s %s %s." % (part1, adj1, place1)
			
		elif linechoice == 1:
			adj2 = random.choice(descriptors)
			while check_strings(adj1, adj2):
				adj2 = random.choice(descriptors)
			
			if random.randint(0,1) == 0:
				lineout = "%s %s %s %s." % (part1, adj1, adj2, place1)
			else:
				lineout = "%s %s, %s %s." % (part1, adj1, adj2, place1)
		
		if linechoice == 2:
			lineout = "%s %s %s in %s." % (part1, adj1, place1, geo)
		
		if linechoice == 3:
			situation = random.choice(["version of", "place in",
										"concept of","interpretation of",
										"depiction of","stand-in for",
										"rendition of","portrayal of",
										"presentation of","parody of",
										"location a bit like",
										"location a lot like",
										"location much like",
										"location strangely like",
										"view of", "perspective of",
										"location in", "area of",
										"site in", "representation of",
										"setting in", "place within",
										"place just outside",
										"loose interpretation of"])
			lineout = "%s %s %s %s." % (part1, adj1, situation, geo)
		
		#Modifers
		modcount = 0
		all_mods = []
		
		#General mood
		if random.randint(0,0) == 0:
			modcount = modcount +1
			modchoice = random.choice(templates["mood_templates"])
			modtext = modchoice[0]
			new_word_types = modchoice[1:]
			new_words = {}
			for word_type in new_word_types:
				if word_type in new_words.keys():
					new_words[word_type].append(random.choice(words[word_type]))
				else:
					new_words[word_type] = [random.choice(words[word_type])]
			mod = modtext.format(**new_words)
				
			all_mods.append(mod)
		
		#Decoration and composition
		if random.randint(0,5) == 0:
			modcount = modcount +1
			modchoice = random.choice(templates["materials_templates"])
			modtext = modchoice[0]
			new_word_types = modchoice[1:]
			new_words = {}
			for word_type in new_word_types:
				if word_type in new_words.keys():
					new_words[word_type].append(random.choice(words[word_type]))
				else:
					new_words[word_type] = [random.choice(words[word_type])]
			mod = modtext.format(**new_words)
				
			all_mods.append(mod)
		
		#Colors and highlights
		if random.randint(0,5) == 0:
			modcount = modcount +1
			modchoice = random.choice(templates["color_mod_templates"])
			modtext = modchoice[0]
			new_word_types = modchoice[1:]
			new_words = {}
			for word_type in new_word_types:
				if word_type in new_words.keys():
					new_words[word_type].append(random.choice(words[word_type]))
				else:
					new_words[word_type] = [random.choice(words[word_type])]
			mod = modtext.format(**new_words)
				
			all_mods.append(mod)
		
		#Location and situation
		if random.randint(0,2) == 0:
			modcount = modcount +1
			modchoice = random.choice(templates["situation_templates"])
			modtext = modchoice[0]
			new_word_types = modchoice[1:]
			new_words = {}
			for word_type in new_word_types:
				if word_type in new_words.keys():
					new_words[word_type].append(random.choice(words[word_type]))
				else:
					new_words[word_type] = [random.choice(words[word_type])]
			mod = modtext.format(**new_words)
				
			all_mods.append(mod)
			
		#State of the setting
		if random.randint(0,4) == 0:
			modcount = modcount +1
			modchoice = random.choice(templates["state_templates"])
			modtext = modchoice[0]
			new_word_types = modchoice[1:]
			new_words = {}
			for word_type in new_word_types:
				if word_type in new_words.keys():
					new_words[word_type].append(random.choice(words[word_type]))
				else:
					new_words[word_type] = [random.choice(words[word_type])]
			mod = modtext.format(**new_words)
				
			all_mods.append(mod)
				
		#What happens or will happen in the setting
		if random.randint(0,2) == 0:
			modcount = modcount +1
			modchoice = random.choice(templates["plot_templates"])
			modtext = modchoice[0]
			new_word_types = modchoice[1:]
			new_words = {}
			for word_type in new_word_types:
				if word_type in new_words.keys():
					new_words[word_type].append(random.choice(words[word_type]))
				else:
					new_words[word_type] = [random.choice(words[word_type])]
			mod = modtext.format(**new_words)
				
			all_mods.append(mod)
			
		#Residents	
		if random.randint(0,2) == 0:
			modcount = modcount +1
			modchoice = random.choice(templates["resident_templates"])
			modtext = modchoice[0]
			new_word_types = modchoice[1:]
			new_words = {}
			for word_type in new_word_types:
				if word_type in new_words.keys():
					new_words[word_type].append(random.choice(words[word_type]))
				else:
					new_words[word_type] = [random.choice(words[word_type])]
			mod = modtext.format(**new_words)
				
			all_mods.append(mod)			
			
		#Smell
		if random.randint(0,7) == 0:
			modcount = modcount +1
			modchoice = random.choice(templates["smell_templates"])
			modtext = modchoice[0]
			new_word_types = modchoice[1:]
			new_words = {}
			for word_type in new_word_types:
				if word_type in new_words.keys():
					new_words[word_type].append(random.choice(words[word_type]))
				else:
					new_words[word_type] = [random.choice(words[word_type])]
			mod = modtext.format(**new_words)
				
			all_mods.append(mod)
			
		#Sounds
		if random.randint(0,8) == 0:
			modcount = modcount +1
			modchoice = random.choice(templates["sound_and_music_templates"])
			modtext = modchoice[0]
			new_word_types = modchoice[1:]
			new_words = {}
			for word_type in new_word_types:
				if word_type in new_words.keys():
					new_words[word_type].append(random.choice(words[word_type]))
				else:
					new_words[word_type] = [random.choice(words[word_type])]
			mod = modtext.format(**new_words)
				
			all_mods.append(mod)
			
		#Personal connections or characters
		if random.randint(0,3) == 0:
			modcount = modcount +1
			modchoice = random.choice(templates["person_templates"])
			modtext = modchoice[0]
			new_word_types = modchoice[1:]
			new_words = {}
			for word_type in new_word_types:
				if word_type in new_words.keys():
					new_words[word_type].append(random.choice(words[word_type]))
				else:
					new_words[word_type] = [random.choice(words[word_type])]
			mod = modtext.format(**new_words)
				
			all_mods.append(mod)
		
		#Relate to Wikipedia concept
		if random.randint(0,14) == 0:
			wp_pages = get_wp_pages()
			modcount = modcount +1
			#title1 = (random.choice(wp_pages)).encode('ascii', 'ignore')
			title1 = random.choice(wp_pages)
			part2 = random.choice([" involves", " involves the story of",
									" tells the history of", "'s all about",
									" may remind you of", 
									"s local history concerns",
									" involves"])
			mod11 = "It%s %s." % (part2, title1)
			all_mods.append(mod11)
		
		#Shuffle the mods, combine some, and add to the first string
		random.shuffle(all_mods)
		
		if modcount > 1:
			comb_mods = []
			i = 1
			
			for mod in all_mods:
				if i == 1:
					if mod[0] == "*":
						mod = mod[1:]
					if modcount == 2:
						new_mod = mod.replace(".","")
					else:
						new_mod = mod.replace(".",",")
				elif i == modcount:
					if mod[0] != "*":
						new_mod = "and " + mod[0].lower() + mod[1:]
					else:
						new_mod = "and " + mod[1:]
				else:
					if mod[0] != "*":
						new_mod = (mod[0].lower() + mod[1:]).replace(".",",")
					else:
						new_mod = (mod[1:]).replace(".",",")
				comb_mods.append(new_mod)
				i = i +1
				
			all_mods = comb_mods
		
		elif modcount == 1:
			if all_mods[0][0] == "*":
				all_mods[0] = all_mods[0][1:]
				
		modstring = " ".join(all_mods)
		
		#Need to do grammar checks here, like for a/an
		#
		#
		#
		
		lineout = "%s %s" % (lineout, modstring)
		
		if len(lineout) <= 140:
			makeplace = False
		
	print(lineout)
	
	return lineout

#Main
def main():
	
	mode = input('Operating mode:\n 1 for testing\n 3 for posting.\n')
	mode = int(mode)
	generating = True
	
	# For twitter OAuth
	if tweeting:
		try:
			tweepy_file = open("tw.auth")
			print("Found Twitter auth values.")
			tw_auths = []
			for line in tweepy_file:
				#print(line)
				tw_auths.append(line.rstrip())
			auth.set_access_token(tw_auths[0], tw_auths[1])
			need_auth = False
		except IOError as e:
			print("Could not find Twitter auth values - need to authorize.")
			need_auth = True
		
		if need_auth:
			try:
			    redirect_url = auth.get_authorization_url()
			    webbrowser.open(redirect_url, new =0)
			    verifier = input('Verifier:')
			except tweepy.TweepError:
			    print('Error! Failed to get request token.')
			    
			try:
			    auth.get_access_token(verifier)
			except tweepy.TweepError:
			    print('Error! Failed to get access token.')
			    
			auth.set_access_token(auth.access_token, auth.access_token_secret)
			tweepy_file = open("tw.auth", 'w')
			tweepy_file.write(auth.access_token + "\n")
			tweepy_file.write(auth.access_token_secret + "\n")
			tweepy_file.close()
			
	api = tweepy.API(auth)

	if mode == 1: 	#So we're in testing mode.
		print("Testing mode. Won't post.")
	
	while generating:
		
		lineout = make_place()
		
		if mode == 3:
			try:
				api.update_status(status=lineout)
				print("Posted.")
			except tweepy.TweepError as te:
				#api.update_status(status="Listen to the world around you.") #Throws TweepError usu. if message is >140 char, so just post something else rather than messing around with truncation
				print(te)
				print("Text longer than 140 chars or some other Twitter problem came up. Didn't post.")
		else:
			print("This one wasn't posted.")
			
		if mode == 1:
			wait_time = random.randint(60,3600)	#Wait up to 20 minutes
			minutes, seconds = divmod(wait_time, 60)
			hours, minutes = divmod(minutes, 60)
			print("Would have posted again in %02d minutes, %02d seconds." % (minutes, seconds))
			sys.exit("Exiting...")
		if mode == 3:
			wait_time = random.randint(60,3600)	#Wait up to 20 minutes
			minutes, seconds = divmod(wait_time, 60)
			hours, minutes = divmod(minutes, 60)
			print("Posting again in %02d minutes, %02d seconds." % (minutes, seconds))
			time.sleep(wait_time)

if __name__ == "__main__":
	sys.exit(main())
	
