# NoBroker Playwright Scraper

This is a web scraper built using Playwright in Python. This web scraper scrapes for data on rental properties listed on nobroker.in that are located near the existing metro lines of Mumbai (lines 1, 2A, and 7). Basically, this scraper scrapes for rental properties located near every single metro station.

I have used proxy ip addresses for scraping to avoid blacklisting my own public ip address by the website.

The scraped data goes beyond just monthly rental prices. This data dives deep into each property, revealing exact addresses or locality details, whether it's a spacious independent house or an apartment (and on which floor!), the total number of floors, and even nearby landmarks. Plus, get the inside scoop on resident amenities, water source (municipal or borewell), listing/reactivation dates, proximity to the nearest metro station, etc.

For each metro station, the data on the nearby properties is stored in a dictionary format and is then inserted inside a MongoDB collection in the ascending order of the insertion timestamp.


