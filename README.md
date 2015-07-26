# broado-server
##Contributors : Anurag Tiwari, Ashwini Purohit, Amit Kumar Rai, Shubhodeep Mukherjee, Gautham K. Reddy
## The server deployed on : http://dwealo.com:5000/api/<br />
### An API engine for our hackathon App broado for travelbased system.
#Server Deployed on Amazon Web Service for testing we used Heroku

##Problem Statement :   
#(2nd) Creating new ways to capture data on mobile for example: user experience of capturing reviews or improving the overall booking experience.

Implementation of a user-user collaborative filtering for better recommendations of Hotels, Restaurants, places to go around in a city. We have created 3 API's , the link to them is given below. 

##Process Flow:

To help fighting bugging user all the time to get the reviews in form of questionaires or to rate in a 5 point scale, what we as a team came up with is to eliminate the need for user reviews. A user on his trip uses his camera to click the pics of the places he visits. We upload the photos on user's permission to our server to and apply IMAGE PROCESSING Algorithms to detect the user's facial expression and get his/her smile percentage.
We upload upto 5 images each time for normalizing the smile percentage. We then implement a ranking algorithm to rank a place he/she visits.

In our second module, we on the basis of ranks of our places recommend best places for him/her to visit on the basis of genders, age and every possible normalizing factor. For new customes based on their new profile we build their taste by recommending them the most visited places by other users. And in future when we have his taste we build up recommendations using his/her taste (higher priority) and other users lower priority.

In our third module, we use machine learning algorithm to automatically learn from users ratings from his previous experieces and predicting for new users. We also implement a budget base filtering of locations. Based upon user's budget, we will suggest him the best hotels, restaurants and places to go for him.

In our fourth module, we exclusively focussed on to not only plan a perfect SINGLE DAY TRIP for a person but also planning his whole trip based on his budget.


##Technologies used:

Python, OpenCv, Faceplus API, Image recognition API's, Android app.

##Finally, we developed a fully functional android app with all the above modules. 




API's : 

http://broado-server.herokuapp.com/api?img=url&latitude=num&longitude=num<br />
http://broado-server.herokuapp.com/travelApi?location=bangalore (chennai or mumbai)<br />
http://broado-server.herokuapp.com/budgetApi?city=bangalore&living=normal
