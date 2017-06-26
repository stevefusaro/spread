import time

from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select

from constants import ABREV_BY_MASCOT, DATA_DIR
from driver import get_driver


def _fetch_week_html(driver, week):
    driver.get('http://www.runyourpool.com/nfl/confidence/reports/nfl_results.cfm')
    select = Select(driver.find_element_by_css_selector('[name=week]'))
    select.select_by_value(str(week))
    time.sleep(1)
    html = driver.page_source
    return html


def _get_week_html(driver, week, force_update):
    html_path = '{}/html/week_{}_scores.html'.format(DATA_DIR, week)
    try:
        if force_update:
            raise FileNotFoundError
        with open(html_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        html = _fetch_week_html(driver, week)
        with open(html_path, 'w') as f:
            f.write(html)
        return html


def get_html_scores_by_week(weeks, source):
    assert source in ('file', 'web')
    force_update = False if source == 'file' else True
    driver = get_driver() if source == 'web' else None
    html_by_week = {}
    try:
        for week in weeks:
            html = _get_week_html(driver, week, force_update)
            html_by_week[week] = html
    finally:
        if driver:
            driver.quit()
    return html_by_week


def html_scores_to_json(html):
    """
    Locate and parse an HTML table of NFL scores.
    Columns are: date, away_team, away_score, spread, home_score, home_team.
    """
    games = []
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='table')
    for row in table.find_all('tr', class_='gameRow'):

        away_mascot = row.find_all(class_='mascot')[0].text
        away_team = ABREV_BY_MASCOT[away_mascot]
        away_score = int(row.find(class_='score_away').text)

        spread = row.find(class_='spread').text
        spread = spread.replace('(', '').replace(')', '')

        home_mascot = row.find_all(class_='mascot')[1].text
        home_team = ABREV_BY_MASCOT[home_mascot]
        home_score = int(row.find(class_='score_home').text)

        if home_score > away_score:
            won_team = home_team
            lost_team = away_team
        else:
            won_team = away_team
            lost_team = home_team

        games.append({
            'away_team': away_team,
            'away_score': away_score,
            'home_team': home_team,
            'home_score': home_score,
            'spread_str': spread,  # e.g. "+1" or "-0.5"
            'spread_float': float(spread[1:]),
            'spread_dir': spread[0],   # TODO rename dir to directon,
            'won_team': won_team,
            'lost_team': lost_team
        })

    return games
