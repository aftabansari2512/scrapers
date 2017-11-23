"""
dependency:
pip3 install beautifulsoup4

"""

from urllib.request import urlopen as req
from bs4 import BeautifulSoup as soup
import json
import os

root = os.path.dirname(os.path.realpath(__file__)) + '/' # + '/../../'
target_folder = root + 'target'
master_folder = root + 'json/'
file_name = 'restaurants.json'
# create directory if it does not exist
if not os.path.exists(master_folder):
    os.mkdir(master_folder)

url = "https://www.yelp.com/search?find_loc=Helsinki,+Finland&start=0&attrs=BusinessAcceptsCreditCards,GoodForMeal.breakfast,GoodForMeal.brunch"

data = []

def getData(url):
    try:
        response = req(url)
    except req.HTTPError as e:
        return None
    try:
        data_raw = response.read()
        page_soup = soup(data_raw, "html.parser")
        containers = page_soup.findAll("div", {"class": "biz-listing-large"})
        for container in containers:
            title= container.div.div.h3.a.span.get_text()
            title = title.strip() # remove white space
            r = container.findAll("span", {"class": "review-count rating-qualifier"})
            rating = r[0].text
            rating = rating.strip().split(' ')[0] # split by white space and take first part
            item = {'name': title , 'rating' : rating, 'position': 0} # construct dictionary
            data.append(item)
    except AttributeError as e:
        return None

getData(url)

for k in data:
    """ Assign elements's index number as position for each entry"""
    k['position'] = data.index(k)

with open(master_folder + file_name, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)

