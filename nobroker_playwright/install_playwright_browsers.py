from subprocess import call



def install_browsers():


	command_list = ['playwright', 'install']


	print('''\nExecuting 'playwright install' Command\n''')


	call(command_list)


	print('''\nSuccessfully Executed 'playwright install' Command\n''')





if __name__ == "__main__":

	pass