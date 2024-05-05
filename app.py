from flask import Flask, request, jsonify, render_template
app = Flask(__name__)
import requests,re,json,tk
from bs4 import BeautifulSoup


def get_tequipment(Product_name):
    cookies = {}

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'adrum': 'isAjax:true',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'visid_incap_619296=6aVUMukyQYazjs/17aKuMmF8+mUAAAAAQUIPAAAAAABq0aJ/IIWLgYIPfFC+XJfU; sidcor=HzaQ1JYwwMKz4yrndYVMs0K3TIEv%2bmeLPz%2fA8AnkvtI%3d; OriginReferer=origin-www.tequipment.net; CertonaScriptUrl=%2f%2fedge1.certona.net%2fcd%2f184c51d2%2ftequipment.net%2fscripts%2fresonance.js; _pxvid=b234de58-e67f-11ee-8cb5-6f127274a3b8; visid_incap_619305=9TgjL1cTQvuMWsZsbf7OQUfVAGYAAAAAQUIPAAAAAADbooG/yBnNtvPMsc+KNz6f; osano_consentmanager_uuid=5a4509f3-d417-452e-982a-615bb7e517e3; osano_consentmanager=DzXPSlOILvlggB9coFZKK-rHEO4LJzldl1ZnjJhFhtU_r-MhFmFQmXIPLLj0IN9AVBPuV_O1TRbHePfTWzjwhATh3mPQZRlmb2axDUl6NoY9BJzoLIiEQfenmp_Y0ffd1sP4lzbW644fc7RDNX9mJ4iA90l8npvQlln8VsPv3zr0t_bmV3x6Dz1yrKZDyqO1IbARTDs-Y9GLTFL5IswLPAiORYh9_1ACAQRvtv46nw58EGaJ8jQhww32iWIWR5NrmfTk2Qu3tV7mg_JwIr9M_IwU9WCSyr38q2KkAA==; _ga=GA1.1.795774182.1711330669; _ga=GA1.1.795774182.1711330669; _ga_2SMSM5SHBQ=GS1.1.1711330669.1.0.1711330669.60.0.0; _ga_2SMSM5SHBQ=GS1.1.1711330669.1.0.1711330669.60.0.0; RES_TRACKINGID=534455838423412; ResonanceSegment=1; _hjSessionUser_1232208=eyJpZCI6Ijg4ODIxOTczLWVmNzMtNWEzZi1iNmMwLWNmYTk3YzFlNGU5OCIsImNyZWF0ZWQiOjE3MTEzMzA3MDEwMTQsImV4aXN0aW5nIjp0cnVlfQ==; bluecoreNV=false; _gcl_au=1.1.212514835.1712803612; idevlayout=list; _gid=GA1.2.770237207.1714441871; KC2soX8QyVu9VSpCE5K1OiX8fFlZnUoIulfa3CnQ34U%3d=; midcor=; tokcor=; EBiVxdSEqAahmFSkfnErzp5jEnZ40jBtddb4aUdPaqI%3d=iDmOujDdV1llyBjTQ7zBEOrc7u5dIQGZ%2bBaz3PSd7SpOxgZ6xCAyFdSVHEdCc4Sm; PmqutB2U4h6QrsV5vssBJwq%2boKPsJEvP2CjloGYu9p4%3d=; oidcor=; Dx4FQQIsCsCk%2bXmKmMt15NwNqNNy%2fdSzkxNjAmtjRKI%3d=; qidcor=; fcaid=bac300d861ac490e60b93c08686d64d89074eee8665618c949f29286026acb20; frontChatChannelToken=0gbLyQQD-n-Sab57VBrvP6gJYU_uIE4S0OryES3S3kMmwJ1LTl6K3c7H7HhaBypycFwc6F4f4ocSZ7hJjcub2uIb9A; pxcts=13419d28-0694-11ef-b00b-c298f51ff129; fcuid=39c2b052-66b4-484a-b6a7-3f6f299244de; fccid=583ba72b-24ad-4e8a-9fb2-c291f8bc827c; cl0%2f%2fjNWDfRPd1ZzE%2fbznzLGxuRCgisA%2fVwPtBGU1QGyAquw07Su0Tg8MqZsDzs4=; pdKvWm75WZXalyv78ju12znIcgYTZ1b3KpN3Igs3kMxxodoJr%2bdTzEc%2frT7QBzrf=; incap_ses_256_619296=Wzb/bE7ZQnaQq0HEq36NA9lqMGYAAAAAfsr6qiPYbWQ80yPMf/DsMQ==; incap_ses_415_619296=0boacsGVwjd+22/DWGDCBRaNMGYAAAAAwoVzAyscEh48kO2f8s5dQg==; SessionValueId=456326; uQBJTAzERbI1ij1afIBBYW0%2bTgcJkCiwNLZLK%2br6ir%2fd9p%2fA5zVNuq8vdMqIOCnO=y%2b9MkkT312%2b9YS%2f%2bmKFFxtvb5F0xHaowJfZgFsOz6ENoEbYZCVNAZrn7NizHwDGelDao%2bPIt%2f1xuOqH3YG2agotAgHiB4fKVh2ZuiYZkyY6qmFJufPZz6dy%2b9igOOohZwPV%2f%2bEzbwHTaFY4Y6pjrMJvk4QXJr5nhKVC7ObLREoknoZj3p3AdYxD6NMp2wT5eKoqFVkfARriMIw4bJ3ubak1h5JysDsoxTwK8YNnYHh5eeHiYh2JA4hRo0tkUmN2mUfNEvVN44fq6ZmJTI26cFyr7Ycnxau0Jn6vu4Bb4O2ogMWiTKTiXU7jZtRnm%2f3N88L8Z2DposzPY0VTHnLG28v%2f9rJTUJwx4cFedt2f%2btkaad9U7oDia7T5aa1JJv05%2fm8X3P8ALbk%2bfuFwJHaGHxXsKSnlJx35rkGbEKx46hfNh2IpZ3Tle%2f%2bOR3V0hABY2; LastItemId_3=869328; incap_ses_1045_619296=f9d/YCEbjnnsa+eb/ZWADqGbMGYAAAAAX2fe0LrQ5FfxHrSr35Tx4A==; RES_SESSIONID=269685779535628; incap_ses_426_619296=Nh1ZYajZrkUAXE3T0HTpBa2bMGYAAAAACGMnLYJJrXvwntSc5ZoaVA==; bc_invalidateUrlCache_targeting=1714461636824; _hjSession_1232208=eyJpZCI6IjhhYmQyNDIxLWRjYzEtNDdiYS1iYmE1LTU0YmYwNDM2NTZkMiIsImMiOjE3MTQ0NjE2MzkzMTUsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; ADRUM=s=1714461644448&r=https%3A%2F%2Fwww.tequipment.net%2FProduction-Basics%2FESD-Laminate-Station%2FWorkbenches%2F%3Fhash%3D1826049377; mp_tequipment_mixpanel=%7B%22distinct_id%22%3A%20%2218e5a75e91350a-0ee86ab2aa9403-4c657b58-1fa400-18e5a75e9141940%22%2C%22bc_persist_updated%22%3A%201711334645705%2C%22bc_id_cache%22%3A%20%22%7B%5C%22obem%5C%22%3A130310361%7D%22%2C%22bc_id%22%3A%20130310361%2C%22g_search_engine%22%3A%20%22bing%22%7D; _uetsid=1ea10990069411ef9fb6cd0e417c8c9a|1pszgie|2|fld|0|1581; _ga=GA1.1.795774182.1711330669; _ga_2SMSM5SHBQ=GS1.1.1714461639.8.1.1714461645.54.0.0; cto_bundle=XA-jfV96SmhVYnJwZWVURDRHOEhNZm5aeWp1ZmhnQVQyTUtsT1VFcFNFQVdwOXZkTFVxbHFjQWZhVzB4U1lYRUFCelFsem5nYTJ4TTVqRURtejVFZElWOXIzNld0JTJCJTJCWHVBTHR6Q2dycU52Z1c2NzZCTDFzenNrclIlMkZPTGRURzZEUTNwQVV2NTRoNjNvOSUyRiUyQmNpZ0Fhd2tnNGt3JTNEJTNE; _uetvid=b12b5680e67f11eea2f8695d0b282930|3d3oxr|1714461647018|3|1|bat.bing.com/p/insights/c/t; _dd_s=logs=1&id=8dbca03e-a51c-4dde-a208-630ac1e9d26e&created=1714461626401&expire=1714462623012',
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

    get_tequipment_data = requests.post('https://www.tequipment.net/ajax/store/idevajax.aspx', cookies=cookies, headers=headers,
                             data=data).json()
    return get_tequipment_data




