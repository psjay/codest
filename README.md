# codest

Coding at local like you do it on remote.

## Features

* Automatically: monitor changes.
* Instantly: Sync just after change.
* Incrementally: only sync changed parts.
* Efficiently: aggregate all changes within a specifield interval and respect your git-ignore rules, only sync need files.

## Installation

Please make sure these programs installed and available in your `PATH`:

* rsync >= 3.1.0
* git >= 2.3.0

```
$ pip install codest
```

## Usage

Monitor changes and sync diff:

```
$ codest path/to/local/foo [user[:password]@]host:/path/on/remote/bar
```

Then, all the code in `/path/on/remote/bar` on the **remote** host will keep syncing with local `foo` directory.

If you just want to sync your code manually, you can put a `-s` argument after the command:

```
$ codest -s path/to/local/foo [user[:password]@]host:/path/on/remote/bar
```

This will cause a sync, and codest will exit.

And you can specifiy sync interval by setting `-i` option:

```
$ codest -i 2 path/to/local/foo [user[:password]@]host:/path/on/remote/bar
```

Then, codest will sync to remote every 2 seconds if changes happened.

To show help message:

```
$ codest -h
```
