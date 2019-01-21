# Simple declarative package management
## For Arch Linux

List the packages you want installed in `/etc/decpac.conf`.  Run `decpac` and packages will be installed/uninstalled until the set of installed packages matches the list.  This doesn't manage config files, cache files, other generated files, etc.  If you like this but want more rigorous declarative package management check out [Nix](https://nixos.org/nix/) and [NixOS](https://nixos.org/).

I've been using it for a couple months now (April 2018).

##### Why declarative management?

1. You want to install the same packages on a different system.  Just copy `decpac.conf` over and run `decpac`!
2. You're looking for a program that does X, and there are 10 programs that say they do X.  If you install them all, you'll definitely forget to uninstall them.  Install them using pacman directly and decpac will uninstall them the next time you run it.
3. You're trying to clean up your system but you don't remember why you installed a package, or even what it does.  Organize and annotate your `decpac.conf` with comments!
4. Help me out here.
5. Diff your package list!

# Usage

Install with
```
pip install decpac
```

If you don't have a configuration file, create one with
```
sudo decpac generate
```

Edit your `/etc/decpac.conf` (be careful not to delete system files) (see **Config file syntax** below).

Then run
```
decpac
```
to synchronize your packages.

# Config file syntax

The config file looks like:

```
{
        install_main: [
                sudo,
                pacman,
                --noconfirm,
                -S,
        ],
        install_aur: [
                trizen,
                --noconfirm,
                -S,
        ],
        installed: [
                nvidia,
                lib32-nvidia-utils,
                trizen,
		...

                * audio *
                alsa-utils,
                (aur) alsaequal,
                alsaequal-mgr,
                alsaplayer,
		...
	],
},
```
This is a [luxem](https://gitlab.com/rendaw/luxem) file, which is like JSON but quotes are optional for single words and you can add comments like `* this is a comment *`.

`(aur)` specifies an AUR package.  It's installed with whatever helper you specified in `install_aur` (trizen worked for me).

# Implementation notes

Most AUR helpers had issues, such as installing all deps from AUR or not flagging dependencies as dependencies (or rather, flagging them all as explicit).  I worked around that somewhat but it would be nice to implement AUR functionality directly.  It may make things more efficient too.

Customizing AUR builds makes things nonreproducible so I avoid doing that.  Specifying customizations in `decpac.conf` might be a good feature.

It would be awesome if decpac could install Ruby/Node packages as well using `npm2arch` and its ilk.

Renamed packages need to be renamed in the config manually.  decpac could update the config file automatically but de/reserializing deletes comments.  Maybe making a `(comment)` type would work?

# Related projects

* [Nix](https://nixos.org/nix/) - A strict declarative package (and config) manager that can be used on Arch, and also the basis of Linux distro [NixOS](https://nixos.org/)
* [aconfmgr](https://github.com/CyberShadow/aconfmgr) - A declarative Arch-native package and config manager
