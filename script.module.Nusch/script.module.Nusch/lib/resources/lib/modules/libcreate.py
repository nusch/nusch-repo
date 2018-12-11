import os
import json
import urllib
import glob
import time
import xbmc
import xml.etree.ElementTree as ET
try: from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database


from resources.lib.modules import libtools
from commoncore import kodi
from resources.lib.modules import control

def lib_setup():
		try:
			libtools.lib_tools.create_folder(os.path.join(control.transPath(control.setting('library.movie')), ''))
			libtools.lib_tools.create_folder(os.path.join(control.transPath(control.setting('library.tv')), ''))
		except:
			pass
		movielibraryfolder = kodi.get_setting(os.path.join(control.transPath(control.setting('library.movie')), ''))+"/"
		kodi.log(movielibraryfolder)
		try:
			setup_movie_library(movielibraryfolder)
		except: pass
		tvlibraryfolder = kodi.get_setting(os.path.join(control.transPath(control.setting('library.tv')), ''))+"/"
		try:
			setup_tv_show_library(tvlibraryfolder)
		except: pass
		xbmc.executebuiltin('CleanLibrary(video)')
		xbmc.executebuiltin('UpdateLibrary(video)')
	
def setup_movie_library(library_folder):
	LANG=xbmc.getLanguage(xbmc.ISO_639_1,)
	library_folder = kodi.get_setting('library.movie')+"/"
	kodi.log(xbmc.getLanguage(xbmc.ISO_639_1,))
        # auto configure folder
    #msg = _("Would you like to automatically set [COLOR yellow]Nusch[/COLOR] as a movies video source?")
	kodi.log("Ask Movie...")
	yes = control.yesnoDialog("Add Nusch Movies to your library?", '', '')
	if yes:
	#if dialogs.yesno(_("Library setup"), "Would you like to automatically set [COLOR yellow]Nusch[/COLOR] as a Movie source?"):
		try:
			source_thumbnail = 'special://home/addons/plugin.video.Nusch/icon.png' #get_icon_path("movies")
			kodi.log(source_thumbnail)
			source_name = "Nusch Movies"
			kodi.log(source_name)
			source_content = "('{0}','movies','metadata.themoviedb.org',NULL,2147483647,1,'<settings><setting id=\"RatingS\" value=\"TMDb\" /><setting id=\"certprefix\" value=\"Rated \" /><setting id=\"fanart\" value=\"true\" /><setting id=\"imdbanyway\" value=\"false\" /><setting id=\"keeporiginaltitle\" value=\"false\" /><setting id=\"language\" value=\"en\" /><setting id=\"tmdbcertcountry\" value=\"us\" /><setting id=\"trailer\" value=\"true\" /></settings>',0,0,NULL,NULL)".format(library_folder, LANG)
			add_source(source_name, library_folder, source_content, source_thumbnail)
			return True
		except: pass
		xbmc.executebuiltin('UpdateLibrary(video,'+library_folder+')')
	# return translated path
	return xbmc.translatePath(library_folder)

def setup_tv_show_library(library_folder):
	LANG=xbmc.getLanguage(xbmc.ISO_639_1,)
	library_folder = kodi.get_setting('library.tv')+"/"
        # auto configure folder
    #msg = _("Would you like to automatically set [COLOR yellow]Nusch[/COLOR] as a tv shows source?")
	kodi.log("Ask TV Show...")
	yes = control.yesnoDialog("Add Nusch TV Shows to your library?", '', '')
	if yes:
	#if dialogs.yesno(_("Library setup"), "Would you like to automatically set [COLOR yellow]Nusch[/COLOR] as a TV Show source?"):
		try:
			source_thumbnail = 'special://home/addons/plugin.video.Nusch/icon.png'
			source_name = "Nusch TV shows"
			source_content = "('{0}','tvshows','metadata.tvdb.com',NULL,0,0,'<settings><setting id=\"RatingS\" value=\"TheTVDB\" /><setting id=\"absolutenumber\" value=\"false\" /><setting id=\"alsoimdb\" value=\"false\" /><setting id=\"dvdorder\" value=\"false\" /><setting id=\"fallback\" value=\"true\" /><setting id=\"fallbacklanguage\" value=\"en\" /><setting id=\"fanart\" value=\"true\" /><setting id=\"language\" value=\"en\" /><setting id=\"usefallbacklanguage1\" value=\"true\" /></settings>',0,0,NULL,NULL)".format(library_folder, LANG)
			add_source(source_name, library_folder, source_content, source_thumbnail)
			return True
		except: pass
		xbmc.executebuiltin('UpdateLibrary(video,'+library_folder+')')
    # return translated path
	return xbmc.translatePath(library_folder)

