import argparse
from src.record import record
from src.play import play


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
