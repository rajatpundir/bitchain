import os, shutil
from strong_model import StrongModel
from weak_model import WeakModel
from reset import reset_and_rebuild_database
from latest import build_superimposed_database
import time

def build_diff_database(diff_databse='diff.db', latest_databse='0.db'):
	if not os.path.exists('database'):
		os.mkdir('database')
	if not os.path.exists('database/0.db'):
		reset_and_rebuild_database()
		return(None)
	build_superimposed_database()
	latest_model = StrongModel('database/latest.db', False)
	os.chdir('database')
	db_nums = []
	for database in sorted(os.listdir()):
	    try:
	        db_nums.append(int(database.split('.')[0]))
	    except:
	        pass
	os.chdir('..')
	diff_databse_name = str(sorted(db_nums)[-1] + 1) + '.db'
	diff_model = WeakModel('database/' + diff_databse_name, True)
	if not os.path.exists('root'):
		os.mkdir('root')
	os.chdir('root')
	start_time = time.time()
	try:
		for module_name in sorted(os.listdir('.')):
			if module_name.endswith('.txt'):
				continue
			if os.path.exists(module_name + '/ignore.txt'):
				continue
			try:
				module_id = latest_model.modules.get_id(module_name)
				if module_id == 'NULL':
					module_id = diff_model.modules.insert(module_name)
				os.chdir(module_name)
				for language_name in sorted(os.listdir('.')):
					if language_name.endswith('.txt'):
						continue
					if os.path.exists(language_name + '/ignore.txt'):
						continue
					try:
						language_id = None
						if os.path.exists(language_name + '/id.txt'):
							try:
								f = open(language_name + '/id.txt', 'r')
								language_id = int(f.readline())
								f.close()
							except Exception as e:
								print(e)
						if language_id == None:
							language_id = latest_model.languages.get_id(language_name, module_id)
						if language_id == 'NULL':
							language_id = max(latest_model.languages.get_max_id(module_id), diff_model.languages.get_max_id(module_id))
							diff_model.languages.insert(module_id, language_id, language_name)
							os.chdir(language_name)
							f = open('id.txt', 'w')
							f.write(str(language_id) + '\n')
							f.close()
							os.chdir('..')
						else:
							if language_name != latest_model.languages.get_name(language_id):
								diff_model.languages.insert(module_id, language_id, language_name)
						os.chdir(language_name)
						for platform_name in sorted(os.listdir('.')):
							if platform_name.endswith('.txt'):
								continue
							if os.path.exists(platform_name + '/ignore.txt'):
								continue
							try:
								image_url = 'NULL'
								os.chdir(platform_name)
								try:
									f = open('image.txt', 'r')
									image_url = str(f.readline())
									f.close()
								except:
									pass
								os.chdir('..')
								platform_id = None
								if os.path.exists(platform_name + '/id.txt'):
									try:
										f = open(platform_name + '/id.txt', 'r')
										platform_id = int(f.readline())
										f.close()
									except Exception as e:
										print(e)
								if platform_id == None:
									platform_id = latest_model.platforms.get_id(platform_name, module_id, language_id)
								if platform_id == 'NULL':
									platform_id = max(latest_model.platforms.get_max_id(module_id), diff_model.platforms.get_max_id(module_id))
									diff_model.platforms.insert(module_id, platform_id, image_url, platform_name, language_id)
									os.chdir(platform_name)
									f = open('id.txt', 'w')
									f.write(str(platform_id) + '\n')
									f.close()
									os.chdir('..')
								else:
									# Image_URL and Name could be fetched in single query.
									if image_url != latest_model.platforms.get_other_fields(platform_id):
										diff_model.platforms.insert(module_id, platform_id, image_url, platform_name, language_id)
									elif platform_name != latest_model.platforms.get_name(platform_id):
										diff_model.platforms.insert(module_id, platform_id, image_url, platform_name, language_id)
								os.chdir(platform_name)
								for publisher_name in sorted(os.listdir('.')):
									if publisher_name.endswith('.txt'):
										continue
									if os.path.exists(publisher_name + '/ignore.txt'):
										continue
									try:
										image_url = 'NULL'
										os.chdir(publisher_name)
										try:
											f = open('image.txt', 'r')
											image_url = str(f.readline())
											f.close()
										except:
											pass
										os.chdir('..')
										publisher_id = None
										if os.path.exists(publisher_name + '/id.txt'):
											try:
												f = open(publisher_name + '/id.txt', 'r')
												publisher_id = int(f.readline())
												f.close()
											except Exception as e:
												print(e)
										if publisher_id == None:
											publisher_id = latest_model.publishers.get_id(publisher_name, module_id, platform_id)
										if publisher_id == 'NULL':
											publisher_id = max(latest_model.publishers.get_max_id(module_id), diff_model.publishers.get_max_id(module_id))
											diff_model.publishers.insert(module_id, publisher_id, image_url, publisher_name, platform_id)
											os.chdir(publisher_name)
											f = open('id.txt', 'w')
											f.write(str(publisher_id) + '\n')
											f.close()
											os.chdir('..')
										else:
											if image_url != latest_model.publishers.get_other_fields(publisher_id):
												diff_model.publishers.insert(module_id, publisher_id, image_url, publisher_name, platform_id)
											elif publisher_name != latest_model.publishers.get_name(publisher_id):
												diff_model.publishers.insert(module_id, publisher_id, image_url, publisher_name, platform_id)
										os.chdir(publisher_name)
										for playlist_name in sorted(os.listdir('.')):
											if playlist_name.endswith('.txt'):
												continue
											if os.path.exists(playlist_name + '/ignore.txt'):
												continue
											try:
												image_url = 'NULL'
												os.chdir(playlist_name)
												try:
													f = open('image.txt', 'r')
													image_url = str(f.readline())
													f.close()
												except:
													pass
												os.chdir('..')
												playlist_id = None
												if os.path.exists(playlist_name + '/id.txt'):
													try:
														f = open(playlist_name + '/id.txt', 'r')
														playlist_id = int(f.readline())
														f.close()
													except Exception as e:
														print(e)
												if playlist_id == None:
													playlist_id = latest_model.playlists.get_id(playlist_name, module_id, publisher_id)
												if playlist_id == 'NULL':
													playlist_id = max(latest_model.playlists.get_max_id(module_id), diff_model.playlists.get_max_id(module_id))
													diff_model.playlists.insert(module_id, playlist_id, image_url, playlist_name, publisher_id)
													os.chdir(playlist_name)
													f = open('id.txt', 'w')
													f.write(str(playlist_id) + '\n')
													f.close()
													os.chdir('..')
												else:
													if image_url != latest_model.playlists.get_other_fields(playlist_id):
														diff_model.playlists.insert(module_id, playlist_id, image_url, playlist_name, publisher_id)
													elif playlist_name != latest_model.playlists.get_name(playlist_id):
														diff_model.playlists.insert(module_id, playlist_id, image_url, playlist_name, publisher_id)
												os.chdir(playlist_name)
												print(playlist_name)
												for episode_name in sorted(os.listdir('.')):
													if episode_name.endswith('.txt') or episode_name == 'Batch':
														continue
													if os.path.exists(episode_name + '/ignore.txt'):
														continue
													try:
														image_url = 'NULL'
														os.chdir(episode_name)
														try:
															f = open('image.txt', 'r')
															image_url = str(f.readline())
															f.close()
														except:
															pass
														os.chdir('..')
														episode_id = None
														if os.path.exists(episode_name + '/id.txt'):
															try:
																f = open(episode_name + '/id.txt', 'r')
																episode_id = int(f.readline())
																f.close()
															except Exception as e:
																print(e)
														if episode_id == None:
															episode_id = latest_model.episodes.get_id(episode_name, module_id, playlist_id)
														if episode_id == 'NULL':
															episode_id = max(latest_model.episodes.get_max_id(module_id), diff_model.episodes.get_max_id(module_id))
															diff_model.episodes.insert(module_id, episode_id, image_url, episode_name, playlist_id)
															os.chdir(episode_name)
															f = open('id.txt', 'w')
															f.write(str(episode_id) + '\n')
															f.close()
															os.chdir('..')
														else:
															if image_url != latest_model.episodes.get_other_fields(episode_id):
																diff_model.episodes.insert(module_id, episode_id, image_url, episode_name, playlist_id)
															elif episode_name != latest_model.episodes.get_name(episode_id):
																diff_model.episodes.insert(module_id, episode_id, image_url, episode_name, playlist_id)
														os.chdir(episode_name)
														for source_name in sorted(os.listdir('.')):
															if source_name.endswith('.txt'):
																continue
															if os.path.exists(source_name + '/ignore.txt'):
																continue
															try:
																os.chdir(source_name)
																magnet_link = 'NULL'
																file_num = 0
																f = open('magnet.txt', 'r')
																link = f.readline().strip()
																if link.startswith('magnet'):
																	magnet_link = link
																try:
																	file_num = int(f.readline().strip())
																except:
																	pass
																f.close()
																magnet_link_id = latest_model.magnet_links.get_id(magnet_link, module_id)
																if magnet_link_id == 'NULL':
																	try:
																		magnet_link_id = max(latest_model.magnet_links.get_max_id(module_id), diff_model.magnet_links.get_max_id(module_id))
																		diff_model.magnet_links.insert(module_id, magnet_link_id, magnet_link)
																	except:
																		magnet_link_id = diff_model.magnet_links.get_id(magnet_link, module_id)
																source_id = None
																if os.path.exists(source_name + '/id.txt'):
																	try:
																		f = open(source_name + '/id.txt', 'r')
																		source_id = int(f.readline())
																		f.close()
																	except Exception as e:
																		print(e)
																if source_id == None:
																	source_id = latest_model.sources.get_id(source_name, module_id, episode_id)
																if source_id == 'NULL':
																	source_id = max(latest_model.sources.get_max_id(module_id), diff_model.sources.get_max_id(module_id))
																	diff_model.sources.insert(module_id, source_id, magnet_link_id, file_num, source_name, episode_id)
																	f = open('id.txt', 'w')
																	f.write(str(source_id) + '\n')
																	f.close()
																else:
																	if (magnet_link_id, file_num) != latest_model.sources.get_other_fields(source_id):
																		diff_model.sources.insert(module_id, source_id, magnet_link_id, file_num, source_name, episode_id)
																	elif source_name != latest_model.sources.get_name(source_id):
																		diff_model.sources.insert(module_id, source_id, magnet_link_id, file_num, source_name, episode_id)
																os.chdir('..')
															except Exception as e:
																print(e)
																print('source', module_name, language_name, platform_name, publisher_name, playlist_name, episode_name, source_name)
														os.chdir('..')
													except Exception as e:
														print(e)
														print('episode', module_name, language_name, platform_name, publisher_name, playlist_name, episode_name)
												os.chdir('..')
											except Exception as e:
												print(e)
												print('playlist', module_name, language_name, platform_name, publisher_name, playlist_name)
										os.chdir('..')
									except Exception as e:
										print(e)
										print('publisher', module_name, language_name, platform_name, publisher_name)
								os.chdir('..')
							except Exception as e:
								print(e)
								print('platform', module_name, language_name, platform_name)
						os.chdir('..')
					except Exception as e:
						print(e)
						print('language', module_name, language_name)
				os.chdir('..')
			except Exception as e:
				print(e)
				print('module', module_name)
		print('TIME :', time.time() - start_time)
	finally:
		os.chdir('..')
		diff_model.compact_database()
		print('DIFF : SUCCESS')
		
if __name__ == "__main__":
	build_diff_database()
