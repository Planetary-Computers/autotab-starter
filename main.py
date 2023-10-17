import argparse
from src.record import record
from src.play import play

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="Command to run", choices=["record", "play"])
    args = parser.parse_args()

    if args.command == "record":
        record()
    elif args.command == "play":
        play()

if __name__ == "__main__":
    main()