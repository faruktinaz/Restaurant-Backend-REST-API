from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
import random
import enums


HOST = "localhost"
PORT = 8080

# TODO: Clean Code, is data empty
# split code into functions

def getMenu(filtered_menu, ingre, is_vegan):
    v_menu = []
    for meal in filtered_menu:
        isMealVegetarian = True
        for meal_ingredient in meal['ingredients']:
            for main_in in ingre:
                if meal_ingredient['name'] == main_in['name']:
                    if 'vegetarian' not in main_in['groups'] or (is_vegan and 'vegan' not in main_in['groups']):
                        isMealVegetarian = False
                    else:
                        isMealVegatarian = True
                    break
            if not isMealVegatarian:
                break
        if isMealVegetarian:
            v_menu.append(meal)
    return v_menu

def findMeal(menu, meal_id):
	for meal in menu['meals']:
         if meal['id'] == meal_id:
             return meal

def findIngredient(menu, ingredient):
    for d_ingre in menu['ingredients']:
        if d_ingre['name'] == ingredient:
            return d_ingre
    return -1

def sendStatus(Handler, message, status):
    Handler.send_response(status)
    Handler.end_headers()
    error_response = {
		'error':{
			'code': status,
            'message': message.decode()
		}
	}
    message = json.dumps(error_response, indent=2).encode()
    Handler.wfile.write(message)

def calculatePriceRandom(menu, meal_ingredients, quality):
	price = 0
	for ingredient in meal_ingredients:
		data_ingredient = findIngredient(menu, ingredient['name'])
		if data_ingredient == -1:
			continue
		price += (ingredient['quantity'] / 1000) * data_ingredient['options'][quality]['price']
	return price

def filteredHighestMenu(menu, budget):
    meals = menu['meals']
    highest_meals = []
    for meal in meals:
        price = calculatePriceRandom(menu, meal['ingredients'], 0)
        if price <= budget:
            highest_meals.append(meal)
    return(highest_meals)

def calculateQuality(Handler, f_meal, data):
	quality_score = 0
	for ingredients in f_meal['ingredients']:
		if (ingredients['name'].lower() in data):
			try:
				quality_score += enums.QualityEnum[data[ingredients['name'].lower()]].value
			except:
				sendStatus(Handler, b'You can only choose from {high, medium, low}.', 400)
				return -1
		else:
			quality_score += enums.QualityEnum['high'].value
	return quality_score // len(f_meal['ingredients'])

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        menu = read_menu('data.json')
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if (parsed_path.path == '/listMeals'):
            is_vegetarian = query_params.get('is_vegetarian', ['false'])[0].lower() == 'true'
            is_vegan = query_params.get('is_vegan', ['false'])[0].lower() == 'true'
            filtered_menu = menu['meals']
            ingre = menu['ingredients']
            if (is_vegetarian or is_vegan):
                filtered_menu = getMenu(filtered_menu, ingre, is_vegan)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(sorted(filtered_menu, key=lambda x: x['name']), indent=2).encode()) # checkl
            
        elif (parsed_path.path == '/getMeal'):
            length = len(menu['meals'])
            meal_id = int(query_params.get('id', [-1])[0])
            if (meal_id <= 0 or meal_id > length):
                sendStatus(self, b'Invalid ID provided. Please provide a valid ID. 1-' + str(length).encode(), 400)
                return
            ingre = menu['ingredients']
            selected_meal = []

            selected_meal.append(findMeal(menu, meal_id))
            for ingredient in ingre:
                exists_ingrdts_it = next((ing for ing in selected_meal[0]['ingredients'] if ing['name'] == ingredient['name']), None)
                if (exists_ingrdts_it):
                    exists_ingrdts_it.update(ingredient)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(selected_meal, indent=2).encode())

        else:
            sendStatus(self, b'Path not found.', 404)

    def do_POST(self):
        menu = read_menu('data.json')
        content_length = int(self.headers['Content-Length'])
        parsed_path = urlparse(self.path)
        meals_length = len(menu['meals'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = parse_qs(post_data)
        post_params = {key.lower(): value[0] for key, value in parsed_data.items()}
        
        if (parsed_path.path == '/quality'):
            meal_id = int(parsed_data.get('meal_id', [-1])[0])

            if (meal_id <= 0 or meal_id > meals_length):
                sendStatus(self, b'Invalid ID provided. Please provide a valid meal ID. 1-' + \
                           		str(meals_length).encode(), 400)
                return

            f_meal = findMeal(menu, meal_id)
            quality_score = calculateQuality(self, f_meal, post_params)
            if (quality_score == -1):
                return

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"quality": quality_score}, indent=2).encode())

        elif (parsed_path.path == '/price'):
            price = 0;
            meal_id = int(parsed_data.get('meal_id', [-1])[0])
            f_meal = findMeal(menu, meal_id)
            for ingredients in f_meal['ingredients']:
                data_ingredient = findIngredient(menu, ingredients['name'])
                if (data_ingredient == -1):
                    sendStatus(self, b'Ingredient information could not be found. ' + ingredients['name'].encode(), 404)
                    return
                if (ingredients['name'].lower() in post_params and \
                    				post_params[ingredients['name'].lower()] in enums.QualityEnum.__members__):
                    for options in data_ingredient['options']:
                        if (options['quality'] == post_params[ingredients['name'].lower()]):
                            price += (ingredients['quantity'] / 1000) * options['price'] + enums.serviceFee[options['quality']].value
                else:
                    price += (ingredients['quantity'] / 1000) * data_ingredient['options'][0]['price']

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"price": price}, indent=2).encode())
        
        elif (parsed_path.path == '/random'):
            budget = int(parsed_data.get('budget', [-1])[0])
            if budget > 0:
                random_menu = filteredHighestMenu(menu, budget)
            else:
                random_menu = menu['meals']
            random_meal = random.choice(random_menu)
            random_quality = 0
            random_ingredients = []
            
            price = 0
            for ingredient in random_meal['ingredients']:
                data_ingredient = findIngredient(menu, ingredient['name'])
                if (data_ingredient == -1):
                    sendStatus(self, b'Ingredient information could not be found. ' + ingredient['name'].encode(), 404)
                    return
                random_option = random.choice(data_ingredient['options'])
                random_ingredients.append(ingredientsJson(data_ingredient['name'], random_option))
                price += (ingredient['quantity'] / 1000) * random_option['price'] + enums.serviceFee[random_option['quality']].value
                random_quality += enums.QualityEnum[random_option['quality']].value
                print(random_option)
            quality_score = random_quality // len(random_meal['ingredients'])
            result = {
				'id': random_meal['id'],
				'name': random_meal['name'],
				'price': round(price, 2),
				'quality_score': quality_score,
				'ingredients': random_ingredients
			}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result, indent=2).encode())
        else:
            sendStatus(self, b'Path not found.', 404)

def ingredientsJson(name, option):
    ingredient = {
		'name': name,
		'quality': option['quality']
	}
    return ingredient

def runServer():
    server = HTTPServer((HOST, PORT), Handler)
    print(f"localhost / port = {PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()

def read_menu(path):
     with open(path, "r") as file:
          return json.load(file)

if __name__ == "__main__":
	runServer()
 