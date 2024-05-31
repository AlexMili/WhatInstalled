import os
import argparse

# brew list --versions
# port installed
# pip list
# dpkg --list
# pkgutil --pkgs
# npm list -g --depth=0
# yarn global list
# cargo install --list
# apt list --installed

# Darwin
# ls /usr/bin
# ls /usr/sbin
# ls /usr/local/bin
# ls /usr/local/sbin
# ls /opt/local/bin
# ls /opt/local/sbin

keywords = {
    "mac": ["brew install", "brew cask install", "port install"],
    "linux": [
        "apt-get install",
        "aptitude install",
        "yum install",
        "pacman install",
        "dpkg -i",
        "dnf install",
        "zypper in",
        "make install",
        "tar ",
    ],
    "lua": ["luarocks install", "luarocks make"],
    "python": ["pip install", "easy_install", "conda install"],
    "ruby": ["gem install", "rvm install"],
    "node": ["npm install", "bower install", "yarn add"],
}


def whatinstalled():
    parser = argparse.ArgumentParser(
        description="A simple tool to retrieve what you installed using CLI"
    )
    parser.add_argument(
        "-f",
        "--file",
        dest="bash_file",
        type=str,
        help="custom file to parse",
        default="~/.zsh_history",
    )
    parser.add_argument(
        "-p",
        "--profile",
        dest="profile",
        type=str,
        help="specific profile to use",
        default="python",
    )
    args = parser.parse_args()

    global keywords

    h_files = [
        "~/.zsh_history",
        "~/.bash_history",
    ]

    if args.profile is None and args.profile in keywords:
        keywords = {args.profile: keywords[args.profile]}
    elif args.profile is None and args.profile not in keywords:
        print("\n[ERROR]Profile doesn't exist\n")
        return

    for h_file in h_files:
        history_file = os.path.expanduser(h_file)

        if os.path.exists(history_file) is True:
            with open(history_file, "r", errors="ignore") as fp:
                for line in fp:
                    for category in keywords:
                        for item in keywords[category]:
                            if item in line:
                                pos = line.find(item)
                                final = line[pos:-1].replace(item, "").strip("\t\n\r")

                                # Skip wrongly formed lines
                                if len(final) == 0:
                                    continue

                                # Node version
                                # if final[0] == "@":
                                #     final = final[1:]

                                # Skip pip install -r
                                if (
                                    category == "python"
                                    and "pip" in line
                                    and ("-r" in line or "-e" in line)
                                ):
                                    continue

                                print(f"[{category}]{final}")
