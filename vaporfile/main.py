import sys
import argparse
import shlex
import logging

from . import __version__
import credentials
import website

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("vaporfile")

def main():
    parser_template = argparse.ArgumentParser(add_help=False)
    parser_template.add_argument("-v", "--verbose", dest="verbose",
                                 default=False, action="store_true",
                                 help="Be verbose")
    parser_template.add_argument("-vv", "--veryverbose", dest="veryverbose",
                                 default=False, action="store_true",
                                 help="Be extra verbose")
    parser = argparse.ArgumentParser(parents=[parser_template])
    parser.version = "vaporfile -- {0} -- http://www.enigmacurry.com"\
        .format(__version__)
    
    subparsers = parser.add_subparsers()

    ### Credentials
    p_cred = subparsers.add_parser(
        "credentials", help="Manage Amazon AWS credentials",
        parents=[parser_template])
    p_cred_subparsers = p_cred.add_subparsers()
    p_cred_store = p_cred_subparsers.add_parser(
        "store", help="Store credentials locally")
    p_cred_store.set_defaults(func=credentials.prompt_save_credentials)

    ### Create site
    p_create = subparsers.add_parser(
        "create", help="Create a new S3 website",
        parents=[parser_template])
    p_create.set_defaults(func=website.prompt_create_website)

    ### Upload
    p_upload = subparsers.add_parser(
        "upload", help="Upload a previously configured website",
        parents=[parser_template])
    p_upload.add_argument("WEBSITE", help="Name of configured website")
    p_upload.add_argument("--no-delete", action="store_true", help="Don't delete old files from S3")
    p_upload.set_defaults(func=website.upload_website)

    ### List
    p_list = subparsers.add_parser(
        "list", help="List all configured websites",
        parents=[parser_template])
    p_list.set_defaults(func=website.list_websites)
    

    if len(sys.argv) <= 1:
        parser.print_help()
        parser.exit(1)
    else:
        args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.INFO)
        logger.info("Setting verbose output mode")
    if args.veryverbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Setting very verbose output mode")
    args.func(args)