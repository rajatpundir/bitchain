import os, shutil
from strong_model import StrongModel

def reset_and_rebuild_database(database_name='0.db', reset_database_directory=True):
	if reset_database_directory:
		if os.path.exists('database'):
			shutil.rmtree('database')
	try:
		os.mkdir('database')
	except:
		pass
	model = StrongModel('database/' + database_name, True)
	if not os.path.exists('root'):
		os.mkdir('root')
	os.chdir('root')
	try:
		for module_name in sorted(os.listdir('.')):
			if module_name.endswith('.txt'):
				continue
			try:
				module_id = model.modules.insert(module_name)
				language_id = model.languages.get_max_id(module_id)
				platform_id = model.platforms.get_max_id(module_id)
				publisher_id = model.publishers.get_max_id(module_id)
				playlist_id = model.playlists.get_max_id(module_id)
				episode_id = model.episodes.get_max_id(module_id)
				source_id = model.sources.get_max_id(module_id)
				magnet_link_counter = model.magnet_links.get_max_id(module_id)
				os.chdir(module_name)
				for language_name in sorted(os.listdir('.')):
					if language_name.endswith('.txt'):
						continue
					try:
						model.languages.insert(module_id, language_id, language_name)
						os.chdir(language_name)
						f = open('id.txt', 'w')
						f.write(str(language_id) + '\n')
						f.close()
						for platform_name in sorted(os.listdir('.')):
							if platform_name.endswith('.txt'):
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
								model.platforms.insert(module_id, platform_id, image_url, platform_name, language_id)
								os.chdir(platform_name)
								f = open('id.txt', 'w')
								f.write(str(platform_id) + '\n')
								f.close()
								for publisher_name in sorted(os.listdir('.')):
									if publisher_name.endswith('.txt'):
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
										model.publishers.insert(module_id, publisher_id, image_url, publisher_name, platform_id)
										os.chdir(publisher_name)
										f = open('id.txt', 'w')
										f.write(str(publisher_id) + '\n')
										f.close()
										for playlist_name in sorted(os.listdir('.')):
											if playlist_name.endswith('.txt'):
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
												model.playlists.insert(module_id, playlist_id, image_url, playlist_name, publisher_id)
												os.chdir(playlist_name)
												f = open('id.txt', 'w')
												f.write(str(playlist_id) + '\n')
												f.close()
												for episode_name in sorted(os.listdir('.')):
													if episode_name.endswith('.txt') or episode_name == 'Batch':
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
														model.episodes.insert(module_id, episode_id, image_url, episode_name, playlist_id)
														os.chdir(episode_name)
														f = open('id.txt', 'w')
														f.write(str(episode_id) + '\n')
														f.close()
														for source_name in sorted(os.listdir('.')):
															if source_name.endswith('.txt'):
																continue
															try:
																os.chdir(source_name)
																f = open('id.txt', 'w')
																f.write(str(source_id) + '\n')
																f.close()
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
																magnet_link_id = magnet_link_counter
																try:
																	model.magnet_links.insert(module_id, magnet_link_counter, magnet_link)
																	magnet_link_counter += 1
																except:
																	magnet_link_id = model.magnet_links.get_id(magnet_link, module_id)                                                            
																model.sources.insert(module_id, source_id, magnet_link_id, file_num, source_name, episode_id)
																f = open('ignore.txt', 'w')
																f.close()
																os.chdir('..')
																source_id += 1
															except Exception as e:
																print(e)
																print('source', module_name, language_name, platform_name, publisher_name, playlist_name, episode_name, source_name)
														os.chdir('..')
														episode_id += 1
													except Exception as e:
														print(e)
														print('episode', module_name, language_name, platform_name, publisher_name, playlist_name, episode_name)
												os.chdir('..')
												playlist_id += 1
											except Exception as e:
												print(e)
												print('playlist', module_name, language_name, platform_name, publisher_name, playlist_name)
										os.chdir('..')
										publisher_id += 1
									except Exception as e:
										print(e)
										print('publisher', module_name, language_name, platform_name, publisher_name)
								os.chdir('..')
								platform_id += 1
							except Exception as e:
								print(e)
								print('platform', module_name, language_name, platform_name)
						os.chdir('..')
						language_id += 1
					except Exception as e:
						print(e)
						print('language', module_name, language_name)
				os.chdir('..')
			except Exception as e:
				print(e)
				print('module', module_name)
	finally:
		os.chdir('..')
		model.conn.commit()
		model.compact_database()
		print('RESET : SUCCESS')
		
if __name__ == "__main__":
	reset_and_rebuild_database()
