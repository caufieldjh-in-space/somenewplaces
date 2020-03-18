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

import random, re, string, sys, time, tweepy, wikipedia, webbrowser

#Contants and Setup
tweeting = True
with open("tw.keys") as tw_api_file:
	tw_api_keys = []
	for line in tw_api_file:
		tw_api_keys.append(line.rstrip())
auth = tweepy.OAuthHandler(tw_api_keys[0], tw_api_keys[1])
auth.secure = True

#Methods
def get_words():
	places = []
	descriptors = []
	materials = []
	emotions = []
	colors = []
	smells = []
	geoareas = []
	sounds = []
	
	clothes = []
	concepts = []
	animals = []
	
	lastnames = []
	
	with open("place_words.tsv") as wordfile:
		wordfile.readline()
		for line in wordfile:
			splitline = (line.rstrip()).split("\t")
			if splitline[1] == "1":
				places.append(splitline[0])
			if splitline[2] == "1":
				materials.append(splitline[0])
			if splitline[3] == "1":
				descriptors.append(splitline[0])
			if splitline[4] == "1":
				emotions.append(splitline[0])
			if splitline[5] == "1":
				colors.append(splitline[0])
			if splitline[6] == "1":
				smells.append(splitline[0])
			if splitline[7] == "1":
				geoareas.append(splitline[0])
			if splitline[8] == "1":
				sounds.append(splitline[0])
	
	with open("object_words.tsv") as wordfile:
		wordfile.readline()
		for line in wordfile:
			splitline = (line.rstrip()).split("\t")
			if splitline[1] == "1":
				clothes.append(splitline[0])
			if splitline[2] == "1":
				concepts.append(splitline[0])
			if splitline[3] == "1":
				animals.append(splitline[0])
	
	name_input_files = ["female_fn.txt","male_fn.txt","lastnames.txt"]
	names = [] #Don't care if they're male or female or first or last
	for filename in name_input_files:
		with open(filename) as wordfile:
			wordfile.readline()
			for line in wordfile:
				if filename == "lastnames.txt":
					word = (line.rstrip()).capitalize()
				else:
					word = line.rstrip()
				names.append(word)
			
	words = [places, materials, descriptors, emotions, colors, smells, 
			geoareas, sounds, clothes, concepts, animals, names]
			
	return words
	
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
	places = words[0]
	materials = words[1]
	descriptors = words[2]
	emotions = words[3]
	colors = words[4]
	smells = words[5]
	geoareas = words[6]
	sounds = words[7]
	
	clothes = words[8]
	concepts = words[9]
	animals = words[10]
	
	names = words[11]
	
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
		
		#None of the following modifiers have final probs yet
		#Modifers
		modcount = 0
		all_mods = []
		
		#General mood
		if random.randint(0,4) == 0:
			modcount = modcount +1
			emotion1 = random.choice(emotions).lower()
			modchoice = random.randint(0,4)
			if emotion1[0].lower() in ["a","e","i","o","u","y"]:
				part1 = "an"
			else:
				part1 = "a"	
			if modchoice == 0:
				part2 = random.choice(["appears","is","seems","looks"])
				mod1 = "It %s %s." % (part2, emotion1)
			elif modchoice == 1:
				part2 = random.choice(["air","mood","atmosphere","disposition",
										"spirit","feeling"])
				mod1 = "It has %s %s %s." % (part1, emotion1, part2)
			elif modchoice == 2:
				part2 = random.choice(["may","will","can","might","could"])
				mod1 = "It %s make you feel %s." % (part2, emotion1)
			elif modchoice == 3:
				part2 = random.choice(["really","quite","entirely",
										"utterly","generally","perfectly",
										"totally","emotionally","terribly",
										"suspiciously","dubiously",
										"unbelievably","barely","genuinely",
										"quite","truly","almost","hardly"])
				mod1 = "It's %s %s." % (part2, emotion1)
			elif modchoice == 4:
				part2 = random.choice(["is","may be","recently became"])
				mod1 = "Its history %s %s." % (part2, emotion1)
			all_mods.append(mod1)
		
		#Decoration and composition
		if random.randint(0,3) == 0:
			modcount = modcount +1
			mat1 = random.choice(materials)
			modchoice = random.randint(0,5)
			if modchoice == 0:
				mod2 = "It's decorated with %s." % mat1
			elif modchoice == 1:
				mod2 = "It's made of %s." % mat1
			elif modchoice == 2:
				mod2 = "Bits of %s are strewn about." % mat1
			elif modchoice == 3:
				mod2 = "It's littered with %s." % mat1
			elif modchoice == 4:
				mat2 = random.choice(materials)
				mod2 = "It's ornately decorated with %s and %s." % (mat1, mat2)
			elif modchoice == 5:
				mat2 = random.choice(materials)
				mod2 = "It's built out of %s and %s." % (mat1, mat2)
			all_mods.append(mod2)
		
		#Colors and highlights
		if random.randint(0,2) == 0:
			modcount = modcount +1
			color1 = random.choice(colors)
			modchoice = random.randint(0,5)
			if color1[0].lower() in ["a","e","i","o","u","y"]:
				part1 = "an"
			else:
				part1 = "a"	
			if modchoice == 0:
				mod3 = "It has %s %s glow." % (part1, color1)
			elif modchoice == 1:
				mod3 = "It's very %s." % color1
			elif modchoice == 2:
				mod3 = "It has hints of %s." % color1
			elif modchoice == 3:
				mod3 = "It's a bit %s." % color1
			elif modchoice == 4:
				mod3 = "It's mostly %s in color." % color1
			elif modchoice == 5:
				part2 = random.choice(["distant","glaring","faint",
										"blinking","flickering",
										"dimming"])
				mod3 = "There's a %s %s light." % (part2, color1)
			all_mods.append(mod3)
		
		#Location and situation
		if random.randint(0,2) == 0:
			modcount = modcount +1
			place2 = random.choice(places)
			while check_strings(place1, place2):
				place2 = random.choice(places)
			modchoice = random.randint(0,5)
			if place2[0].lower() in ["a","e","i","o","u","y"]:
				part1 = "an"
			else:
				part1 = "a"	
			if modchoice == 0:
				mod4 = "It's actually %s %s." % (part1, place2)
			elif modchoice == 1:
				part2 = random.choice(["may","will","can","might","could"])
				if random.randint(0,1) == 0:
					mod4 = "It %s be %s %s." % (part2, part1, place2)
				else:
					timestr = random.choice(["now", "sometimes", "soon"])
					mod4 = "It %s be %s %s %s." % (part2, part1, place2, timestr)
			elif modchoice == 2:
				mod4 = "It looks like %s %s." % (part1, place2)
			elif modchoice == 3:
				mod4 = "It's inside %s %s." % (part1, place2)
			elif modchoice == 4:
				part2 = random.choice(["around","near","beside"])
				mod4 = "It's built %s %s %s." % (part2, part1, place2)
			elif modchoice == 5:
				part2 = random.choice(["nearby","in the area","being built"])
				mod4 = "There is also %s %s %s." % (part1, place2, part2)
			all_mods.append(mod4)
			
		#State of the setting
		if random.randint(0,5) == 0:
			modcount = modcount +1
			modchoice = random.randint(0,20)
			if modchoice == 0:
				part2 = random.choice(["truly","mostly","partly",
								"entirely","completely","strangely",
								"oddly","absolutely","altogether",
								"quite"])
				real = random.choice(["unbelievable","realistic",
								"astonishing","implausible","incredible",
								"outlandish","flimsy","credible",
								"reasonable","believable","authentic",
								"plausible","tenable","acceptable"])
				if random.randint(0,1) == 0:
					mod5 = "It's %s %s." % (part2, real)
				else:
					mod5 = "It's %s." % (real)		
			elif modchoice == 1:
				worldtype = random.choice(["virtual", "fantasy", "mystical",
								"realistic","surreal","fictional"])
				mod5 = "It's in a %s world." % worldtype
			elif modchoice == 2:
				energy = random.choice(["magic","dark forces","wizardry",
								"alchemy","conjuration","necromancy",
								"voodoo","thaumaturgy","witchcraft",
								"superstition","enchantment","sorcery",
								"demons","demonic energy","angels",
								"fairies","spirits","occultism","illusions",
								"mysticism"])
				mod5 = "It's full of %s." % energy
			elif modchoice == 3:
				if random.randint(0,1) == 0:
					mod5 = "It's part of the afterlife."
				else:
					mod5 = "You may see it when you die."
			elif modchoice == 4:
				if random.randint(0,1) == 0:
					mod5 = "It hasn't existed for very long."
				else:
					mod5 = "It's still new."
			elif modchoice == 5:
				if random.randint(0,1) == 0:
					mod5 = "It's about to reach a violent end."
				else:
					emotion2 = random.choice(emotions).lower()
					mod5 = "It's about to seem more %s." % emotion2
			elif modchoice == 6:
				if random.randint(0,1) == 0:
					mod5 = "It existed long ago."
				else:
					mod5 = "It's historic."
			elif modchoice == 7:
				if random.randint(0,1) == 0:
					mod5 = "It can't escape its fate."
				else:
					mod5 = "It may escape its fate."
			elif modchoice == 8:
				if random.randint(0,1) == 0:
					mod5 = "It's where a series of battles will begin."
				else:
					mod5 = "A battle will end here."
			elif modchoice == 9:
				animal = random.choice(animals)
				mod5 = "It's a giant %s." % animal
			elif modchoice == 10:
				weather = random.choice(["bright","sunny","clear",
										"pleasant","rainy","stormy",
										"foggy","snowy","wintry",
										"icy","unpleasant","hazy",
										"dangerous","windy","hot"])
				mod5 = "The weather is %s." % weather
			elif modchoice == 11:
				if random.randint(0,1) == 0:
					mod5 = "It's isolated."
				else:
					mod5 = "It's a crossroads."
			elif modchoice == 12:
				mod5 = "It's a source of wealth."
			elif modchoice == 13:
				mod5 = "It's the setting for a movie franchise."
			elif modchoice == 14:
				mod5 = "It's where a culture's myths take place."
			elif modchoice == 15:
				animal = random.choice(animals)
				concept = random.choice(concepts)
				mod5 = "The %s will learn about %s here." % (animal, concept)
			elif modchoice == 16:
				animal = random.choice(animals).capitalize()
				mod5 = "It involves the story of %s." % (animal)
			elif modchoice == 17:
				mod5 = "This place is hell for some."
			elif modchoice == 18:
				mod5 = "It's a sort of purgatory."
			elif modchoice == 19:
				mod5 = "It's a dream made real."
			elif modchoice == 20:
				concept = random.choice(concepts)
				mod5 = "It provides a moral lesson about %s." % (concept)
			all_mods.append(mod5)
				
		#What happens or will happen in the setting
		if random.randint(0,2) == 0:
			modcount = modcount +1
			concept1 = random.choice(concepts)
			concept2 = random.choice(concepts)
			modchoice = random.randint(0,22)
			
			if modchoice == 0:
				if random.randint(0,1) == 0:
					part2 = random.choice(["truly","mostly","partly","entirely"])
					mod6 = "It's %s ruled by %s." % (part2, concept1)
				else:
					part2 = random.choice(["illustrates","exposes","depicts",
											"allegorizes","reveals","exhibits"])
					part3 = random.choice(["danger","promise","peril","virtues"])
					mod6 = "It %s the %s of %s." % (part2, part3, concept1)
			elif modchoice == 1:
				part2 = random.choice(["built","constructed","engineered",
										"constructed","assembled"])
				mod6 = "It's %s around %s." % (part2, concept1)
			elif modchoice == 2:
				mod6 = "It's in a state of anarchy."
			elif modchoice == 3:
				part2 = random.choice(["built","created","constructed"])
				if random.randint(0,1) == 0:
					concept2 = random.choice(concepts)
					mod6 = "It's %s upon %s and %s." % (part2, concept1, concept2)
				else:
					emotion2 = random.choice(emotions).lower()
					mod6 = "It's %s upon %s %s." % (part2, emotion2, concept1)
			elif modchoice == 4:
				if random.randint(0,1) == 0:
					mod6 = "It's a result of %s and %s." % (concept1, concept2)
				else:
					mod6 = "It depends on %s to exist." % concept1
			elif modchoice == 5:
				active_place = random.choice(["bazaar","market",
						"hospital","factory","center of government"])
				mod6 = "It serves as a %s." % active_place
			elif modchoice == 6:
				if random.randint(0,1) == 0:
					mod6 = "It's our last hope."
				else:
					mod6 = "It's a source of faith."
			elif modchoice == 7:
				if random.randint(0,1) == 0:
					mod6 = "It's a center of knowledge."
				else:
					mod6 = "It's hiding some information."
			elif modchoice == 8:
				mod6 = "It will be rebuilt soon."
			elif modchoice == 9:
				mod6 = "It cannot be escaped."
			elif modchoice == 10:
				mod6 = "It's metaphorically empty."
			elif modchoice == 11:
				mod6 = "Someone was just murdered here."	
			elif modchoice == 12:
				if random.randint(0,1) == 0:
					mod6 = "It's a battleground."
				else:
					mod6 = "It's a peaceful place."
			elif modchoice == 13:
				if random.randint(0,1) == 0:
					mod6 = "It's a holy place."
				else:
					mod6 = "It's an unholy place."
			elif modchoice == 14:
				group = random.choice(["gang","police","corporate",
				"scholarly","paranormal","tourist"])
				mod6 = "There's %s activity here." % group
			elif modchoice == 15:
				event = random.choice(["party","celebration","wedding",
					"meeting","unification","conference","seminar",
					"dinner","journey","birthday party","retreat",
					"showdown","sporting event","graduation",
					"performance","discussion","debate",
					"colloquium","congress","fair","gala",
					"workshop","crime","scandal","caper","rumor",
					"disease outbreak","quest"])
				mod6 = "A %s will begin here soon."	% event
			elif modchoice == 16:
				mod6 = "It hides the answer to a riddle."
			elif modchoice == 17:
				mod6 = "It's a source of temptation."
			elif modchoice == 18:
				mod6 = "It was recently discovered."
			elif modchoice == 19:
				mod6 = "It provides a rite of passage."
			elif modchoice == 20:
				mod6 = "Someone is searching for help here."
			elif modchoice == 21:
				mod6 = "It exists only for you."
			elif modchoice == 22:
				mod6 = "You will live and die here."	
			all_mods.append(mod6)
			
		#Residents	
		if random.randint(0,2) == 0:
			part2 = random.choice(["Its","The","Some of its"])
			people = (["residents","occupants","people",
							"inhabitants","rulers","owners","overseers",
							"administrators","laborers","workers","priests",
							"aristocrats","businesspeople","doctors","lawyers",
							"lawmakers","protectors","navigators","judges",
							"warriors","managers","directors","executives",
							"governors","artisans","operatives","peasants",
							"ministers","emissaries","dignitaries","celebrities",
							"luminaries","artists","VIPs","authorities","heroes",
							"conquerors","scientists","researchers",
							"engineers","idols","gods","demigods","giants",
							"directors","janitors","surveyors","robots",
							"cyborgs","aliens","elves","thieves","gangsters",
							"politicians","soldiers","heroines","pioneers",
							"travelers","tourists","pirates","mercenaries",
							"champions"])
			peopleword = random.choice(people)
			modcount = modcount +1
			modchoice = random.randint(0,24)
			
			if modchoice == 0:
				emotion2 = random.choice(emotions).lower()
				choice = random.randint(0,2)
				if choice == 0:
					mod7 = "%s %s are perpetually %s." % (part2, peopleword, emotion2)
				elif choice == 1:
					emotion3 = random.choice(emotions).lower()
					mod7 = "%s %s are usually %s" \
							" but have been %s lately." % (part2, peopleword, emotion2, emotion3)
				elif choice == 2:
					emotion3 = random.choice(emotions).lower()
					mod7 = "%s %s are %s" \
							" and %s." % (part2, peopleword, emotion2, emotion3)
			elif modchoice == 1:
				choice = random.randint(0,2)
				if choice == 0:
					mod7 = "%s %s cannot lie." % (part2, peopleword)
				elif choice == 1:
					mod7 = "%s %s cannot tell the truth." % (part2, peopleword)
				elif choice == 2:
					mod7 = "%s %s mix truth with lies." % (part2, peopleword)
			elif modchoice == 2:
				mod7 = "%s %s are immortal." % (part2, peopleword)
			elif modchoice == 3:
				mat2 = random.choice(materials)
				cloth_sing = random.choice(clothes)
				if cloth_sing[-1:] != "s":
					cloth1 = cloth_sing + "s"
				else:
					cloth1 = cloth_sing
				if random.randint(0,1) == 0:
					mod7 = "%s %s wear %s made of %s." % (part2, peopleword, cloth1, mat2)
				else:
					mod7 = "%s %s wear %s of %s." % (part2, peopleword, cloth1, mat2)
			elif modchoice == 4:
				count1 = random.randint(3,7)
				mod7 = "%s %s have %s genders." % (part2, peopleword, count1)
			elif modchoice == 5:
				mod7 = "%s %s are undead." % (part2, peopleword)
			elif modchoice == 6:
				concept1 = random.choice(concepts)
				lostverb = random.choice(["abandoned","neglected","renounced"])
				mod7 = "%s %s have %s %s." % (part2, peopleword, lostverb, concept1)
			elif modchoice == 7:
				mod7 = "%s %s are the last of their kind." % (part2, peopleword)
			elif modchoice == 8:
				mod7 = "%s %s are very young." % (part2, peopleword)
			elif modchoice == 9:
				mod7 = "%s %s are hidden." % (part2, peopleword)
			elif modchoice == 10:
				mod7 = "%s %s cannot forget." % (part2, peopleword)
			elif modchoice == 11:
				anim_sing = random.choice(animals)
				if anim_sing[-1:] != "s":
					anim1 = anim_sing + "s"
				else:
					anim1 = anim_sing
				if random.randint(0,1) == 0:
					mod7 = "%s %s are anthropomorphic %s." % (part2, peopleword, anim1)
				else:
					mod7 = "%s %s look like %s." % (part2, peopleword, anim1)
			elif modchoice == 12:
				anim1 = random.choice(animals)
				mod7 = "%s %s worship the %s." % (part2, peopleword, anim1)
			elif modchoice == 13:
				mod7 = "%s %s created this place." % (part2, peopleword)
			elif modchoice == 14:
				mod7 = "%s %s like to show off." % (part2, peopleword)
			elif modchoice == 15:
				mod7 = "%s %s are ignoring something obvious." % (part2, peopleword)
			elif modchoice == 16:
				mod7 = "%s %s are devoutly religious." % (part2, peopleword)
			elif modchoice == 17:
				mod7 = "%s %s are giants." % (part2, peopleword)
			elif modchoice == 18:
				mod7 = "%s %s are dangerous." % (part2, peopleword)
			elif modchoice == 19:
				mod7 = "%s %s are fighting with each other." % (part2, peopleword)
			elif modchoice == 20:
				mod7 = "%s %s are powerless." % (part2, peopleword)
			elif modchoice == 21:
				people2 = random.choice(people)
				mod7 = "%s %s are pursuing the %s." % (part2, peopleword, people2)
			elif modchoice == 22:
				people2 = random.choice(people)
				mod7 = "%s %s are escaping the %s." % (part2, peopleword, people2)
			elif modchoice == 23:
				concept1 = random.choice(concepts)
				emotion1 = random.choice(emotions).lower()
				mod7 = "%s %s feel %s about %s." % (part2, peopleword, emotion1, concept1)
			elif modchoice == 24:
				peopleword2 = random.choice(people)
				mod7 = "%s %s are really %s." % (part2, peopleword, peopleword2)
			all_mods.append(mod7)
			
		#Smell
		if random.randint(0,7) == 0:
			modcount = modcount +1
			smell1 = random.choice(smells)
			mod8 = "It smells %s." % smell1
			all_mods.append(mod8)
			
		#Sounds
		if random.randint(0,8) == 0:
			modcount = modcount +1
			modchoice = random.randint(0,2)
			if modchoice == 0:
				sound1 = random.choice(["noisy","boisterous","unruly",
								"quiet","calm","serene"])
				mod9 = "It sounds %s." % sound1
			elif modchoice == 1:
				sound1 = random.choice(sounds)
				mod9 = "There are echoes of %s." % sound1
			elif modchoice == 2:
				sound1 = random.choice(sounds)
				mod9 = "There's the sound of %s." % sound1
			all_mods.append(mod9)
			
		#Personal connections or characters
		if random.randint(0,7) == 0:
			modcount = modcount +1
			modchoice = random.randint(0,0)
			if random.randint(0,5) == 0:
				indiv = random.choice(["You", "He", "She", "They", "We", "Ze", "It"])
				proper_name = False
			else:
				# * is a special char indicating a proper name
				indiv = "*%s" % random.choice(names)
				proper_name = True
			condition_list = ["may have been",
								"could have been", "voyaged","explored",
								"should have been","trained","got a ride",
								"planned to be","played","played a role",
								"wanted to go","emigrated","wished to go",
								"lived", "stayed", "stopped", "settled",
								"traveled","journeyed", "worked",
								"remained", "had fun","researched"]
			if indiv in ["He", "She", "Ze", "It"] or proper_name == True:
				for phrase in ["was", "wasn't", "was forced to be"]:
					condition_list.append(phrase)
			else:
				for phrase in ["were", "weren't", "were forced to be"]:
					condition_list.append(phrase)
			condition = random.choice(condition_list)
			if modchoice == 0:
				past = random.choice(["once before", "twice before",
										"as a child", "in a dream",
										"in a past life", "on vacation",
										"for a job", "for no good reason",
										"for good reasons", "with detailed plans",
										"as a prisoner", "with your family",
										"on business", "on assignment",
										"as a spy", "for years",
										"a long time ago", "during the war",
										"last week", "with a friend"])
				mod10 = "%s %s there %s." % (indiv, condition, past)
			all_mods.append(mod10)
		
		#Relate to Wikipedia concept
		if random.randint(0,14) == 0:
			wp_pages = get_wp_pages()
			modcount = modcount +1
			title1 = (random.choice(wp_pages)).encode('ascii', 'ignore')
			part2 = random.choice([" involves", " involves the story of",
									" tells the history of", "'s all about"])
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
		lineout = "%s %s" % (lineout, modstring)
		
		if len(lineout) <= 140:
			makeplace = False
		
	print(lineout)
	
	return lineout

#Main
def main():
	
	mode = raw_input('Operating mode:\n 1 for testing\n 3 for posting.\n')
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
			    verifier = raw_input('Verifier:')
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
	
