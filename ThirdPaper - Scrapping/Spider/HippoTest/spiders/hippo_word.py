# -*- coding: utf-8 -*-
import scrapy
import html2text
import re
from scrapy.selector import HtmlXPathSelector



class HippoWordSpider(scrapy.Spider):
    name = 'hippo_word'
    #allowed_domains = ['https://documentation.bloomreach.com/library/concepts/plugins/tagging/configuration.html']

    '''
    # testing with a few links
    list_url = ['https://www.onehippo.org/library/concepts/usage-statististics/usage-statistics.html','https://documentation.bloomreach.com/library/concepts/plugins/tagging/configuration.html',
    'https://www.onehippo.com/en/about/news/2013/11/hippo-named-critics-choice-for-best-open-source-cms-by-cms-critic.html',
    'http://www.onehippo.com/connect/boston',
    'https://www.onehippo.org/library/concepts/web-files/web-files-best-practices.html']
    '''
    list_url = []
    txt_import = open("url_file.txt", "r")
    for i in txt_import:
        list_url.append(i)
    # List of URL's
    print(len(list_url))
    start_urls = [i for i in list_url]

    def parse(self, response):

        '''
        # Give this output: "Tagging Plugin Configuration", "Configuration", "The Tagging plugin can be added to your project
        print("procesing:"+response.url)

        all_text = [i.strip() for i in response.xpath('//*[@class = "text"]//text()').extract() if i.strip()] # works better for stripping
        #all_text2 = response.xpath('//*[@class = "text"]//text()').xpath('normalize-space()').extract() # works but cleans them 1 by 1
        created_time = response.xpath('//*[@class = "created_at"]//text()').extract() # maybe use it for refreshing repository? Will see but good to have it.

        blq = []
        scraped_info = {}
        for i in all_text:
            blq.append(i)
        scraped_info[response.url] = blq
        yield scraped_info

        # Above works but it tokenizes everything and i still dont know if i want it like this
        '''

        '''
        # Same output
        print("procesing:"+response.url)

        scraped_info = {}
        all_text = [i.strip() for i in response.xpath('//*[@class = "text"]//text()').extract() if i.strip()] # works better for stripping
        #all_text2 = response.xpath('//*[@class = "text"]//text()').xpath('normalize-space()').extract() # works but cleans them 1 by 1
        created_time = response.xpath('//*[@class = "created_at"]//text()').extract() # maybe use it for refreshing repository? Will see but good to have it.

        scraped_info[response.url] = all_text
        yield scraped_info
        '''

        # Give this output: 'Tagging Plugin ConfigurationConfigurationThe Tagging plugin can be added to your project
        print("procesing:"+response.url)

        scraped_info = {}
        all_text = response.xpath('//*[@class = "text"]').extract() # works better for stripping
        menu_scrub =  response.xpath('//*[@class = "menu-crumbs"]').extract() # check it for the keywords on top of the article
        if len(all_text) == 0:
            all_text = response.xpath('//*[@class = "row"]').extract()
        #all_text2 = response.xpath('//*[@class = "text"]//text()').xpath('normalize-space()').extract() # works but cleans them 1 by 1
        created_time = response.xpath('//*[@class = "created_at"]//text()').extract() # maybe use it for refreshing repository? Will see but good to have it.
        print(type(all_text))
        good_text =  re.sub('<[^>]*>', '', str(all_text)) # remove the html tags
        good_text =  re.sub(r'\s\s+', '', good_text)  # remove double empty spaces or more
        good_text =  good_text.replace('\\n\\n', ' ')
        good_text =  good_text.replace('\\n', '')
        good_text =  good_text.replace('\\', '')
        print(good_text)
        print(type(good_text))
        scraped_info[response.url] = good_text
        yield scraped_info
        