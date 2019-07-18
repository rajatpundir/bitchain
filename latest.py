import os
from strong_model import StrongModel

def build_superimposed_database():
	if not os.path.exists('database'):
	    os.mkdir('database')
	if os.path.exists('database/latest.db'):
	    os.remove('database/latest.db')
	os.chdir('database')
	db_nums = []
	for database in sorted(os.listdir()):
	    try:
	        db_nums.append(int(database.split('.')[0]))
	    except:
	        pass
	sorted_db_nums = []
	for x in sorted(db_nums):
	    sorted_db_nums.append(str(x) + '.db')
	os.chdir('..')
	latest_model = StrongModel('database/latest.db', True)
	attached_database_name = 'CURRENT_DIFF'
	for database_filename in sorted_db_nums:
	    latest_model.attach_replace_detach('database/' + database_filename, attached_database_name)
	    print(database_filename)
	latest_model.compact_database()
	print('SUPERIMPOSITION : SUCCESS')

if __name__ == "__main__":
	build_superimposed_database()
