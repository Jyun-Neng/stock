import argparse


def parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--year",
        "-y",
        default=2000,
        type=int,
        help="The year when fetch start")
    parser.add_argument(
        "--month", "-m", default=1, type=int, help="The month when fetch start")
    parser.add_argument(
        "--url",
        "-u",
        default="127.0.0.1",
        type=str,
        help="MongoDB url connection")
    parser.add_argument(
        "--port", "-p", default=27017, type=int, help="MongoDB listening port")
    parser.add_argument("--id", "-i", type=str, required=True, help="Stock ID")
    return parser.parse_args()


if __name__ == "__main__":
    args = parsing()
    print(args.id)
    print(args.year)
    print(args.month)
