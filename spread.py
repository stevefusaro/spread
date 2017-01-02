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


def _get_spread_picks(week_games):
    week_games.sort(key=lambda x: -x['spread_float'])
    picks = {}
    points = 16
    won = 0
    for g in week_games:
        pick = g['home_team'] if g['spread_dir'] == '+' else g['away_team']
        picks[points] = pick
        if pick == g['won_team']:
            won += points
            g['outcome'] = 'won'
        else:
            g['outcome'] = 'lost'
        g['pick'] = '{} for {} pts'.format(pick, points)
        g['points'] = points
        points -= 1


def main():
    args = _parse_args()
    week_html = get_nfl_html(args.weeks, args.source)
    for week, html in week_html.items():
        print('---- WEEK {} ----'.format(week))
        games = extract_html_games(html)
        _get_spread_picks(games)
        games.sort(key=lambda x: -x['points'])
        for g in games:
            print('{} {} {} {} {} picked {} and {}'.format(
                g['home_team'], g['away_team'], g['home_score'], g['away_score'],
                g['spread_str'], g['pick'], g['outcome'])
            )

if __name__ == '__main__':
    main()
