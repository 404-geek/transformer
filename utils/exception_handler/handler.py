import logging
import os


def setup_logger():
    ''' Configure the logger '''
    if not os.path.exists('logs'):
        os.mkdir('logs')
    logging.basicConfig(filename='logs/error.log', 
                        level=logging.ERROR, 
                        format='%(asctime)s - %(levelname)s - %(message)s')

def log_error(e: Exception, file_name: str, uuid: str, start: int, end: int):
    ''' Log the error message and stack trace '''
    logging.error(f"Exception occurred for file {file_name} with uuid {uuid} for chunk [{start}, {end}]", exc_info=True)
