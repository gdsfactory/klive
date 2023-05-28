# Development Installation

A development installation can be done with a symlink. First it is recommended to make a new `$KLAYOUT_HOME` to not pollute the standard
KLayout installation

## Development KLayout

KLayout can use a different directory than the standard `$HOME/.klayout`. It will read the environment variable `KLAYOUT_HOME` on startup.
So, simply setting that variable to a new folder works to make a completely new environment for KLayout and can server as a macro development
environment.

### Linux

This of course can be automated with a script as follows for bash or the like (should work on MacOS and Linux).

```bash
#!/bin/bash

export KLAYOUT_HOME=$HOME/.klayout-dev

/usr/bin/klayout
```

If this is e.g. copied to `/usr/local/bin/klayout-dev` (should work under any Debian and derivates such as Ubuntu etc.) and the execute flag is set (`chmod +x /usr/local/bin/klayout-dev`),
it can be called with `klayout-dev` from a terminal (probably most DEs will also pick this up).

## klive development

In  the development environment the repository of klive can by symlinked into `$KLAYOUT_HOME/salt/klive` for example. With this, KLayout will pick it
up on startup and still allows modifications with either the macro development or an external IDE.

The following will work under linux, but should also work in MacOS or PowerShell on Windows.

```bash
ln -s <path_to_klive_repository>/klayout $HOME/.klayout-dev/salt/klive
```

## Build docs

Install mkdocs with

```bash
python -m pip install mkdocs mkdocs-material mkdocs-section-index mkdocs-video pymdown-extensions
```

To use it locally run `make docs`. To use the internal mkdocs serve `make docs-serve`