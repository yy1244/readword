# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup


class sbs():

    def __init__(self,html):
        self.soup = BeautifulSoup(html, 'lxml')
        #研究人员
        self.researchersrs = []
        #研究领域
        self.researchareas = ''
        #协作单位
        self.cooperationUnits = []
        #申报编号
        self.declareCode = ''

    def parse(self):
        self.research_areas()
        self.cooperation_units()
        self.researchersr()
        self.declare_code()
        return {'researchersrs':self.researchersrs,'researchareas':self.researchareas,'cooperationUnits':self.cooperationUnits,'declareCode':self.declareCode}


    '''
        研究领域
    '''
    def research_areas(self):

        table = self.soup.find_all('table')[2]
        self.researchareas = table.find_all('tr')[1].find_all('td')[1].get_text()

    '''
        研究人员
    '''
    def researchersr(self):
        table = self.soup.find_all('table')[5]
        trs = table.find_all('tr')
        flag = False
        nameTrs = []
        for tr in trs:
            if tr.td.string != None and tr.td.string.strip() == u'归口部门意见':
                flag = False
            if flag:
                nameTrs.append(tr)
            if tr.td.string != None and tr.td.string.strip() == u'主要研究人员':
                flag = True

        for tr in nameTrs:
            tds = tr.find_all('td')
            if tds[0].get_text().strip() == "":
                continue
            item = {}
            # 姓名
            item['name'] = tds[0].get_text().strip()
            # 学位
            item['degree'] = tds[1].get_text().strip()
            # 职称
            item['jobTitle'] = tds[2].get_text().strip()
            # 专业
            item['profession'] = tds[3].get_text().strip()
            self.researchersrs.append(item)

    '''
        协作单位
    '''
    def cooperation_units(self):
        table = self.soup.find_all('table')[5]
        trs = table.find_all('tr')
        flag = False
        its_tr = []
        for tr in trs:
            if tr.td.string != None and tr.td.string.strip() == u'项目负责人':
                flag = False
            if flag:
                its_tr.append(tr)
            if tr.td.string != None and tr.td.string.strip() == u'协作单位':
                flag = True

        for tr in its_tr:
            tds = tr.find_all('td')
            if tds[0].get_text().strip() == "":
                continue
            item = {}
            # 名称
            item['name'] = tds[0].get_text().strip()
            # 分工
            item['dtw'] = tds[1].get_text().strip()
            self.cooperationUnits.append(item)

    '''
        申报编号
    '''
    def declare_code(self):
        table = self.soup.find_all('table')[0]
        self.declareCode = table.find_all('tr')[0].find_all('td')[1].get_text().strip()