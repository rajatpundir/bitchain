import sqlite3, table

class WeakModel:
	def __init__(self, database_name='weak.db', drop_tables=False):
		self.conn = sqlite3.connect(database_name, isolation_level='Exclusive')
		self.conn.execute("PRAGMA synchronous = 0;")
		self.conn.execute("PRAGMA journal_mode = OFF;")
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
