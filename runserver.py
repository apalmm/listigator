"""
module that runs the server hosting the Flask application
"""

import sys
import argparse

<<<<<<< HEAD
from listigator.__init__ import create_app
=======
from __init__ import create_app
>>>>>>> main

app = create_app()

def parse_args() -> dict:
    """Parse CLI arguments"""

    parser = argparse.ArgumentParser(description='Server for the Flask application',
                                     allow_abbrev=False)

    parser.add_argument('port',
                        metavar='port',
                        type=int,
                        help='the port at which the server should listen')
    
    args = parser.parse_args()

    return vars(args)

def run_server(port: int) -> None:
    """Run the server for the Flask application"""

    try:
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)


def main():
    """Parses CLI arguments and runs server if valid"""
    args = parse_args()
    port = args['port']
    run_server(port)

if __name__ == '__main__':
    main()
