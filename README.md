# otsimo-2024
## Transparent Restaurant Backend

 Bu kısımda end pointleri kodlarken nasıl ilerlediğimi ve algoritmayı anlatıyor olacağım.

 Kullandigim ekran goruntuleri kodun guncel halini temsil etmeyebilir.

### List Meals

```
PATH: /listMeals
METHOD: GET
PARAMS:
  is_vegetarian: (boolean, optional) default=false
  is_vegan: (boolean, optional) default=false
SAMPLE: http://localhost:8080/listMeals?is_vegetarian=true
```

Yemeğin içindeki malzemelerin her birini, menu['ingredients'] içindeki öğelerle isimlerine göre eşleştirerek, eşleşen malzemelerin ingredient['groups'] içinde vejetaryen veya vegan olup olmadığını kontrol etmem gerekiyor.

Eşleşen malzemeleri vegatarian_menu.append() kullanarak menüye ekleyip son durumda filtered_menu'yu vegatarian menü'ye esitleyerek döndürdüm.

![image](https://github.com/faruktinaz/otsimo-2024/assets/114104599/1d4ea13f-847c-4b2c-8dee-7c641f870f41)

![image](https://github.com/faruktinaz/otsimo-2024/assets/114104599/aed04629-1a32-48ec-bbe0-c75cf2ec7a5e)

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

Bunun için yemeğin içerisindeki malzemelerin tamamını, veri setimizden gelen malzemelerin isimleriyle karşılaştırdım. Eşleşen malzemeleri exists_ingrdts_it değişkenine iteratör kullanarak atadım, ve opsiyonları exists_ingrdts_it.update(ingredient) işlevini kullanarak üzerine ekledim."

![Screenshot from 2024-05-06 02-03-30](https://github.com/faruktinaz/otsimo-2024/assets/114104599/6f10c008-9f47-4456-a629-cf3ce4015909)


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

gelen parametrelerin her birini key-value olarak tutmak istedim. 

Örnek:
	data["chicken"] = "high"

Bu sayede yemeğin malzemelerinin girilen parametrelerin içerisinde olup olmadığını kontrol ettim.

```python
class QualityEnum(Enum):
high = 5
medium = 3
low = 1
```

Eğer yemeğin içerisindeki malzemenin isimi gelen post isteğindeki parametreler ile eşleşiyorsa, parametrenin değerini "QualityEnum" enum'u üzerinden "QualitiyEnum['name'].value()" özelliğini kullanarak qualitiy_score'a ekliyorum.  

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


Arama işlemini oluşturduğum findIngredient() fonkisyonunu kullanarak bir değişkene atadım. Bu sayede fiyatı hesaplayabilmem için gerekli çoğu veriye eriştim.

Son olarak, API isteğinde gelen parametreler arasında malzemenin varlığını kontrol ettim. Varsa, malzemenin options['quality']'den gelen veriyi girilen parametrenin kalitesiyle karşılaştırdım ve fiyatlandırdım. Yoksa, default olarak 'high' fiyatlandırmasını kullandım. 
