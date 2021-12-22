# autoaur

A tool for automating builds of AUR packages and putting them on a repo.

## Basic Usage

1. Create folders for the repo and PKGBUILDs:

   `mkdir repo packages`

2. Add your favorite AUR packages to a file:

   `echo awesome-git >> packages.list && echo yay >> packages.list`

3. Run autoaur:

   `./autoaur.py --packages packages.list --packages-path $(pwd)/packages --output $(pwd)/repo`

## Automating Updates

Automating updates is possible with a cron job. Here's an example that checks for updates every hour at minute zero:

```sh
0 * * * * /home/exampleuser/autoaur/autoaur.py --packages packages.list --packages-path /home/exampleuser/autoaur/packages --output /home/exampleuser/autoaur/packages/repo
```
