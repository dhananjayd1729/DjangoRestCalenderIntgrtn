## Google calender integration in Django REST API
You have to implement google calendar integration using django rest api. You need to use the OAuth2 mechanism to
get users calendar access. Below are detail of API endpoint and corresponding views which you need to implement 
<br />

/rest/v1/calendar/init/ -> GoogleCalendarInitView() <br />
This view should start step 1 of the OAuth. Which will prompt user for his/her credentials <br />

/rest/v1/calendar/redirect/ -> GoogleCalendarRedirectView() 
<br /> This view will do two things 
1. Handle redirect request sent by google with code for token. You need to implement mechanism to get access_token from given code. <br />
2. Once got the access_token get list of events in users calendar

I have deployed this API on [replit](https://replit.com/). To know more about the same visit this [URL](https://replit.com/@DhananjayDaundk/DjangoRestCalenderIntgrtnCOVIN?v=1).



