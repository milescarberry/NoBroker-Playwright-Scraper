from time import *


def get_timer():
	

	global scrape_timer


	scrape_timer = 0


	for i in range(10000):

		scrape_timer += 1

		sleep(1)


	print()

	print("Timer Ends.")

	print()




if __name__ == "__main__":


	pass           # Do Nothing