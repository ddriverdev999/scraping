from lxml import etree
import requests
import json

from pathlib import Path


##### download from url
def download(urls):
	for url in urls:
		filename = Path("2021/" + url[0] + "-" + url[1] + "-" + url[2].split("/")[-1])
		response = requests.get(url[2])
		filename.write_bytes(response.content)
######################

target_url = "http://www.ceo.kerala.gov.in/detailedResultsGE2021.html"
page = requests.get(target_url)
tree = etree.HTML(page.text)
distNos = tree.xpath('//*[@id="distNo"]/option/@value')
distNames = tree.xpath('//*[@id="distNo"]/option/text()')
distNos.pop(0)
distNames.pop(0)

### get total pdf link
def get_link(distNames):
	distNo = distNames.split(".")[0]
	destrict = distNames.split(".")[1]
	url = "http://www.ceo.kerala.gov.in/generalelections/lacListAjax2021.html?distNo="+distNo+"&sEcho=1&iColumns=2&sColumns=&iDisplayStart=0&iDisplayLength=100&iSortingCols=1&iSortCol_0=0&sSortDir_0=asc&bSortable_0=false&bSortable_1=false&undefined=undefined"

	payload={}
	headers = {
	  'Accept': 'application/json, text/javascript, */*',
	  'Accept-Language': 'en-US,en;q=0.9',
	  'Connection': 'keep-alive',
	  'Content-Type': 'application/x-www-form-urlencoded',
	  'Cookie': 'JSESSIONID=WS1~439E8951211DDCE071690F4701773C6F',
	  'Referer': 'http://www.ceo.kerala.gov.in/detailedResults.html',
	  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
	  'X-Requested-With': 'XMLHttpRequest'
	}

	response = requests.request("GET", url, headers=headers, data=payload)

	json_data = json.loads(response.text)

	result = []
	for item in json_data['aaData']:
		assembly = item[0]
		a_tag = item[1];
		a_tag_html = etree.HTML(a_tag)
		
		result.append([destrict, assembly, a_tag_html.xpath('//@href')[0]])
	return result

total_links = [];
for distName in distNames:
	total_links = total_links + get_link(distName)

download(total_links)
#############################################


