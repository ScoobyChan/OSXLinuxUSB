#!/usr/bin/env python3
# Debian
# Arch Tested 

import os
os.system('sudo pip3 install wget BeautifulSoup4')

# try:
# 	os.system('sudo pacman -S --noconfirm dmg2img')
# 	os.system('sudo apt-get update dmg2img')
# except:
# 	pass

import wget
import requests
from bs4 import BeautifulSoup

print(os.system('lsblk | grep disk'))
disk = input('What disk do you want to erase eg sda?  ')
con = input('You sure?  ')
con = con.lower()
if (con == 'y' or con == 'yes') and not disk == 'sda':
	if os.path.exists('disk.sh'):	
		# os.system(f'./disk.sh {disk}')
		pass
	else:
		print('missing disk.sh')
		exit()
else:
	print('Invalid input')
	exit()

print('Linux to OSX Fork')

p = 'macOS Downloads/publicrelease/'
num = 0
_folder = []

if not os.path.exists(p):
	print('\n\nOS X folder not downloaded')
	print('Please use gib macos to download OSX installer')

	# os.system('python gibMacOS.command')
	exit()

for f in os.listdir(p):
	print(f'{num} - {f}')
	_folder.append(f)
	num += 1

print('\n')

folder = int(input('What Folder do you want?  '))
f = _folder[folder]

_p = f'{p}{f}'

os.chdir(_p)
if not os.path.exists('base.iso'):
	os.system(f'dmg2img BaseSystem.dmg base.iso')

os.chdir('../../../')

_path = _p.replace(' ', '\ ')

####  Download Clover  ####
url = 'https://github.com/CloverHackyColor/CloverBootloader/releases'

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
# ver = soup.find_all("a")[i].text
containers = soup.findAll("span", {"class": "css-truncate-target"})
for i in containers:
	ver = str(i).split('>')
	ver.pop(0)
	ver.pop(1)
	ver = ''.join(ver)
	ver = ver.split('<')
	ver.pop(1)
	ver = ''.join(ver)
	break

wget.download(f'https://github.com/CloverHackyColor/CloverBootloader/releases/download/{ver}/CloverISO-{ver}.tar.lzma')
if not os.path.exists('Clover'):
	os.mkdir('Clover')

os.system(f'cp CloverISO-{ver}.tar.lzma Clover/')
os.system(f'sudo rm -r CloverISO-{ver}.tar.lzma')
os.chdir('Clover')     
os.system(f'tar --lzma -xvf CloverISO-{ver}.tar.lzma')
os.chdir('../')

# Add to partitions
os.system(f'dd bs=4M if=Clover/Clover-v2.5k-{ver}-X64.iso  of=/dev/{disk}1')
os.system(f'dd bs=4M if={_path}base.iso of=/dev/{disk}2')
os.system(f'sudo rm -r Clover')

# os.system(f'mount /run/media /dev/{disk}1')