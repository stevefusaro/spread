My family does a football pool every year (Pickem not Fantasy). The rules are:
- Users pick the winner of each game each week
- They number their picks from 1-16 (this number is the point wager)
- If they win a pick, they get the number of points they wagered
- If they lose a pick, they get zero points
- Whoever has the most points at the end of the season wins

At the end of every season I wonder how I compared against the spread. In other words, how many points would I get if my picks were just a list of games ordered by the spread, chosing those most likely to win at the top (wagering 16 points) and those least likely to win at the bottom (wagering 1 point)?

This year I figured I'd write some python that reads the scores and spreads from RunYourPool.com using Selenium and calculates how many points the spread would get. There is a margin of error to take into consideration given multiple games can have the same spread and therefore ordering by spread can yield somewhat random results. For example if game A and B both have a spread of +3, should a be higher or lower than B? Its hard to say, but if the list is ordered the difference can at most be 1. So each time this happens we add 1 to a "margin or error" counter.