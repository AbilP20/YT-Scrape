from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep; import logging as lg
import mysql.connector as sqltor

application = Flask(__name__)

@application.route("/")
def homepage():
    try:
        return render_template("index.html")
    except Exception as e:
        lg.info(f"Exception! - {e}")

@application.route("/uploads",methods=['GET'])
def getUploads():
    try:
        obj = yt_scrape()
        obj.Get_Upload()
        return render_template("upload_count.html",uploads=obj.uploads)
    except Exception as e:
        lg.info(f"Exception! - {e}")

@application.route('/result',methods=['GET','POST'])
def search_vid():
    try:
        url = request.form['url']
        obj = yt_scrape()
        obj.Search_Vid(url)
        return render_template("search_result.html",url=url,title=obj.title, channel=obj.chan, subs=obj.subs, views=obj.views,
                               likes=obj.likes, date=obj.date, desc=obj.desc, comments=obj.comment)
    except NoVideoFoundError:
        lg.info(f"No Video was found on the searched url : {url}")
        return render_template("Search_result_error.html",url=url)
    except Exception as e:
        lg.info(f"Exception! - {e}")

class yt_scrape:
    def __init__(self):
        self.title=''
        self.views=''
        self.date=''
        self.likes=''
        self.desc=[]
        self.comment=dict()
        self.channel = ["https://www.youtube.com/@krishnaik06","https://www.youtube.com/@iNeuroniNtelligence","https://www.youtube.com/@CollegeWallahbyPW"]
        self.chan_name = ["Krish Naik","INeuron Intelligence","College Wallah"]
        self.uploads=dict()
        lg.basicConfig(filename="YoutubeScraper.log", level=lg.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def Search_Vid(self,url):
        """
        url = a youtube video url you want to get the data about
        this function scrapes YT Video details - Name, Channel, Subs, Likes, Views, Date of upload, Description, Comments
        """
        try:
            lg.info("Opening Chrome")
            s = Service("chromedriver.exe")
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("--window-size=1051,805")
            driver = webdriver.Chrome(service=s, options=options)
            lg.info(f"Loading {url}")
            driver.get(url)
            sleep(2)
            driver.execute_script("window.scrollTo(0,500)")
            self.title = driver.find_element(By.XPATH,'//*[@id="title"]/h1/yt-formatted-string').text
            print("Getting Video Details...",end='')
            lg.info("Fetched Title")
            self.chan= driver.find_element(By.XPATH,'//*[@id="text"]/a').text
            lg.info("Fetched Channel Name")
            self.subs=driver.find_element(By.XPATH,'//*[@id="owner-sub-count"]').text
            lg.info("Fetched Subscribers")
            self.views = driver.find_element(By.XPATH,'//*[@id="info"]/span[1]').text
            lg.info("Fetched Views")
            self.date = driver.find_element(By.XPATH,'//*[@id="info"]/span[3]').text
            lg.info("Fetched Date Uploaded")
            self.likes = driver.find_element(By.XPATH,'//*[@id="segmented-like-button"]/ytd-toggle-button-renderer/yt-button-shape/button/div[2]').text
            lg.info("Fetched Likes")
            try:
                driver.find_element(By.XPATH,'//*[@id="expand"]').click()
                lg.info("Clicked 'View More' in description")
            except:
                lg.info(f"Exception! - {e}")
            a = driver.find_element(By.XPATH,'//*[@id="description-inline-expander"]/yt-formatted-string')
            self.desc = a.text.split("\n")
            lg.info("Fetched Description")
            sleep(2)
            try:
                driver.execute_script("window.scrollTo(0,700)")
                sleep(1)
                driver.execute_script("window.scrollTo(0,1400)")
                sleep(1)
                driver.execute_script("window.scrollTo(0,1800)")
                c = driver.find_element(By.XPATH,'//*[@id="sections"]')
                sleep(1)
                driver.execute_script("window.scrollTo(0,2500)")
                sleep(1)
                driver.execute_script("window.scrollTo(0,4000)")
                sleep(2)
                d = c.find_elements(By.XPATH,'//*[@id="main"]')         
                n=0
                if len(d)>30:
                    n=30
                else:
                    n=len(d)
                for i in range(n):
                    com=d[i].text.split('ago')
                    name = com[0].split('\n')[0]
                    com = " ".join(com[1].split('\n')[:-2])
                    self.comment[name] = com
                lg.info(f"Fetched {n} Comments")
            except Exception as e:
                lg.info(f"Exception! - {e}")
            print("Completed.")
            self.__sql_push()
        except Exception as e:
            lg.info(f"Exception! - {e}")
            raise NoVideoFoundError()

    def Get_Upload(self):
        """
        this function fetches the no. of uploads of Krish Naik, Ineuron Intelligence and College Wallah Channels
        """
        try:
            for i in range(3):
                lg.info("Opening Chrome")    
                s = Service("chromedriver.exe")
                options = webdriver.ChromeOptions()
                options.add_argument('--no-sandbox')
                options.add_argument('--headless')
                options.add_argument('--disable-gpu')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument("--window-size=1051,805")
                driver = webdriver.Chrome(service=s, options=options)
                driver.get(self.channel[i])
                lg.info(f"Loading {self.channel[i]}")
                sleep(2)
                driver.execute_script("window.scrollTo(0,500)")
                try:
                    driver.find_element(By.XPATH,'//*[@id="play-button"]/ytd-button-renderer/yt-button-shape/a/yt-touch-feedback-shape/div/div[2]').click()
                    sleep(3)
                    count = driver.find_element(By.XPATH,'//*[@id="publisher-container"]/div/yt-formatted-string/span[3]').text
                except:
                    driver.find_element(By.XPATH,'//*[@id="video-title"]').click()
                    sleep(2)
                    driver.execute_script("window.scrollTo(0,1000)")
                    count = driver.find_element(By.XPATH,'//*[@id="publisher-container"]/div/yt-formatted-string/span[3]').text
                    count=str(int(count)+2)
                driver.quit()
                lg.info(f"Fetched no. of uploads of {self.chan_name[i]}")
                self.uploads[self.chan_name[i]]=count
        except Exception as e:
            lg.info(f"Exception! - {e}")

    def __sql_push(self):
        """
        this function pushes the data retrieved(if available) on the local mySQL in the given collection(By default)
        """  
        try:
            lg.info(f"PUSHING '{self.title}' INTO MYSQL DB")
            print("Storing in mySQL DB...",end='')
            con = sqltor.connect(host="localhost", user="root", passwd="pass", database='ineuron_db')
            lg.info("mySQL Connection Established.")
            cur = con.cursor()
            try:
                cur.execute(f'insert into video_details values("{self.title}","{self.date}","{self.views}","{self.likes}","{self.chan}","{self.subs}")')
                con.commit()
            except sqltor.IntegrityError:
                print("Video Detail Exists...Completed")
                lg.info("Video Detail Already Exists.")
            except Exception as e:
                print(e)
                lg.info(f"Exception! - {e}")
            else:
                print("Completed.")
                lg.info("Insert Successful.")                
            con.close()
            lg.info("mySQL Connection Terminated.")
        except Exception as e:
            lg.info("Insert Unsuccessful.")
            lg.info(f"Exception! - {e}")
class NoVideoFoundError(Exception):
    pass
# DRIVER_PATH = r"chromedriver.exe"
if __name__=="__main__":
    application.run()