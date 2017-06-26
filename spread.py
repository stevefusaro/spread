import argparse
from crawl import get_html_scores_by_week, html_scores_to_json


def _parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('source', choices=['file', 'web'])
    parser.add_argument('-w', '--weeks', type=int, nargs='*', default=range(1, 18))
    return parser.parse_args()


def _get_spread_picks(week_games):
    picks = {}
    points = 16
    week_games.sort(key=lambda x: -x['spread_float'])
    for game in week_games:
        pick = game['home_team'] if game['spread_dir'] == '+' else game['away_team']
        picks[points] = (game, pick)
        points -= 1
    return picks


def _make_picks(week_games):
    picks = _get_spread_picks(week_games)
    won = 0
    for points, (game, pick) in sorted(picks.items(), key=lambda x: -x[0]):
        if pick == game['won_team']:
            outcome = 'won'
            won += points
        else:
            outcome = 'lost'

        print('{points:>2}: {pick:<3}  {outcome:<4}  ({away_team:<3} @ {home_team:<3} {spread_str})'.format(
            points=points,
            pick=pick,
            outcome=outcome,
            away_team=game['away_team'],
            home_team=game['home_team'],
            spread_str=game['spread_str']
        ))

    spreads = [g['spread_float'] for g in week_games]
    error = len(spreads) - len(set(spreads))
    return won, error


def main():
    args = _parse_args()
    points_won = 0
    points_error = 0
    html_by_week = get_html_scores_by_week(args.weeks, args.source)
    for week, html in html_by_week.items():
        print('---- Week {} ----'.format(week))
        games = html_scores_to_json(html)
        won, error = _make_picks(games)
        points_won += won
        points_error += error

    print('\nTotal points for Spread: {} points (+/- {})\n'.format(points_won, points_error))

if __name__ == '__main__':
    main()
