from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as b
import time
import scrapTop5
import login
import xlsxwriter
import datetime

driver = 0
# temperory
email='Put Your Email'
password='Put Your Password' 
countryList=['malaysia', 'indonesia']
top5FacebookPageURL=[]

def main():
    global driver
    print('running script..')
    # driver = webdriver.Chrome('D://a1/software_installer/chromedriver_win32/chromedriver.exe')
    
    option = Options()

    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")

    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option("prefs", { 
        "profile.default_content_setting_values.notifications": 1 
    })

    for country in countryList:
        print("\nScrap For : " + country)
        print("_______________________\n")

        driver = webdriver.Chrome(chrome_options=option, executable_path='D://a1/software_installer/chromedriver_win32/chromedriver.exe')

        listTop5=scrapTop5.ScrapTop5(driver)

        print('\n*Try to scrap the top 5 Facebook page URL...')
        top5FacebookPageURL=listTop5.scrapTop5YesterdayFacebookPageURL(country)
        print("\n*Scrap the top 5 Facebook page URL SUCCEED!")

        
        print('\n*Try to login into Facebook...')
        l=login.Login(driver, email, password)
        l.signin()
        print('\n*Login into Facebook SUCCEED!')

        current_time=datetime.datetime.now()

        rYear=current_time.year
        rMonth=current_time.month
        rDay=current_time.day
        rHour=current_time.hour
        rMinute=current_time.minute

        rDate=str(rDay)+"/"+str(rMonth)+"/"+str(rYear)
        rDate2=str(rDay)+"_"+str(rMonth)+"_"+str(rYear)
        rTime=str(rHour)+":"+str(rMinute)

        
        workbook = xlsxwriter.Workbook('C:/laragon/www/web_exploring/rankbot/rank_web_scrapping/top5pages_' + country+'('+rDate2+').xlsx')
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': 1})
        chart = workbook.add_chart({'type': 'column'})
        chart.set_x_axis({
        'name': 'Facebook Page (Rank by Total Increase in Follower)',
        'num_font':  {'italic': True },
        })

        chart.set_y_axis({
        'name': 'Number of Reactions (People)',
        })

        chart.set_title({'name': "Reactions from the Latest Five 24 Hours Posting by Facebook Page from "+country+" with the Top 5 Greatest Increase in Followers Yesterday (Retrieve at " + rDate+ "_"+ rTime +")"})
        
        worksheet.write('A1', 'Name', bold)
        worksheet.write('B1', 'Photo', bold)
        worksheet.write('C1', 'Followers (Last 24 hours)', bold)
        worksheet.write('D1', 'Post Number', bold)
        worksheet.write('E1', 'Date (in s/m/h/d)', bold)
        worksheet.write('F1', 'Like', bold)
        worksheet.write('G1', 'Love', bold)
        worksheet.write('H1', 'Care', bold)
        worksheet.write('I1', 'Wow', bold)
        worksheet.write('J1', 'Haha', bold)
        worksheet.write('K1', 'Angry', bold)
        worksheet.write('L1', 'Sad', bold)
        worksheet.write('M1', 'Total (by post)', bold)

        pageCount=0
        row=0
        postLength=0
        totalLoc=[]
        print('\n*Try to scrap all the engagement data...')
        for n in top5FacebookPageURL:
            try:
                postInfo=listTop5.scrapThePostEngageData(n, pageCount)
            except:
                pass
            worksheet.write('A'+str(pageCount+2+postLength), postInfo['pageName'])
            worksheet.write('B'+str(pageCount+2+postLength), postInfo['pageProfilePhoto'])
            worksheet.write('C'+str(pageCount+2+postLength), str(postInfo['pageTotalFollowers']))
            worksheet.write('C'+str(pageCount+2+postLength+1), '+'+str(postInfo['pageTotalIncrFol']))
            for k in range(len(postInfo['postList'])):
                worksheet.write('D'+str(pageCount+k+2+postLength), float(k+1))
                worksheet.write('E'+str(pageCount+k+2+postLength), postInfo['postList'][k]['date'])
                worksheet.write('F'+str(pageCount+k+2+postLength), postInfo['postList'][k]['reaction']['like'])
                worksheet.write('G'+str(pageCount+k+2+postLength), postInfo['postList'][k]['reaction']['love'])
                worksheet.write('H'+str(pageCount+k+2+postLength), postInfo['postList'][k]['reaction']['care'])
                worksheet.write('I'+str(pageCount+k+2+postLength), postInfo['postList'][k]['reaction']['wow'])
                worksheet.write('J'+str(pageCount+k+2+postLength), postInfo['postList'][k]['reaction']['haha'])
                worksheet.write('K'+str(pageCount+k+2+postLength), postInfo['postList'][k]['reaction']['angry'])
                worksheet.write('L'+str(pageCount+k+2+postLength), postInfo['postList'][k]['reaction']['sad'])
                worksheet.write('M'+str(pageCount+k+2+postLength), '=SUM(F'+str(pageCount+k+2+postLength)+':L'+str(pageCount+k+2+postLength)+')', bold)
            
            worksheet.write('E'+str(pageCount+len(postInfo['postList'])+2+postLength), 'Total (by reaction)', bold)
            if len(postInfo['postList'])==0:
                worksheet.write('F'+str(pageCount+len(postInfo['postList'])+2+postLength), 0, bold)
                worksheet.write('G'+str(pageCount+len(postInfo['postList'])+2+postLength), 0, bold)
                worksheet.write('H'+str(pageCount+len(postInfo['postList'])+2+postLength), 0, bold)
                worksheet.write('I'+str(pageCount+len(postInfo['postList'])+2+postLength), 0, bold)
                worksheet.write('J'+str(pageCount+len(postInfo['postList'])+2+postLength), 0, bold)
                worksheet.write('K'+str(pageCount+len(postInfo['postList'])+2+postLength), 0, bold)
                worksheet.write('L'+str(pageCount+len(postInfo['postList'])+2+postLength), 0, bold)
                worksheet.write('M'+str(pageCount+len(postInfo['postList'])+2+postLength), 0, bold)
            else:
                worksheet.write('F'+str(pageCount+len(postInfo['postList'])+2+postLength), '=SUM(F'+ str(pageCount+2+postLength) +':F'+str(pageCount+len(postInfo['postList'])+1+postLength)+')', bold)
                worksheet.write('G'+str(pageCount+len(postInfo['postList'])+2+postLength), '=SUM(G'+ str(pageCount+2+postLength) +':G'+str(pageCount+len(postInfo['postList'])+1+postLength)+')', bold)
                worksheet.write('H'+str(pageCount+len(postInfo['postList'])+2+postLength), '=SUM(H'+ str(pageCount+2+postLength) +':H'+str(pageCount+len(postInfo['postList'])+1+postLength)+')', bold)
                worksheet.write('I'+str(pageCount+len(postInfo['postList'])+2+postLength), '=SUM(I'+ str(pageCount+2+postLength) +':I'+str(pageCount+len(postInfo['postList'])+1+postLength)+')', bold)
                worksheet.write('J'+str(pageCount+len(postInfo['postList'])+2+postLength), '=SUM(J'+ str(pageCount+2+postLength) +':J'+str(pageCount+len(postInfo['postList'])+1+postLength)+')', bold)
                worksheet.write('K'+str(pageCount+len(postInfo['postList'])+2+postLength), '=SUM(K'+ str(pageCount+2+postLength) +':K'+str(pageCount+len(postInfo['postList'])+1+postLength)+')', bold)
                worksheet.write('L'+str(pageCount+len(postInfo['postList'])+2+postLength), '=SUM(L'+ str(pageCount+2+postLength) +':L'+str(pageCount+len(postInfo['postList'])+1+postLength)+')', bold)
                worksheet.write('M'+str(pageCount+len(postInfo['postList'])+2+postLength), '=SUM(M'+ str(pageCount+2+postLength) +':M'+str(pageCount+len(postInfo['postList'])+1+postLength)+')', bold)
                
            
            totalLoc.append(str(pageCount+len(postInfo['postList'])+2+postLength))

            postLength=postLength+len(postInfo['postList'])+1


            print('\n\nRank ' + str(pageCount+1))
            print('_________')
            print('\nPage: '+ postInfo['pageName'])
            print('\nprofilePhoto: '+postInfo['pageProfilePhoto'])
            print('\nTotal Followers: '+ str(postInfo['pageTotalFollowers']))
            print('\nTotal Increase in Follower Yesterday: +'+ str(postInfo['pageTotalIncrFol']))
            print('\nTotal Considered Post: ' + str(len(postInfo['postList'])))
            print('')
            for k in range(len(postInfo['postList'])):
                print('Date: '+postInfo['postList'][k]['date'])
                print('Reactions: ' + 'Likes: ' + str(postInfo['postList'][k]['reaction']['like'])+ ' Loves: ' + str(postInfo['postList'][k]['reaction']['love'])+ ' Cares: ' + str(postInfo['postList'][k]['reaction']['care'])+ ' Wow: ' + str(postInfo['postList'][k]['reaction']['wow'])+ ' Haha: ' + str(postInfo['postList'][k]['reaction']['haha'])+
                ' Angry: ' + str(postInfo['postList'][k]['reaction']['angry'])+ ' Sad: ' + str(postInfo['postList'][k]['reaction']['sad']))
            pageCount+=1
        
        # print('\ntotalLoc len: ' + str(len(totalLoc))+'\n')
        chart.add_series({'name':'Like', 'values': '=(Sheet1!$F$'+totalLoc[0]+',Sheet1!$F$'+totalLoc[1]+',Sheet1!$F$'+totalLoc[2]+',Sheet1!$F$'+totalLoc[3]+',Sheet1!$F$'+totalLoc[4]+')'})
        chart.add_series({'name':'Love', 'values': '=(Sheet1!$G$'+totalLoc[0]+',Sheet1!$G$'+totalLoc[1]+',Sheet1!$G$'+totalLoc[2]+',Sheet1!$G$'+totalLoc[3]+',Sheet1!$G$'+totalLoc[4]+')'})
        chart.add_series({'name':'Care', 'values': '=(Sheet1!$H$'+totalLoc[0]+',Sheet1!$H$'+totalLoc[1]+',Sheet1!$H$'+totalLoc[2]+',Sheet1!$H$'+totalLoc[3]+',Sheet1!$H$'+totalLoc[4]+')'})
        chart.add_series({'name':'Wow', 'values': '=(Sheet1!$I$'+totalLoc[0]+',Sheet1!$I$'+totalLoc[1]+',Sheet1!$I$'+totalLoc[2]+',Sheet1!$I$'+totalLoc[3]+',Sheet1!$I$'+totalLoc[4]+')'})
        chart.add_series({'name':'Haha', 'values': '=(Sheet1!$J$'+totalLoc[0]+',Sheet1!$J$'+totalLoc[1]+',Sheet1!$J$'+totalLoc[2]+',Sheet1!$J$'+totalLoc[3]+',Sheet1!$J$'+totalLoc[4]+')'})
        chart.add_series({'name':'Angry', 'values': '=(Sheet1!$K$'+totalLoc[0]+',Sheet1!$K$'+totalLoc[1]+',Sheet1!$K$'+totalLoc[2]+',Sheet1!$K$'+totalLoc[3]+',Sheet1!$K$'+totalLoc[4]+')'})
        chart.add_series({'name':'Sad', 'values': '=(Sheet1!$L$'+totalLoc[0]+',Sheet1!$L$'+totalLoc[1]+',Sheet1!$L$'+totalLoc[2]+',Sheet1!$L$'+totalLoc[3]+',Sheet1!$L$'+totalLoc[4]+')'})
        
        chart.set_table()
        chart.set_table({'show_keys': True})
        chart.set_size({'x_scale': 1.25, 'y_scale': 1.75})

        worksheet.insert_chart('P2', chart)
        print("\n*Scrap the engagement data SUCCEED!")

        workbook.close()




if __name__ =='__main__':
    main()