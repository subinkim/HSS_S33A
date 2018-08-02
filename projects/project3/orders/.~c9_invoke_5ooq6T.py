from django.db import models

# Create your models here.
class Pizza(models.Model):
    pizzaType = models.CharField(max_length = 64) #Pizza type: cheese, one (one topping), two, three, special - but they can add new types
    menu = models.CharField(64) #Regular or Sicilian - they can add new pizzas
    size = models.CharField(1) # L or S
    topping = models.CharField(64)

class Subs(models.Model): #includes pasta, salads and dinner platters
    subType = models.CharField(64)
    menu = models.CharField(64)
    size = models.CharField(1) # L or S (or N if no size options)


