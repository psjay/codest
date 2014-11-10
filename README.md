# LiveCode

Live sync your local code in Git repository to remote development server via rsync.

Features:

* Sync your code only, no other shit.
* Aggregating changes within a second.

**DISCLAIMER**: This software has not been well tested, use it on your own risks.

## Installation

```
$ pip install LiveCode
```

## Usage

Monitor changes and sync diff:

```
$ livecode path/to/local/git-repo [user[:password]@]host:/path/on/remote
```

Do a sync then exit:

```
$ livecode -s path/to/local/git-repo [user[:password]@]host:/path/on/remote
```
