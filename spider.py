"""
@Describe :
@Time     : 2021/8/18 10:08
@Author   : weizhoujie
"""
import requests
from requests.adapters import HTTPAdapter
import csv
session = requests.session()
session.mount('http://', HTTPAdapter(max_retries=3))
session.mount('https://', HTTPAdapter(max_retries=3))
def get_brand():
    print('-------开始获取品牌Id--------')
    brand_list = []
    brand_url = 'https://res.jddmoto.com/oss/clientconfig/carport/brand/list.json?token=&platform=3&version=3.38.0  &deviceId='
    res = session.get(url=brand_url,timeout=15)
    try:
        result = res.json()
        for i in result:
            brand_list.append(i['brandId'])
        print('-------获取品牌id成功--------')
    except:
        print('获取品牌ID失败')
    return brand_list

def get_score(good_id):
    score = ''
    url = 'https://api.jddmoto.com/carport/goods/praise/v1/score/{0}'.format(str(good_id))
    res = session.get(url=url,timeout=15)
    result = res.json()['data']
    if result['totalScore'] and str(result['totalScore']) != '0.0':
        score = str(result['totalScore'])
    else:
        score = '暂无'
    return score

def get_good(brand_list):
    if len(brand_list):
        good_list = []
        for i in brand_list:
            page = 1
            while(1):
                good_url = 'https://api.jddmoto.com/carport/goods/v4/brand/{0}?page={1}'.format(str(i),str(page))
                res = session.get(url=good_url,timeout=15)
                result = res.json()['data']
                if result:
                    for j in result:
                        brandName = j['brandName']
                        goodAbs = j['goodAbs']
                        if j['goodCoolDown']:
                            goodCoolDown = j['goodCoolDown']
                        else:
                            goodCoolDown = '未知'
                        if j['goodCylinder']:
                            goodCylinder = j['goodCylinder']
                        else:
                            goodCylinder = '未知'
                        goodName = j['goodName']
                        goodPic = j['goodPic']
                        if j['goodVolume']:
                            goodVolume = j['goodVolume']
                        else:
                            goodVolume = '未知'
                        if j['maxPrice'] and str(j['maxPrice']) != '0':
                            goodPrice = j['maxPrice']
                        else:
                            goodPrice = '暂无'
                        goodId = j['goodId']
                        goodScore = get_score(goodId)
                        good = [brandName,goodName,goodAbs,goodCoolDown,goodCylinder,goodPic,goodVolume,goodPrice,goodScore]
                        good_list.append(good)
                    print('--------获取id为{0}的第{1}页数据成功'.format(str(i), str(page)))
                    page = page+1
                else:
                    break

        return good_list

def write_data(good_list):
    print('---------开始写入--------')
    f = open('摩托.csv', 'w', encoding='utf-8',newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(["品牌", "名字", "abs","冷却系统","汽缸数","图片","排量","价格","口碑"])
    for i in good_list:
        print(i)
        csv_writer.writerow(i)
    f.close()
    print('---------写入完成--------')



if __name__ == '__main__':
    write_data(get_good(get_brand()))
