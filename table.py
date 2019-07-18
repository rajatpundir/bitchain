class Table:
	def __init__(self, conn):
		self.conn = conn
		self.table_name = None
		self.column_names = None
		self.parent_table_name = None

	def create_table(self):
		exec_string = "CREATE TABLE IF NOT EXISTS " + str(self.table_name) + "("
		if self.table_name == 'MODULES':
			exec_string += "ID INTEGER PRIMARY KEY"
		else:
			exec_string += "MODULE_ID INTEGER NOT NULL, "
			exec_string += "ID INTEGER NOT NULL"
		for column in self.column_names:
			if column == 'NAME':
				if self.table_name == 'MODULES':
					exec_string += ", NAME TEXT UNIQUE NOT NULL"
				else:
					exec_string += ", NAME TEXT NOT NULL"
			elif column == 'MAGNET_URL':
				exec_string += ", MAGNET_URL TEXT NOT NULL"
			elif column == 'MAGNET_LINK_ID':
				exec_string += ", " + str(column) + " INTEGER NOT NULL"
			elif column == 'FILE_NUM':
				exec_string += ", " + str(column) + " INTEGER NOT NULL DEFAULT 0"
			else:
				exec_string += ", " + str(column) + " TEXT"
		if self.parent_table_name:
			if self.table_name == 'LANGUAGES':
				exec_string += ", FOREIGN KEY(MODULE_ID) REFERENCES MODULES(ID)"
				exec_string += ", PRIMARY KEY(MODULE_ID, ID)"
				exec_string += ", UNIQUE(MODULE_ID, NAME)"
			else:
				exec_string += ", PARENT_ID INTEGER NOT NULL"
				exec_string += ", FOREIGN KEY(MODULE_ID) REFERENCES MODULES(ID)"
				exec_string += ", PRIMARY KEY(MODULE_ID, ID)"
				exec_string += ", FOREIGN KEY(MODULE_ID, PARENT_ID) REFERENCES " + str(self.parent_table_name) + "(MODULE_ID, ID)"
				exec_string += ", UNIQUE(MODULE_ID, PARENT_ID, NAME)"
				if self.table_name == 'SOURCES':
					exec_string += ", FOREIGN KEY(MODULE_ID, MAGNET_LINK_ID) REFERENCES MAGNET_LINKS(MODULE_ID, ID)"
		elif self.table_name == 'MAGNET_LINKS':
			exec_string += ", FOREIGN KEY(MODULE_ID) REFERENCES MODULES(ID)"
			exec_string += ", PRIMARY KEY(MODULE_ID, ID)"
			exec_string += ", UNIQUE(MODULE_ID, MAGNET_URL)"
		exec_string += ");"
		# print(exec_string, '\n')
		self.conn.execute(exec_string)
		self.conn.commit()
		self.create_index()

	def create_index(self):
		# Since Unique Constraint is enforced, we may not really need them.
		if self.table_name in ['PLATFORMS', 'PUBLISHERS', 'PLAYLISTS', 'EPISODES', 'NAME']:
			exec_string = "CREATE INDEX IF NOT EXISTS " + self.table_name + "_NAME_INDEX  ON " + self.table_name + "(NAME, ID)"
			# print(exec_string, '\n')
			self.conn.execute(exec_string)
			self.conn.commit()

		
	def drop_table(self):
		exec_string = "DROP TABLE " + str(self.table_name) + ";"
		# print(exec_string, '\n')
		self.conn.execute(exec_string)
		self.conn.commit()
		
	def insert_into_table(self, values):
		if self.table_name == 'MODULES':
			exec_string = "INSERT INTO " + str(self.table_name) + "(ID"
		else:
			exec_string = "INSERT INTO " + str(self.table_name) + "(MODULE_ID, ID"
		for column in self.column_names:
			exec_string += ", " + str(column)
		if self.parent_table_name and self.table_name != 'LANGUAGES':
			exec_string += ", PARENT_ID"
		if self.table_name == 'MODULES':
			exec_string += ") VALUES (:1"
		else:
			exec_string += ") VALUES (:1, :2"
		for i in range(len(self.column_names)):
			if self.table_name == 'MODULES':
				exec_string += ", :" + str(i + 2)
			else:
				exec_string += ", :" + str(i + 3)
		if self.parent_table_name and self.table_name != 'LANGUAGES':
			exec_string += ", :" + str(len(self.column_names) + 3)
		exec_string += ")"
		# print(exec_string, '\n')
		self.conn.execute(exec_string, values)
		self.conn.commit()
		
	def print_table(self):
		cursor = self.conn.execute("SELECT *  from " + str(self.table_name))
		print('TABLE:', self.table_name)
		column_string = ''
		if self.table_name != 'MODULES':
			column_string += 'MODULE_ID\t'
		column_string += 'ID'
		for column in self.column_names:
			column_string += '\t' + str(column)
		if self.parent_table_name and self.table_name != 'LANGUAGES':
			column_string += '\t' + 'PARENT_ID'
		print(column_string)
		for row in cursor:
			column_string = ""
			for i in range(len(row)):
				column_string += str(row[i]) + '\t'
			print(column_string)
		self.conn.commit()

	def get_max_id(self, mid):
		max_id = 1
		try:
			cursor = self.conn.execute('SELECT MAX(ID) FROM ' + self.table_name + " WHERE MODULE_ID=" + str(mid))
			for row in cursor:
				max_id = int(row[0]) + 1
				break
		except:
			pass
		return(max_id)

	def get_id(self, name, mid=None, parent_id=None):
		rid = 'NULL'
		name = str(name).replace("'", "''")
		if self.table_name == 'MODULES':
			cursor = self.conn.execute("SELECT ID FROM " + self.table_name + " WHERE NAME=" + "'" + str(name) + "' LIMIT 1")
			for row in cursor:
				rid = row[0]
				break
		elif self.table_name == 'MAGNET_LINKS':
			cursor = self.conn.execute("SELECT ID  from " + str(self.table_name) +" WHERE MODULE_ID=" + str(mid) + " AND MAGNET_URL=" + "'" + str(name) + "' LIMIT 1" )
			for row in cursor:
				rid = int(row[0])
				break
		else:
			exec_string = "SELECT ID FROM " + self.table_name
			exec_string += " WHERE MODULE_ID=" + str(mid)
			if self.table_name != 'LANGUAGES':
				exec_string += " AND PARENT_ID=" + str(parent_id)
			exec_string += " AND NAME=" + "'" + str(name) + "' LIMIT 1"
			cursor = self.conn.execute(exec_string)
			for row in cursor:
				rid = row[0]
				break
		self.conn.commit()
		return(rid)

	def get_other_fields(self, rid):
		if self.table_name in ['PLATFORMS', 'PUBLISHERS', 'PLAYLISTS', 'EPISODES']:
			image_url = 'NULL'
			cursor = self.conn.execute('SELECT IMAGE_URL FROM ' + self.table_name + " WHERE ID=" + str(rid))
			for row in cursor:
				image_url = str(row[0])
				break
			return(image_url)
		elif self.table_name == 'SOURCES':
			magnet_link_id = None
			file_num = 0
			cursor = self.conn.execute('SELECT MAGNET_LINK_ID, FILE_NUM FROM ' + self.table_name + " WHERE ID=" + str(rid))
			for row in cursor:
				magnet_link_id = int(row[0])
				file_num = int(row[1])
				break
			return(magnet_link_id, file_num)
		return(None)

	def get_name(self, rid):
		if self.table_name != 'MAGNET_LINKS':
			name = 'NULL'
			cursor = self.conn.execute('SELECT NAME FROM ' + self.table_name + " WHERE ID=" + str(rid))
			for row in cursor:
				name = str(row[0])
				break
			return(name)

	def replace_with_attached_database(self, attached_database_name):
		self.conn.execute('REPLACE INTO ' + self.table_name + ' SELECT * FROM ' + attached_database_name + '.' + self.table_name)
		self.conn.commit()
		
