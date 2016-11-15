import os

history_file = os.path.expanduser("~")+"/.bash_history"
f = open(history_file,"r")

keywords = ["pip", "tar", "brew", "apt-get", "install", "luarocks", "easy_install", "gem", "npm"]

for line in f:
	for item in keywords:
		if item in line:
			print(line[:-1])
			break