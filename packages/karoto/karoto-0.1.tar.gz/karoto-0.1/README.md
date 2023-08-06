# Karoto Shopping List

A Linux mobile app that helps you with your groceries.

It is not just a fancy replacement for your notes app but instead works a bit like a stock management software.
The heart of the app is a list with things you always want to have at home.
Before you go to the grocery store or whereever you get your stuff from you can go through this list and check for every item how much you have in your storage.
The app then generates the shopping list for you which makes it impossible to forget anything.
If you need something like a new knive or some new plates e.g. there is the "only once" option where the item automatically gets deleted as soon as you got it once.

# Screenshots
Left/Top: Storage Feed (you go through this list at home), Right/Bottom: Shopping Feed (for in the store e.g.)

![Storage Feed](screenshots/storage_feed.png) ![Shopping Feed](screenshots/shopping_feed.png)

The screenshots were created by gnome-screenshot on a PinePhone with Arch Linux ARM (DanctNIX) installed.
The software gets also tested on a OnePlus 6 with postmarketOS edge.
Both devices are running Phosh at the moment.

# Installing

Karoto depends on python3 and PyQt6 to run.
All instructions assume you have cloned the repository and are in its root folder:
```
git clone https://codeberg.org/DrRac27/karoto.git
cd karoto
```

## No installing
Without installing you can use `./helper.sh run` to start and test the app.

## Using pip (the easiest if you are not using Arch Linux)
First make sure you have [pip installed](https://packaging.python.org/en/latest/guides/installing-using-linux-tools/#installing-pip-setuptools-wheel-with-linux-package-managers) and then:
```
sudo pip install karoto
sudo install -Dm 644 packaging/karoto.desktop /usr/share/applications/
sudo install -Dm 644 packaging/karoto.svg /usr/share/icons/hicolor/scalable/apps/
```
This will install it system-wide.
If you want to install it for the user only use `~/.local/share/applications` and `~/.icons` for the commands above and omit the `sudo`.

## postmarketOS / Alpine

There is an APKBUILD you can build using `abuild` in this repo.
Follow the [setup instructions](https://wiki.alpinelinux.org/wiki/Creating_an_Alpine_package#Setup_your_system_and_account) for abuild and create the package using `./helper.sh postmarketos-package` in the root folder of this project.
You can now install the resulting package. Depending on how you set up abuild the command for this may be something like `sudo apk add --allow-untrusted ~/packages/path/to/built/app.apk`.

## Arch Linux / Arch Linux ARM / DanctNIX / Kupfer / ...
There are the AUR packages [karoto](https://aur.archlinux.org/packages/karoto) and [karoto-git](https://aur.archlinux.org/packages/karoto-git).
If you e.g. use yay:
```
yay -S karoto
```
If you want to change something before installing there is also a PKGBUILD in `packaging/archlinux` (like for postmarketOS) that you can install using the helper script.

# Roadmap aka some ideas that may get implemented soon™ (by you?)
- Tags: For example you can tag your items with "Hygiene" or "Fruits/Vegetables" and when you are in the supermarket you can filter your list for the department where you are at that moment. Tags like "Fridge" or "Storage Area" will help while you are putting your list together at home. Or maybe you want to create tags for suppliers?
- Translation
- Feedback via feedbackd
- More styles? Dark style? Custom user styles?
- Multiple lists to choose from via GUI (already supported via CLI)?
- Flatpak?
- support for Android (F-Droid)? PRs welcome! (pyqtdeploy?)


# Dev Notes
- if you want git to stop annoying you with the changed tests/data files you can use
```
git update-index --assume-unchanged <file>
```
If you want to start tracking changes again:

```
git update-index --no-assume-unchanged <file>
```
([src](https://stackoverflow.com/a/11366713))

# License
This app is dual-licensed under MIT for people that care about licenses/legal stuff and under the anarchist license for those who don't.
