import argparse

from play import play
from record import record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="Command to run", choices=["record", "play"])
    parser.add_argument("--agent", help="Agent to run", default="agent")
    args = parser.parse_args()

    if args.command == "record":
        record(args.agent)
    elif args.command == "play":
        play(args.agent)


if __name__ == "__main__":
    main()
