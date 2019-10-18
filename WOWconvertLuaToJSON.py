import json
import re

data = {}

itemsTitle = "Loot Tables"
contentTitle = "Content Type"

current = "";
items = False;
name = "";

with open("data.lua", "r") as f:
	for l in f:
		line = l.replace(" ", "")
		line = line.strip()

		if "data[" in line:
			items = False
			start = line.find("\"") + 1
			end = line[start:len(line)].find("\"") + start
			current = line[start:end]
			data[current] = {}

		if "ContentType=" in line:
			start = line.find("=") + 1
			end = line.find(",")
			data[current][contentTitle] = line[start:end]

		if "items=" in line:
			items = True
			data[current][itemsTitle] = {}

			while True:
				line = f.readline()
				line = line.strip()

				if "name" in line:
					start = line.find("\"") + 1
					end = line[start:len(line)].find("\"") + start
					name = line[start:end]
					data[current][itemsTitle][name] = {}

				test = re.compile("{\s*[0-9]{1,2},\s*[0-9]{4,5}\s*},\s*--\s*.+")
				if test.match(line):
					matchId = re.compile("[0-9]{4,5}")
					id = matchId.search(line).group(0)
					
					start = line.find("-") + 2
					itemName = line[start:len(line)]
					itemName = itemName.strip()

					data[current][itemsTitle][name][id] = {"id":id, "name":itemName}


				if line == "}":
					items = False
					break


print(json.dumps(data))

f = open("WoWInstanceItems.json", "w")
f.write(json.dumps(data))
f.close()