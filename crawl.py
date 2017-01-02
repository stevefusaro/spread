import time

from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select

from constants import ABREV_BY_MASCOT, DATA_DIR
from driver import get_driver


def get_nfl_html(weeks, source):
    assert source in ('file', 'web')
    force_update = False if source == 'file' else True
    driver = get_driver() if source == 'web' else None
    week_html = {}
    try:
        for week in weeks:
            html = _get_week_html(driver, week, force_update)
            week_html[week] = html
    finally:
        if driver:
            driver.quit()
    return week_html


def _get_week_html(driver, week, force_update):
    html_path = '/'.join([DATA_DIR,
                          'html',
                          'week_%s_scores.html' % week])
    try:
        if force_update:
            raise FileNotFoundError
        with open(html_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        driver.get('http://www.runyourpool.com/nfl/confidence/reports/nfl_results.cfm')
        select = Select(driver.find_element_by_css_selector('[name=week]'))
        select.select_by_value(str(week))
        time.sleep(1)
        html = driver.page_source
        # html = html.encode(errors='ignore')
        with open(html_path, 'w') as f:
            f.write(html)
        return html


def _foo(v):
    try:
        v = v.text
    except AttributeError:
        return None
    try:
        return int(v)
    except ValueError:
        return v


def extract_html_games(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='table')
    games = []
    for row in table.find_all('tr', class_='gameRow'):
        # Columns: date | away_team | away_score | spread | home_score | home_team
        if not row.find(class_='score_away'):
            games.append({})
            continue
        game = {
            'away_score': _foo(row.find(class_='score_away')),
            'home_score': _foo(row.find(class_='score_home')),
            'away_mascot': row.find_all(class_='mascot')[0].text,
            'home_mascot': row.find_all(class_='mascot')[1].text,
        }
        game.update({
            'home_team': ABREV_BY_MASCOT[game['home_mascot']],
            'away_team': ABREV_BY_MASCOT[game['away_mascot']],
        })
        games.append(game)
    return games
