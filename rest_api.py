from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
from enum import Enum


HOST = "localhost"
PORT = 8080

# TODO: Clean Code
# split code into functions

# PATH: /getMeal
# TODO: id: N (integer, required) check
# METHOD: GET
# PARAMS:
#     id: N (integer, required)
# SAMPLE: http://localhost:8080/getMeal?id=2

# PATH: /quality
# METHOD: POST
# PARAMS:
#   meal_id: (integer, TODO: ->required)
#   <ingredient-1>: (enum, values: ["high", "medium", "low"], optional) default="high"
#   <ingredient-2>: (enum, values: ["high", "medium", "low"], optional) default="high"
#   ...


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

class QualityEnum(Enum):
    high = 5
    medium = 3
    low = 1

def sendStatus(Handler, message, status):
	Handler.send_response(int(status))
	Handler.end_headers()
	Handler.wfile.write(message)

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
            self.wfile.write(json.dumps(sorted(filtered_menu, key=lambda x: x['name']), indent=2).encode())
            
        elif (parsed_path.path == '/getMeal'):
            meal_id = int(query_params.get('id', [0])[0])
            ingre = menu['ingredients']
            selected_meal = []

            selected_meal.append(findMeal(menu, meal_id))
            for ingredient in ingre:
                exists_ingrdts_it = next((ing for ing in selected_meal[0]['ingredients'] if ing['name'] == ingredient['name']), None)
                if exists_ingrdts_it:
                    exists_ingrdts_it.update(ingredient)
                            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(selected_meal, indent=2).encode())

        else:
            sendStatus(self, b'Something went wrong', 404)

    def do_POST(self):
        menu = read_menu('data.json')
        content_length = int(self.headers['Content-Length'])
        parsed_path = urlparse(self.path)
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = parse_qs(post_data)
        data = {key: value[0] for key, value in parsed_data.items()}
        
        if (parsed_path.path == '/quality'):
            quality_score = 0
            meal_id = int(parsed_data.get('meal_id', [-1])[0])
            if meal_id <= 0 or meal_id > len(menu['meals']):
                sendStatus(self, b'Something went wrong: bad request: enter a valid meal_id value 1-' + str(len(menu['meals'])).encode('utf-8'), 400)
                return
            f_meal = findMeal(menu, meal_id)
            for ingredients in f_meal['ingredients']:
                if ingredients['name'].lower() in data:
                    try:
                        quality_score += QualityEnum[data[ingredients['name'].lower()]].value
                    except:
                        sendStatus(self, b'Something went wrong: bad request: you can only choose {high, medium, low}', 400)
                        break
                else:
                    quality_score += 5
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"quality": quality_score}, indent=2).encode())
        else:
            sendStatus(self, b'Something went wrong', 404)
        

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
