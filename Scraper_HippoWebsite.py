# -*- coding: utf-8 -*-
import scrapy
import html2text
import re
from scrapy.selector import HtmlXPathSelector
from bs4 import BeautifulSoup
from w3lib.html import remove_tags

class HippoWordSpider(scrapy.Spider):
    name = 'hippo_word'
    #allowed_domains = ['https://documentation.bloomreach.com/library/concepts/plugins/tagging/configuration.html']
    '''
    # testing with a few links
    list_url = ['https://www.onehippo.org/library/concepts/usage-statististics/usage-statistics.html','https://documentation.bloomreach.com/library/concepts/plugins/tagging/configuration.html',
    'https://www.onehippo.com/en/about/news/2013/11/hippo-named-critics-choice-for-best-open-source-cms-by-cms-critic.html',
    'http://www.onehippo.com/connect/boston',
    'https://www.onehippo.org/library/concepts/web-files/web-files-best-practices.html',
    'https://documentation.bloomreach.com/trails/developer-trail/develop-new-features/add-secondary-navigation-menu.html',
    'https://documentation.bloomreach.com/library/enterprise/installation-and-configuration/create-separate-distributions-for-cms-and-site.html',
    'https://developers.bloomreach.com/blog/2015/adding-a-workflow-to-hippo-cms-editor-toolbar.html',
    'https://www.onehippo.com/en/partners']
    '''
    list_url = []
    txt_import = open("url_file.txt", "r") # load list with ulr's
    for i in txt_import:
        list_url.append(i)
    def visible(self,element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif re.match('<!--.*-->', str(element.encode('utf-8'))):
            return False
        return True
    # List of URL's
    start_urls = [i for i in list_url]

    def parse(self, response):

        scraped_info = {}
        # Gathering info
        all_text = response.xpath('//*[@class = "text"]').extract() # works better for stripping
        if len(all_text) == 0:
            all_text = response.xpath('//*[@class = "row"]').extract()
        elif len(all_text) == 0:
            soup = BeautifulSoup(response.body, "lxml") 
            all_text = soup.findAll(text=True)
            all_text = list(filter(self.visible, all_text))
        #created_time = response.xpath('//*[@class = "created_at"]//text()').extract() # maybe use it for refreshing repository? Will see but good to have it.
        # Taking care of tags and words after that, preventing concatanation
        good_text = re.sub('(?<=[>])(?=[^\s])', ' ', str(all_text)) # Use this regex to match locations where preceding character is a dot or a comma and the next character isn't a space
        # Soup processing
        soup = BeautifulSoup(good_text, "html.parser")
        for div in soup.findAll("pre"): 
            div.decompose()
        for div in soup.findAll("span", {'class':'code'}): 
            div.decompose()
        good_text = soup.get_text()
        # Standard processing
        good_text =  re.sub('<[^>]*>', ' ', good_text) # remove the html tags
        good_text = re.sub("[\d+ % &]", " ", good_text)
        good_text = re.sub("(?<=[''])[✓_]|[✓_](?=[''])", " ", good_text)
        good_text = re.sub("(?<=[' '])[✓_]|[✓_](?=[' '])", " ", good_text)
        good_text =  re.sub(r'\s\s+', ' ', good_text)  # remove double empty spaces or more   
        good_text =  re.sub('&lt.*&gt;','',good_text)
        good_text =  good_text.replace('\\n\\n', ' ')
        good_text =  good_text.replace('\\n', '')
        good_text =  good_text.replace('\\', '')       
        good_text = good_text.replace('xa0',' ')
        good_text = good_text.replace('xa','')
        good_text = good_text.replace('  ',' ')
        good_text  = re.sub(r'([r])\1+', r'\1', good_text) # this and the one below remove r r r r r rr, which happens after the replace statements, changed it from a-z to only r because it messes up words otherwise
        good_text = re.sub(r'\b(\w+)( \1\b)+', r'\1', good_text)# removes combinations like this r r r r r r r r r
        '''
            Test for the two things above:
            - https://regex101.com/r/w0fcEL/1
            - https://regex101.com/r/3imhbd/1
        '''
        good_text =  re.sub(r'\s\s+', ' ', good_text)
        # Storing the cleaning good text
        #scraped_info[response.url] = good_text # stores the redirected pages
        original_url = response.meta.get('redirect_urls', [response.url])[0] # Deal with redirection
        scraped_info[original_url] = good_text
        yield scraped_info