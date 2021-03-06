from  selenium import webdriver
import time
import  pymysql



driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://www.toutiao.com/')
driver.implicitly_wait(10)
driver.find_element_by_link_text('热点').click()
driver.implicitly_wait(10)

titles_list,comments_list,sources_list,times_list,hrefs_list=[],[],[],[],[]
def get_info():
        #获取标题
        titles=driver.find_elements_by_class_name('title-box')
        for title  in   titles:
            titles_list.append(title.text)
        #获取来源
        sources = driver.find_elements_by_class_name('source')
        for  source in sources:
            sources_list.append(source.text)
        #获取评论数
        comments=driver.find_elements_by_css_selector('.comment')
        for comment in comments:
            comments_list.append(comment.text)
        #获取观看时间
        times=driver.find_elements_by_css_selector('span.lbtn')
        for time in times:
            times_list.append(time.text)
        #获取该标题的链接
        urls=driver.find_elements_by_xpath('//div[@class="title-box"]/a')
        for url in urls:
            url = url.get_attribute('href')
            hrefs_list.append(url)
#通过js加载更多的信息
def get_manyinfo():
    driver.execute_script("window.scrollTo(0,1000);")
    time.sleep(1)
    #爬取的数量控制
    while len(titles_list) < 5:
        for i in range(3):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(3)
        get_info()
        driver.refresh()
    else:
        driver.quit()
#数据的保存
def  save_info():
    infos=zip(titles_list,hrefs_list,sources_list,comments_list,times_list)
    for info in infos:
        data={
            '标题':info[0],
            '链接':info[1],
            '来源':info[2],
            '评论':info[3],
            'time':info[4]
        }
        print(data)
        conn = pymysql.connect(host='localhost', user='root',
                           passwd='1422127065', port=3306, db='toutiao')
        cur=conn.cursor()
        sql='insert into ReDian(title,href,source,comment,time_view) values (%s,%s,%s,%s,%s)'
        cur.execute(sql,(info[0],info[1],info[2],info[3],info[4]))
        conn.commit()
        conn.close()
if __name__ == '__main__':
    get_info()
    get_manyinfo()
    save_info()



