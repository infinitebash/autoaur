# autoaur

A tool for automating builds of AUR packages and putting them on a repo.

## Basic Usage

Create folders for the repo and PKGBUILDs:

```sh
mkdir repo packages
```

Add your favorite AUR packages to a file:

```sh
echo awesome-git >> packages.list && echo yay >> packages.list
```

Run autoaur:

```sh
./autoaur.py --packages packages.list --packages-path $(pwd)/packages --output $(pwd)/repo
```

## Automating Updates

Automating updates is possible with a cron job. Here's an example that checks for updates every hour at minute zero:

```sh
0 * * * * /home/exampleuser/autoaur/autoaur.py --packages packages.list --packages-path /home/exampleuser/autoaur/packages --output /home/exampleuser/autoaur/packages/repo
```
