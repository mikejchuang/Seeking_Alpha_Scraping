from scrapy import Spider, Request
from scrapy.selector import Selector
from webscraping.items import LightningItem
import pandas as pd
import logging

saurl = pd.read_csv('/Users/michaelchuang/git_project/mjc_WebScraping/Lightning_round_URLS1.csv')
saurl = saurl.drop('TITLE.1', axis=1)
saurl['DATE'] = saurl.TITLE.str[-11:]
saurl['DATE']= saurl['DATE'].str.split(' ').str[1]



class LightningSpider(Spider):
    name= "lightninground"
    allowed_urls = ['https://seekingalpha.com/']
    start_urls = [x for x in saurl['URL']]
    #print(start_url[0])


    def parse(self, response):

        title1 = response.xpath('//h1/text()').extract()
        date1 = response.xpath('//time/@content').extract()
        #try:
        #bullish1 = response.xpath('//div[@id ="a-body"]/p[preceding-sibling::h3[1][.= "Bullish Calls"]]/a/text()').extract()
        #except:
        bullish1 = response.xpath('//div[@id ="a-body"]/*[preceding::*[contains(text(),"Bullish")]]//@href').extract()
       # try:
            #bearish1 = response.xpath('//div[@id ="a-body"]/p[preceding-sibling::h3[1][.= "Bearish Calls"]]/a/text()').extract()
       # except:
        bearish1 = response.xpath('//div[@id ="a-body"]/*[preceding::*[contains(text(),"Bearish")]]//@href').extract()

        item = LightningItem()
        item['title'] = title1
        item['date'] = date1
        item['bullish'] = bullish1
        item['bearish'] = bearish1

        yield item







#notes
#Bullish Calls
#response.xpath('//div[@id ="a-body"]/p[preceding-sibling::h3[1][.= "Bullish Calls"]]/a/text()').extract()
#Bearish
#response.xpath('//div[@id ="a-body"]/p[preceding-sibling::h3[1][.= "Bearish Calls"]]/a/text()').extract()
#Time
#response.xpath('//time/@content').extract()
#Title
#response.xpath('//h1/text()').extract()


#response.xpath('//*[preceding-sibling::*[text()= "Bullish Calls"]]').extract()
#response.xpath('//*[text()= "Bullish Calls"]/../p').extract()
#response.xpath('//strong[text()= "Bullish Calls"]/../*').extract()

#response.xpath('//div[@id ="a-body"]/p[preceding::*[.= "Bullish Calls"]]/a/text()').extract()

#response.xpath('//div[@id ="a-body"]/p[preceding::*[.= "Bullish Calls"]]/a/@symbol').extract()
#response.xpath('//div[@id ="a-body"]/*[preceding::*[contains(text(),"Bullish)]]/*').extract()

#response.xpath('//div[@id ="a-body"]/*[preceding::*[contains(text(),"Bullish")]]//@href').extract()

response.xpath('//div[@id ="a-body"]/*[preceding::*[contains(text(),"Bearish")]]//@href').extract()
