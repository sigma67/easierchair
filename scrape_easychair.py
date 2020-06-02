#!/usr/bin/python
# -*- coding: utf-8  -*-
""" Bot to scrape a list of EasyChair submissions and upload them to a wiki """
#
# (C) Federico Leva, 2016
#
# Distributed under the terms of the MIT license.
#
__version__ = '0.1.0'

import requests
from lxml import html
import re
import json
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')

cj = requests.cookies.cookiejar_from_dict(json.loads(config['settings']['cookie']))
headers = {"User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0" }
index = requests.get("https://easychair.org/conferences/submissions?a=" + config['settings']['conference_id'], cookies=cj, headers=headers)
indexdata = html.fromstring(index.text)
urls = indexdata.xpath('//a[contains(@href,"submission_view")]/@href')
export = open("easychair-submissions.json", "w+", encoding='utf-8')
papers = []

for url in urls:
	sub = html.fromstring(requests.get("https://easychair.org/" + url, cookies=cj, headers=headers).text)
	thispaper = {}
	thispaper['number'] = re.findall("[0-9]+", sub.xpath('//div[@class="pagetitle"]/text()')[0])[0]
	thispaper['title'] = sub.xpath('//td[text()="Title:"]/../td[2]/text()')[0].strip()
	# thispaper['names'] = sub.xpath('//b[text()="Authors"]/../../..//tr[position()>2]/td[1]/text()')
	# thispaper['surnames'] = sub.xpath('//b[text()="Authors"]/../../..//tr[position()>2]/td[2]/text()')
	# thispaper['emails'] = sub.xpath('//b[text()="Authors"]/../../..//tr[position()>2]/td[3]/text()')
	# thispaper['countries'] = sub.xpath('//b[text()="Authors"]/../../..//tr[position()>2]/td[4]/text()')
	thispaper["abstract"] = sub.xpath('//td[text()="Abstract:"]/../td[2]/text()')
	thispaper["decision"] = sub.xpath('//td[text()="Decision:"]/../td[2]/b/text()')
	thispaper['keywords'] = sub.xpath('//div[parent::td[@class="value"]]/text()')
	papers.append(thispaper)

export.write(json.dumps(papers))

export.close()