class Modules(Table):
	def __init__(self, conn, drop_tables):
		super().__init__(conn)
		self.table_name = 'MODULES'
		self.column_names = ['NAME']
		try:
			if drop_tables:
				self.drop_table()
		except:
			pass
		self.create_table()
	def insert(self, name):
		rid = self.get_random_id()
		name = str(name)
		values = [rid, name]
		self.insert_into_table(values)
		cursor = self.conn.execute('SELECT ID FROM ' + self.table_name + " WHERE NAME='" + str(name) + "' LIMIT 1")
		for row in cursor:
			return row[0]
	def get_random_id(self):
		rid = None
		check = True
		while check:
			cursor = self.conn.execute('SELECT RANDOM()')
			for row in cursor:
				rid = row[0]
				break
			check = False
			cursor = self.conn.execute('SELECT ID FROM ' + self.table_name + " WHERE ID=" + str(rid))
			for row in cursor:
				check = True
				break
		return(rid)
		
class Languages(Table):
	def __init__(self, conn, drop_tables):
		super().__init__(conn)
		self.table_name = 'LANGUAGES'
		self.column_names = ['NAME']
		self.parent_table_name = 'MODULES'
		try:
			if drop_tables:
				self.drop_table()
		except:
			pass
		self.create_table()
	def insert(self, mid, rid, name):
		mid = int(mid)
		rid = int(rid)
		name = str(name)
		values = [mid, rid, name]
		self.insert_into_table(values)

