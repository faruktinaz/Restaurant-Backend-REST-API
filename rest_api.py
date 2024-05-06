from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

HOST = "localhost"
PORT = 8080

# TODO: Clean Code
# split code into functions

# PATH: /getMeal
# METHOD: GET
# PARAMS:
#     id: N (integer, required)
# SAMPLE: http://localhost:8080/getMeal?id=2

# PATH: /quality
# METHOD: POST
# PARAMS:
#   meal_id: (integer, required)
#   <ingredient-1>: (enum, values: ["high", "medium", "low"], optional) default="high"
#   <ingredient-2>: (enum, values: ["high", "medium", "low"], optional) default="high"
#   ...


def getMenu(filtered_menu, ingre, is_vegan):
    vegetarian_menu = []
    for meal in filtered_menu:
        isMealVegetarian = True
        for meal_ingredient in meal['ingredients']:
            isMealVegatarian = False
            for main_in in ingre:
                if meal_ingredient['name'] == main_in['name']:
                    if 'vegetarian' not in main_in['groups'] :
                        isMealVegetarian = False
                    else:
                        isMealVegatarian = True
                        if is_vegan and 'vegan' not in main_in['groups']:
                            isMealVegatarian = False
                    break
            if not isMealVegatarian:
                isMealVegetarian = False
                break
        if isMealVegetarian:
            vegetarian_menu.append(meal)
    return vegetarian_menu

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
            meals = menu['meals']
            selected_meal = []
            for meal in meals:
                if meal_id == meal['id']:
                    selected_meal.append(meal)
                    for ingredient in ingre:
                        exists_ingrdts_it = next((ing for ing in selected_meal[0]['ingredients'] if ing['name'] == ingredient['name']), None)
                        if exists_ingrdts_it:
                            exists_ingrdts_it.update(ingredient)
                            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(selected_meal, indent=2).encode())

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Something went wrong')

    def do_POST(self):
        print('test')
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        

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
