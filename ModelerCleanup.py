import os
import re
import sys

rootdir = os.getcwd()

regex1 = re.compile('^.*\.pr\.(c|cpp)$')
regex2 = re.compile('^.*\.(dev64|opt64)\.i0\.pr\.obj$')
regex3 = re.compile('^.*\.(dev64|opt64)\.i0\.nt\.(dll|dll\.manifest|exp|lib|pdb)$')
regex4 = re.compile('^.*-DES-[0-9]+\.(desinfo|ef|ov|ot)$')
regex5 = re.compile('^.*-DES-[0-9]+\.olf\.dir')

for root, dirs, files in os.walk(rootdir):

	for file in files:
		if regex1.match(file):
			print("Removing {}".format(os.path.join(root,file)))
			os.remove(os.path.join(root,file))
			pass

		if regex2.match(file):
			print("Removing {}".format(os.path.join(root,file)))
			os.remove(os.path.join(root,file))
			pass

		if regex3.match(file):
			print("Removing {}".format(os.path.join(root,file)))
			os.remove(os.path.join(root,file))
			pass

		if regex4.match(file):
			print("Removing {}".format(os.path.join(root,file)))
			os.remove(os.path.join(root,file))
			pass

	if regex5.match(root):
		for file in files:
			print("Removing file {}".format(file))
			os.remove(os.path.join(root,file))
		print("Removing directory {}".format(root))
		os.rmdir(root)
		