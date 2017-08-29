

from argparse import ArgumentParser

from search.ReinforcementLearningSearcher import ReinforcementLearningSearcher
from applications.ApplicationFactory import ApplicationFactory

import logging

class SearchDriver:
    def __init__(self, options):
        self.options = options

    def run(self):
        application = ApplicationFactory.create(self.options["application"], self.options)

        ReinforcementLearningSearcher(application, self.options).run()

def main():
    parser = ArgumentParser(description='Run neural network architecture search.')

    parser.add_argument('-a', '--application', default='mnist', type=str,
                    help='The name of the application to run.')
    parser.add_argument('-d', '--data-directory', default='data', type=str,
                    help='The directory path to store training data in.')
    parser.add_argument('--data-type', default='float32', type=str,
                    help='The data type to use (float32 or float16).')
    parser.add_argument('--network-embedding-size', default=16, type=int,
                    help='The size of the network embedding to use (represents complete networks).')
    parser.add_argument('--layer-embedding-size', default=8, type=int,
                    help='The size of the layer embedding to use (represents single layers).')
    parser.add_argument('-v', '--verbose', default = False, action='store_true',
        help = 'Print out verbose logging info.')

    options = vars(parser.parse_args())

    if options["verbose"]:
        logging.basicConfig(level=logging.INFO)


    SearchDriver(options).run()

if __name__ == "__main__":
    main()







