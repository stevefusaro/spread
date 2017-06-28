
from game import Game
from spread import _get_spread_picks


def test_sorts_by_spread():
    kwargs = {
        'away_team': 'NYG',
        'away_score': 5,
        'home_team': 'DAL',
        'home_score': 6,
        'spread_float': 15.0,
        'spread_dir': '+',
    }
    games = []
    spread_floats = [4.5, 1.5, 10.5, 2.5, 3.5]
    for spread_float in spread_floats:
        game = Game(**kwargs)
        game.spread_float = spread_float
        games.append(game)

    picks = _get_spread_picks(games)

    min_point = min(picks.keys())
    max_point = max(picks.keys())

    assert picks[max_point][0].spread_float == max(spread_floats)
    assert picks[min_point][0].spread_float == min(spread_floats)
