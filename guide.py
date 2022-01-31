import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.shell import inspect_response


class GuideSpider(CrawlSpider):
    name = 'guide'
    allowed_domains = ['www.bmg.org.uk']
    start_urls = ['https://www.bmg.org.uk/find-a-guide']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="guides-filter"]/following-sibling::ul/li/a'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):

        name = response.xpath('//h1/text()').get()
        short_bio = response.xpath('//div[@class="guide-bio-extract"]/text()').get().strip().replace('\n', '').replace('\t', '')

        other_links = []

        website = None
        email = None
        phone = None
        contact = response.xpath('//div[@class="guide-contact"]/ul/li').getall()
        for i in contact:
            k = Selector(text=i).xpath('.//a/text()').getall()
            b = []
            for a in k:
                a = a.strip().replace('\n', '').replace('\t', '')
                if a != '':
                    b.append(a)
            k = b

            if '@' in k[0]:
                email = k
            elif 'http' in k[0]:
                website = k
            else:
                phone = k


        facebook = None
        ig = None
        twitter = None
        linkedin = None
        social = response.xpath('//div[@class="social-links"]/ul/li/a/@href').getall()
        for i in social:
            i = i.strip().replace('\n', '').replace('\t', '')

            if 'twitter' in i:
                twitter = i
            elif 'facebook' in i:
                facebook = i
            elif 'instagram' in i:
                ig = i
            elif 'linkedin' in i:
                linkedin = i
            else:
                other_links.append(i)
        activities = []    
        a = response.xpath('(//div[@class="guide-activities"])[1]/ul/li/text()').getall()
        for b in a:
            b = b.strip().replace('\n', '').replace('\t', '')
            if b != '':
                activities.append(b)
        activities2 = []
        c= response.xpath('(//div[@class="guide-activities"])[2]/ul/li/a/text()').getall()
        for d in c:
            d = d.strip().replace('\n', '').replace('\t', '')
            if d != '':
                activities2.append(d)

        membership_type = response.xpath('string(//div[@class="guide-activities"]/p)').get().strip().replace('\n', '').replace('\t', '')

        print('\n\n')
        return {
            'Name': name,
            'Membership Type': membership_type,
            'Short Bio': short_bio,
            'Activities': activities,
            'Activities 2': activities2,
            'Email': email,
            'Phone Number': phone,
            'Website': website,
            'LinkedIn': linkedin,
            'Instagram': ig,
            'Facebook': facebook,
            'Twitter': twitter,
            "Other Links": other_links
        }