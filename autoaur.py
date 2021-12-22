#!/usr/bin/env python3

import os
import feedparser
import re
import argparse

def is_update(package):
  aurFeed = feedparser.parse("https://aur.archlinux.org/rss/")

  titles = []
  for entry in aurFeed['entries']:
    titles.append(entry['title'])

  if package in titles:
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

def main():
  parser = argparse.ArgumentParser(
    prog="autoaur",
    description="A tool for automaing aur builds")  
  parser.add_argument(
    "--packages", 
    type=str,
    nargs=1,
    required=True,
    help="Path to a file containing a new-line seperated list of packages")
  parser.add_argument(
    "--packages-path",
    type=str,
    nargs=1,
    required=True,
    help="Path to store package builds in"
  )
  parser.add_argument(
    "--output", "-o",
    type=str,
    nargs=1,
    required=True,
    help="Path to output packages/repo database to (i.e. a folder served via a web server)"
  )

  args = parser.parse_args()
  outdir = args.output[0]
  packages_path = args.packages_path[0]
  with open(args.packages[0]) as f:
    packages = f.read().splitlines()

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
  main()