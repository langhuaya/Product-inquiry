from flask import Flask, request, jsonify, render_template
import requests
import re
import json
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

def get_current_timestamp():
    timestamp = int(time.time() * 1000)
    return timestamp

def get_tequipment(Product_name):
    try:
        cookies = {}
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'adrum': 'isAjax:true',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.tequipment.net',
            'priority': 'u=1, i',
            'referer': 'https://www.tequipment.net/',
            'sec-ch-ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
            'x-requested-with': 'XMLHttpRequest',
        }

        data = {
            'f': 'DisplaySuggest',
            'q': Product_name,
        }

        response = requests.post('https://www.tequipment.net/ajax/store/idevajax.aspx', cookies=cookies, headers=headers, data=data)
        return response.json()
    except Exception as e:
        print(f"Error fetching data from TEquipment: {e}")
        return None

def get_tester(Product_name):
    try:
        cookies = {}
        headers = {}
        params = {
            'search': Product_name,
            '_': str(get_current_timestamp()),
        }

        response = requests.get('https://www.tester.co.uk/search/es/index', params=params, cookies=cookies, headers=headers)
        return response.json()["items"]
    except Exception as e:
        print(f"Error fetching data from Tester: {e}")
        return None

def get_instrumart(Product_name):
    try:
        cookies = {}
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.instrumart.com',
            'priority': 'u=1, i',
            'referer': 'https://www.instrumart.com/',
            'sec-ch-ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
            'x-requested-with': 'XMLHttpRequest',
        }

        data = {
            'query': Product_name,
        }

        ab = requests.post('https://www.instrumart.com/search/get-ab', cookies=cookies, headers=headers, data=data).text
        params = {
            'query': Product_name,
            'ab': ab,
        }

        html_doc = requests.get('https://www.instrumart.com/search', params=params, cookies=cookies, headers=headers).text
        soup = BeautifulSoup(html_doc, 'html.parser')
        products = soup.find_all('div', class_='card--product-stacked')
        return products
    except Exception as e:
        print(f"Error fetching data from Instrumart: {e}")
        return None


def get_testequipmentdepot(product_name):
    try:
        cookies = {
        }

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'priority': 'u=0, i',
            'referer': 'https://www.testequipmentdepot.com/',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        }

        params = {
            'q': product_name,
        }

        response = requests.get(
            'https://www.testequipmentdepot.com/catalogsearch/result/',
            params=params,
            cookies=cookies,
            headers=headers,
        ).text

        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(response, 'html.parser')

        # 查找所有<script type="text/x-magento-init">标签
        scripts = soup.find_all('script', {'type': 'text/x-magento-init'})

        # 提取JSON数据并解析
        data_testmeter_list = []
        for script in scripts:
            json_data = script.string.strip()
            data_testmeter_list.append(json.loads(json_data))

        return \
        data_testmeter_list[1]["*"]["DecimaDigital_DataLayer/js/view/google-tag-manager"]["items"][1]["ecommerce"][
            "items"]

    except requests.RequestException as e:
        print(f"Network-related error occurred: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error occurred: {e}")
    except IndexError as e:
        print(f"Index error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None

def get_test_meter(Product_name):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Origin': 'https://www.test-meter.co.uk',
        'Referer': 'https://www.test-meter.co.uk/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'content-type': 'application/x-www-form-urlencoded',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-algolia-api-key': 'ZTdhYzYwYjQ2YWJkMDQzNjcyNjhhMWEwY2FkOGUyYzI3ODBlZDU2YzNjZGVlMWI3NDBiNGI3MzcwOGE3N2ZhN3RhZ0ZpbHRlcnM9',
        'x-algolia-application-id': '3JOKTRZ7OO',
    }

    data = '{"requests":[{"indexName":"magento_default_products","query":"'+Product_name+'","params":"hitsPerPage=6&highlightPreTag=__aa-highlight__&highlightPostTag=__%2Faa-highlight__&numericFilters=visibility_search%3D1&ruleContexts=%5B%22magento_filters%22%2C%22%22%5D&clickAnalytics=true"}]}'

    try:
        response = requests.post(
            'https://3joktrz7oo-2.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.5.1)%3B%20Browser%3B%20autocomplete-core%20(1.6.3)%3B%20autocomplete-js%20(1.6.3)',
            headers=headers,
            data=data,
        ).json()
        return response["results"][0]["hits"]
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return []
    except KeyError as e:
        print(f"Key error: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_transcat(Product_name):
    cookies = {}

    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'priority': 'u=1, i',
        'referer': 'https://www.transcat.com/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'q': Product_name,
        '_': str(get_current_timestamp()),
    }

    product_details = []

    def extract_price(html_content):
        # Define regex patterns
        call_for_price_pattern = r'<div class="call-for-price">Call for price</div>'
        price_pattern = r'<span class="price">\$(.*?)</span>'

        # Search for matches
        call_for_price_match = re.search(call_for_price_pattern, html_content)
        price_match = re.search(price_pattern, html_content)

        # Extract price information
        if call_for_price_match:
            return "Call for price"
        elif price_match:
            price = price_match.group(1)
            return f"${price}"
        else:
            return "Price not found"

    try:
        response = requests.get('https://www.transcat.com/search/ajax/suggest/', params=params, cookies=cookies, headers=headers).json()
        product_entries = [entry for entry in response if entry['type'] == 'product']

        for product in product_entries:
            product_detail = {
                'title': product['title'],
                'price': extract_price(product['price']),
                'url': product['url']
            }
            product_details.append(product_detail)
    except Exception as e:
        print(f"An error occurred: {e}")

    return product_details
