from constants import NFL_WEEKLY_MAX_GAME_COUNT
from crawl import get_html_scores_by_week, html_scores_to_games


def _get_spread_picks(week_games):
    picks = {}
    points = NFL_WEEKLY_MAX_GAME_COUNT
    week_games.sort(key=lambda x: -x.spread_float)
    for game in week_games:
        pick = game.home_team if game.spread_dir == '+' else game.away_team
        picks[points] = (game, pick)
        points -= 1
    return picks


def _make_picks(week_games):
    picks = _get_spread_picks(week_games)
    won = 0
    for points, (game, pick) in sorted(picks.items(), key=lambda x: -x[0]):
        if pick == game.won_team:
            outcome = 'won'
            won += points
        else:
            outcome = 'lost'

        print('{points:>2}: {pick:<3}  {outcome:<4}  ({away_team:<3} @ {home_team:<3} {spread_str})'.format(
            points=points,
            pick=pick,
            outcome=outcome,
            away_team=game.away_team,
            home_team=game.home_team,
            spread_str=game.spread_str
        ))

    spreads = [g.spread_float for g in week_games]
    error = len(spreads) - len(set(spreads))
    return won, error


def calculate_spread_score(weeks, source):
    points_won = 0
    error_margin = 0
    html_by_week = get_html_scores_by_week(weeks, source)
    for week, html in html_by_week.items():
        print('---- Week {} ----'.format(week))
        games = html_scores_to_games(html)
        _points_won, _error_margin = _make_picks(games)
        points_won += _points_won
        error_margin += _error_margin
    return points_won, error_margin
