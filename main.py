import argparse
from spread import calculate_spread_score


def _parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('source', choices=['file', 'web'])
    parser.add_argument('-w', '--weeks', type=int, nargs='*', default=range(1, 18))
    return parser.parse_args()


def main():
    args = _parse_args()
    points, error = calculate_spread_score(args.weeks, args.source)
    print('\nTotal points for Spread: {} points (+/- {})\n'.format(points, error))

if __name__ == '__main__':
    main()
