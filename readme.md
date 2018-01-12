# Simple declarative package management
## For Arch Linux

List the packages you want installed in `/etc/decpac.conf`.  Run `decpac` and packages will be installed/uninstalled until the set of installed packages matches the list.  This doesn't manage config files, cache files, other generated files, etc.  If you like this but want more rigorous declarative package management check out [Nix](https://nixos.org/nix/) and [NixOS](https://nixos.org/).

##### Why declarative management?

1. You want to install the same packages on a different system.  Just copy `decpac.conf` over and run `decpac`!
2. You're looking for a program that does X, and there are 10 programs that say they do X.  If you install them all, you'll definitely forget to uninstall them.  Write a note in `decpac.conf`!
3. You're trying to clean up your system but you don't remember why you installed a package, or even what it does.  Organize and annotate your `decpac.conf` with comments!
4. Help me out here.
5. Diff your config files!

# Usage

Install with
```
pip install decpac
```

If you don't have a configuration file, create one with
```
sudo decpac generate
```

Edit your `/etc/decpac.conf` (be careful not to delete system files).  This is a [luxem](https://github.com/rendaw/luxem) file, which is like JSON but quotes are optional for single words and you can add comments like `* this is a comment *`.

Then run
```
sudo decpac
```
to synchronize your packages.
