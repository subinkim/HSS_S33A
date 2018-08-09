Tourist attraction data:
From google travel guide

# YOUR NEW ENGLAND

* Sorry! I forgot to submit status report!

## I.Introduction

This project aims to build a website that introduces some of the major cities in New England.

## II. Goals
There were two main goals that I tried to reach.
- Users have to be able to their experience at each city based on the following criteria: local food, safety, cleanliness, number of tourist attractions, and local residents.
    - 'GOOD': Users can comment on each city and enter the rating. Ratings out of 5 and they are shown with the text feedback.
    - 'BETTER': Ratings given by the users are shown in star icons. Overall rating (for each comment) is calculated automatically.
    - 'BEST': Average ratings for the city are calcualted automatically. If no data, show no data.
- Users have to be able to share the schedule of their own trip around the cities in New England
    - 'GOOD': Users can show the list of schedules shared by people. Users can share their own.
    - 'BETTER': Users can search the trip schedule that contains the city that they want to visit.
    - 'BEST': Users can 'like' the trip schedule, which is then saved to their database.

## III. Features of the website
1. index.html

Users can register or login to the website. However, even without an account, the users can still access the information, although
they won't be able to comment or use save/like functions.
Users have to enter the followings to register:
- First name
- Last name
- Username
- Password

2. cities.html

When the users click on 'search cities', they will be redirected to cities.html page, which contains the list of cities in New England,
whose population is bigger than 100,000 (there are 12). I have used `import.py` and `cities.csv` to create a database.
```
Boston, MA (655,884)
Bridgeport, CT (147,629)
Cambridge, MA (107,289)
Hartford, CT (124,893)
Lowell, MA (109,945)
Manchester, NH (110,448)
New Haven, CT (131,024)
Providence, RI (179,207)
Springfield, MA (153,060)
Stamford, CT (130,824)
Waterbury, CT (109,676)
Worcester, MA (184,815)

```
> [Data based on 2010 census](https://en.wikipedia.org/wiki/List_of_cities_by_population_in_New_England)

Some of the main functionalities of this page are:
- Search:
    - Users can search the city by their name or by the state they are located in.
    - `db.execute('SELECT * FROM cities')` looks for any cities that contain the user input.
    - For instance, entering 'b' would return 'boston', 'bridgeport', and 'waterbury'.
    - Users can choose the state using the dropdown menu.
- 'More Info':
    - 'More Info' button redirects users to an individual page that introduces the city.

3. city.html

city.html introduces each city. The bootstrap `blockquote` item right below the title is the short introduction on the city.
The followings are some main features of the page:
- city ratings:
    - city ratings are calcualted based on the user ratings on the city. I have used python to calculate the average values of each category and the overall rating. Please check `application.py` for codes.
    - If there's no data for city ratings, i.e. none of the users left comment on the city, it shows 'no data'.
- location:
    - I have embedded Google Maps onto the website to show the location of the city on the map.
    - `https://maps.google.com/maps?q={{city.city}}%2C%20{{city.state}}&t=&z=13&ie=UTF8&iwloc=&output=embed` I have put jinja2 variables into the address so that I won't need to write down 12 different URLs.
- Tourist attractions:
    - The page shows some top tourist attractions that users might like to visit. It includes the name of the place and a short description about the place.
- Weather:
    - Uses Dark SKY API to show weather data.
- Comments:
    - If logged in:
        - You can view and write comments.
        - If any of the comments are written by you, '(you)' is added next to your username in comments to show that it was written by you.
    - If not logged in:
        - You can only view comments.
        - There is an additional button at the bottom which redirects you to login.html when you click on it.
- Save:
    - You can simply save the city by clicking on 'save' button. This only appears when you are logged in.
    - All the cities that you saved would be available on your 'saved cities' list on 'My Page'.
    - If you have already saved the city, you cannot save it again.

4. schedules.html

schedules.html shows the list of schedules people have shared to the website. Users can filter the schedules by entering the (part of the) name of the city they want to go to.
'Read' button allows users to read the trip schedule details. If you press 'read', it redirects you to `read.html`.
'Share your trip schedule!' button allows users to share their trip schedule to other users. If you click on 'share your trip schedule',
then you will be redirected to `schedule.html`.

5. schedule.html

schedule.html allows user to enter their own trip schedule information. Users have to choose the cities that they have visited in their trip
and write a description about their trip. `application.py` checks if all fields have values, and adds new schedule to the database.
User is redirected to `schedules.html`.

6. read.html

read.html shows the schedule that the users have shared. It shows the username of the user who shared the schedule, and if it is you, then it shows '(you)'
 next to the username. The followings are some of the main features of the page:
- like:
    - if you are not a writer of the schedule and if you are logged in, then you are allowed to like the schedule.
    - Once you 'liked' it, you can see it on 'my page'.
- comment:
    - Users can leave comment on the schedule.
    - '(you)' shown if the comment is written by you.

7. mypage.html

The main features of My Page include the followings:
- List of comments written by the user:
    - My Page shows the list of comment written by you. If there's none, it shows 'you have no comments'.
- Cities you have saved:
    - My Page shows the list of cities the user has saved.
    - You can go back to the city page by clicking on 'check out (city)' or unsave the city by clicking 'unsave (city)'.
- Schedules you shared:
    - Shows the schedules that you shared.
    - Only list of cities and schedule id are shown by default, but if you click on 'show description' button, it toggles the description.
    - I used JavaScript function to make this work.
- Schedules you liked:
    - Shows the list of schedules you have liked.
- Comments that you left on schedules:
    - Shows the list of comments that you have left on schedules.
    - By pressing 'check your comment', you will be redirected to the schedule page.

## III. Database
1. users

- Stores user information.
    - firstname (var char)
    - lastname (var char)
    - username (var char)
    - password (var char)
    - saved (text[]): list of cities the user saved
    - liked (text[]): list of IDs of schedules user liked

2. cities
- Generated by `import.py` and `cities.csv`
- Contains the list of cities, their states, their population, lat and long, and short description.

3. comments
- Used to store user comments.
- Only 12 rows - one for each city.
- comments are stored in list.
- usernames, times and other ratings are all stored in lists so that later I can access them by using the appropraite index.

4. descriptions
- Descriptions on the cities.
    - attraction: name of the place
    - info: description of the place
    - city: name of the city
    - id: id of the description.

5. schedules
- Stores schedules that users have shared.
    - username: username of the user who shared the schedule
    - likes: number of likes it received.
    - usernames, comments, times: same with comments
    - city: stores the list of cities that user has visited in the trip
    - info: description about the trip
    - id: id given to schedule.

## Thank you for the wonderful summer!
Thank you for the wonderful 7 weeks that I could spend here at Harvard. This was a great learning experience for me.
I hope that with this experience, I could reach closer to my dream of becoming a developer.
Thank you for spending your time marking my assignments and writing comments on how to improve them, Alex. Those have been very helpful.
Have a nice rest of the summer!