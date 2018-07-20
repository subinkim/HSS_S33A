# Project 1

Web Programming with Python and JavaScript

# Index.html
The website starts with index.html page, where you can register yourself or direct yourself to a login page.
It is also possible to search the locations without logging in, if you click 'proceed without login' button.
I have used jinja2 if statements so that index.html changes by your login state.
Also, if your username is shorter than 6 characters or your password is shorter than 8 characters, the website displays an
error message that they should be longer than 6 or 8 characters, respectively.
When you are already logged in, it only shows you a button that leads you to the search page, instead of a form to fill
for registration.

# Login.html
The registration form will not be accepted when any of the fields are empty or the username you have chosen is already taken
by someone. When you click on register after you successfully complete the form, you will be directed to login.html page,
where you have to enter your username and password to login. If you enter a wrong username or password, it displays an error
message and asks you to re-enter your credentials. If you are already logged in, the page displays a message 'you already
logged in', so that there will be no confusions created.

# Error.html
Error.html page is used in order to display error messages in various occasions. I have put {{message}} in the html file so
that I can put any message freely on the website.

# Layout.html
Layout.html is a layout to all the pages of the website. It contains basic structures.

# Locations.html
Locations.html is a search page that you will be directed to once you login or if you click on 'proceed without login' button.
At first, it displays the complete list of zipcodes that the database has. You can simply choose one of them from the list and
clikc on 'More info' button to get more information about the location. The button redirects you to location.html file.
If you perform a query by entering either zipcode or city name or both, the website displays all the results that matches
or contains your inputs. For example, entering 02 in zipcode and C in city will result in the list of all the cities that
have c in their name and 02 in their zipcode.

# Location.html
Once you get a search result, you can then move onto location.html, where you will be able to see the information about the
city, plus the current weather. Humidity is displayed in percentage.
You can also add a comment by writing comment in the text box and clicking on submit. When there's no comment written, by
default it prints out the message 'None', but this message is replaced by your comment when you enter your first comment.
And as the instructions stated, those messages are not editable and not deletable once you write them.
In my 'locations' db table, 'comment' is a field with a type array, but it is set to NULL by default. So, the if statement
checks if the array is empty or not, and if empty, it replaces NULL with the comment entered so that NULL is not printed out
onto the screen. Also, it checks if the comment is entered and if nothing is entered in the textarea, then it returns an
error message saying that you have to enter something in order to submit a comment.
It is also possible to check in, by clicking on check_in button. I have prevented the number of check ins auto-incrementing
when you reload the page, by using redirect function instead of render template. Also, you cannot check in more than once
with the same account.
