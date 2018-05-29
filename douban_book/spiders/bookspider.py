import scrapy  
from douban_book.items import DoubanBookItem  
  
  
class BookSpider(scrapy.Spider):  
	"""docstring for BookSpider"""  
	name = 'douban-book'  
	allowed_domain = ['douban.com']  
	start_urls = ['https://book.douban.com/top250']  
  
	def parse(self, response):  
		yield scrapy.Request(response.url, callback = self.parse_page)  
  
		for page in response.xpath('//div[@class="paginator"]/a'):  
			link = page.xpath('@href').extract()[0]  
			yield scrapy.Request(link, callback = self.parse_page)  
  
	def parse_page(self, response):  
		for item in response.xpath('//tr[@class="item"]'):  
			book = DoubanBookItem()  
			book['name'] = item.xpath('td[2]/div[1]/a/@title').extract()[0]  
			book['ratings'] = item.xpath('td[2]/div[2]/span[@class="rating_nums"]/text()').extract()[0]  
			# book['ratings'] = item.xpath('td[2]/div[2]/span[2]/text()').extract()[0]  
			book_info = item.xpath('td[2]/p[1]/text()').extract()[0]  
			book_info_contents = book_info.strip().split(' / ')
			num = len(book_info_contents)
			if num == 4:
				book['author'] = book_info_contents[0]  
				book['publisher'] = book_info_contents[1]  
				book['edition_year'] = book_info_contents[2]  
				book['price'] = book_info_contents[3]
			if num == 5:
				book['author'] = book_info_contents[0]
				book['author1'] = book_info_contents[1]  
				book['publisher'] = book_info_contents[2]  
				book['edition_year'] = book_info_contents[3]  
				book['price'] = book_info_contents[4]
			yield book




