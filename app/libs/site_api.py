import time,requests,hashlib
from godaddypy import Client, Account
import json


class DnsApi(object):
    def __init__(self, apiKey, Secret):
        self.__apiKey = apiKey
        self.__Secret = Secret
        self.__req_public_args = {
            "apiKey": self.__apiKey,
            "timestamp": int(time.time())
        }

    def _signature(self, args_dict):
        args_str = ''
        commonParameters = {
            "apiKey": self.__apiKey,
            "timestamp": int(time.time())
        }
        self.__req_public_args["timestamp"] = int(time.time())
        if not isinstance(args_dict, dict):
            raise Exception("{0} must be a dict. ".format(args_dict))
        args_dict = dict(args_dict, **self.__req_public_args)
        # print("签名字典:", args_dict)
        for k in sorted(args_dict.keys()):
            args_str = args_str + k + '=' + str(args_dict[k]) + '&'
        args_str = args_str.rstrip('&') + self.__Secret
        return self._md5(args_str)

    def _md5(self, args_str):
        md5 = hashlib.md5()
        md5.update(args_str.encode('utf-8'))
        return md5.hexdigest()


    def record_create(self, domainID, type ,host, value, interface_address="https://www.dns.com/api/record/create/"):
        self.__req_public_args["hash"] = self._signature({"domainID": domainID, "type": type,"host": host,"value": value})
        self.__req_public_args["domainID"] = domainID
        self.__req_public_args["type"] = type
        self.__req_public_args["host"] = host
        self.__req_public_args["value"] = value
        req = requests.get(interface_address, params=self.__req_public_args)
        return req.json()

    def record_edit(self,domainID,recordID,newhost,newtype,newvalue,interface_address="https://www.dns.com/api/record/modify/"):
        self.__req_public_args["hash"] = self._signature({"domainID":domainID,"recordID":recordID,"newhost":newhost,"newtype":newtype,"newvalue":newvalue})
        self.__req_public_args["domainID"] = domainID
        self.__req_public_args["recordID"] = recordID
        self.__req_public_args["newhost"] = newhost
        self.__req_public_args["newtype"] = newtype
        self.__req_public_args["newvalue"] = newvalue
        req = requests.get(interface_address,params=self.__req_public_args)
        return req.json()

    def record_delete(self, domainID, recordID, interface_address="https://www.dns.com/api/record/remove/"):
        self.__req_public_args["hash"] = self._signature({"domainID": domainID, "recordID": recordID})
        self.__req_public_args["domainID"] = domainID
        self.__req_public_args["recordID"] = recordID
        req = requests.get(interface_address, params=self.__req_public_args)
        return req.json()

    def record_list(self, domainID, pageSize=10000, interface_address="https://www.dns.com/api/record/list/"):
        self.__req_public_args["hash"] = self._signature({"domainID": domainID, "pageSize": pageSize})
        self.__req_public_args["domainID"] = domainID
        self.__req_public_args["pageSize"] = pageSize
        req = requests.get(interface_address, params=self.__req_public_args)
        print(self.__req_public_args)
        return req.json()


    def record_search(self,domainID,host,interface_address="https://www.dns.com/api/record/list/"):
        self.__req_public_args["hash"] = self._signature({"domainID": domainID,"host": host})
        self.__req_public_args["domainID"] = domainID
        self.__req_public_args["host"] = host
        req = requests.get(interface_address, params=self.__req_public_args)
        return req.json()

    def domain_create(self, domain, interface_address="https://www.dns.com/api/domain/create/"):
        self.__req_public_args["hash"] = self._signature({"domain": domain})
        self.__req_public_args["domain"] = domain
        req = requests.get(interface_address, params=self.__req_public_args)
        return req.json()

    def domain_lock(self, domain, interface_address="https://www.dns.com/api/domain/lock/"):
        self.__req_public_args["hash"] = self._signature({"domain": domain})
        self.__req_public_args["domain"] = domain
        req = requests.get(interface_address, params=self.__req_public_args)
        return req.json()

    def domain_unlock(self, domain, interface_address="https://www.dns.com/api/domain/unlock/"):
        self.__req_public_args["hash"] = self._signature({"domain": domain})
        self.__req_public_args["domain"] = domain
        req = requests.get(interface_address, params=self.__req_public_args)
        return req.json()

    def domain_pause(self, domain, interface_address="https://www.dns.com/api/domain/pause/"):
        self.__req_public_args["hash"] = self._signature({"domain": domain})
        self.__req_public_args["domain"] = domain
        req = requests.get(interface_address, params=self.__req_public_args)
        return req.json()

    def domain_start(self, domain, interface_address="https://www.dns.com/api/domain/start/"):
        self.__req_public_args["hash"] = self._signature({"domain": domain})
        self.__req_public_args["domain"] = domain
        req = requests.get(interface_address, params=self.__req_public_args)
        return req.json()

    def domain_delete(self, domain, interface_address="https://www.dns.com/api/domain/remove/"):
        self.__req_public_args["hash"] = self._signature({"domain": domain})
        self.__req_public_args["domain"] = domain
        req = requests.get(interface_address, params=self.__req_public_args)
        return req.json()

    def domain_search(self, query, pageSize=10000, interface_address="https://www.dns.com/api/domain/search/"):
        self.__req_public_args["hash"] = self._signature({"query": query, "pageSize": pageSize})
        self.__req_public_args["query"] = query
        self.__req_public_args["pageSize"] = pageSize
        req = requests.get(interface_address, params=self.__req_public_args)
        return req.json()


    def get_domain_id(self, query, pageSize=10000, interface_address="https://www.dns.com/api/domain/search/"):
        self.__req_public_args["hash"] = self._signature({"query": query, "pageSize": pageSize})
        self.__req_public_args["query"] = query
        self.__req_public_args["pageSize"] = pageSize
        req = requests.get(interface_address, params=self.__req_public_args)
        result = req.json()
        id = result['data']['data'][0]['domainsID']
        return id


    def domain_list(self, pageSize=100, interface_address="https://www.dns.com/api/domain/list/"):
        pageCount = 1
        combineData = []
        errorCount = 0
        pageIndex = 1
        while pageIndex <= pageCount:
            pageIndex = pageIndex + 1
            self.__req_public_args["pageSize"] = pageSize
            self.__req_public_args["page"] = pageIndex-1
            sign_hash = self._signature({"pageSize": pageSize, "page": pageIndex-1})
            req_parameters = dict({"hash": sign_hash}, **self.__req_public_args)
            print("请求参数", req_parameters)
            res_content = requests.get(interface_address, params=req_parameters)
            if res_content.status_code == requests.codes.ok and res_content.headers['Content-Type'] == 'application/json':
                try:
                    res_json = res_content.json()
                except ValueError:
                    return {'status': 'failed', 'error': 0, 'msg': "the response have no json data"+ValueError.args}
            if res_json["code"] == 0:
                if pageCount == 1:
                    pageCount = res_json['data']['pageCount']
                combineData.extend(res_json['data']['data'])
            else:
                errorCount = errorCount + 1
        tempData = {"state": "success", "error": errorCount, "data": combineData}
        return tempData

    def get_single_domain(self, domainID, interface_address="https://www.dns.com/api/domain/getsingle"):
        self.__req_public_args["hash"] = self._signature({"domainID": domainID})
        self.__req_public_args["domainID"] = domainID
        req = requests.get(interface_address, params=self.__req_public_args)
        return req.json()

    def default_ns_record(self, domain, interface_address="https://www.dns.com/api/domain/default/nsrecord"):
        self.__req_public_args["hash"] = self._signature({"domain": domain})
        self.__req_public_args["domain"] = domain
        req = requests.get(interface_address, params=self.__req_public_args)
        return req.json()

    def real_time_qps(self, domainID, interface_address="https://www.dns.com/api/domain/qps/hour"):
        self.__req_public_args["hash"] = self._signature({"domainID": domainID})
        self.__req_public_args["domainID"] = domainID
        req = requests.get(interface_address, params=self.__req_public_args)
        return req.json()

    def day_qps(self, domainID, interface_address="https://www.dns.com/api/domain/qps/day"):
        self.__req_public_args["hash"] = self._signature({"domainID": domainID})
        self.__req_public_args["domainID"] = domainID
        req = requests.get(interface_address, params=self.__req_public_args)
        return req.json()

    def month_qps(self, domainID, interface_address="https://www.dns.com/api/domain/qps/year"):
        self.__req_public_args["hash"] = self._signature({"domainID": domainID})
        self.__req_public_args["domainID"] = domainID
        req = requests.get(interface_address, params=self.__req_public_args)
        return req.json()


