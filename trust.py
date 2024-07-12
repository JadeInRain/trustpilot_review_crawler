# coding=utf-8
import csv

import requests
import json
from bs4 import BeautifulSoup

def get_html_source(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查是否请求成功
        response.encoding = response.apparent_encoding
        html_source = response.text
        return html_source
    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
        return None


class TrustPioltSpider:
    def __init__(self):
        self.results = []

    def fetch_url(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
if __name__ == "__main__":

    with open("trust_mailchimp", "r", encoding="utf-8") as file:
        start_urls = [line.strip() for line in file.readlines()]

    spider = TrustPioltSpider()
    for url in start_urls[0:50]:
        response = spider.fetch_url(url)
        if response:
            soup = BeautifulSoup(response, 'html.parser')


            next_data_script = soup.find('script', id='__NEXT_DATA__')
            next_data_json = json.loads(next_data_script.string)

            reviews = next_data_json['props']['pageProps']['reviews']
            for review in reviews:
                consumer_country = review['consumer']['countryCode']
                language = review['language']
                consumer_name = review['consumer']['displayName']
                consumer_isVerified = review['consumer']['isVerified']
                rating = review['rating']
                review_title = review['title']
                review_text = review['text']
                rating = review['rating']
                review_is_verified = review['labels']['verification']['isVerified']
                review_likes = review['likes']
                review_is_pending = review['pending']
                date_of_experience = review['dates']['experiencedDate']
                date_of_published = review['dates']['publishedDate']
                date_of_updated = review['dates']['updatedDate']
                reply = review['reply']
                if reply:
                    reply=reply['message']

                with open("trustpilot_mailchimp.csv", "a", newline="", encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    # writer.writerow(["Business_Identify", "Business_Name", "Business_Website", "Consumer_Country", "Consumer_Name",
                    #                  "Consumer_is_Verified", "Rating", "Review_Title", "Review_Text", "Review_is_Verified",
                    #                  "Review_Language", "Review_Likes", "Review_is_Pending", "Date_of_Experience", "Date_of_Published",
                    #                  "Date_of_Updated", "Reply_Message"])
                    writer.writerow(["www.mailchimp.com", "Mailchimp", "https://www.mailchimp.com/", consumer_country, consumer_name,
                                     consumer_isVerified, rating, review_title, review_text, review_is_verified, language,
                                     review_likes, review_is_pending, date_of_experience, date_of_published,
                                     date_of_updated, reply])
