# Omer-Faruk-Genc-otsimo-internship-task-2024
## Transparent Restaurant Backend

Verilen data setinde meal_id'si 5 olan yemeğin içerisindeki 'Pork chops' malzemesi, Malzemelerin bilgilerini içeren data['ingredients']'in içerisinde bulunmuyor. 

Bu durumun hatalı olup olmadığından emin değilim. Yine de bu durumu kontrol edip 'pork chops' un bilgilerine erişilmeye çalışıldığına hata durumu döndürdüm. 

Anlatırken kullandigim Kod blokları kodun güncel halini temsil etmeyebilir.

Değerlendirme için şimdiden teşekkür ederim.
### How to run

##### Windows
* Python yüklü değilse, [Python'un resmi web sitesinden](https://www.python.org/downloads/) Python'u indirin ve yükleyin.
* Github Reposunu indirelim veya klonlayalım.
* cmd veya powershell kullanarak projenin dizinine gidelim. Ardından çalıştırabilmek için 
```
python rest_api.py
```

##### Linux
* Git clone atarak projeyi çektikten sonra, Terminal açıp projenin dizinine gidelim
* Python kodunu çalıştırmak için 'python3' kullanabiliriz
```
$ python3 rest_api.py
```

![otsimotask3](https://github.com/faruktinaz/Omer-Faruk-Genc-otsimo-internship-task-2024/assets/114104599/57b49491-809d-4b40-9ddd-7f43294bf684)

---

### List Meals

```
PATH: /listMeals
METHOD: GET
PARAMS:
is_vegetarian: (boolean, optional) default=false
is_vegan: (boolean, optional) default=false
SAMPLE: http://localhost:8080/listMeals?is_vegetarian=true
```

Yemeğin içindeki malzemelerin her birini, `menu['ingredients']` içindeki öğelerle isimlerine göre eşleştirerek, eşleşen malzemelerin `ingredient['groups']` içerisinde vejetaryen veya vegan olup olmadığını kontrol etmem gerekiyor.

Kontrolleri ve koşul durumları doğru ise `vegatarian_menu.append()` kullanarak menüye ekleyip son durumda filtered_menu'yu `getMenu()` fonksiyonundan dönen menüye eşitledim.

![image](https://github.com/faruktinaz/otsimo-2024/assets/114104599/1d4ea13f-847c-4b2c-8dee-7c641f870f41)

---

### Get Meal

```
PATH: /getMeal
METHOD: GET
PARAMS:
id: N (integer, required)
SAMPLE: http://localhost:8080/getMeal?id=2
```

Girilen ID numarasını öncelikle yemeklerin ID numaralarıyla eşleştirdim. Ardından eşleşen ID numaralı yemeği selected_meal değişkenine ekledim.

Şimdi ise yemeğin içerisinde bulunan malzemelerin opsiyonlarını yemeğin içerisine eklenmesi gerekiyor.

Bunun için yemeğin içerisindeki malzemelerin tamamını, veri setimizden gelen malzemelerin isimleriyle karşılaştırdım. Eşleşen malzemeleri exists_ingrdts_it değişkenine iteratör kullanarak atadım, ve opsiyonları `exists_ingrdts_it.update(ingredient)` işlevini kullanarak üzerine ekledim.

---

### Quality

```
PATH: /quality
METHOD: POST
PARAMS:
meal_id: (integer, required)
<ingredient-1>: (enum, values: ["high", "medium", "low"], optional) default="high"
<ingredient-2>: (enum, values: ["high", "medium", "low"], optional) default="high"
...
```

Bu kısımda öncelikle gelen parametreleri düzgün bir şekilde almayı hedefledim. `self.rfile.read(content_length)` işlevini kullanarak parametreleri okudum.

gelen parametrelerin her birini dictionary yapısına ekledim.

Örnek:

```python
data = {
"chicken": "high",
"garlic": "low",
"rice": "medium"
}
```

Bu sayede yemeğin malzemelerinin girilen parametrelerin içerisinde olup olmadığını kontrol ettim.

```python
class QualityEnum(Enum):
high = 5
medium = 3
low = 1
```

Eğer yemeğin içerisindeki malzemenin isimi gelen post isteğindeki parametreler ile eşleşiyorsa, parametrenin değerini "QualityEnum" enum'u üzerinden `QualitiyEnum['name'].value()` özelliğini kullanarak qualitiy_score'a ekliyorum.

---
### Price

```
PATH: /price
METHOD: POST
PARAMS:
meal_id: (integer, required)
<ingredient-1>: (enum, values: ["high", "medium", "low"], optional) default="high"
<ingredient-2>: (enum, values: ["high", "medium", "low"], optional) default="high"
...
```

Bu kısımda yemeğin tüm malzemeleri fiyatlandıracağım için bir döngüye alarak başladım.

Sonrasında yemeğin içinde bulunan malzemeleri, veri setinden gelen ingredients'in içerisinde aradım.

```python
def findIngredient(menu, ingredient):
	for d_ingre in menu['ingredients']:
		if d_ingre['name'] == ingredient:
			return d_ingre
	return -1
```

Arama işlemini oluşturduğum `findIngredient()` fonkisyonunu kullanarak bir değişkene atadım. Bu sayede fiyatı hesaplayabilmem için gerekli çoğu veriye eriştim.

Son olarak, API isteğinde gelen parametreler arasında malzemenin varlığını kontrol ettim. Varsa, malzemenin `options['quality']` den gelen veriyi girilen parametrenin kalitesiyle karşılaştırdım ve fiyatlandırdım. Yoksa, default olarak 'high' fiyatlandırmasını kullandım.

Düşük kaliteli malzemeler seçildiğinde servis ücretini alabilmek için `serviceFee()` adinda bir enum oluşturdum.

```python
class serviceFee(Enum):
high = 0.0
medium = 0.05
low = 0.10
```

Bu sayede eşleşen malzemenin kalitesine göre, fiyata ek olarak `serviceFee[ingredient_qualitiy].value` kullanarak ekledim.

---

### Random

```
PATH: /random
METHOD: POST
PARAMS:
  budget: (double, optional) default=unlimited
```

Random endpointinde `random.choice()` fonksiyonunu kullanarak veri setindeki meals listesinin içerisinden random bir yemek belirledim.

Yemeğin içerisindeki malzemelerin kalitesinin de random bir şekilde belirlemem gerekiyor. Bir for döngüsü açarak yemeğin içerisindeki bütün malzemelerin kalitesini belirledim. Ardından kalite skorunu ve fiyatını hesapladım.

Bütçe parametresi girildiğine bunu nasıl yapabileceğimi tekrar tekrar düşündüm ve sonuç olarak random kalitede malzemelerin bütçe ile uyumlu olabilmesi için bütçemizin, yemeğin pahalı malzemeler ile hazırlanılmış halinin fiyatlandırmasından daha büyük olması gerektiğini düşündüm.

Yeni bir liste oluşturup bu listenin içerisine veri setindeki bütün yemeklerin kalitesini `'high'` varsayarak fiyatlandırdım. Bütçe yemeğin fiyatını karşılıyorsa yemeği listeye ekledim. Bunu için `filteredHighestMenu()` fonksiyonu oluşturdum. Böylece rastgele bir yemek seçerken bu menünün içerisinden seçecektim.

```python
def filteredHighestMenu(menu, budget):
	meals = menu['meals']
	highest_meals = []
		for meal in meals:
		price = calculatePriceRandom(menu, meal['ingredients'], 0)
		if price <= budget:
			highest_meals.append(meal)
	return(highest_meals)
```

Sonunda JSON body sinin içerisinde yemeğin `id, name, price, quality_score, ingredients` biglileri olacağı için bu bilgileri toplayarak response olarak gönderdim.

```python
result = {
	'id': random_meal['id'],
	'name': random_meal['name'],
	'price': round(price, 2),
	'quality_score': quality_score,
	'ingredients': random_ingredients
}
```
