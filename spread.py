import argparse
from pprint import pprint
from crawl import get_nfl_scores


def _parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
    games = get_nfl_scores(args.weeks)
    pprint(games)
    for week, data_list in games.items():
        print('Week {}'.format(week))
        for data in data_list:
            print('{} {} {} {}'.format(data['home_team'], data['away_team'], data['home_score'], data['away_score']))
    import ipdb; ipdb.set_trace()

if __name__ == '__main__':
    main()