class Platforms(Table):
	def __init__(self, conn, drop_tables):
		super().__init__(conn)
		self.table_name = 'PLATFORMS'
		self.column_names = ['IMAGE_URL', 'NAME']
		self.parent_table_name = 'LANGUAGES'
		try:
			if drop_tables:
				self.drop_table()
		except:
			pass
		self.create_table()
	def insert(self, mid, rid, image_url, name, parent_id):
		mid = int(mid)
		rid = int(rid)
		image_url = str(image_url)
		name = str(name)
		parent_id = int(parent_id)
		values = [mid, rid, image_url, name, parent_id]
		self.insert_into_table(values)

class Publishers(Table):
	def __init__(self, conn, drop_tables):
		super().__init__(conn)
		self.table_name = 'PUBLISHERS'
		self.column_names = ['IMAGE_URL', 'NAME']
		self.parent_table_name = 'PLATFORMS'
		try:
			if drop_tables:
				self.drop_table()
		except:
			pass
		self.create_table()
	def insert(self, mid, rid, image_url, name, parent_id):
		mid = int(mid)
		rid = int(rid)
		image_url = str(image_url)
		name = str(name)
		parent_id = int(parent_id)
		values = [mid, rid, image_url, name, parent_id]
		self.insert_into_table(values)

class Playlists(Table):
	def __init__(self, conn, drop_tables):
		super().__init__(conn)
		self.table_name = 'PLAYLISTS'
		self.column_names = ['IMAGE_URL', 'NAME']
		self.parent_table_name = 'PUBLISHERS'
		try:
			if drop_tables:
				self.drop_table()
		except:
			pass
		self.create_table()
	def insert(self, mid, rid, image_url, name, parent_id):
		mid = int(mid)
		rid = int(rid)
		image_url = str(image_url)
		name = str(name)
		parent_id = int(parent_id)
		values = [mid, rid, image_url, name, parent_id]
		self.insert_into_table(values)

class Episodes(Table):
	def __init__(self, conn, drop_tables):
		super().__init__(conn)
		self.table_name = 'EPISODES'
		self.column_names = ['IMAGE_URL', 'NAME']
		self.parent_table_name = 'PLAYLISTS'
		try:
			if drop_tables:
				self.drop_table()
		except:
			pass
		self.create_table()
	def insert(self, mid, rid, image_url, name, parent_id):
		mid = int(mid)
		rid = int(rid)
		image_url = str(image_url)
		name = str(name)
		parent_id = int(parent_id)
		values = [mid, rid, image_url, name, parent_id]
		self.insert_into_table(values)
		
class Sources(Table):
	def __init__(self, conn, drop_tables):
		super().__init__(conn)
		self.table_name = 'SOURCES'
		self.column_names = ['MAGNET_LINK_ID', 'FILE_NUM', 'NAME']
		self.parent_table_name = 'EPISODES'
		try:
			if drop_tables:
				self.drop_table()
		except:
			pass
		self.create_table()
	def insert(self, mid, rid, magnet_link_id, file_num, name, parent_id):
		mid = int(mid)
		rid = int(rid)
		magnet_link_id = int(magnet_link_id)
		file_num = int(file_num)
		name = str(name)
		parent_id = int(parent_id)
		values = [mid, rid, magnet_link_id, file_num, name, parent_id]
		self.insert_into_table(values)
		
class MagnetLinks(Table):
	def __init__(self, conn, drop_tables):
		super().__init__(conn)
		self.table_name = 'MAGNET_LINKS'
		self.column_names = ['MAGNET_URL']
		try:
			if drop_tables:
				self.drop_table()
		except:
			pass
		self.create_table()
	def insert(self, mid, rid, url):
		mid = int(mid)
		rid = int(rid)
		url = str(url)
		values = [mid, rid, url]
		self.insert_into_table(values)
		
