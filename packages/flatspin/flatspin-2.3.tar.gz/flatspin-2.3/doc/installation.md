(installation)=

# Installation

The latest *stable* release of flatspin can be installed and updated using `pip`:

```sh
pip install -U flatspin
```

Install the latest *development* version with:

{{ "```sh\npip install git+{repo}#egg=flatspin\n```".format(repo=flatspin_repo) }}

If you downloaded flatspin, e.g., from the {{flatspin_repo_link}}, you can install it with:

```sh
pip install -U path/to/flatspin
```

Developers will want to install with `--user -e` and the `[dev]` extras:

```sh
pip install --user -e -U path/to/flatspin[dev]
```

## Python version

flatspin requires a stable release of Python 3.5 or later.
