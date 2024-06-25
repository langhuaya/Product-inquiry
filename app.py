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

def query_data(product_name):
    data_tequipment = get_tequipment(product_name)
    data_instrumart = get_instrumart(product_name)
    data_tester_list = get_tester(product_name)

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

    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_name = request.form['product_name']
        if product_name:
            data = query_data(product_name)
            return render_template('results.html', data=data)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
