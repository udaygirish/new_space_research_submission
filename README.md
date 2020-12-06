# New_Space_Research_sampletask_sub
Repository for submitting the task for initial screening (Object Detection and Data gather and Vis)

### This Branch is for Data Gathering and Visualisation

* The main.py helps to scrape a web page save it as a html file and then read the html and parse it and get a dataframe which consists of ratings and reviews from the page
* Note this script only work for Google play store.
* Run sudo pip3 install -r requirements.txt before running main script

### <u>Arguments</u>
* Sample run ex: python3 main.py -url https://play.google.com/store/apps/details?id=it.rortos.realflight -fn test

* -url to take any url path (Google play store path) and do the necessary steps.
* -fn is filename which user can modify to get the outputs with the same string attached

* output of this sample run will be in the output folder
with files namely test.csv, test.html,test_rating_1.png,test_rating_5.png.

### Limitations
* Currently the script is not that configured to scroll infinitely or more time as the load more reviews is not yet handled. Given time this can be handled.

*** 
For any quries please contact einsteingirish@gmail.com , Ph.No : 8137080271

My Website: https://udaygirish.github.io/


