#!/usr/local/bin/python2.7
# -*- coding: UTF-8 -*-
# 
#  Generate thumbnails for site
#

import os
import sys
from PIL import Image

diro = sys.argv[1]
t_diro = '{}/thumb_'.format(diro)

get_dirs = [ d for d in os.listdir(diro) if os.path.isdir('{}/{}'.format(diro, d)) if 'thumb' not in d ]

for d in get_dirs:
	if not os.path.isdir('{}/thumb_{}'.format(diro, d)):
		os.mkdir('{}/thumb_{}'.format(diro, d))

for d in get_dirs:
	list_dir = filter(None, os.listdir('{}/{}'.format(diro, d)))
	for i in list_dir:
		img = Image.open('{}/{}/{}'.format(diro, d, i))
		img.thumbnail([ int(s*0.1) for s in img.size ], Image.ANTIALIAS)
		img.save('{}/thumb_{}/{}'.format(diro, d, i))

for d in get_dirs:
	if not os.path.isdir('{}/mid_{}'.format(diro, d)):
		os.mkdir('{}/mid_{}'.format(diro, d))

for d in get_dirs:
	list_dir = filter(None, os.listdir('{}/{}'.format(diro, d)))
	for i in list_dir:
		img = Image.open('{}/{}/{}'.format(diro, d, i))
		img.thumbnail([ int(s*0.5) for s in img.size ], Image.ANTIALIAS)
		img.save('{}/mid_{}/{}'.format(diro, d, i))
