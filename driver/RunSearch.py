

from argparse import ArgumentParser

from search.ReinforcementLeariningSearcher import ReinforcementLearningSearcher
from application.ApplicationFactory import ApplicationFactory

class SearchDriver:
    def __init__(self, options):
        self.options = options

    def run(self):
        application = ApplicationFactory.create(self.options["application"])

        ReinforcementLearningSearcher(application, self.options).run()

def main():
    parser = ArgumentParser(description="Run neural network architecture search.")

    parser.add_argument('-a', '--application', default="mnist", type=str,
                    help="The name of the application to run.")

    options = vars(parser.parse_args())

    SearchDriver(options).run()

if __name__ == "__main__":
    main()







