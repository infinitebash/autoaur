#!/usr/bin/env python3

import os
import feedparser
import sys
import re

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
  print("Updating")
  os.chdir(package_path)
  os.system("git pull")
  build_package(package_path, outdir)

def download_package(packages_path, package):
  os.chdir(packages_path)
  os.system("git clone https://aur.archlinux.org/" + package + ".git")

def build_package(package_path, outdir):
  print("Building")
  os.chdir(package_path)
  os.system("makepkg --sign -s --noconfirm")
  os.system("mv *.pkg* " + outdir)

def update_repo(outdir):
  print("Updating repo")
  os.chdir(outdir)
  os.system("repo-add -R -s -v repo.db.tar.zst *.pkg.tar.zst")

def main(argv):
  try:
    packages = os.getenv("PACKAGES").split(" ")
    packages_path = os.getenv("PACKAGES_PATH")
    outdir = os.getenv("PACKAGES_OUTPUT")
  except:
    sys.exit("Error: Missing environment variables")

  for package in packages:
    package_path = packages_path + "/" + package

    if package not in os.listdir(packages_path):
      print("Package " + package + " not found! Attempting to download it.")
      download_package(packages_path, package)
      build_package(package_path, outdir)

    if is_update(package):
      print("Package " + package + "has an update available!")
      update_package(package_path, outdir)

    if not re.search(package + "(.*)", " ".join(os.listdir(outdir))):
      print("Package " + package + " found in list but has not been built!")
      build_package(package_path, outdir)
    
  update_repo(outdir)

if __name__ == "__main__":
  main(sys.argv[1:])