from flask import Blueprint, render_template
from flask_login import LoginManager, login_required, current_user
from base64 import b64encode
from itertools import islice
from sqlalchemy.sql import text
import bs4 as bs
import string
import urllib.request


from models import db, Users

home = Blueprint('home', __name__, template_folder='../templates')
login_manager = LoginManager()
login_manager.init_app(home)

@home.route('/home', methods=['GET'])
@login_required
def show():
    #news_images = db.session.query(News).all()
    #image_list = islice([b64encode(img.imageNews).decode('ascii') for img in reversed(news_images)], 0, 3)

    #indies_images = db.session.query(IndieGame).first()
    #indie_list = [b64encode(indies_images.imageIndie).decode('ascii')]

    cards_scrape = 'https://gg.deals/news/deals/'
    cards_imgs = scrapeCards(cards_scrape)

    hotsales_scrape = 'https://gg.deals/deals/new-deals/?page=1'
    hotsales_imgs = scrapeHotSales(hotsales_scrape)

    indies_scrape = 'https://gg.deals/deals/?sort=date&tag=1'
    indie_img = scrapeIndies(indies_scrape)

    return render_template('home.html', cards_list=cards_imgs, hotsales_list=hotsales_imgs, indies_list=indie_img)

def scrapeCards(url):
    try:
        with urllib.request.urlopen(url) as response:
            my_url = response.read()

        soup = bs.BeautifulSoup(my_url, 'lxml')

        img_tags = [item.img['src'].split('352w, ')[-1].split(' 704w')[0] for item in soup.select('div.news-image-wrapper')][:3]
        link_tags = ['https://gg.deals' + item['href'] for item in soup.find_all('a', {'class':'full-link'})]

        return zip(img_tags, link_tags)

    except Exception as e:
        print(f"An error ocurred: {e}")
        return None

def scrapeHotSales(url):
    try:
        with urllib.request.urlopen(url) as response:
            my_url = response.read()

        soup = bs.BeautifulSoup(my_url, 'lxml')

        title_tags = [item.text for item in soup.find_all('a', {'class':['game-info-title', 'title']})][:4]
        discount_tags = [item.text for item in soup.find_all('span', {'class':'discount'})][:4]
        img_tags = [item.picture.img['src'].split('x, ')[-1].split(' 2x')[0] for item in soup.select('a.main-image')][:4]
        total_tags = [item.text for item in soup.find_all('span', {'class':['price-inner', 'game-price-new']})][:4]
        link_tags = ['https://gg.deals' + item['href'] for item in soup.find_all('a', {'class':'full-link'})][:4]

        return zip(title_tags, discount_tags, img_tags, total_tags, link_tags)
    except Exception as e:
        print(f"An error ocurred: {e}")
        return None

def scrapeIndies(url):
    try:
        with urllib.request.urlopen(url) as response:
            my_url = response.read()

        soup = bs.BeautifulSoup(my_url, 'lxml')

        img_tag = soup.select('a.main-image source')

        img_tags = [img_tag[1]['srcset'].split(' 1x,')[-1].split(' 2x')[0]]

        link_tags = ['https://gg.deals' + item['href'] for item in soup.find_all('a', {'class':'full-link'})][:1]


        return zip(img_tags, link_tags)
    except Exception as e:
        print(f"An error ocurred: {e}")
        return None