def query_data(product_name):
    data_tequipment = get_tequipment(product_name)
    data_instrumart = get_instrumart(product_name)
    data_tester_list = get_tester(product_name)
    data_test_meter_list = get_test_meter(product_name)
    data_testequipmentdepot_list = get_testequipmentdepot(product_name)
    data_transcat_list = get_transcat(product_name)

    results = []
    if data_tequipment and "Products" in data_tequipment:
        for item in data_tequipment["Products"]:
            results.append({
                'source': 'TEquipment',
                'name': item['ProductName'],
                'price': item['Price'],
                'link': f"https://www.tequipment.net{item['URL']}"
            })

    if data_instrumart:
        for product in data_instrumart:
            name = product.find('div', class_='product-name').text.strip()
            price = product.find('div', class_='product-price').text.strip()
            link = product.find('a')['href']
            full_link = 'https://www.instrumart.com' + link
            results.append({
                'source': 'Instrumart',
                'name': name,
                'price': price,
                'link': full_link
            })

    if data_tester_list:
        for data_tester in data_tester_list:
            results.append({
                'source': 'Tester',
                'name': data_tester['name'],
                'price': data_tester['price_label'],
                'link': f"https://www.tester.co.uk{data_tester['url']}"
            })
    if data_test_meter_list:
        for data_test_meter in data_test_meter_list:
            # print(data_test_meter["name"])
            # print(data_test_meter["url"])
            # print(data_test_meter["price"]["USD"]["default_formated"])
            results.append({
                'source': 'test_meter',
                'name': data_test_meter['name'],
                'price': data_test_meter["price"]["USD"]["default_formated"],
                'link': data_test_meter["url"]
            })

    if data_testequipmentdepot_list:
        for data_testmeter in data_testequipmentdepot_list:
            # print(f"产品标题: {data_testmeter['item_name']}")
            # print(f"产品价格: {data_testmeter['price']}USD")
            # print(f"产品链接: {data_testmeter['item_url']}")
            results.append({
                'source': 'testequipmentdepot',
                'name': data_testmeter['item_name'],
                'price': f"${data_testmeter['price']}",
                'link': data_testmeter['item_url']
            })
    if data_transcat_list:
        for data_transcat in data_transcat_list:
            results.append({
                'source': 'transcat',
                'name': data_transcat['title'],
                'price': data_transcat['price'],
                'link': data_transcat['url']
            })
    return results



@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    if request.method == 'POST':
        product_name = request.form['product_name']
        if product_name:
            data = query_data(product_name)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