def get_aicaigou(Product_name):
    try:
        cookies = {}

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'priority': 'u=0, i',
            'referer': 'https://b2b.baidu.com/s?q=MIT300&from=sug&fid=83951616%2C1714445010442&pi=b2b.index.sug...5745581331674132',
            'sec-ch-ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
        }

        params = {
            'q': Product_name,
            'from': 'search',
            'fid': '83951616,1714445010442',
            'pi': 'b2b.s.search...8510291871107560',
        }

        response = requests.get('https://b2b.baidu.com/s', params=params, cookies=cookies, headers=headers).text
        # print(response)
        html_data = response

        # 使用正则表达式提取 JSON 数据
        pattern = re.compile(r'window\.data\s*=\s*(\{.*?\});', re.DOTALL)
        match = pattern.search(html_data)
        if match:
            json_text = match.group(1)
            json_data = json.loads(json_text)
            # print(json_data)
            return  json_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_instrumart(Product_name):
    cookies = {}

    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '_gcl_au=1.1.113513761.1711334740; hblid=H7mKlQGGosryiIEt8c6VW0Hj60rAK00b; olfsk=olfsk0019320933387076966; .AspNetCore.Session=CfDJ8Ox80PtyDpJIuSdnj%2FGdjzfUl9JKtfJUYh30QxYw9oMlsIp5Z9oKaDdGf9bltN6sEBwHfUOQ2SUPmvsiSRquBJzEDmgvMAOqGl49Ar%2BucXJflWOaM93llRYy4b1%2BHqodFIJDgAf1SSoSjeQ5a1NfV3mNbA4BH0ocYuJcCC6vu2wx; b1P=314c5465cde4cb493c7ca2f9ec28061c_1714463902; _gid=GA1.2.291146928.1714463926; _ga_DYPEKWV2LM=GS1.1.1714472524.4.0.1714472524.60.0.0; _ga=GA1.2.2026169834.1711334740; _dc_gtm_UA-2248646-1=1; __cookieprobe=1714472524400; wcsid=dTZj6WtqLujxeGzh8c6VW0HoBOz0A0ab; _oklv=1714472538543%2CdTZj6WtqLujxeGzh8c6VW0HoBOz0A0ab',
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
    # print(ab)
    params = {
        'query': Product_name,
        'ab': ab,
    }

    html_doc = requests.get('https://www.instrumart.com/search', params=params, cookies=cookies, headers=headers).text
    # print(html_doc)

    # 假设你已经将HTML内容加载到了一个名为html_doc的字符串变量中
    soup = BeautifulSoup(html_doc, 'html.parser')

    # 查找所有的产品卡片
    products = soup.find_all('div', class_='card--product-stacked')

    # 遍历每个产品卡片并提取信息
    return products




