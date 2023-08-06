# FritchCrawler
package for crawling the fritchi main page to extract products data using Playwright
due to the application being dynamicly rendered on client side.  
Since the product since is mainly static and refreshed once per day at 8h00, the data is cached
in a pickle file until a request was made the next day.