from bridgebeam import application
from bridgebeam.controllers import *
import logging

def run():

    # config log format 
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)-21s %(levelname)s %(name)s (%(funcName)-s) %(process)d:%(thread)d - %(message)s',
                        filename='lol.log')

    print config
    print application.config
    return application