# def query_data(Product_name):
#     data_tequipment_list = get_tequipment(Product_name)
#     print("tequipment搜索到：", data_tequipment_list["Count"], "个相关数据")
#     for data_tequipment in data_tequipment_list["Products"]:
#         print("产品名称：" + data_tequipment["ProductName"], "产品SKU:" + data_tequipment["SKU"],
#               "产品型号：" + data_tequipment["CatalogNumber"], "产品价格最低价：" + data_tequipment["Price"] + "美金",
#               "产品链接：https://www.tequipment.net" + data_tequipment["URL"],
#               "产品描述：" + data_tequipment["ShortDescription"])
#
#     data_aicaigou_list = get_aicaigou(Product_name)
#     if data_aicaigou_list != None:
#         print("爱采购找到：" + str(data_aicaigou_list["dispNum"]) + "个产品链接")
#         # for data_aicaigou in data_aicaigou_list["productList"][:-1]:
#         for data_aicaigou in data_aicaigou_list["productList"]:
#             if 'type' in data_aicaigou:
#                 continue
#             print("产品标题：【" + data_aicaigou["fullName"] + "】", "产品链接：" + data_aicaigou["jUrl"],
#                   "价格：【" + data_aicaigou["price"] + "】"+data_aicaigou["pCurrency"], "商家名称：" + data_aicaigou["fullProviderName"],
#                   "位置地点：" + data_aicaigou["location"])
#     data_instrumart_list = get_instrumart(Product_name)
#     print("instrumart平台找到"+str(len(data_instrumart_list))+"个产品信息")
#     for product in data_instrumart_list:
#         name = product.find('div', class_='product-name').text.strip()
#         description = product.find('div', class_='product-description').text.strip()
#         price = product.find('div', class_='product-price').text.strip()
#         link = product.find('a')['href']  # 提取产品链接
#         base_url = 'https://www.instrumart.com'
#         full_link = base_url + link
#         print(f"产品标题: {name}")
#         print(f"产品描述: {description}")
#         print(f"产品价格: {price}")
#         print(f"产品链接: {full_link}")
#         print("----------")


def query_data(product_name):
    # 假设这里是你的数据抓取逻辑
    # 这里只是一个示例，你应该根据实际返回的数据结构来调整
    data_tequipment = get_tequipment(product_name)
    data_aicaigou = get_aicaigou(product_name)
    data_instrumart = get_instrumart(product_name)

    results = []
    if data_tequipment and "Products" in data_tequipment:
        for item in data_tequipment["Products"]:
            results.append({
                'source': 'TEquipment',
                'name': item['ProductName'],
                'price': item['Price'],
                'link': f"https://www.tequipment.net{item['URL']}"
            })

    if data_aicaigou and "productList" in data_aicaigou:
        for item in data_aicaigou["productList"]:
            results.append({
                'source': 'Aicaigou',
                'name': item['fullName'],
                'price': item['price'],
                'link': item['jUrl']
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

    return results


# query_data("mit515")





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
