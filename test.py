import sqlite3


connect = sqlite3.connect('db.sqlite3')
cursor = connect.cursor()
cursor.execute("SELECT COUNT(id) FROM cocktails_ingridient")
my_dict = {}
# cursor.execute("SELECT id FROM cocktails_ingridient")
# results = cursor.fetchall()
ingridients_ids = int(cursor.fetchall()[0][0])
for ing in range(1, ingridients_ids + 1):
    cursor.execute(f"SELECT COUNT(id) FROM cocktails_cocktail_ingridients WHERE ingridient_id = {ing}")
    count = int(cursor.fetchall()[0][0])
    my_dict[ing] = count
print(my_dict)
# print(results)
connect.close()

ing_dict = {1: 1, 2: 11, 3: 28, 4: 19, 5: 1, 6: 0, 7: 2, 8: 18, 9: 5, 10: 10, 11: 0, 12: 10, 13: 1, 14: 9, 15: 5, 16: 7, 17: 6, 18: 0, 19: 2, 20: 0, 21: 1, 22: 0, 23: 8, 24: 16, 25: 3, 26: 4, 27: 1, 28: 0, 29: 7, 30: 0, 31: 15, 32: 1, 33: 4, 34: 0, 35: 0, 36: 0, 37: 4, 38: 1, 39: 2, 40: 2, 41: 9, 42: 4, 43: 2, 44: 0, 45: 5, 46: 5, 47: 13, 48: 0, 49: 3, 50: 1, 51: 0, 52: 13, 53: 15, 54: 1, 55: 1, 56: 0, 57: 15, 58: 0, 59: 78, 60: 1, 61: 5, 62: 2, 63: 8, 64: 3, 65: 1, 66: 5, 67: 1, 68: 96, 69: 96, 70: 1}


sorted_ings = sorted(ing_dict.items(), key=lambda item: item[1], reverse=True)
list_ing = []
for i in range(30):
    list_ing.append(sorted_ings[i][0])
print(list_ing)

connect = sqlite3.connect('db.sqlite3')
cursor = connect.cursor()
cursor.execute(f"SELECT id FROM cocktails_ingridient_cost WHERE cocktail_id_id=98")
ingridients_ids = cursor.fetchall()
print(ingridients_ids)
connect.close()

querysety_2 = Cocktail.objects.all().order_by('name')

for cock in querysety_2:
    print(cock)


gg = [68, 69, 59, 3, 4, 8, 24, 31, 53, 57, 47, 52, 2, 10, 12, 14, 41, 23, 63, 16, 29, 17, 9, 15, 45, 46, 61, 66, 26, 33, 37, 42, 25, 49, 64, 7, 19, 39, 40, 43]