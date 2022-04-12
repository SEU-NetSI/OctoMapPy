import logging
from Inputter import Inputter

# Only output errors from the logging framework
logging.basicConfig(level=logging.WARN)
logger = logging.getLogger()

def main():
    input = Inputter()

if __name__=="__main__":
    main()