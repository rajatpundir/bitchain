import sqlite3, table

class StrongModel:
	def __init__(self, database_name='strong.db', drop_tables=False):
		self.conn = sqlite3.connect(database_name, isolation_level='Exclusive')
		self.conn.execute("PRAGMA synchronous = 0;")
		self.conn.execute("PRAGMA journal_mode = OFF;")
		self.conn.execute("PRAGMA foreign_keys = ON;")
		self.modules = table.Modules(self.conn, drop_tables)
		self.languages = table.Languages(self.conn, drop_tables)
		self.platforms = table.Platforms(self.conn, drop_tables)
		self.publishers = table.Publishers(self.conn, drop_tables)
		self.playlists = table.Playlists(self.conn, drop_tables)
		self.episodes = table.Episodes(self.conn, drop_tables)
		self.magnet_links = table.MagnetLinks(self.conn, drop_tables)
		self.sources = table.Sources(self.conn, drop_tables)
	def compact_database(self):
		self.conn.execute("VACUUM")
		self.conn.commit()
	def attach_database(self, database_filename, attached_database_name='CURRENT_DIFF'):
		self.conn.execute("ATTACH '" + str(database_filename) + "' AS " + attached_database_name)
		self.conn.commit()
	def detach_database(self, attached_database_name='CURRENT_DIFF'):
		self.conn.execute("DETACH DATABASE " + attached_database_name)
		self.conn.commit()
	def replace_with_attached_database(self, attached_database_name):
		self.modules.replace_with_attached_database(attached_database_name)
		self.languages.replace_with_attached_database(attached_database_name)
		self.platforms.replace_with_attached_database(attached_database_name)
		self.publishers.replace_with_attached_database(attached_database_name)
		self.playlists.replace_with_attached_database(attached_database_name)
		self.episodes.replace_with_attached_database(attached_database_name)
		self.magnet_links.replace_with_attached_database(attached_database_name)
		self.sources.replace_with_attached_database(attached_database_name)
	def attach_replace_detach(self, database_filename, attached_database_name='CURRENT_DIFF'):
		self.attach_database(database_filename, attached_database_name)
		self.replace_with_attached_database(attached_database_name)
		self.detach_database(attached_database_name)
		self.compact_database()
