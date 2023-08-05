(contributing)=
# Contributing

Contributions to flatspin are very welcome!

There are many ways to contribute to the project, for example:
* Found a bug? Please let us know by [filing a bug report](contributing-bugs)!
* Have a feature request? Please [open an issue](contributing-bugs)!
* If you would like to make changes to the code, please [see below](contributing-code) on how to get started.
* We are also grateful for any improvements to the [documentation](contributing-docs) :)

(contributing-bugs)=
## Bugs and feature requests

Please use {{ "[the issue tracker]({url})".format(url=flatspin_bug_tracker) }} to file bug reports, feature requests or any other issues.

(contributing-code)=
## Code contributions

Both code and documentation live in the {{ flatspin_repo_link }}.

To get started, check out the repository with:

{{ "```sh\ngit clone {repo}\n```".format(repo=flatspin_repo) }}

Next, install flatspin in development mode:

```sh
cd flatspin
pip install --user -e -U .[dev]
```

This will install all dependencies needed for development.
In addition, any changes to the code in your local checkout will be immediately available from Python without having to reinstall the flatspin package.

### Tests

flatspin comes with a suite of unit tests that verifies various parts of the simulator.
Any new features should come with a unit test that verifies correctness.

You may run the full suite of tests with:

```sh
pytest tests
```

Or alternatively, skipping the time-consuming benchmarks:

```sh
pytest --benchmark-skip tests
```

(contributing-docs)=
## Documentation

The {{ "[flatspin documentation]({url})".format(url=flatspin_website) }} is created using the excellent [Jupyter Book](https://jupyterbook.org).

To build the documentation locally, use:

```sh
jupyter-book build doc
```

Please note that some of the examples in the documentation will fail to build, since they depend on some flatspin datasets which are not included in the repository.

(contributing-merge)=
## Merge requests

Once you are ready to contribute your changes, either to the code or documentation, please open a {{ "[merge request]({url})".format(url=flatspin_merge_request) }}.
