# LiveCode

Edit your code at local like you do it on remote.

## Features

* Automatically: monitor changes.
* Instantly: Sync just after change
* Incrementally: only sync changed parts.
* Efficiently: aggregate all changes within a specifield interval and respect your git-ignore rules, only sync need files.

## Installation

```
$ pip install LiveCode
```

## Usage

Monitor changes and sync diff:

```
$ livecode path/to/local/foo [user[:password]@]host:/path/on/remote/bar
```

Then, all the code in `/path/on/remote/bar` on the **remote** host will be exactly
the same as in the local `foo` directory.

If you just want to sync your code manually, you can put a `-s` argument after the command:

```
$ livecode -s path/to/local/foo [user[:password]@]host:/path/on/remote/bar
```

This will cause a sync, then LiveCode will exit.

And you can specifiy sync interval by setting `-i` option:

```
$ livecode -i 2 path/to/local/foo [user[:password]@]host:/path/on/remote/bar
```

Then, LiveCode will sync to remote every 2 seconds if changes happened.

Show help message:

```
$ livecode -h
```

