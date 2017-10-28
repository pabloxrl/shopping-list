import argparse
import os
import csv
from enum import Enum

BREAKFAST = 1
II_BREAKFAST = 2
III_BREAKFAST = 3
LUNCH = 4
DINNER = 5

class Ingredient(object):
    def __init__(self, name, weight):
        self._name = name
        self._weight = weight

    def name(self):
        return self._name

    def weight(self):
        return self._weight

    def __mul__(self, other):
        self._weigh *= other


class Recipe(object):
    def __init__(self, recipe_id):
        self._id = recipe_id.strip()
        self._ingredients = []

    def add_ingredient(self, name, weight):
        self._ingredients.append(Ingredient(name.strip(), int(weight)))

    def ingredients(self):
        return self._ingredients

class RecipeDatabase(object):
    def __init__(self, path):
        assert os.path.exists(path)

        self._database = dict()

        with open(path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for line in reader:
                self.push(*line)

    def push(self, meal_type, recipe_id, ingredient, weight):
        if meal_type in self._database:
            meals_by_type = self._database[meal_type]

            meal = [item for item in meals_by_type if item._id == recipe_id.strip()]
            if meal:
                assert len(meal) == 1
                meal[0].add_ingredient(ingredient, weight)
            else:
                new_recipe = Recipe(recipe_id)
                new_recipe.add_ingredient(ingredient, weight)

                meals_by_type.append(new_recipe)
        else:
            new_recipe= Recipe(recipe_id)
            new_recipe.add_ingredient(ingredient, weight)

            self._database[meal_type] = [new_recipe]

    def get(self, meal_type, recipe_id):
        return [recipe for recipe in self._database[str(meal_type)] if recipe._id == recipe_id][0]


class ShoppingList(object):
    def __init__(self):
        self._items = dict()

    def add(self, ingredients):
        for ingredient in ingredients:
            if ingredient.name() in self._items:
                self._items[ingredient.name()] += ingredient.weight()
            else:
                self._items[ingredient.name()] = ingredient.weight()

    def print(self):
        print('Shopping list: \n')

        for name in self._items:
            print(name + ': ' + str(self._items[name]) + ' grams')

def main():
    parser = argparse.ArgumentParser(description='Generate shopping list.')
    parser.add_argument('--input', dest='database_path', help='Path to the recipe database')
    args = parser.parse_args()

    recipe_database = RecipeDatabase(args.database_path)

    person_count = int(input("For how many people is the shopping? "))
    day_count = input("For how many days is the shopping? ")

    shopping_list = ShoppingList()

    for idx in range(int(day_count)):
        print('\nDay ' + str(idx + 1) + ':\n')

        if int(person_count) > 1:
            ret = input('Select Mariola\'s breakfast: ')
            if ret != '':
                shopping_list.add(recipe_database.get(BREAKFAST, ret).ingredients())

            ret = input('Select Pablo\'s breakfast: ')
            if ret != '':
                shopping_list.add(recipe_database.get(BREAKFAST, ret).ingredients())
        else:
            ret = input('Select breafast: ')
            if ret != '':
                shopping_list.add(recipe_database.get(BREAKFAST, ret).ingredients())

        ret = input('Select 2nd breafast: ')
        if ret != '':
            for i in range(person_count):
                shopping_list.add(recipe_database.get(II_BREAKFAST, ret).ingredients())

        ret = input('Select 3rd breafast for Pablo: ')
        if ret != '':
            shopping_list.add(recipe_database.get(III_BREAKFAST, ret).ingredients())

        ret = input('Select lunch: ')
        if ret != '':
            for i in range(person_count):
                shopping_list.add(recipe_database.get(LUNCH, ret).ingredients())

        ret = input('Select dinner: ')
        if ret != '':
            for i in range(person_count):
                shopping_list.add(recipe_database.get(DINNER, ret).ingredients())

    print('\n\n\n')
    shopping_list.print()


if "__main__":
    main()