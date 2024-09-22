import scrapy

class CarSpider(scrapy.Spider):
    name = "car_spider"
    allowed_domains = ["cars.com"]
    start_urls = ['https://www.cars.com/shopping/results/?page=1&page_size=100&zip=60606']

    def parse(self, response):
        self.log('Đang xử lý URL: %s' % response.url)  # Ghi log URL để xác nhận trang đang được xử lý

        # Lặp qua tất cả các phần tử xe trên trang
        for car in response.css('div.vehicle-card'):
            # Kiểm tra dữ liệu có được thu thập không
            title = car.css('h2.title::text').get()
            stock_type = car.css('p.stock-type::text').get()
            mileage = car.css('div.mileage::text').get()
            price = car.css('span.primary-price::text').get()
            dealer_name = car.css('div.dealer-name strong::text').get()
            dealer_link = car.css('div.isa-dealer-deeplink a::attr(href)').get()

            if title and stock_type and price:
                yield {
                    'title': title,
                    'stock_type': stock_type,
                    'mileage': mileage,
                    'price': price,
                    'dealer_name': dealer_name,
                    'dealer_link': dealer_link,
                }
            else:
                self.log('Dữ liệu không đầy đủ: %s' % {
                    'title': title,
                    'stock_type': stock_type,
                    'mileage': mileage,
                    'price': price,
                    'dealer_name': dealer_name,
                    'dealer_link': dealer_link
                })
            # Pagination - follow next page if available
        next_page = response.xpath('//spark-button[@aria-label="Next page"]/@href').get()
        if next_page:
            next_page_url = response.urljoin(next_page)  # Tạo liên kết đầy đủ cho trang tiếp theo
            self.log('Đang chuyển đến trang tiếp theo: %s' % next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)