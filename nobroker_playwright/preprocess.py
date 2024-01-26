from subprocess import call


def preprocess_func():



	print('''\nExecuting Preprocessing Script\n''')


	command_list = [

	'python', 


	'../realty_rental_analysis/new_nobroker_rent_data_preprocessing_analysis.py'

	]


	call(command_list)



	print('''\nSuccessfully Executed Preprocessing Script\n''')





if __name__ == '__main__':



	pass           # Do Nothing