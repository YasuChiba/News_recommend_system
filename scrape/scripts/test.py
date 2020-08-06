


from news_sites.NewsSiteScraper import NewsSiteScraper

url1 = "https://t.co/rrVWxTf5rn?amp=1"


scraper = NewsSiteScraper()

url, text, og_image, og_site_name, og_title, og_description = scraper.scrape(url1)
print(url)
print(og_site_name)