import scrapy
import pandas as pd
df = pd.read_csv('F:\Web Scraping\Golabal\keywords.csv')
base_url = 'https://teamauctions.com/search/{}'

class TeamSpider(scrapy.Spider):
    name = 'team'
    
    def start_requests(self):
        for index in df:
            yield scrapy.Request(base_url.format(index), meta={"pyppeteer": True},cb_kwargs={'index':index})

    def parse(self, response, index):  
        location = response.xpath('//*[@id="tab1"]//a//div//h4[1]/text()').getall()     
        links = response.css("[id='tab1'] div a::attr(href)")
        date = response.xpath('//*[@id="tab1"]/div/a/div/div/p/text()').getall()
        images = response.xpath('//*[@id="tab1"]/div/a/div/div/div/img/@src').getall()
        counter = 0
        for link in links:
            loc = location[counter]
            auction_date = date[counter]
            image = 'https://teamauctions.com'+images[counter]
            yield response.follow("https://teamauctions.com"+link.get(), callback=self.parse_item, cb_kwargs={'index':index, 'location':loc, 'auction_date':auction_date, 'image':image})  
            counter = counter+1

    def parse_item(self, response, index, location, auction_date, image): 
        print(".................")  
        product_url = response.url
        print(product_url)
       
        print(image)       
        auction_date = auction_date
        print(auction_date)        
        location = location
        print(location)
        product = response.xpath('//p/b/text()').get()
        product_name = product.strip()
        print(product_name)
        try:
            lot_number = response.css('p.h4 b span::text').get().strip()            
            print(lot_number)
        except:
            lot_number = response.css('.tx-small.mL::text').get().strip()
            print(lot_number)

        auctioner = "Team Auctions Cranford"
        print(auctioner)        
        
        yield{            
            'product_url' : response.url,           
            'item_type' :index.strip(),            
            'image_link' : image,          
            'auction_date' : auction_date,            
            'location' : location,           
            'product_name' : product_name,            
            'lot_id' : lot_number,          
            'auctioner' : auctioner,
            'website' : 'teamauctions',
            'description' : ''             
        }