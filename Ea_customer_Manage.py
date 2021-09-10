import json
from time import sleep
import allure
import requests
from Ea_access_token import oa_get_token# 导出外部文件Ea_access_token中的get_token函数
import random
import string
from config.tools import random_str# 导出外部文件config.tools中的random_str函数,在本文件中使用时可定义为变量


rdm_num = random_str()
access_token =oa_get_token()
ip="https://oaapi.qidian.qq.com"


class Customer_Manage():
    """
      /ea/customer/leads/创建
      /ea/customer/leads/修改
      /ea/customer/leads/详情
      /ea/customer/leads/删除
      /ea/customer/leads/搜索
    """


    def create_leads(self):
        """创建线索"""

        # self.access_token = get_token()  # 把Ea_access_token中的get_token()的返回值定义变量,增加self.后作用域在同一个对象内可以被不同的函数中调用,不加self作用域仅为当前函数。
        data = dict()
        data["name"] = "py_api_test_{}".format(rdm_num)
        data["saInfo"] = [{"saType": 2, "value": "15221817000"}]
        # data["_bqq_csrf"] = '342e4fd08d603d3467f06027ea6c1d0daabcad61'# 好像没啥用？,可以不用传.
        josn_data = json.dumps(data)  # 将字典数据转换成json数据
        hearder = {'Content-Type': "application/json"}  # post请求中没有填写hearders时就是没有指定json格式
        action_create = requests.post(
            url=ip+"/cgi-bin/v1/ea/market/customer/leads/create?access_token={}".format(access_token), data=josn_data)
        print(action_create.text, "创建线索")  # 返回响应文本信息
        create_rsp = json.loads(action_create.text)  # 将创建线索的返回信息转换成字典格式
        self.leadsIds = create_rsp["data"]["leadsIds"][0]  # 取创建线索的线索ID
        assert create_rsp["errcode"] == 0  # 对errcode做断言,0为成功
        return self.leadsIds  # 返回线索ID


    def update_leads(self):
        """修改线索"""

        data = dict()
        data['leadsId'] = self.leadsIds
        data['name'] = 'py_api_update'
        data['remark'] = "我是修改线索"
        json_data = json.dumps(data)
        action_update = requests.post(ip+"/cgi-bin/v1/ea/market/customer/leads/update?access_token={}".format(access_token), data=json_data)
        print(action_update.text, "修改线索")
        update_rsp = json.loads(action_update.text)  # 将修改线索的返回信息转成字典格式
        assert update_rsp["errcode"] == 0  # 对修改线索的返回信息中的errcode做断言
        sleep(1)

    def detail_leads(self):
        """线索详情"""
        action_detail=requests.get(ip+"/cgi-bin/v1/ea/market/customer/leads/detail?access_token={}&leadsId={}".format(access_token,self.leadsIds))
        print(action_detail.text)
        sleep(2)

    def delete_leads(self):
        """删除线索"""
        data = dict()
        data["leadsId"] = self.leadsIds
        json_data = json.dumps(data)
        action_delete = requests.post(ip+"/cgi-bin/v1/ea/market/customer/leads/delete?access_token={}".format(access_token), data=json_data)
        print(action_delete.text, "删除线索")
        delete_rsp = json.loads(action_delete.text)  # 将删除线索的返回信息转成字典格式
        assert delete_rsp["errcode"] == 0
        sleep(1)

    def search_leads(self):
        """搜索线索"""
        data=dict()
        data["filter"]=[
        {
            "property": "name",
            "operation": "EQUAL",
            "value":"py_api_update"
        }]

        data["count"]=50
        data["index"]=1
        data["keywords"]="py_api_update"
        json_data=json.dumps(data)
        action_search=requests.post(ip+"/cgi-bin/v1/ea/market/customer/leads/search?access_token={}".format(access_token),data=json_data)
        print(action_search.text)
        search_rsp= json.loads(action_search.text)
        assert search_rsp["errcode"]==0


customerManage = Customer_Manage()

if __name__ == '__main__':
     customerManage.create_leads()  # 执行customerManage对象中的create_leads()函数
     customerManage.update_leads()
     customerManage.detail_leads()
     customerManage.delete_leads()
     customerManage.search_leads()
