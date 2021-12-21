import os
import feedparser
import sys

def get_titles():
  aurFeed = feedparser.parse("https://aur.archlinux.org/rss/")

  titles = []
  for entry in aurFeed['entries']:
    titles.append(entry['title'])
  
  return titles

def is_update(package):
  if package in get_titles():
    return True
  return False

def update_package(package_path, outdir):
  os.chdir(package_path)
  os.system("git pull")
  build_package(package_path, outdir)

def download_package(packages_path, package):
  os.chdir(packages_path)
  os.system("git clone https://aur.archlinux.org/" + package + ".git")

def build_package(package_path, outdir):
  os.chdir(package_path)
  os.system("makepkg -s --noconfirm")
  os.system("cp *.pkg* " + outdir)

def main(argv):
  packages = os.getenv("PACKAGES").split(" ")
  packages_path = os.getenv("PACKAGES_PATH")
  outdir = os.getenv("PACKAGES_OUTPUT")

  print(packages)

  for package in packages:
    package_path = packages_path + "/" + package

    if package not in os.listdir(packages_path):
      download_package(packages_path, package)
      build_package(package_path, outdir)

    if is_update(package):
      update_package(package_path, outdir)

if __name__ == "__main__":
  main(sys.argv[1:])