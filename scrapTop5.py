from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as b
import time


class ScrapTop5:
    def __init__(self, driver):
        self.driver=driver
        self.hrefsFacebookPage=[]
        self.fbpProfilePhoto=[]
        self.fbpNameList=[]
        self.fbpTotalIncrFol=[]
        self.fbpTotalFol=[]

    def scrapTop5YesterdayFacebookPageURL(self, country):
        hrefsStatistics=[]

        print('\nOpen the socialbakers site...')
        self.driver.get('https://www.socialbakers.com/statistics/facebook/pages/total/'+country)
        print('Open the socialbakers site SUCCEED!')
        time.sleep(2)
        topGrowing = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#top-growings > ul.graph-growing-list.block-1.items-5')))
        sTopGrowing=b(topGrowing.get_attribute('innerHTML'), 'html.parser')

        fail=False

        print('\nTry to retrieve all 5 last 24 hours top Facebook page statistics url...')
        for p in sTopGrowing.findAll('li'):
            try:

                hlink=p.findAll('a')[0]['href']
                # print(hlink)
                if 'div' in hlink:
                    pass
                else:
                    hrefsStatistics.append("https://www.socialbakers.com/"+hlink)
            except:
                fail=True
                pass

            try:
                hPhoto=p.findAll('img')[0]['src']
                if 'span' in hPhoto:
                    pass
                else:
                    self.fbpProfilePhoto.append(hPhoto)
            except:
                fail=True
                pass

        if fail==False:
            print('Retreive SUCCEED!')
        elif fail==True:
            print('Ops, retrieve FAILED! Something is not right')

        fail=False

        print('\nTry to get all the total increase in followers...')
        try:
            facebookPageTotalIncrFol = sTopGrowing.findAll('strong')
            tempName=''
            for x in facebookPageTotalIncrFol:
                tempName=x.getText().replace('+', '')
                tempName=tempName.replace(' Fans', '')
                tempName=tempName.replace(' ', '')
                self.fbpTotalIncrFol.append(tempName)
            print('Retrieve SUCCEED!')
        except:
            print('Ops, retrieve FAILED! Something is not right')
            pass

        print('\nTry to go the statistic details pages to get the Facebook page name and URL...')
        try:
            for r in hrefsStatistics:
                try:
                    self.driver.get(r)
                    time.sleep(2)
                    topGrowingFBPageName = WebDriverWait(self.driver, 7).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.page > div.content.content--subpages > div > section > div.page-head > h1 > div')))
                    sTopGrowingFBPageName=b(topGrowingFBPageName.get_attribute('innerHTML'), 'html.parser')
                    tempName=sTopGrowingFBPageName.getText().replace(' Facebook statistics', '')
                    tempName=tempName.replace('\n', '')
                    tempName=tempName.replace('\t', '')
                    self.fbpNameList.append(tempName)

                    topGrowingFBPageURLTemp = WebDriverWait(self.driver, 7).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.page > div.content.content--subpages > div > section > div.account-detail > ul > li:nth-child(2)')))
                    sTopGrowingFBPageURLTemp=b(topGrowingFBPageURLTemp.get_attribute('innerHTML'), 'html.parser')
                    hlink=sTopGrowingFBPageURLTemp.find('a')['href']
                    self.hrefsFacebookPage.append(hlink)

                    
                    totalFollowers = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.page > div.content.content--subpages > div > section > div.account-detail > ul')))
                    sTotalFollowers=b(totalFollowers.get_attribute('innerHTML'), 'html.parser')
                    
                    # nTotalFollowers=sTotalFollowers.findAll('span',{'class':'p-nw'})[0]
                    nTotalFollowers=sTotalFollowers.findAll('strong')[0]
                    try:
                        nTotalFollowers= nTotalFollowers.replace('<strong>', '')
                        nTotalFollowers= nTotalFollowers.replace('</strong>', '')
                    except:
                        pass
                    self.fbpTotalFol.append(nTotalFollowers)
                except:
                    self.fbpNameList.append('unknown')
                    self.hrefsFacebookPage.append('unknown')
                    self.fbpProfilePhoto.append('unknown')
                    self.fbpTotalFol.append('unknown')
                    
                

            print('Retrieve SUCCEED!')
        except:
            print('Ops, retrieve FAILED! Something is not right')
            pass

        return self.hrefsFacebookPage

    def scrapThePostEngageData(self, fbProfileURL, pageCount):
        facebookPage={}
        reactions={}
        time.sleep(2)
        count=0
        countPostTaken=0
        countPostValid=0
        reactType=['Like', 'Love', 'Care', 'Wow', 'Haha', 'Angry', 'Sad']
        facebookPage['pageName']=self.fbpNameList[pageCount]
        facebookPage['pageProfilePhoto']=self.fbpProfilePhoto[pageCount]
        facebookPage['pageTotalFollowers']=self.fbpTotalFol[pageCount]
        facebookPage['pageTotalIncrFol']=self.fbpTotalIncrFol[pageCount]
        facebookPage['postList']=[]

        self.driver.get(str(fbProfileURL))
        
        time.sleep(10)

        self.scroll=WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="facebook"]')))
        self.driver.execute_script('arguments[0].scrollTop=arguments[0].scrollHeight', self.scroll)
        
        time.sleep(10)

        postDate = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mount_0_0 > div > div:nth-child(1) > div.rq0escxv.l9j0dhe7.du4w35lb > div.rq0escxv.l9j0dhe7.du4w35lb > div > div > div.j83agx80.cbu4d94t.d6urw2fd.dp1hu0rb.l9j0dhe7.du4w35lb > div.l9j0dhe7.dp1hu0rb.cbu4d94t.j83agx80 > div.bp9cbjyn.j83agx80.cbu4d94t.d2edcug0 > div.rq0escxv.d2edcug0.ecyo15nh.hv4rvrfc.dati1w0a.cxgpxx05 > div > div.rq0escxv.l9j0dhe7.du4w35lb.qmfd67dx.hpfvmrgz.gile2uim.buofh1pr.g5gj957u.aov4n071.oi9244e8.bi6gxh9e.h676nmdw.aghb5jc5 > div.dp1hu0rb.d2edcug0.taijpn5t.j83agx80.gs1a9yip')))
        sPostDate=b(postDate.get_attribute('innerHTML'), 'html.parser')

        for k in sPostDate.findAll('div', {'class': 'du4w35lb k4urcfbm l9j0dhe7 sjgh65i0'}):
            for p in k.findAll('span', {'class': 'tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41'}):
                try:
                    date=p.findAll('div',{'class':'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw'})[0]['aria-label']

                    if 'span' in date:
                        pass
                    else:
                        count+=1
                        # if (('s' in date) or ('m' in date) or ('h' in date) or ('1d' in date)) and (('March' not in date) and ('May' not in date) and ('Sept' not in date) and ('Nov' not in date) and ('Dec' not in date)):
                        
                        if (('s' in date) or ('m' in date) or ('h' in date)) and (('March' not in date) and ('May' not in date) and ('Aug' not in date) and ('Sept' not in date) and ('Nov' not in date) and ('Dec' not in date) and (countPostTaken<5)):
                            countPostTaken+=1
                            reactsTotal=[0,0,0,0,0,0,0]
                            temp=[]
                            q=k.findAll('span', {'class': 'bp9cbjyn j83agx80 b3onmgus'})[0]
                            
                            try:
                                for j in range(len(q)):
                                    try:
                                        div=q.findAll('div',{'class':'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl l9j0dhe7 abiwlrkh p8dawk7l'})[j]['aria-label']
                                        temp.append(div)
                                    except:
                                        pass

                                for k in range(len(temp)):
                                    reactTemp=temp[k]

                                    reactTemp= reactTemp.replace(': ', '')

                                    if ',' in reactTemp:
                                        reactTemp= reactTemp.replace(',', '')

                                    if 'people' in reactTemp:
                                        reactTemp= reactTemp.replace(' people', '')

                                    if 'person' in reactTemp:
                                        reactTemp= reactTemp.replace(' person', '')
                                    
                                    for m in range(len(reactType)):
                                        try:
                                            if reactType[m] in reactTemp:
                                                reactTemp=reactTemp.replace(reactType[m], '')
                                                if 'K' in reactTemp:
                                                    reactTemp=float(reactTemp[:-1]) * 10**3
                                                elif 'M' in reactTemp:
                                                    reactTemp=float(reactTemp[:-1]) * 10**6
                                                else:
                                                    reactTemp=float(reactTemp)
                                                reactsTotal[m]=reactTemp
                                        except:
                                            break
                                    
                            except:
                                pass

                            facebookPage['postList'].append({"date": date, "reaction": {"like": reactsTotal[0], "love": reactsTotal[1], "care": reactsTotal[2], "wow": reactsTotal[3], "haha": reactsTotal[4], "angry": reactsTotal[5], "sad": reactsTotal[6]}})

                            countPostValid+=1         
                        else:
                            if count==1:
                                pass
                            else:    
                                break
                except:
                    pass

        
        return facebookPage