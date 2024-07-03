from flask import Flask, request, jsonify, render_template
import requests
import re
import json
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor

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
def get_testequity(Product_name):
    cookies = {}  # 如果有需要，可以在这里设置cookies
    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'if-modified-since': 'Wed, 26 Jun 2024 07:18:13 GMT',
        'if-none-match': 'W/"ab296c70221041249e9856806b84821a"',
        'priority': 'u=1, i',
        'referer': 'https://www.testequity.com/Search?query=megger%20mit515',
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
        'includeSuggestions': 'true',
        'search': Product_name,
        'expand': 'attributes,facets,variantTraits,badges,properties',
        'applyPersonalization': 'true',
        'includeAttributes': 'includeOnProduct'
    }

    try:
        response = requests.get(
            'https://www.testequity.com/api/v2/products',
            params=params,
            cookies=cookies,
            headers=headers,
        )
        response.raise_for_status()  # 如果请求不成功，会抛出异常
        return response.json().get("products", [])  # 返回产品列表，如果没有则返回空列表
    except requests.exceptions.RequestException as e:
        print(f"Error fetching product data: {e}")
        return []  # 出错时返回空列表，或者根据需求返回其他默认值
def get_grainger(Product_name):
    cookies = {}

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Referer': 'https://www.grainger.com/product/MEGGER-Megohmmeter-100-kiloohm-to-40D468?searchQuery=mit525&searchBar=true',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-dtpc': 'ignore',
    }

    params = {
        't': Product_name,
        'tae': 'true',
        '_': str(get_current_timestamp()),
    }

    try:
        response = requests.get('https://www.grainger.com/tap', params=params, cookies=cookies, headers=headers)
        response.raise_for_status()
        response_json = response.json()
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
        return None

    try:
        product_url = 'https://www.grainger.com' + response_json[0]["url"]
        product_response = requests.get(product_url, headers=headers)
        product_response.raise_for_status()
        product_page = product_response.text
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None

    pattern = re.compile(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', re.DOTALL)
    match = pattern.search(product_page)

    if match:
        json_str = match.group(1).strip()
        try:
            data_json = json.loads(json_str)
            return data_json
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        print("No JSON found in the HTML data.")
        return None
def get_hken_rs(product_name):
    cookies = {}

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'referer': 'https://hken.rs-online.com/web/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    }

    params = {
        'searchTerm': product_name,
    }

    try:
        response = requests.get('https://hken.rs-online.com/web/c/', params=params, cookies=cookies, headers=headers)
        response.raise_for_status()  # 确保请求成功
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []

    try:
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找 <script> 标签并提取 JSON 数据
        script_tag = soup.find('script', {'id': '__NEXT_DATA__', 'type': 'application/json'})
        json_data = script_tag.string

        # 解析 JSON 数据并赋值给变量 data
        data = json.loads(json_data)

        # 提取需要的数据
        datas = data["props"]["pageProps"]["searchFilterResultsData"]["groupBySearchResults"]["resultsList"]["records"]
        return datas
    except (AttributeError, KeyError, json.JSONDecodeError) as e:
        print(f"Data extraction failed: {e}")
        return []

def query_data(product_name):
    with ThreadPoolExecutor(max_workers=9) as executor:
        future_tequipment = executor.submit(get_tequipment, product_name)
        future_instrumart = executor.submit(get_instrumart, product_name)
        future_tester = executor.submit(get_tester, product_name)
        future_test_meter = executor.submit(get_test_meter, product_name)
        future_testequipmentdepot = executor.submit(get_testequipmentdepot, product_name)
        future_transcat = executor.submit(get_transcat, product_name)
        future_testequity = executor.submit(get_testequity, product_name)
        future_grainger = executor.submit(get_grainger, product_name)
        future_hken_rs = executor.submit(get_hken_rs, product_name)
        results = []

        data_tequipment = future_tequipment.result()
        data_instrumart = future_instrumart.result()
        data_tester_list = future_tester.result()
        data_test_meter_list = future_test_meter.result()
        data_testequipmentdepot_list = future_testequipmentdepot.result()
        data_transcat_list = future_transcat.result()
        data_testequity_list = future_testequity.result()
        data_grainger_list = future_grainger.result()
        data_hken_rs_list = future_hken_rs.result()
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
        if data_testequity_list:
            for data_testequity in data_testequity_list:
                results.append({
                    'source': 'testequity',
                    'name': data_testequity['productTitle'],
                    'price': data_testequity['unitListPriceDisplay'],
                    'link': "https://www.testequity.com/"+data_testequity["canonicalUrl"]
                })
        if data_grainger_list:
            data_grainger = data_grainger_list
            results.append({
                'source': 'grainger',
                'name': data_grainger['model']+" "+data_grainger["name"],
                'price': "$"+data_grainger['offers']["price"],
                'link': data_grainger['offers']["url"]
            })
        if data_hken_rs_list:
            for data_hken_rs in data_hken_rs_list:
                results.append({
                    'source': 'hken_rs',
                    'name': data_hken_rs["name"],
                    'price': data_hken_rs["breakPrice"],
                    'link': "https://hken.rs-online.com"+data_hken_rs["productUrl"]
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
