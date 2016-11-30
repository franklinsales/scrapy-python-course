# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request


class ProjectSpider(Spider):
	name = "project"
	allowed_domains = ["books.toscrape.com"]
	start_urls = ['http://books.toscrape.com/']

	infoBooks = []

	def parse(self, response):
		#Get all links Books
		linksBooks = response.xpath('//*[@class="product_pod"]/h3/a/@href').extract()
		for linkBook in linksBooks:
			finalLink = response.urljoin(linkBook)
			yield Request(finalLink, self.bookInfos)			
		nextLink = response.xpath('//*[@class="next"]/a/@href').extract_first()
		nextUrl = response.urljoin(nextLink)
		yield Request(nextUrl)		


	def bookInfos(self, response):
		titleBook = response.xpath("//h1/text()").extract_first()
		categoryBook = response.xpath('//*[@class="breadcrumb"]/li[3]/a/text()').extract_first()
		availability = response.xpath('//*[@class="col-sm-6 product_main"]/*[@class="instock availability"]').extract_first()
		if availability == []:
			availabilityBook = "No"
		else:
			availabilityBook = "Yes"

		priceBook = response.xpath('//*[@class="table table-striped"]/tr[4]/td[1]/text()').extract_first()

		contentRating = response.xpath('//*[@class="col-sm-6 product_main"]/p[3]/@class').extract_first().split(" ")
		ratingBook = contentRating[1]

		srcImg = response.xpath('//*[@id="product_gallery"]/*[@class="thumbnail"]/*[@class="carousel-inner"]/*[@class="item active"]/img/@src').extract_first()
		imageBook = srcImg.replace("../../", self.start_urls[0])


		descriptionBook = response.xpath('//*[@class="product_page"]/p/text()').extract_first()

		return {
			'Title': titleBook,
			'Category': categoryBook,
			'Availability': availabilityBook,
			'Price': priceBook,
			'Rating': ratingBook,
			'Image': imageBook,
			'Description': descriptionBook
		}
