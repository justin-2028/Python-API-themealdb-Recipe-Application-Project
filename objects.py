"""
This is where the objects are stored, making it easier to work with the data. 
Each of them contains the essential information for that specific item. 
"""
 
class Category:
    def __init__(self, category):
        self.__category = category

    def get_category(self):
        return self.__category


class Meal:
    def __init__(self, name, instructions="", ingredients={}):
        self.__name = name
        self.__instructions = instructions
        self.__ingredients = ingredients

    def get_meal_name(self):
        return self.__name
    def get_meal_instructions(self):
        return self.__instructions
    def get_meal_ingredients(self):
        return self.__ingredients


class Area:
  def __init__(self, area):
      self.__area = area
  
  def get_area_name(self):
    return self.__area