def add_source(source_name, source_path, source_content, source_thumbnail):
	kodi.log(source_name)
	kodi.log(source_path)
	kodi.log(source_content)
	kodi.log(source_thumbnail)
	kodi.log("Add Source...")
	xml_file = xbmc.translatePath('special://profile/sources.xml')
	if not os.path.exists(xml_file):
		with open(xml_file, "w") as f:
			f.write("""<sources>
    <programs>
        <default pathversion="1" />
    </programs>
    <video>
        <default pathversion="1" />
    </video>
    <music>
        <default pathversion="1" />
    </music>
    <pictures>
        <default pathversion="1" />
    </pictures>
    <files>
        <default pathversion="1" />
    </files>
</sources>""")
	existing_source = _get_source_attr(xml_file, source_name, "path")
	if existing_source and existing_source != source_path:
		_remove_source_content(existing_source)
	if _add_source_xml(xml_file, source_name, source_path, source_thumbnail):
		kodi.log("source content")
		_set_source_content(source_content)
	_set_source_content(source_content)
#########   XML functions   #########

def _add_source_xml(xml_file, name, path, thumbnail):
	kodi.log("Add Source XML...")
	tree = ET.parse(xml_file)
	root = tree.getroot()
	sources = root.find('video')
	existing_source = None
	for source in sources.findall('source'):
		xml_name = source.find("name").text
		xml_path = source.find("path").text
		if source.find("thumbnail"): xml_thumbnail = source.find("thumbnail").text
		else: xml_thumbnail = ""
		if xml_name == name or xml_path == path:
			existing_source = source
			break
	if existing_source is not None:
		xml_name = source.find("name").text
		xml_path = source.find("path").text
		if source.find("thumbnail"): xml_thumbnail = source.find("thumbnail").text
		else: xml_thumbnail = ""
		if xml_name == name and xml_path == path and xml_thumbnail == thumbnail:
			return False
		elif xml_name == name:
			source.find("path").text = path
			source.find("thumbnail").text = thumbnail
		elif xml_path == path:
			source.find("name").text = name
			source.find("thumbnail").text = thumbnail
		else:
			source.find("path").text = path
			source.find("name").text = name
	else:
		new_source = ET.SubElement(sources, 'source')
		new_name = ET.SubElement(new_source, 'name')
		new_name.text = name
		new_path = ET.SubElement(new_source, 'path')
		new_thumbnail = ET.SubElement(new_source, 'thumbnail')
		new_allowsharing = ET.SubElement(new_source, 'allowsharing')
		new_path.attrib['pathversion'] = "1"
		new_thumbnail.attrib['pathversion'] = "1"
		new_path.text = path
		new_thumbnail.text = thumbnail
		new_allowsharing.text = "true"
	_indent_xml(root)
	tree.write(xml_file)
	return True

def _indent_xml(elem, level=0):
	i = "\n" + level*"  "
	if len(elem):
		if not elem.text or not elem.text.strip():
			elem.text = i + "  "
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
		for elem in elem:
			_indent_xml(elem, level+1)
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
	else:
		if level and (not elem.tail or not elem.tail.strip()):
			elem.tail = i

def _get_source_attr(xml_file, name, attr):
	tree = ET.parse(xml_file)
	root = tree.getroot()
	sources = root.find('video')
	for source in sources.findall('source'):
		xml_name = source.find("name").text
		if xml_name == name:
			return source.find(attr).text
	return None

#########   Database functions  #########

def _db_execute(db_name, command):
	databaseFile = _get_database(db_name)
	kodi.log("databaseFile")
	kodi.log(databaseFile)
	if not databaseFile:
		return False
	dbcon = database.connect(databaseFile)
	dbcur = dbcon.cursor()
	#dbcur.execute(command)
	try:
		dbcur.execute(command)
	except database.Error as e:
		kodi.log("MySQL Error :", e.args[0], q.decode("utf-8"))
		return False
	dbcon.commit()
	return True

def _get_database(db_name):
	path_db = "special://profile/Database/" + db_name
	filelist = glob.glob(xbmc.translatePath(path_db))
	kodi.log(filelist)
	if filelist:
		return filelist[-1]
	return None

def _remove_source_content(path):
	q = "DELETE FROM path WHERE strPath LIKE '%{0}%'".format(path)
	return _db_execute("MyVideos*.db", q)

def _set_source_content(content):    
	q = "INSERT OR REPLACE INTO path (strPath,strContent,strScraper,strHash,scanRecursive,useFolderNames,strSettings,noUpdate,exclude,dateAdded,idParentPath) VALUES "
	q += content
	kodi.log(q)
	return _db_execute("MyVideos*.db", q)