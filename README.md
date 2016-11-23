# WhatInstalled
WhatInstalled is a simple tool to retrieve what you installed using command line.

## Installation
After cloning this repository simply run :
```bash
cd whatinstalled/
pip install -e .
```

## Usage

You just need to run :
```bash
whatinstalled
```

By default the tool will look in `~/.bash_history`. If you want to specify a different file use the `-f` or `--file` argument :
```bash
whatinstalled -f ~/.zsh_history
```

WhatInstalled allow you to select a specific profile among the following :
```python
{\
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
```

Choose a specific profile :
```bash
whatinstalled -p python
```
Output :
```bash
[python]sudo easy_install pip
[python]pip install awscli
```
