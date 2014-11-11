# LiveCode

Edit your code at local like you do it on remote.

Live sync your local code in Git repository to remote development server via rsync.

## Features

* Sync your code only, no other unnecessary files(including `.git` directory and
  files matched in `.gitignore`).
* Aggregating changes within one second.

## Installation

```
$ pip install LiveCode
```

## Usage

Monitor changes and sync diff:

```
$ livecode path/to/local/git-repo [user[:password]@]host:/path/on/remote
```

Then, all the code in `/path/on/remote/git-repo` on the **remote** host will be exactly
the same as in the local `git-repo` directory.

If you just want to sync your code manually, you can plus a `-s` argument after the command:

```
$ livecode -s path/to/local/git-repo [user[:password]@]host:/path/on/remote
```

This will cause a sync operation, then LiveCode will exit.
