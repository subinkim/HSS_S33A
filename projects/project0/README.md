# Project 0

Web Programming with Python and JavaScript

1. Index.html

Index.html is a homepage that explains the main purpose of this website - introducing myself - and contains links to other web pages
on its navigation bar. At the top, I have used an image of Harvard summer school crest as a header image.
Navigation bar and footer are composed of bootstrap column layouts, and they are mobile-responsive. The message at the top changes
by the size of the screen - when large, it displays the message, "Welcome to Subin's Webpage", and when small, it displays a simple
message, "Welcome :)" with additional h3 element below which displays the message, "Rachael's webpage".

2. about.html

about.html is about my life - my hometown, my schools and my dream. It has the same nav bar and a footer as index.html, but it also
contains a link to each section of the webpage, which I coded using <a href = "#id"> tags.

3. interest.html

interest.html is about my interests - computer science, soccer, baseball, and maths. Its contents are brief, because they are
contained in a text box, so I deliberately made them short.

4. lecture.html

lecture.html is lists the lectures that I am taking at Harvard Summer School and contains links that redirect the users to the
webpages that contain course descriptions.

5. Additional info

I got the hex code for crimson colour at 'https://www.seas.harvard.edu/', Harvard John A. Paulson School of Engineering and
Applied Sciences.

6. main.scss

I have created one css file which codes for all four html pages. I have used sass variable to replace crimson, and used sass
inheritance in two parts - for interest.html when all the text boxes have similar properties and for nav bar. I used sass
nesting for lecture.html. I have added brief comments to each part of css to make it more decodable.