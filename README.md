This app aims to scrap flight ticket prices and display them on a locally hosted web page.

**Disclaimer**: It was created for learning purposes. Using this app for data scraping could be against the site's policy.  

The server runs locally on Arch Linux (with LXQt desktop environment to run a non-headless browser) with Nginx and Gunicorn support. It also contains a script to schedule jobs and randomize bot working hours.

The bot (puppet module) is running on undetected Chrome created by [ultrafunkamsterdam](https://github.com/ultrafunkamsterdam/undetected-chromedriver). 
It enters links provided in links.txt and scraps their content. Next, the fetched data is stored in the Sqlite3 database.

The interface module is a simple Flask app hosted as a local web page to aggregate and display data in edible form. 

MIT License.