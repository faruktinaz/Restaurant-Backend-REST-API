import json

with open('data.json', 'r') as data:
	mydata = json.load(data)


filtered_menu = mydata['meals']
ingre = mydata['ingredients']

print(json.dumps(mydata, indent=2))


for x in filtered_menu:
	if x['id'] == 1:
		print(x['name'])
		for veg in x['ingredients']:
			print(veg['name'])
			for i in mydata['ingredients']:
				if veg['name'] == i['name'] and ('vegan' in i['groups']):
					print(i['name'])




# for x in mydata['ingredients']:
# 	print(x['name'], x['groups'])
# 	if 'vegan' in x['groups']:
# 		print('yes')