class GodaddyApi:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        my_acct = Account(api_key, api_secret)
        self.__client = Client(my_acct)
        self.Authorization = "sso-key %s:%s" % (self.api_key, self.api_secret)
        self.headers = {"Authorization": self.Authorization, "accept": "application/json","Content-Type": "application/json"}

    def domain_list(self):
        Authorization = "sso-key %s:%s" % (self.api_key, self.api_secret)
        headers = {"Authorization": Authorization}
        all_domain = []
        status = True
        marker = ""
        while True:
            url = 'https://api.godaddy.com/v1/domains?limit=1000&marker={}'.format(marker)
            r = requests.get(url, headers=headers)
            status = True if r.json() else False
            if not status: break
            for domain in r.json():
                all_domain.append(domain['domain'])
                marker = domain['domain']
        return all_domain

    def domain_info(self, domain):
        '''
        :param domain: get "domain" information.
        :return: dict
        '''
        return self.__client.get_domain_info(domain)
        # return self.__client.get_domain_info(domain)['expires']
        # return self.__client.get_domain_info(domain)['nameServers']

    def record_list(self, domain):
        '''
        :param domain: get "domain" records.
        :return: list, each one record is a dict, include 'data' 'name' 'ttl' and 'type' field.
        '''
        return self.__client.get_records(domain)

    def record_create(self,domain,data,name,type):
        data_dict = [{"data": data, "name": name, "ttl": 3600, "type": type}]
        data_dict_json = json.dumps(data_dict)
        Authorization = "sso-key %s:%s" % (self.api_key, self.api_secret)
        headers = {"Authorization": Authorization,"accept": "application/json","Content-Type": "application/json"}
        url = "https://api.godaddy.com/v1/domains/{}/records".format(domain)
        r = requests.patch(url,data_dict_json,headers=headers)
        return r.status_code

    def record_edit(self,domain, data, record_type=None, name=None):
        data_dict = [{"data":data}]
        data_dict_json = json.dumps(data_dict)
        url = "https://api.godaddy.com/v1/domains/{}/records/{}/{}".format(domain,record_type,name)
        r = requests.put(url,data_dict_json,headers=self.headers)
        return r.status_code

    #获取单个记录的值,也用来判断记录是否存在
    def get_record(self,domain,record,type):
        """
        返回的结果为[{'data': '42.97.23.79', 'name': 'test2', 'ttl': 600, 'type': 'A'}]这种数据结构
        """
        url = "https://api.godaddy.com/v1/domains/{}/records/{}/{}".format(domain,type,record)
        r = requests.get(url,headers=self.headers)
        return r.json()

    def record_delte(self,domain,record_name):
        self.__client.delete_records(domain,record_name)

    def edit_ns(self,domain,nameservers):
        """nameservers为列表,元素为需要设置的nameserver域名"""
        data = {"locked":True,"nameServers":nameservers,"renewAuto":False}
        url = "https://api.godaddy.com/v1/domains/{}".format(domain)
        r = requests.patch(url,data=json.dumps(data),headers=self.headers)
        return r.text


