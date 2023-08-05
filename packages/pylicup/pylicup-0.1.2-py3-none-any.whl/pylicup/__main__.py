import argparse
import logging

from pylicup.license_manager import license_header_manager

if __name__ == "__main__":
    """For now we only accept inserting as a direct call from the main"""
    # Define the argparser helper:
    parser = argparse.ArgumentParser(
        description="Manages files license header. \n"
        + "Sets the last license header given in all files of the file directory."
        + "If multiple license headers are given, the first one will be added to all files and replace the rest provided."
        + "It is possible to include multiple directories where to insert / replace header files."
    )
    parser.add_argument(
        "-l, --licenses",
        dest="licenses",
        type=str,
        nargs="+",
        required=True,
        help="License headers file path. The first occurrence is considered as the new one to replace the rest.",
    )
    parser.add_argument(
        "-d, --directories",
        dest="directories",
        nargs="+",
        required=True,
        help="Directories where to insert / replace licenses.",
    )
    args = parser.parse_args()
    logging.info("Initializing license manager.")
    license_header_manager(args.licenses, args.directories)
    logging.info("License manager finished.")
