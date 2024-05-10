from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
import random
import enums
import functions

HOST = "localhost"
PORT = 8080

# is data empty

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        menu = read_menu('data.json')
        if (menu == -1):
            functions.sendStatus(self, 'Failed to load the JSON file', 500)
            return
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if (parsed_path.path == '/listMeals'):
            is_vegetarian = query_params.get('is_vegetarian', ['false'])[0].lower() == 'true'
            is_vegan = query_params.get('is_vegan', ['false'])[0].lower() == 'true'
            data_ingredients = menu['ingredients']
            filtered_menu = menu['meals']

            if (is_vegetarian or is_vegan):
                filtered_menu = functions.getMenu(menu, is_vegan)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(sorted(filtered_menu, key=lambda x: x['name']), indent=2).encode()) # checkl

        elif (parsed_path.path == '/getMeal'):
            length = len(menu['meals'])
            try:            
                meal_id = int(query_params.get('id', [-1])[0])
            except:
                functions.sendStatus(self, 'ID must be integer.', 400)
                return
            data_ingredients = menu['ingredients']
            selected_meal = []

            if (meal_id <= 0 or meal_id > length):
                functions.sendStatus(self, f'Invalid ID provided. Please provide a valid ID. [1-{str(length)}]', 400)
                return

            selected_meal.append(functions.findMeal(menu, meal_id))
            functions.updateIngredient(data_ingredients, selected_meal)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(selected_meal, indent=2).encode())

        else:
            functions.sendStatus(self, f'Path not found: {parsed_path.path}', 404)

    def do_POST(self):
        menu = read_menu('data.json')
        if (menu == -1):
            functions.sendStatus(self, 'Failed to load the JSON file', 500)
            return
        content_length = int(self.headers['Content-Length'])
        parsed_path = urlparse(self.path)
        meals_length = len(menu['meals'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = parse_qs(post_data)
        post_params = {key.lower(): value[0] for key, value in parsed_data.items()}
        
        if (parsed_path.path == '/quality'):
            try:
                meal_id = int(parsed_data.get('meal_id', [-1])[0])
            except:
                functions.sendStatus(self, 'ID must be integer.', 400)
                return

            if (meal_id <= 0 or meal_id > meals_length):
                functions.sendStatus(self, f'Invalid ID provided. Please provide a valid meal ID. [1-{str(meals_length)}]', 400)
                return

            f_meal = functions.findMeal(menu, meal_id)
            quality_score = functions.calculateQuality(self, f_meal, post_params)
            if (quality_score == -1):
                return

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"quality": quality_score}, indent=2).encode())

        elif (parsed_path.path == '/price'):
            try:
                meal_id = int(parsed_data.get('meal_id', [-1])[0])
            except:
                functions.sendStatus(self, 'ID must be integer.', 400)
                return
            if (meal_id <= 0 or meal_id > meals_length):
                functions.sendStatus(self, f'Invalid ID provided. Please provide a valid meal ID. [1-{str(meals_length)}]', 400)
                return

            finded_meal = functions.findMeal(menu, meal_id)
            price = functions.calculatePrice(self, menu, finded_meal, post_params)
            if (price == -1):
                return

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"price": price}, indent=2).encode())
        
        elif (parsed_path.path == '/random'):
            budget = float(parsed_data.get('budget', [-1])[0])
            minimum_budget = functions.minBudget(menu)
            if budget >= minimum_budget:
                random_menu = functions.filteredHighestMenu(menu, budget)
            elif budget < minimum_budget:
                functions.sendStatus(self, 'minimum budget is: ' + str(minimum_budget), 400)
                return
            else:
                random_menu = menu['meals']

            random_meal = random.choice(random_menu)
            random_quality = 0
            random_ingredients = []
            price = 0

            for ingredient in random_meal['ingredients']:
                data_ingredient = functions.findIngredient(menu, ingredient['name'])
                if (data_ingredient == -1):
                    functions.sendStatus(self, 'Ingredient information could not be found: ' + ingredient['name'], 404)
                    return
                random_option = random.choice(data_ingredient['options'])
                random_ingredients.append(functions.ingredientsJson(data_ingredient['name'], random_option))
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
            functions.sendStatus(self, f'Path not found: {parsed_path.path}', 404)

def runServer():
    server = HTTPServer((HOST, PORT), Handler)
    print(f"localhost / port = {PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()

def read_menu(path):
     with open(path, "r") as file:
        try:
            json_file = json.load(file)
            return json.load(json_file)
        except:
            print('Failed to load the JSON file')
            return -1

if __name__ == "__main__":
	runServer()
 