class CloudflareApi(object):
    def __init__(self, api_key, api_email):
        self.api_key = api_key
        self.api_email = api_email
        self.baseurl = "https://api.cloudflare.com/client/v4/"
        self.headers = {"X-Auth-Key": self.api_key, "X-Auth-Email": self.api_email,"Content-Type": "application/json"}


    def get_zones(self):
        url = self.baseurl + "zones"
        r = requests.get(url,  headers=self.headers)
        return r.json()

    def get_domain_id(self,domain):
        ret = self.get_zones()
        for el in ret['result']:
            if el['name'] == domain: return el['id']
        else:
            return False

    def record_list(self,domain_id):
        url = self.baseurl + "zones/" + domain_id + "/dns_records"
        r = requests.get(url,headers=self.headers)
        return r.json()

    def get_record(self,domain_id,domain,name,type):
        #这里必须将host和域名拼接起来,传递过去才能识别
        name = name + "." + domain
        url = self.baseurl + "zones/" + domain_id + "/dns_records"
        payload = {"name":name,"type":type}
        r = requests.get(url,headers=self.headers,params=payload)
        result = r.json()
        return result

        # if result['result']:
        #     return True
        # else:
        #     return False


    def get_record_id(self,domain_id,domain,name,type):
        result = self.get_record(domain_id,domain,name,type)
        record_id = result['result'][0]['id']
        return record_id


    def record_create(self,domain_id,name,type,value):
        url = self.baseurl + "zones/" + domain_id + "/dns_records"
        data = {"name":name,"type":type,"content":value,"ttl":120}
        data = json.dumps(data)
        r = requests.post(url,headers=self.headers,data=data)
        return r.json()


    def record_edit(self,domain_id,record_id,domain,name,type,value):
        name = name + "." + domain
        url = self.baseurl + "zones/" + domain_id + "/dns_records/" + record_id
        data = {"name":name,"type":type,"content":value,"ttl":120}
        data = json.dumps(data)
        r = requests.put(url,headers=self.headers,data=data)
        return r.json()