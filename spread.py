import argparse
from pprint import pprint
from crawl import get_nfl_html, extract_html_games


def _parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('source', choices=['file', 'web'])
    parser.add_argument('-w', '--weeks', type=int, nargs='*', default=range(1, 18))
    return parser.parse_args()


def _process_games(weekly_games):
    for week, games in weekly_games.items():
        for data in games:
            home_team = data['home_team']
            away_team = data['away_team']
            away_score = data.get('away_score', 0)
            home_score = data.get('home_score', 0)
            if home_score > away_score:
                won_team = home_team
                lost_team = away_team
            else:
                won_team = away_team
                lost_team = home_team


def main():
    args = _parse_args()
    week_html = get_nfl_html(args.weeks, args.source)
    for week, html in week_html.items():
        print('Week {}'.format(week))
        games = extract_html_games(html)
        for g in games:
            print('{} {} {} {} {}'.format(g['home_team'], g['away_team'], g['home_score'], g['away_score'], g['spread']))

if __name__ == '__main__':
    main()
