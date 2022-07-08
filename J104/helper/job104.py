from dataclasses import dataclass
from tokenize import String
from typing import List
from bs4 import BeautifulSoup
import re, time, requests

url_Job104 = 'https://www.104.com.tw/jobs/search/?ro=1&keyword={KEYWORD}&page={PAGE}'

@dataclass
class Job104:

    KEYWORD: String
    MAX_PAGES: int
    MUST_INCLUDE: List = False

    def Crawler(self):

        url_Job104 = self._UrlJob104(PAGE=1)
        r = requests.get(url_Job104)
        PAGES = self._GetPages(RAW=BeautifulSoup(r.text, 'html.parser'))

        for page in range(1, PAGES+1):
            url_Job104 = self._UrlJob104(PAGE=page)
            r = requests.get(url_Job104)
            list_AllJobLinks = self._FindAllJobLinks(RAW=BeautifulSoup(r.text, 'html.parser'))
            for url_JobLink in list_AllJobLinks:
                r = requests.get(url_JobLink)
                soup = BeautifulSoup(r.text, 'html.parser')
                dict_JobData = self._ReturnDictOfJobData(RAW=soup)

                dict_JobData['Url'] = url_JobLink
                yield dict_JobData
                time.sleep(1)
    

    def _UrlJob104(self, PAGE):
        return url_Job104.format(KEYWORD=self.KEYWORD, PAGE=PAGE)
    

    def _GetPages(self, RAW):
        script = str(RAW.findAll('script')[-9])
        json_ScriptData = eval(script.split('var initFilter =')[1].split(';')[0])
        return min(json_ScriptData['totalPage'], self.MAX_PAGES)
    

    def _FindAllJobLinks(self, RAW):
        list_JobLinks = RAW.find_all('a', attrs={'class': 'js-job-link'})
        return self._FilteredAllJobLinks(list_JobLinks=list_JobLinks)
    

    def _FilteredAllJobLinks(self, list_JobLinks):
        list_FilteredJobLinks = []
        url_Format = 'https://{href}'
        for a in list_JobLinks:
            if 'relevance' in a['href']:
                if self.MUST_INCLUDE:
                    if any(must_include in a.text for must_include in self.MUST_INCLUDE):
                        list_FilteredJobLinks.append(url_Format.format(href=a['href'].strip('/')))
                else:
                    list_FilteredJobLinks.append(url_Format.format(href=a['href'].strip('/')))
        return list_FilteredJobLinks

    # ==========================================================================================

    def _ReturnDictOfJobData(self, RAW):
        JobTitle, JobCompany = self._FindJobTitleAndCompany(RAW=RAW)
        dict_JobInfo = {
            
            'Title': JobTitle,
            'Company': JobCompany,
            'County': self._FindJobCounty(RAW=RAW),
            'Salary': self._FindJobSalary(RAW=RAW),
            'Category': self._FindJobCategory(RAW=RAW),
            'JobDescription': self._FindJobDescription(RAW=RAW),
            
        }
        dict_JobInfo.update(self._FindDivJobDescription(RAW=RAW))
        return dict_JobInfo



    def _FindJobTitleAndCompany(self, RAW):
        JTC = re.sub(
            pattern='｜|－|-|【|】|《|》|〈|〉|（|）|_|104 人力銀行|.{0,5}市|.{0,6}區', 
            repl=' ', 
            string=RAW.find(attrs={'data-v-4ab46abb': '', 'property': 'og:title'})['content']
        )
        JTC = JTC.replace('(', ' ').replace(')', ' ').replace('[', ' ').replace(']', ' ').replace('|', ' ')
        JTC = [e for e in JTC.split(' ') if e]
        Company = []
        Title = []
        for title in JTC:
            c = re.findall(
                pattern='(.{1,30}集團|.{1,30}公司|.{1,30}診所|.{1,30}金控|.{1,30}有限|.{1,30}無限|.{1,30}兩合)', 
                string=title)
            if c:
                Company.extend(c)
            else:
                Title.append(title)
        
        return Title, Company


    def _FindJobDescription(self, RAW):
        return RAW.find('p', attrs={'class': 'job-description__content'}).text


    def _FindJobCategory(self, RAW):
        JobCategory = [jc.text for jc in RAW.find_all(attrs={'data-gtm-content': '職務類別'})]
        JobCategory = '／'.join(JobCategory).split('／')
        return JobCategory

    
    def _FindJobSalary(self, RAW):
        try:
            Salary = RAW.find('div', attrs={'class': 'list-row row mb-2 identity-type'}).text.replace(',', '')
            Salary = re.findall('(\d{0,5}.{0,1}萬元|\d+|待遇面議)', string=Salary)
            return Salary
        except:
            return ''

    def _FindJobCounty(self, RAW):
        try: 
            return RAW.find('div', attrs={'class': 'job-address'})['addressarea']
        except:
            return ''


    def _FindDivJobDescription(self, RAW):
        
        dict_RegularExpression = self._dict_RegularExpression()
        list_DivJobDescription = RAW.find_all('div', attrs={'class': 'list-row row mb-2'})
        dict_JobInfo = {}
        
        for d in list_DivJobDescription[1:-1]:
            try:
                for ColName in dict_RegularExpression:
                    
                    text = re.sub(pattern='贊助提升專業能力|、', repl=' ', string=d.text)
                    list_FindRegularExpression = re.findall(pattern=dict_RegularExpression[ColName], string=text)
                    
                    if bool(list_FindRegularExpression):
                        list_FindRegularExpression = list_FindRegularExpression[0].split(' ')
                        dict_JobInfo[ColName] = [e for e in list_FindRegularExpression if e][1:]
            except:
                pass
        try:
            dict_JobInfo['Others'] = list_DivJobDescription[-1].p.p.text
        except:
            dict_JobInfo['Others'] = ''
        return dict_JobInfo


    def _dict_RegularExpression(self):
        return {
            'Experience':  '.{0,5}工作經歷.{0,20}',
            'Education': '.{0,5}學歷要求.{0,20}',
            'Major': '.{0,5}科系要求.{0,20}',
            'Language': '.{0,5}語文條件.{0,20}',
            'Skills': '.{0,5}擅長工具.{0,50}',
        }

