import pandas as pd
import requests
import random
import execjs
import json
import os
if not os.path.exists(
        r'C:\Windows\AgentPool.xlsx'):
    input('注意注意！\n请确保存在\'C:\Windows\AgentPool.xlsx\'的ip代理文件\n否则，ip池功能将无法使用\n继续使用请敲击回车键')
class info():
    def show():
        print('测试成功，可以使用')
    def HowToUse():
        print('调用YesOrNot使用说明\nYesOrNot(ip,\'yes\'):表示调用改代理ip并进行检测\nYesOrNot(ip,\'\'):表示没有使用代理ip\n')
class function():
    def GetCityNumFromLiepin(place):
        ip = function.GetIpPool()
        ip = ip[random.randint(0, len(ip))]
        print('猎聘网正在查询城市编码')
        case=1
        OutNum=1
        while case==1:
            try:
                sheng = place[:place.find('省')]
                shi = place[place.find('省') + 1:place.find('市')]
                url = "https://apidok.liepin.com/api/com.liepin.bd.p.v3.get-all-dq"
                data = "sceneCode=6&from=component"
                header = {
                    "Accept": "application/json, text/plain, */*",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-Client-Type": "web",
                    "X-Fscp-Fe-Version": "",
                    "X-Fscp-Version": "1.1",
                    "X-Fscp-Std-Info": "{\"client_id\": \"40108\"}",
                    "X-Requested-With": "XMLHttpRequest",
                    "X-Fscp-Trace-Id": "8136730b-00b0-4daa-b975-59728e3c2a5a",
                    "X-XSRF-TOKEN": "1vL6nJjVRCu01PAwwQmdEg"
                }
                data = requests.post(url, data=data, headers=header).json()
                name = data['data']['data']['city']['list']
                num = data['data']['data']['city']['relations']
                name = str(name)
                citysNum = num[str(((name.split(sheng)[0]).split('\'code\': \'')[-1])[:3])]
                for son in citysNum:
                    qu = ((name.split(str(shi))[0]).split('\'code\': \'')[-1])[:6]
                    cityName = \
                    (((name.split('\'' + str(qu) + '\', \'seoUri\': \'')[1]).split('\', \'category\'')[0])).split('\'')[-1]
                    if son == qu:
                        result = num[qu]
                        print('已经为你找到' + sheng + '省' + cityName + '市的所有区县，即将为你查询')
                        break
                    else:
                        result = []
                return result
                case=2
            except:
                OutNum=OutNum+1
                if OutNum==10:
                    print('抱歉，城市编码查询失败')
                    case=2
                else:
                    continue
    def GetIpPool():
        IpPool = []
        data = pd.read_excel(r'C:\Windows\AgentPool.xlsx')
        data = data.values.T.tolist()
        ip = data[0]
        port = data[1]
        for i in range(0, len(ip)):
            list = {}
            list[str(ip[i]).replace(' ', '')] = str(port[i]).replace(' ', '')
            IpPool.append(list)
        return IpPool
    def GetCityNumFromBossZhiPing(city):
        ip = function.GetIpPool()
        ip = ip[random.randint(0, len(ip))]
        city=(city.split('省')[1]).split('市')[0]
        print('boss直聘查询说明\n本功能只能通过城市名字查询一个，关键词例如(宁波)，返回结果不是区的字典，只是当前城市代码。\n正在查询Boss的城市代码')
        res = requests.get('https://www.zhipin.com/wapi/zpCommon/data/cityGroup.json',proxies=ip).json()
        res = str(res['zpData']['cityGroup'])
        res = (res.split(str(city))[0]).split('code\': ')[-1].replace(', \'name\': \'', '')
        res=[str(res)]
        return res
    def GetCityNameFromLiepin(num):
        ip = function.GetIpPool()
        ip = ip[random.randint(0, len(ip))]
        case = 1
        while case == 1:
            try:
                sheng = num[:num.find('省')]
                shi = num[num.find('省') + 1:num.find('市')]
                url = "https://apidok.liepin.com/api/com.liepin.bd.p.v3.get-all-dq"
                data = "sceneCode=6&from=component"
                header = {
                    "Accept": "application/json, text/plain, */*",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-Client-Type": "web",
                    "X-Fscp-Fe-Version": "",
                    "X-Fscp-Version": "1.1",
                    "X-Fscp-Std-Info": "{\"client_id\": \"40108\"}",
                    "X-Requested-With": "XMLHttpRequest",
                    "X-Fscp-Trace-Id": "8136730b-00b0-4daa-b975-59728e3c2a5a",
                    "X-XSRF-TOKEN": "1vL6nJjVRCu01PAwwQmdEg"
                }
                data = requests.post(url, data=data, headers=header, proxies=ip).json()
                data = str(data)
                data = data.split('\'sort\': \'' + str(num) + '\'')[1]
                data = data.split('\', \'name\': \'')[1]
                data = data.split('\', \'category\'')[0]
                case = 2
                return data
            except:
                continue
    def YesOrNot(ip,case):
        def get():
            jsdata = '''
            function r() {
            var e = 1 > 0 && void 0 !== 32 ? 32 : 32;
            console.assert(e >= 32, "最少需生成32位");
            var t = (new Date).getTime()
              , n = e < 32 ? 32 : e
              , r = new Array(n).join("x")
              , a = "".concat(r, "y").replace(/[xy]/g, (function(e) {
                var n = (t + 36 * Math.random()) % 36 | 0;
                return t = Math.floor(t / 36),
                ("x" == e ? n : 3 & n | 32).toString(36)
            }
            ));
            return a
        }'''
            sign = execjs.compile(jsdata).call('r')
            return sign
        def get_data(city, town, work, page, ip,townName):
            ckId_value = get()
            data = '{"data":{"mainSearchPcConditionForm":{"city":"' + str(city) + '","dq":"' + str(town) + '","pubTime":"","currentPage":"' + str(page) + '","pageSize":500,"key":"' + str(
                work) + '","suggestTag":"","workYearCode":"0","compId":"","compName":"","compTag":"","industry":"","salary":"","jobKind":"","compScale":"","compKind":"","compStage":"","eduLevel":"","otherCity":""},"passThroughForm":{"ckId":"' + str(
                ckId_value) + '","scene":"input","skId":"kidyjuir3x7rmen14hlz2kq1y9z6n3i3lqy","fkId":"kidyjuir3x7rmen14hlz2kq1y9z6n3i3lqy","sfrom":"search_job_pc"}}}'
            data = data.encode('utf-8')
            # print(data)
            header = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json;charset=utf-8;",
                "X-Client-Type": "web",
                "X-Fscp-Fe-Version": "",
                "X-Fscp-Version": "1.1",
                "X-Fscp-Std-Info": "{\"client_id\": \"40108\"}",
                "X-Fscp-Bi-Stat": "{\"location\": \"https://www.liepin.com/zhaopin/?city=410&dq=410&pubTime=&currentPage=0&pageSize=40&key=gs&suggestTag=&workYearCode=0&compId=&compName=&compTag=&industry=&salary=&jobKind=&compScale=&compKind=&compStage=&eduLevel=&otherCity=&sfrom=search_job_pc&scene=input&skId=xne9msayrzxkrk4njg7zq0ym8bfgoueb&fkId=xne9msayrzxkrk4njg7zq0ym8bfgoueb&ckId=" + str(
                    ckId_value) + "&suggestId=\"}",
                "X-Requested-With": "XMLHttpRequest",
                "X-Fscp-Trace-Id": "7400ed8f-fa5d-46b3-ae30-c7b1189ded7c",
                "X-XSRF-TOKEN": "q4fNe47HRBup-djOx7S_0Q"
            }
            url = 'https://apic.liepin.com/api/com.liepin.searchfront4c.pc-search-job'
            if case=='yes':
                data = requests.post(url, data=data, headers=header,proxies=ip)
            else:
                data = requests.post(url, data=data, headers=header)
            res = data
            res.encoding = 'utf-8'
            res=res.json()
            print(ip,res)
        get_data('070030','070030010','数据',0,ip,'温州')
class dealDate():
    def MergeSimilar(dir, names):
        os.chdir(dir)
        data = pd.DataFrame()
        na = []
        num = 1
        for name in os.listdir():
            url = os.path.join(dir, name)
            data = pd.concat([data, pd.read_excel(url)])
            print(url, len(pd.read_excel(url)))
            for i in range(len(pd.read_excel(url))):
                na.append(name)
            num = num + 1
        del (data['Unnamed: 0'])
        data.insert(1, column='文件名', value=na)
        data.to_excel(names)