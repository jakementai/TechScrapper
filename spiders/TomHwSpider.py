import scrapy
from TechSiteScrapper.items import ContentItem, HistoryItem

class TomHwSpider(scrapy.Spider):

    # Scrapy Varaiables 
    name = "TomHwSpider"
    start_urls = [""]

    # User Variable
    pageCounter = 0
    combinedArticleLinks = []
    crawledLinks = []
    homepage_link = "https://forums.tomshardware.com"
    
    def start_requests(self):
        yield scrapy.Request(self.homepage_link, self.parseFindLinks)

    # Used once only, get the category links of the web forum
    def parseFindLinks(self, response):
        categoryLinks = list(response.xpath("//h3[@class='node-title']/a/@href").getall())

        for link in categoryLinks :
            yield scrapy.Request(self.homepage_link + link)

    # Get the article links and if there is a next page link, generate another request
    def parse(self, response):
        articleLinks = response.xpath("//div[contains(@class, 'structItem-title')]/a[not(@class='labelLink')]/@href").getall()
        nextPageLink = response.xpath("//a[@class='pageNav-jump pageNav-jump--next']/@href").get()
        pageTitle = response.xpath("//h1[@class='p-title-value']/text()").get()

        # Pass the link to item Pipeline to save to history 
        crawledLink = HistoryItem()
        crawledLink['link'] = str(response.request.url)
        crawledLink['title'] = str(pageTitle)
        yield crawledLink

        self.combinedArticleLinks += articleLinks
        self.crawledLinks += [nextPageLink]
        
        # Generate new Requests if there is a next page, basically follows the next page link
        # until there is no more next page link
        if nextPageLink:
            self.pageCounter += 1
            #print("Current Page Number: " + str(self.pageCounter)+ " Current Link: " + nextPageLink)
            yield scrapy.Request(url= str(self.homepage_link + nextPageLink))
            
        # Genereate new Request for all the articles in the page
        # Basically get all the contents of the articles
        if articleLinks:
            for link in articleLinks:
                yield scrapy.Request(str(self.homepage_link + link), self.parseArticleContent)


    def parseArticleContent(self, response):
        # TODO yield the article link for history link
        crawledLink = HistoryItem()
        crawledLink['link'] = str(response.request.url)
        crawledLink['title'] = str(response.xpath("//h1[@class='p-title-value']/text()").get())
        yield crawledLink

        # codes to get the content of the articles
        main_cat = response.xpath("//span[@itemprop='name']/text()").getall()[1]
        sub_cat = response.xpath("//span[@itemprop='name']/text()").getall()[2]
        forum_title = response.xpath("//h1[@class='p-title-value']/text()").get()
        contents = response.xpath("//div[@class='bbWrapper']/text()").getall()
        link = response.request.url

        # Send item to pipeline to process and save
        crawledContent = ContentItem()
        crawledContent["forum_title"] = forum_title
        crawledContent["main_category"] = main_cat
        crawledContent["sub_category"] = sub_cat
        crawledContent["link"] = link
        crawledContent["content"] = contents
        yield crawledContent

         
        print("Successffully scraped content!")  

        # if there is a next page in the forum, proceed to scrape the next page
        nextPageLink = response.xpath("//a[@class='pageNav-jump pageNav-jump--next']/@href").get()
        if nextPageLink:
             yield scrapy.Request(str(self.homepage_link + nextPageLink), self.parseArticleContent)

        
    # This Method is called when the spider is Closed
    def closed(self, reason):
        print("[CLOSED] Reason: " + str(reason))
        print("Total Page found : " + str(self.pageCounter))
        print("Total Link article count: " + str(len(self.combinedArticleLinks)))

    

