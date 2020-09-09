import cchardet
from bs4 import BeautifulSoup

from fake_useragent import UserAgent

import requests

import time

import HorseBloodSQLite as HBDB

class HorseData_scraping():
    def __init__(self,interval_time=1,limit_time = 600):
        self.time_out = 3
        ua = UserAgent()
        self.header = {'user-agent':ua.chrome}
        if interval_time >= 1:
            self.interval_time = interval_time
        else:
            self.interval_time = 1

        if limit_time > 0 and limit_time <= 3600:
            self.limit_time = limit_time
        else:
            self.limit_time = 600

        return

    def get_response(self,url):
        response = requests.get(url,headers=self.header,timeout=self.time_out)
        response.encoding = response.apparent_encoding
        enc = cchardet.detect(response.content)
        encoding = enc['encoding']

        return BeautifulSoup(response.text, "html.parser")

    def get_HorseName(self, soup):
        # タイトルから馬名を取得
        _title_ = soup.find('title').get_text(strip=True)
        _title_ = _title_.strip(' - netkeiba.com')
        t = _title_.split('|')
        horse_name = t[0].rstrip(' ')

        return horse_name

    def get_HorseProfile(self, soup):
        horse_birthday = None
        # プロフィールテーブルを取得
        profile_table = soup.find("table",class_="db_prof_table no_OwnerUnit")
        trs = profile_table.find_all('tr')
        for tr in trs:
            th = tr.find('th')
            title = th.get_text()
            if title == '生年月日':
                td = tr.find('td')
                horse_birthday = td.get_text()
                break

        return horse_birthday

    def get_HorseBoold(self, soup):
        link_dict = dict()
        horse_blood = list()

        blood_table = soup.find("table",class_="blood_table")
        links = blood_table.find_all('a')
        for i, link in enumerate(links):
            horse_name = None
            url = link.attrs['href']
            if url.strip('/horse/ped//') != '':
                horse_name = link.get_text()
                horse_blood.append(horse_name)

                url = link.attrs['href']
                url = "https://db.netkeiba.com" + url
                url = self.get_NextHorseInfo(horse_name,url)
                link_dict.setdefault(horse_name,url)
            else:
                horse_blood.append(None)

        f_horse,ff_horse,fm_horse,m_horse,mf_horse,mm_horse = horse_blood

        return horse_blood, link_dict

    def get_NextHorseInfo(self,horse_name,url):
        soup = self.get_response(url)
        print('access:%-16s:%s' % (horse_name,url))
        horse_menu =soup.find("a",title=f'{horse_name}のプロフィールTOP')
        url = horse_menu.attrs['href']
        url = "https://db.netkeiba.com" + url

        return url

    def get_HorseInfo(self,url,horse_pkey,u_link_dict):
        soup = self.get_response(url)
        horse_name = self.get_HorseName(soup)

        print('access:%-16s:%s' % (horse_name,url))
        horse_name = horse_name.replace(' ','_')
        horse_birthday = self.get_HorseProfile(soup)
        horse_blood, horse_blood_link_dict = self.get_HorseBoold(soup)

        self.DB.connect_DB()

        link_dict = dict()

        horse_pkey = self.DB.replace_Horse_Tbl(horse_name,horse_birthday,url,horse_pkey)
        for b_horse_name, b_url in horse_blood_link_dict.items():
            b_horse_name = b_horse_name.replace(' ','_')
            ｂ_horse_pkey = self.DB.replace_Horse_Tbl(b_horse_name,None,b_url,None)
            link_dict.setdefault(b_horse_name,[b_url,ｂ_horse_pkey])

        self.DB.replace_HorseBoold_Tbl(horse_name,horse_birthday,horse_blood,link_dict,url,horse_pkey)

        u_link_dict.update(link_dict)

        self.DB.replace_request_Tbl(u_link_dict)

        self.DB.commit_DB()
        self.DB.disconnect_DB()


        f_horse,ff_horse,fm_horse,m_horse,mf_horse,mm_horse = horse_blood

        print('馬名',horse_name)
        print('生年月日',horse_birthday)
        print('父',f_horse)
        print('父父',ff_horse)
        print('父母',fm_horse)
        print('母',m_horse)
        print('母父',mf_horse)
        print('母母',mm_horse)

        return u_link_dict

    def run(self, url):
        horse_pkey = None
        link_dict = dict()

        self.DB = HBDB.class_SQLite()
        self.DB.connect_DB()
        self.DB.create_Horse_Tbl()
        self.DB.create_HorseBlood_Tbl()
        self.DB.create_Request_Tbl()
        self.DB.commit_DB()
        self.DB.disconnect_DB()

        # 前回の続きのリクエストリストを取得
        link_dict = self.DB.get_request_Tbl()

        def get_next(link_dict):
            next_horse = url = pkey = None
            ans = list(link_dict.keys())
            if ans:
                next_horse = ans[0]
                url = link_dict[next_horse][0]
                pkey = link_dict[next_horse][1]
                link_dict.pop(next_horse)

            return next_horse,url,pkey

        if link_dict:
            self.DB.set_link_dict(link_dict)
            next_horse,url,horse_pkey = get_next(link_dict)

        print('スクレイピングを開始します。')

        start_time = time.time()

        horse_name = dict()

        while(True):
            #time.sleep(self.interval_time)
            link_dict = self.get_HorseInfo(url,horse_pkey,link_dict)

            while(True):
                next_horse, url, horse_pkey = get_next(link_dict)
                if not self.DB.get_HorseURL_Tbl(url):
                    break
                print(next_horse,'既に登録されているため、スキップします。')

            print(len(link_dict))
            if len(link_dict) == 0:
                break

            if next_horse in horse_name:
                horse_name[next_horse] = horse_name[next_horse] +1
            else:
                horse_name.setdefault(next_horse,1)

            ntime = time.time()

            if ntime - start_time > self.limit_time:
                print(f'規定時間{self.limit_time}秒を経過したため、スクレイピングを終了しします。')
                print(horse_name)
                break

        return

if __name__ == '__main__':
    start_url = "https://db.netkeiba.com/horse/2002100816/"
    #start_url = "https://db.netkeiba.com/horse/000a015efd/"
    #start_url = "https://db.netkeiba.com/horse/000a00111d/"
    hScr = HorseData_scraping(limit_time=3000)
    hScr.run(start_url)

