import argparse

from play import play
from record import record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="Command to run", choices=["record", "play"])
    parser.add_argument("--agent", help="Agent to run", default="agent")
    parser.add_argument("--params", help="Specify the params file path", default=None)
    # Dev parameter to specify a custom extension path
    parser.add_argument(
        "--autotab-ext-path",
        help="Path to the extension (optional, for development use only)",
        default=None,
    )
    parser.add_argument(
        "--mirror-disabled",
        help="Disable mirror",
        action="store_true",
    )
    args = parser.parse_args()

    if args.command == "record":
        record(
            args.agent,
            autotab_ext_path=args.autotab_ext_path,
            mirror_disabled=args.mirror_disabled,
            params_filepath=args.params,
        )
    elif args.command == "play":
        play(args.agent, params_filepath=args.params)


if __name__ == "__main__":
    main()
