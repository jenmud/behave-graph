"""
Setup the environment by parsing the command line options and staring
a ruruki http server.
"""
import argparse
import logging
import os
from behave.configuration import Configuration
from behave.runner import Runner, parse_features
from ruruki_eye.server import run
from behave_graph.scrape import GRAPH
from behave_graph.scrape import scrape_features


__all__ = ["load"]


def load(path):
    """
    Load the given path that contains the features and steps.

    :param path: Path where the feature and steps files can be found.
    :type path: :class:`str`
    :returns: A behave runner.
    :rtype: :class:`behave.runner.Runner`
    """
    try:
        config = Configuration(path)
        runner = Runner(config)
        features = parse_features(
            [f.filename for f in runner.feature_locations()]
        )
        scrape_features(features)
        return runner
    except Exception as error:  # pylint: disable=broad-except
        logging.exception(
            "Unexpected error creating configuration %r: %r",
            path, error
        )

        raise argparse.ArgumentTypeError(error)


def parse_arguments():
    """
    Parse the command line arguments.

    :returns: All the command line arguments.
    :rtype: :class:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(
        description="Behave dependency grapher."
    )

    parser.add_argument(
        "-b",
        "--base-dir",
        default=os.getcwd(),
        type=load,
        help=(
            "Behave base directory path "
            "where features and steps can be found. "
            "(default: %(default)s)"
        ),
    )

    parser.add_argument(
        "--runserver",
        action="store_true",
        help="Start a ruruki http server.",
    )

    parser.add_argument(
        "--address",
        default="0.0.0.0",
        help="Address to start the web server on. (default: %(default)s)",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help=(
            "Port number that the web server will accept connections on. "
            "(default: %(default)d)"
        ),
    )

    return parser.parse_args()


def main():
    """
    Entry point.
    """
    logging.basicConfig(level=logging.INFO)
    namespace = parse_arguments()

    if namespace.runserver is True:
        run(namespace.address, namespace.port, False, GRAPH)
