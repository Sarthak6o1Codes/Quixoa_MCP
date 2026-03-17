import argparse
import os

from google_helper import get_credentials


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--print-url", action="store_true", help="Print auth URL to stdout for client to open (e.g. in Docker)")
    args = parser.parse_args()

    token_path = os.getenv('GOOGLE_TOKEN_PATH', 'token.json')
    if args.force and os.path.exists(token_path):
        os.remove(token_path)

    get_credentials(print_auth_url=args.print_url)
