#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re
import sys
import time
import traceback
from datetime import datetime
from datetime import timedelta
import pymysql
import requests
from lxml import etree
from lxml.html import tostring
from settings import mysql_password
# from settings import user_profile_template, user_content_template, user_follow_template

user_profile_template = '''
    insert into weibo_user_profile (username, user_id, weibo_num, following, follower) values("{}","{}","{}","{}","{}") 
'''

user_content_template = '''
    insert into weibo_user_content (username, user_id, weibo_content, weibo_position, publish_time, up_num, repost_num, comment_num, publish_tool) 
    values("{}","{}","{}","{}","{}","{}","{}","{}","{}") 
'''

user_follow_template = '''
    insert into weibo_follow_user (username, user_id, follow_user_name, follow_user_link) values ("{}", "{}","{}","{}")
'''


class Weibo:
    cookie = {
        "Cookie": '_T_WM=e1e85f1a27e03a5daa55091bcef73d67; MLOGIN=0; M_WEIBOCN_PARAMS=uicode%3D10000011%26fid%3D102803; SUB=_2A25xqAfEDeRhGeBG6FAU-S3Iyz-IHXVTUqmMrDV6PUJbkdAKLWrZkW1NRg0Gu1Yobj3b2IGF9wiQ_mBfWnUMqVK9; SUHB=0S7CM1qupy9gjg; SCF=Alh_hWHjS0b7iSwSB7L4cZcKm3v_-8575eYbj4B1ZKbveh9nDe5SUo8oh_hKJPObgIgYsk2FHEEva_fTgRvmdmc.; SSOLoginState=1554806676'
    }  # 将your cookie替换成自己的cookie

    # cookie = {"Cookie":''}
    # Weibo类初始化
    def __init__(self, user_id=0, filter=0):
        self.user_id = user_id  # 用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
        self.filter = filter  # 取值范围为0、1，程序默认值为0，代表要爬取用户的全部微博，1代表只爬取用户的原创微博
        self.username = ''  # 用户名，如“Dear-迪丽热巴”
        self.weibo_num = 0  # 用户全部微博数
        self.weibo_num2 = 0  # 爬取到的微博数
        self.following = 0  # 用户关注数
        self.followers = 0  # 用户粉丝数
        self.weibo_content = []  # 微博内容
        self.weibo_place = []  # 微博位置
        self.publish_time = []  # 微博发布时间
        self.up_num = []  # 微博对应的点赞数
        self.retweet_num = []  # 微博对应的转发数
        self.comment_num = []  # 微博对应的评论数
        self.publish_tool = []  # 微博发布工具
        self.follows = {}
        self.info_dict = {}

    # 获取用户昵称
    def get_username(self):
        try:
            url = "https://weibo.cn/%d/info" % (self.user_id)
            # url = "https://weibo.cn/mayun"
            print(url)
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            username = selector.xpath("//title/text()")[0]
            # username = '张翼ZyzY的资料'
            self.username = username[:-3]
            print(u"用户名: " + self.username)
            print(u"用户名: " + username)
            img_url = selector.xpath("//body/div[3]/img/@src")
            print('img_url:', img_url[0])
            self.info_dict['img_url'] = img_url[0]
            infos = selector.xpath("//body/div[6]/text()")
            print(infos)
            for info in infos:
                info = str(info)
                if '昵称' in info:
                    self.info_dict['nickname'] = info.split(":")[1]
                elif "性别" in info:
                    self.info_dict['gender'] = info.split(":")[1]
                elif "地区" in info:
                    self.info_dict['hometown'] = info.split(":")[1]
                elif "感情状况" in info:
                    self.info_dict['love_status'] = info.split("：")[1]
                elif "认证:" in info:
                    print(info)
                    self.info_dict['authentication'] = info.split(":")[1]
                elif "简介" in info:
                    self.info_dict['introduction'] = info.split(":")[1]
                else:
                    pass

            labels = selector.xpath("//body/div[6]/a/text()")
            self.info_dict['label'] = str(labels[:-1])

            is_enducation = selector.xpath("//body/div[7]/text()")
            print(is_enducation)
            if '学习经历' in is_enducation:
                education = selector.xpath("//body/div[8]/text()")[0]
                self.info_dict['education'] = education
            print(self.info_dict)
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def get_follows(self):
        try:
            print(self.user_id)
            url = "https://weibo.cn/{}/follow?page={}".format(self.user_id, 1)
            html = requests.get(url, cookies=self.cookie).content
            # print(html)
            selector = etree.HTML(html)
            page_num = selector.xpath("//div[@id='pagelist']/form/div/input[@type='hidden']/@value")[0]
            print(page_num)
            name_list = []
            link_list = []
            for page in range(1, int(page_num) + 1):
                url = "https://weibo.cn/{}/follow?page={}".format(self.user_id, page)
                # print(url)
                html = requests.get(url, cookies=self.cookie).content
                selector = etree.HTML(html)
                follows_name = selector.xpath("//table/tr/td[2]/a[1]/text()")
                follows_links = selector.xpath("//table/tr/td[2]/a[1]/@href")
                for name in follows_name:
                    name_list.append(name)
                for link in follows_links:
                    link_list.append(link)
            print(len(name_list), len(link_list))
            for index in range(0, len(name_list)):
                self.follows[name_list[index]] = link_list[index]
            print(self.follows)
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 获取用户微博数、关注数、粉丝数
    def get_user_info(self):
        try:
            url = "https://weibo.cn/u/%d?filter=%d&page=1" % (
                self.user_id, self.filter)
            # url = "https://weibo.cn/mayun?filter=0&page=1"
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            pattern = r"\d+\.?\d*"

            # 微博数
            str_wb = selector.xpath("//div[@class='tip2']/span[@class='tc']/text()")[0]
            guid = re.findall(pattern, str_wb, re.S | re.M)
            for value in guid:
                num_wb = int(value)
                break
            self.weibo_num = num_wb
            print(u"微博数: " + str(self.weibo_num))

            # 关注数
            str_gz = selector.xpath("//div[@class='tip2']/a/text()")[0]
            guid = re.findall(pattern, str_gz, re.M)
            self.following = int(guid[0])
            print(u"关注数: " + str(self.following))

            # 粉丝数
            str_fs = selector.xpath("//div[@class='tip2']/a/text()")[1]
            guid = re.findall(pattern, str_fs, re.M)
            self.followers = int(guid[0])
            print(u"粉丝数: " + str(self.followers))
            print(
                "===========================================================================")

        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 获取"长微博"全部文字内容
    def get_long_weibo(self, weibo_link):
        try:
            html = requests.get(weibo_link, cookies=self.cookie).content
            selector = etree.HTML(html)
            info = selector.xpath("//div[@class='c']")[1]
            wb_content = info.xpath("div/span[@class='ctt']")[0].xpath(
                "string(.)").replace(u"\u200b", "").encode(sys.stdout.encoding, "ignore").decode(
                sys.stdout.encoding)
            return wb_content
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 获取转发微博信息
    def get_retweet(self, is_retweet, info, wb_content):
        try:
            original_user = is_retweet[0].xpath("a/text()")
            if not original_user:
                wb_content = u"转发微博已被删除"
                return wb_content
            else:
                original_user = original_user[0]
            retweet_reason = info.xpath("div")[-1].xpath("string(.)").replace(u"\u200b", "").encode(
                sys.stdout.encoding, "ignore").decode(
                sys.stdout.encoding)
            retweet_reason = retweet_reason[:retweet_reason.rindex(u"赞")]
            wb_content = (retweet_reason + "\n" + u"原始用户: " +
                          original_user + "\n" + u"转发内容: " + wb_content)
            return wb_content
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 获取用户微博内容及对应的发布时间、点赞数、转发数、评论数
    def get_weibo_info(self):
        try:
            url = "https://weibo.cn/u/%d?filter=%d&page=1" % (
                self.user_id, self.filter)
            # url = "https://weibo.cn/mayun?filter=0&page=1"
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            if selector.xpath("//input[@name='mp']") == []:
                page_num = 1
            else:
                page_num = (int)(selector.xpath(
                    "//input[@name='mp']")[0].attrib["value"])
            pattern = r"\d+\.?\d*"
            for page in range(1, page_num + 1):
                url2 = "https://weibo.cn/u/%d?filter=%d&page=%d" % (
                    self.user_id, self.filter, page)
                html2 = requests.get(url2, cookies=self.cookie).content
                selector2 = etree.HTML(html2)
                info = selector2.xpath("//div[@class='c']")
                is_empty = info[0].xpath("div/span[@class='ctt']")
                if is_empty:
                    for i in range(0, len(info) - 2):
                        # 微博内容
                        str_t = info[i].xpath("div/span[@class='ctt']")
                        weibo_content = str_t[0].xpath("string(.)").replace(u"\u200b", "").encode(
                            sys.stdout.encoding, "ignore").decode(
                            sys.stdout.encoding)
                        weibo_content = weibo_content[:-1]
                        weibo_id = info[i].xpath("@id")[0][2:]
                        a_link = info[i].xpath(
                            "div/span[@class='ctt']/a")
                        is_retweet = info[i].xpath("div/span[@class='cmt']")
                        if a_link:
                            if a_link[-1].xpath("text()")[0] == u"全文":
                                weibo_link = "https://weibo.cn/comment/" + weibo_id
                                wb_content = self.get_long_weibo(weibo_link)
                                if wb_content:
                                    if not is_retweet:
                                        wb_content = wb_content[1:]
                                    weibo_content = wb_content
                        if is_retweet:
                            weibo_content = self.get_retweet(
                                is_retweet, info[i], weibo_content)
                        self.weibo_content.append(weibo_content)
                        print(weibo_content)

                        # 微博位置
                        div_first = info[i].xpath("div")[0]
                        a_list = div_first.xpath("a")
                        weibo_place = u"无"
                        for a in a_list:
                            if ("place.weibo.com" in a.xpath("@href")[0] and
                                    a.xpath("text()")[0] == u"显示地图"):
                                weibo_place = div_first.xpath(
                                    "span[@class='ctt']/a")[-1]
                                if u"的秒拍视频" in div_first.xpath("span[@class='ctt']/a/text()")[-1]:
                                    weibo_place = div_first.xpath(
                                        "span[@class='ctt']/a")[-2]
                                weibo_place = weibo_place.xpath("string(.)").encode(
                                    sys.stdout.encoding, "ignore").decode(sys.stdout.encoding)
                                break
                        self.weibo_place.append(weibo_place)
                        print(u"微博位置: " + weibo_place)

                        # 微博发布时间
                        str_time = info[i].xpath("div/span[@class='ct']")
                        str_time = str_time[0].xpath("string(.)").encode(
                            sys.stdout.encoding, "ignore").decode(
                            sys.stdout.encoding)
                        publish_time = str_time.split(u'来自')[0]
                        if u"刚刚" in publish_time:
                            publish_time = datetime.now().strftime(
                                '%Y-%m-%d %H:%M')
                        elif u"分钟" in publish_time:
                            minute = publish_time[:publish_time.find(u"分钟")]
                            minute = timedelta(minutes=int(minute))
                            publish_time = (
                                    datetime.now() - minute).strftime(
                                "%Y-%m-%d %H:%M")
                        elif u"今天" in publish_time:
                            today = datetime.now().strftime("%Y-%m-%d")
                            time = publish_time[3:]
                            publish_time = today + " " + time
                        elif u"月" in publish_time:
                            year = datetime.now().strftime("%Y")
                            month = publish_time[0:2]
                            day = publish_time[3:5]
                            time = publish_time[7:12]
                            publish_time = (
                                    year + "-" + month + "-" + day + " " + time)
                        else:
                            publish_time = publish_time[:16]
                        self.publish_time.append(publish_time)
                        print(u"微博发布时间: " + publish_time)

                        # 微博发布工具
                        if len(str_time.split(u'来自')) > 1:
                            publish_tool = str_time.split(u'来自')[1]
                        else:
                            publish_tool = u"无"
                        self.publish_tool.append(publish_tool)
                        print(u"微博发布工具: " + publish_tool)

                        str_footer = info[i].xpath("div")[-1]
                        str_footer = str_footer.xpath("string(.)").encode(
                            sys.stdout.encoding, "ignore").decode(sys.stdout.encoding)
                        str_footer = str_footer[str_footer.rfind(u'赞'):]
                        guid = re.findall(pattern, str_footer, re.M)

                        # 点赞数
                        up_num = int(guid[0])
                        self.up_num.append(up_num)
                        print(u"点赞数: " + str(up_num))

                        # 转发数
                        retweet_num = int(guid[1])
                        self.retweet_num.append(retweet_num)
                        print(u"转发数: " + str(retweet_num))

                        # 评论数
                        comment_num = int(guid[2])
                        self.comment_num.append(comment_num)
                        print(u"评论数: " + str(comment_num))
                        print(
                            "===========================================================================")

                        self.weibo_num2 += 1

            if not self.filter:
                print(u"共" + str(self.weibo_num2) + u"条微博")
            else:
                print(u"共" + str(self.weibo_num) + u"条微博，其中" +
                      str(self.weibo_num2) + u"条为原创微博"
                      )
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def init_mysql(self):
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password=mysql_password,
            charset='utf8',
            db='online_social_networks')
        cursor = conn.cursor()
        return conn, cursor

    def execute(cursor, conn, sql):
        try:
            cursor.execute(sql)
            conn.commit()
        except:
            print("存入数据库失败")
            conn.rollback()

    def load_mysql(self):
        user_profile = user_profile_template.format()

    def write_mysql(self):
        try:
            if self.filter:
                result_header = u"\n\n原创微博内容: \n"
            else:
                result_header = u"\n\n微博内容: \n"
            conn, cursor = self.init_mysql()
            user_profile = user_profile_template.format(self.username, self.user_id, self.weibo_num, self.following,
                                                        self.followers)
            try:
                print(user_profile)
                cursor.execute(user_profile)
                conn.commit()
            except:
                print("存入数据库失败")
                conn.rollback()
            for i in range(1, self.weibo_num2 + 1):
                user_content = user_content_template.format(self.username, self.user_id, self.weibo_content[i - 1],
                                                            self.weibo_place[i - 1], self.publish_time[i - 1],
                                                            self.up_num[i - 1],
                                                            self.retweet_num[i - 1], self.comment_num[i - 1],
                                                            self.publish_tool[i - 1])
                try:
                    print(user_content)
                    cursor.execute(user_content)
                    conn.commit()
                except:
                    print("存入数据库失败")
                    conn.rollback()

            for (name, link) in self.follows.items():
                follow_user = user_follow_template.format(self.username, self.user_id, name, link)
                print(follow_user)
                try:
                    cursor.execute(follow_user)
                    conn.commit()
                except:
                    print("存入数据库失败")
                    conn.rollback()
            img_url = self.info_dict.get('img_url', '')
            authentication = self.info_dict.get('authentication', '')
            hometown = self.info_dict.get('hometown', '')
            birthday = self.info_dict.get('birthday', '')
            introduction = self.info_dict.get('introduction', '')
            label = self.info_dict.get('label', '')
            gender = self.info_dict.get('gender', '')
            education = self.info_dict.get('education', '')
            profile_2 = '''
                insert into weibo_user_profile_2 (username, user_id, img_url, authentication,hometown,birthday,introduction,
                label,gender,education) values ("{}", "{}","{}","{}","{}", "{}","{}","{}","{}","{}")
            '''
            try:
                cursor.execute(profile_2.format(self.username, self.user_id, img_url, authentication, hometown, birthday, introduction, label, gender, education))
                conn.commit()
            except:
                print(profile_2.format(self.username, self.user_id, img_url, authentication, hometown, birthday, introduction, label, gender, education))
                print("存入数据库失败")
                conn.rollback()
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 运行爬虫
    def start(self):
        try:
            self.get_username()
            self.get_user_info()
            self.get_weibo_info()
            self.get_follows()
            self.write_mysql()
            print(u"信息抓取完毕")
            print(
                "===========================================================================")

        except Exception as e:
            print("Error: ", e)

    def work(self, username):
        try:
            conn, cursor = self.init_mysql()
            sql = "SELECT * FROM online_social_networks.weibo_user_profile where username='{}'".format(username)
            print(sql)
            cursor.execute(sql)
            user = cursor.fetchall()
            if len(user) > 0:
                return user[0][2]
            html = requests.post('https://weibo.cn/find/user', cookies=self.cookie, data={'keyword': username, 'suser':2}).content
            print(html)
            selector = etree.HTML(html)
            user_id = selector.xpath("//body/table[1]/tr[1]/td[1]/a/@href")[0]
            print("user_id:", user_id)
            user_id = user_id[3:]
            print(user_id)
            main(int(user_id))
            return user_id
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def work_special(self, username):
        try:
            html = requests.post('https://weibo.cn/find/user', cookies=self.cookie, data={'keyword': username, 'suser':2}).content
            print(html)
            selector = etree.HTML(html)
            user_id = selector.xpath("//body/table[1]/tr[1]/td[1]/a/@href")[0]
            print("user_id:", user_id)
            user_url = "https://weibo.cn"+user_id
            print("user_url: ", user_url)
            user_id = self.get_user_id(user_url)
            main(int(user_id))
            return user_id
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def get_user_id(self, user_url):
        try:
            html = requests.get(user_url, cookies=self.cookie).content
            selector = etree.HTML(html)
            user_id = selector.xpath("//body/div[3]/table/tr[1]/td[2]/div/a[1]/@href")[0]
            print("user_id: ", user_id)
            real_id = str(user_id).split("=")[1].split("&")[0]
            print(real_id)
            return real_id
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()


