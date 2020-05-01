import sys

from .__about__ import __version__
from .main import get_offers

APEC_API_URL = "https://api-beta.dashblock.com/apec_jobs/search"


def offers(argv=None):
    # Parse command line arguments.
    parser = _get_parser()
    args = parser.parse_args(argv)

    params = {"department_code": args.department_code, "paginate_max": args.paginate_max}
    items = get_offers(APEC_API_URL, args.auth_key, params)

    if items:
        print("Extracted {} job offers in total".format(len(items)))
        for item in items:
            print(item)
    else:
        print("No job offer found using the API, based on the input parameters")


def _get_parser():
    import argparse

    parser = argparse.ArgumentParser(
        description=("Job Offers API client executable."),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("department_code", type=str, help="code of department for the offers search")
    parser.add_argument("paginate_max", type=int, help="pagination max number for the offers results pages")
    parser.add_argument("auth_key", type=str, help="Authentication key for the API")

    __copyright__ = "Copyright (c) 2020 Content Gardening Studio <info@contentgardeningstudio.com>"
    version_text = "\n".join(
        [
            "joboffers_apiclient {} [Python {}.{}.{}]".format(
                __version__,
                sys.version_info.major,
                sys.version_info.minor,
                sys.version_info.micro,
            ),
            __copyright__,
        ]
    )
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=version_text,
        help="display version information",
    )

    return parser
