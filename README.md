# getUdemyFreeCourse
:muscle: Get yourself some udemy free courses

This project is created as I was obsessed with finding free courses in Udemy effortlessly:smiley:, while aiding me to play with Scrapy.

Step taken:
1. Crawl to get the list of url free course ( scrapy - crawl from goviral)
2. Perform checking on that course, as some discount dont last long / not 100% discount ( scrapy - udemy to get the checkout URL )
3. Store the information to sqlite database
4. Run the selenium script to automatically enroll you to courses in databases ( selenium )

TODO :
1. Change the step 2 to using selenium.