def main(user_id):
    try:
        # 使用实例,输入一个用户id，所有信息都会存储在wb实例中
        user_id = user_id  # 可以改成任意合法的用户id（爬虫的微博id除外）
        filter = 0  # 值为0表示爬取全部微博（原创微博+转发微博），值为1表示只爬取原创微博
        wb = Weibo(user_id, filter)  # 调用Weibo类，创建微博实例wb
        wb.start()  # 爬取微博信息
        print(u"用户名: " + wb.username)
        print(u"全部微博数: " + str(wb.weibo_num))
        print(u"关注数: " + str(wb.following))
        print(u"粉丝数: " + str(wb.followers))
        if wb.weibo_content:
            print(u"最新/置顶 微博为: " + wb.weibo_content[0])
            print(u"最新/置顶 微博位置: " + wb.weibo_place[0])
            print(u"最新/置顶 微博发布时间: " + wb.publish_time[0])
            print(u"最新/置顶 微博获得赞数: " + str(wb.up_num[0]))
            print(u"最新/置顶 微博获得转发数: " + str(wb.retweet_num[0]))
            print(u"最新/置顶 微博获得评论数: " + str(wb.comment_num[0]))
            print(u"最新/置顶 微博发布工具: " + wb.publish_tool[0])
    except Exception as e:
        print("Error: ", e)
        traceback.print_exc()

def get_weibo_userid(username):
    wb = Weibo()
    user_id = wb.work(username)
    return user_id

def get_weibo_userid_special(username):
    wb = Weibo()
    user_id = wb.work_special(username)
    return user_id

# 1896891963 方滨兴
ids = [2830273497]
if __name__ == "__main__":
    pass
