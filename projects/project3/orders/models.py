from django.db import models

# List of all the pizza toppings
class Toppings(models.Model):
    topping = models.CharField(max_length = 64)

    def __str__(self):
        return f"{self.topping}"

# List of menu categories, e.g. (cheese / one / two / three / special) pizza / pasta / salad / dinner platter / subs

class Category(models.Model):
    code = models.IntegerField()
    category = models.CharField(max_length = 64)

    def __str__(self):
        return f"{self.category} ({self.code})"

#List of all menu items
class Order(models.Model):
    food = models.ForeignKey(Category, on_delete = models.CASCADE)
    menu = models.CharField(max_length = 64) #Name of the menu
    size = models.CharField(max_length = 1) #L or S (If no size = L)
    price = models.FloatField() #In dollars

    def __str__(self):
        return f"Menu {self.id}: {self.food} {self.menu} of size ({self.size}) = ${self.price}"

class CustomerOrder(models.Model):
    username = models.CharField(max_length = 64)
    food = models.CharField(max_length = 64)
    menu = models.CharField(max_length = 64) #Name of the menu
    size = models.CharField(max_length = 1) #L or S (If no size = L)
    price = models.FloatField() #In dollars
    topping1 = models.CharField(max_length = 64, null = True, blank = True)
    topping2 = models.CharField(max_length = 64, null = True, blank = True)
    topping3 = models.CharField(max_length = 64, null = True, blank = True)
    ordered = models.BooleanField()
    processed = models.BooleanField()

    def __str__(self):
        return f"Order {self.id}: {self.food} {self.menu} of size ({self.size}) with toppings {self.topping1} {self.topping2} {self.topping3} = ${self.price} by {self.username}. Order status = ordered {self.ordered} processed {self.processed}."