import logging

from logging.handlers import SysLogHandler



def get_logger(hostname, port, logger_name):


	handler = SysLogHandler(


	address = (

		hostname, 

		port

		)


	)


	format = "%(asctime)s %(levelname)s  %(message)s"


	formatter = logging.Formatter(format, datefmt = "%Y-%m-%d %H:%M:%S")


	handler.setFormatter(formatter)


	file_handler = logging.FileHandler('./logs/app_logs.log')


	logger = logging.getLogger(logger_name)


	logger.setLevel(logging.INFO)


	logger.addHandler(handler)


	logger.addHandler(file_handler)


	return logger



if __name__ == "__main__":

	pass