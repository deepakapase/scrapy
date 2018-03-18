  
# The requests library
import requests
import json
from exceptions import RuntimeError
  
class WholeFoodsScraper:
    WINE_URL = 'https://redsky.target.com/v1/plp/search/?category=5xsxv&visitorId=01602E03E8670201824D2E9549AE113C&pageId=%2Fc%2F5xsxv&channel=web'
    API_url = 'https://redsky.target.com/v1/plp/search/?category=5xtg6&visitorId=01602E03E8670201824D2E9549AE113C&pageId=%2Fc%2F5xtg6&channel=web'
    BEER_URL ='https://redsky.target.com/v1/plp/search/?category=5xsxx&visitorId=01602E03E8670201824D2E9549AE113C&pageId=%2Fc%2F5xsxx&channel=web'
    SPIRITS_URL = 'https://redsky.target.com/v1/plp/search/?category=5xsxw&visitorId=01602E03E8670201824D2E9549AE113C&pageId=%2Fc%2F5xsxw&channel=web'
    MALT_url = 'https://redsky.target.com/v1/plp/search/?category=mar4j&visitorId=01602E03E8670201824D2E9549AE113C&pageId=%2Fc%2Fmar4j&channel=web'
    HARD_url = 'https://redsky.target.com/v1/plp/search/?category=v6pbq&visitorId=01602E03E8670201824D2E9549AE113C&pageId=%2Fc%2Fv6pbq&channel=web'
    cocktail_mixes_url = 'https://redsky.target.com/v1/plp/search/?category=4uez3&visitorId=01602E03E8670201824D2E9549AE113C&pageId=%2Fc%2F4uez3&channel=web'
    scraped_items = []
    
    def get_stores_info(self, page):
     

        # Making the post request
        count = 90
        offset = page * count;
         
        #response = requests.get(self.WINE_URL,  data = {'count':count, 'offset':offset})
        response = requests.get(self.cocktail_mixes_url + '&count=' + `count` + '&offset=' + `offset`)
        print page
        print self.cocktail_mixes_url + '&count=' + `count` + '&offset=' + `offset`
        print response
        return response.json()['search_response']['items']
    
    def parse_json_field(self, item, field):
        try:
            return item[field]
        except (ValueError, KeyError, TypeError):
            return ''
    
        
    def parse_items(self, data):
        # Creating an lxml Element instance
        for item in data['Item']:
            # The lxml etree css selector always returns a list, so we get
            # just the first item
            title = self.parse_json_field(item, "title")
            url = self.parse_json_field(item, "url")
            description = self.parse_json_field(item, "description")
            brand = self.parse_json_field(item, "brand")
            tcin = self.parse_json_field(item, "tcin")
            dpci = self.parse_json_field(item, "dpci")
            upc = self.parse_json_field(item, "upc")
            bullet_description = self.parse_json_field(item, "bullet_description")
            soft_bullets = self.parse_json_field(item, "soft_bullets")
            available_to_purchase_date_time = self.parse_json_field(item, "available_to_purchase_date_time")
            temp = self.parse_json_field(item, "child_items")
            package_dimensions = self.parse_json_field(temp, "package_dimensions")
            release_date = self.parse_json_field(temp, "release_date")
            images = self.parse_json_field(item, "images")
            # now we add all the info to a dict
            item_info = {
                        'title': title,
                        'url': url,
                        'brand': brand,
                        'upc': upc,
                        'tcin': tcin,
                        'dpci': dpci,
                        'release_date': release_date,
                        'bullet_description': bullet_description,
                        'soft_bullets': soft_bullets,
                        'description': description,
                        'available_to_purchase_date_time': available_to_purchase_date_time,
                        'package_dimensions': package_dimensions,
                        'images': images
                        }
            
            self.scraped_items.append(item_info)
    
    
    def run(self):
        for page in range(1):
            # Retrieving the data
            data = self.get_stores_info(page)
            # Parsing it
            self.parse_items(data)
            #print('scraped the page' + data)

        self.save_data()

    def save_data(self):
        with open('cocktail_mixes_scrapped.json', 'w') as json_file:
            json.dump(self.scraped_items, json_file, indent=4)

if __name__ == '__main__':
    scraper = WholeFoodsScraper()
    scraper.run()            