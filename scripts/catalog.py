from flask import Blueprint, render_template, request
from flask_login import LoginManager, login_required, current_user
import bs4 as bs
import urllib.request
from itertools import chain

from models import db, Users

catalog = Blueprint('catalog', __name__, template_folder='../templates')
login_manager = LoginManager()
login_manager.init_app(catalog)

@catalog.route('/catalog/<int:Number>', methods=['GET', 'POST'])
@login_required
def show(Number):

    epicgames_url_to_scrape = 'https://gg.deals/deals/new-deals/?page=' + str(Number)

    title, current_price_tags, discount_price_tags, img_tags, link = scrapeCatalogue(epicgames_url_to_scrape)

    return render_template('catalog.html', list=zip(title, current_price_tags, discount_price_tags, img_tags, link))

def scrapeCatalogue(url):
    try:
        with urllib.request.urlopen(url) as response:
            my_url = response.read()

        soup = bs.BeautifulSoup(my_url, 'lxml')

        title_tags = [item.text for item in soup.find_all('a', {'class':['game-info-title', 'title']})]
        link_tags = ['https://gg.deals' + item['href'] for item in soup.find_all('a', {'class':'full-link'})]
        current_price_tags = [item.text for item in soup.select('span.price-old')]
        discount_price_tags = [item.text for item in soup.select('span.game-price-new')]
        img_tags = [item.picture.img['src'].split('x, ')[-1].split(' 2x')[0] for item in soup.select('a.main-image')]

        return title_tags, current_price_tags, discount_price_tags, img_tags, link_tags
    except Exception as e:
        print(f"An error ocurred: {e}")
        return None
