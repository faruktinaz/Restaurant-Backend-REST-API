# otsimo-2024
## Transparent Restaurant Backend

 Bu kısımda end pointleri kodlarken nasıl ilerlediğimi ve algoritmayı anlatıyor olacağım.
 
---
#### List Meals

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

![Screenshot from 2024-05-06 01-39-27](https://github.com/faruktinaz/otsimo-2024/assets/114104599/395d17fe-ce2f-4f83-84ab-310a3a703df2)


Python dilinde vejetaryan menu degerlendirmesi:

![Screenshot from 2024-05-06 01-49-01](https://github.com/faruktinaz/otsimo-2024/assets/114104599/9fe638d5-2fc1-4aa2-9b9d-d6a8e15c76e0)


---

#### Get Meal

```
PATH: /getMeal
METHOD: GET
PARAMS:
    id: N (integer, required)
SAMPLE: http://localhost:8080/getMeal?id=2
```

Girilen ID numarasını öncelikle yemeklerin ID numaralarıyla eşleştirdim. Ardından eşleşen ID numaralı yemeği selected_meal değişkenine ekledim.

Şimdi ise yemeğin içerisinde bulunan malzemelerin opsiyonlarını yemeğin içerisine eklenmesi gerekiyor.

Bunun için yemeğin içerisindeki malzemelerin tamamını, veri setimizden gelen malzemelerin isimleriyle karşılaştırdım. Eşleşen malzemeleri exists_ingrdts_it değişkenine iteratör kullanarak güncelledim, ve opsiyonları exists_ingrdts_it.update(ingredient) işlevini kullanarak güncelledim."

![Screenshot from 2024-05-06 02-03-30](https://github.com/faruktinaz/otsimo-2024/assets/114104599/6f10c008-9f47-4456-a629-cf3ce4015909)


---
