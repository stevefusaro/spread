
class Game():
    def __init__(self, *args, **kwargs):
        self.away_team = kwargs['away_team']
        self.away_score = kwargs['away_score']
        self.home_team = kwargs['home_team']
        self.home_score = kwargs['home_score']
        self.spread_float = kwargs['spread_float']
        self.spread_dir = kwargs['spread_dir']

    @property
    def won_team(self):
        if self.home_score > self.away_score:
            return self.home_team
        return self.away_team

    @property
    def lost_team(self):
        if self.home_score > self.away_score:
            return self.away_team
        return self.home_team

    @property
    def spread_str(self):
        return '{}{}'.format(self.spread_dir, self.spread_float)
