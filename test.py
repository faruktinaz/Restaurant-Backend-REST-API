import json
import random
from enum import Enum 

with open('data.json', 'r') as data:
	mydata = json.load(data)


filtered_menu = mydata
ingre = mydata['ingredients']
meal = mydata['meals'][0]['ingredients']

# print(json.dumps(mydata, indent=2))



class QualityEnum(Enum):
    high = 'high'
    medium = 'medium'
    lwo = 'low'


print(random.choice(meal))


# try:
# 	has = QualityEnum(test).value
# 	print(has)
# except:
#     print('you can only choose HIGH MEDIUM LOW')




# test = filtered_menu['meals'][0]['ingredients'][0]
# test2 = mydata['ingredients']

# test3 = filtered_menu['meals']




# print(test3)


# def getMenu(filtered_menu, ingre, is_vegan):
#     vegetarian_menu = []
#     for i in range(len(filtered_menu['meals'])):
#         isMealVegatarian = False
#         for j in range(len(mydata['ingredients'])):
#             if mydata['ingredients'][j]['name'] == filtered_menu['meals'][i]['ingredients']['name']:
                
        
        
    
    # for meal in filtered_menu:
    #     for meal_ingredient in meal['ingredients']:
    #         isMealVegatarian = False
    #         for main_in in ingre:
    #             if meal_ingredient['name'] == main_in['name']:
    #                 isMealVegatarian = 'vegetarian' in main_in['groups'] and (is_vegan and 'vegan' in main_in['groups'])
    #                 break
    #         if not isMealVegatarian:
    #             isMealVegetarian = False
    #             break
    #     if isMealVegetarian:
    #         vegetarian_menu.append(meal)
    # return vegetarian_menu





# for x in filtered_menu:
# 	if x['id'] == 1:
# 		print(x['name'])
# 		for veg in x['ingredients']:
# 			print(veg['name'])
# 			for i in mydata['ingredients']:
# 				if veg['name'] == i['name'] and ('vegan' in i['groups']):
# 					print(i['name'])




# for x in mydata['ingredients']:
# 	print(x['name'], x['groups'])
# 	if 'vegan' in x['groups']:
# 		print('yes')
