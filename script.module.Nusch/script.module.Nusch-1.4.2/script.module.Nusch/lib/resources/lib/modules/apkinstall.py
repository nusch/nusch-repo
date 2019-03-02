import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, HTMLParser, glob, json, time
import shutil
import urllib2,urllib
from resources.lib.modules import apkdownloader


DP             = xbmcgui.DialogProgress()
ADDON_ID       = xbmcaddon.Addon().getAddonInfo('id')
HOME           = xbmc.translatePath('special://home/')
ADDONS         = os.path.join(HOME,      'addons')
PLUGIN         = os.path.join(ADDONS,    ADDON_ID)
PACKAGES       = xbmc.translatePath(os.path.join('/storage/emulated/0/Download',''))
ICON           = os.path.join(PLUGIN,    'icon.png')
ADDONTITLE     = 'Nusch'
DIALOG         = xbmcgui.Dialog()
COLOR1         = 'blue'
COLOR2         = 'yellow'
COLOR3         = 'red'
COLOR4         = 'snow'
COLOR5         = 'lime'

def platform():
	if xbmc.getCondVisibility('system.platform.android'):             return 'android'
	elif xbmc.getCondVisibility('system.platform.linux'):             return 'linux'
	elif xbmc.getCondVisibility('system.platform.linux.Raspberrypi'): return 'linux'
	elif xbmc.getCondVisibility('system.platform.windows'):           return 'windows'
	elif xbmc.getCondVisibility('system.platform.osx'):               return 'osx'
	elif xbmc.getCondVisibility('system.platform.atv2'):              return 'atv2'
	elif xbmc.getCondVisibility('system.platform.ios'):               return 'ios'
	elif xbmc.getCondVisibility('system.platform.darwin'):            return 'ios'

def LogNotify(title, message, times=2000, icon=ICON,sound=False):
	DIALOG.notification(title, message, icon, int(times), sound)

def workingURL(url):
	if url in ['http://', 'https://', '']: return False
	check = 0; status = ''
	while check < 3:
		check += 1
		try:
			req = urllib2.Request(url)
			req.add_header('User-Agent', USER_AGENT)
			response = urllib2.urlopen(req)
			response.close()
			status = True
			break
		except Exception, e:
			status = str(e)
			LogNotify(ADDONTITLE, "Working Url Error: %s [%s]" % (e, url))
			xbmc.sleep(500)
	return status

	
def apkInstaller():
	apk = "Mobdro"
	url = "https://www.mobdro.sc/mobdro.apk"
	path = "androidapp://sources/apps/com.mobdro.android.png"
	if platform() == 'android':
		success = xbmcvfs.exists(path)
		if success == 1
			xbmc.executebuiltin('XBMC.StartAndroidActivity("com.mobdro.android")')
		else:
			yes = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to download and install:" % COLOR2, "[COLOR %s]%s[/COLOR]" % (COLOR1, apk), yeslabel="[B][COLOR green]Download[/COLOR][/B]", nolabel="[B][COLOR red]Cancel[/COLOR][/B]")
			if not yes: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]ERROR: Install Cancelled[/COLOR]' % COLOR2); return
			display = apk
			if yes:
				if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
				#if not workingURL(url) == True: LogNotify(ADDONTITLE, 'APK Installer: [COLOR red]Invalid Apk Url![/COLOR]'); return
				DP.create(ADDONTITLE,'Downloading %s' % display,'', 'Please Wait')
				lib=os.path.join(PACKAGES, "%s.apk" % apk.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', ''))
				try: os.remove(lib)
				except: pass
				apkdownloader.download(url, lib, DP)
				xbmc.sleep(500)
				DP.close()
				DIALOG.ok(ADDONTITLE, "Launching the APK to be installed", "Follow the install process to complete", "If install fails to start please install manually from your Downloads folder")
				command = 'pm install -rgd' + lib
				launch_command(command)
				#xbmc.executebuiltin('StartAndroidActivity("","android.intent.action.VIEW","application/vnd.android.package-archive","file:'+lib+'")')
			else: LogNotify(ADDONTITLE, '[COLOR red]ERROR:[/COLOR] Install Cancelled')
	else: LogNotify(ADDONTITLE, '[COLOR red]ERROR:[/COLOR] None Android Device')

def launch_command(command_launch):
    try:
        xbmc.log('[%s] %s' % ('LAUNCHING SUBPROCESS:', command_launch), 2)
        external_command = subprocess.call(command_launch, shell = True, executable = '/system/bin/sh')
    except Exception, e:
        try:
            xbmc.log('[%s] %s' % ('ERROR LAUNCHING COMMAND !!!', e.message, external_command), 2)
            xbmc.log('[%s] %s' % ('LAUNCHING OS:', command_launch), 2)
            external_command = os.system(command_launch)
        except:
            xbmc.log('[%s]' % ('ERROR LAUNCHING COMMAND !!!', external_command), 2)