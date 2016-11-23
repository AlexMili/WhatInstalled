import os
import argparse

keywords = {\
	"mac":[\
		"brew install",\
		"brew cask install",\
		"port install"\
	],\
	"linux":[\
		"apt-get install",\
		"aptitude install",\
		"yum install",\
		"pacman install",\
		"dpkg -i",\
		"dnf install",\
		"zypper in",\
		"make install",\
		"tar "\
	],\
	"lua":[\
		"luarocks install",\
		"luarocks make"\
	],\
	"python":[\
		"pip install",\
		"easy_install",\
		"conda install"\
	],\
	"ruby":[\
		"gem install",\
		"rvm install"\
	],
	"node":[\
		"npm install",\
		"bower install"\
	],\
}

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Retrieve what you installed on your system using bash history')
	parser.add_argument('-f', '--file',		dest='bash_file', 	type=str, help="custom file to parse", 		default="~/.bash_history")
	parser.add_argument('-p', '--profile',	dest='profile', 	type=str, help="specific profile to use",	default=None)
	args = parser.parse_args()

	history_file = os.path.expanduser(args.bash_file)
	f = open(history_file,"r")

	if(args.profile != None and args.profile in keywords):
		keywords = {args.profile:keywords[args.profile]}
	elif(args.profile != None and args.profile not in keywords):
		print("\n[ERROR]Profile doesn't exist\n")
		exit(0)

	for line in f:
		for category in keywords:
			for item in keywords[category]:
				if item in line:
					print("["+category+"//"+item+"]"+str(line[:-1]))
