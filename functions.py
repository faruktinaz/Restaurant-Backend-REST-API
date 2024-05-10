import json
import enums

# Returns vegan or vegetarian menu
def getMenu(menu, is_vegan):
    v_menu = []
    for meal in menu['meals']:
        isMealVegetarian = True
        for meal_ingredient in meal['ingredients']:
            data_ingredient = findIngredient(menu, meal_ingredient['name'])
            if (data_ingredient == -1):
                print(f"'{meal_ingredient['name']}' not found in the data.")
                continue
            if ('vegetarian' not in data_ingredient['groups'] or (is_vegan and 'vegan' not in data_ingredient['groups'])):
                isMealVegetarian = False
                break
        if isMealVegetarian:
            v_menu.append(meal)
    return v_menu

# Returns meal whose meal id matches from data
def findMeal(menu, meal_id):
	for meal in menu['meals']:
         if meal['id'] == meal_id:
             return meal

# Returns ingredient informations from data
def findIngredient(menu, ingredient): 
    for data_ingredient in menu['ingredients']:
        if data_ingredient['name'] == ingredient:
            return data_ingredient
    return -1

# Assumes the quality of the meal to be high and prepares a menu suitable for the budget entered
def filteredHighestMenu(menu, budget): 
    meals = menu['meals']
    highest_meals = []
    for meal in meals:
        price = calculatePriceRandom(menu, meal['ingredients'], 0)
        if price <= budget:
            highest_meals.append(meal)
    return (highest_meals)

def calculatePriceRandom(menu, meal_ingredients, quality):
	price = 0
	for ingredient in meal_ingredients:
		data_ingredient = findIngredient(menu, ingredient['name'])
		if data_ingredient == -1:
			continue
		price += (ingredient['quantity'] / 1000) * data_ingredient['options'][quality]['price']
	return price

def calculateQuality(Handler, f_meal, data):
	quality_score = 0
	for ingredients in f_meal['ingredients']:
		if (ingredients['name'].lower() in data):
			try:
				quality_score += enums.QualityEnum[data[ingredients['name'].lower()]].value
			except:
				sendStatus(Handler, 'You can only choose from {high, medium, low}.', 400)
				return -1
		else:
			quality_score += enums.QualityEnum['high'].value
	return quality_score // len(f_meal['ingredients'])

def calculatePrice(Handler, menu, finded_meal, post_params):
    price = 0
    for ingredients in finded_meal['ingredients']:
        data_ingredient = findIngredient(menu, ingredients['name'])
        if (data_ingredient == -1):
            sendStatus(Handler, 'Ingredient information could not be found. ' + ingredients['name'], 404)
            return (-1)
        if (ingredients['name'].lower() in post_params):
            if (post_params[ingredients['name'].lower()] not in enums.QualityEnum.__members__):
                sendStatus(Handler, 'You can only choose from {high, medium, low}.', 400)
                return (-1)
            for options in data_ingredient['options']:
                if (options['quality'] == post_params[ingredients['name'].lower()]):
                    price += (ingredients['quantity'] / 1000) * options['price'] + enums.serviceFee[options['quality']].value
        else:
            price += (ingredients['quantity'] / 1000) * data_ingredient['options'][0]['price']
    return (round(price, 2))

def updateIngredient(data_ingredients, selected_meal):
	for ingredient in data_ingredients:
		exists_ingrdts_it = next((ing for ing in selected_meal[0]['ingredients'] if ing['name'] == ingredient['name']), None)
		if (exists_ingrdts_it):
			exists_ingrdts_it.update(ingredient)
   
def sendStatus(Handler, message, status):
    Handler.send_response(status)
    Handler.end_headers()
    error_response = {
		'error':{
			'code': status,
            'message': message
		}
	}
    message = json.dumps(error_response, indent=2).encode()
    Handler.wfile.write(message)
    
def minBudget(menu):
	meals = menu['meals']
	min_price = calculatePriceRandom(menu, meals[0]['ingredients'], 0)
	for meal in meals:
		price = calculatePriceRandom(menu, meal['ingredients'], 0)
		if min_price > price:
			min_price = price
	return (min_price)

def ingredientsJson(name, option):
    ingredient = {
		'name': name,
		'quality': option['quality']
	}
    return ingredient