# Project 3

Web Programming with Python and JavaScript

models.py

I have created a separate model for toppings, category, order and customerorder.
Toppings model stores the list of pizza toppings.
Category model stores the list of categories, e.g. pasta, subs. In case of pizza, I have put 'cheese', 'special', 'one topping',
'two topping', and 'three topping' at the front so that the user can see what type of pizza it is.
Order model stores all the possible menu items and use category as a foreign key for its 'food' field.
CustomerOrder model stores all the orders that have been passed in, including the orders that have not been checked out.
Two boolean variables, 'ordered' and 'processed' show the status of the order.

index.html

It shows the list of menu items available and a button that you use to add them to your shopping cart.

manage.html

link to this page is visible only if you have an admin status.
You can see list of all the orders and mark them 'processed' on this page.

register.html

page for users to register.

checkout.html

where you can see items in your virtual shopping cart and check them out. You can also see your past orders and their status.
