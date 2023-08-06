# CONTRIBUTING

## Versioning

This project uses SemVer for software release versioning. Versioning of all
release components is automated and can be controlled through a Git tag with
a prefixed SemVer version (e.g. `v1.0.0`).

Should the Git HEAD have a tag with a SemVer string prefixed with v as a name,
and the Git stage be empty, this version is then obliged to in all build
processes. However should the Git stage not be empty, or the HEAD not being
tagged, the automation system will increment the patch version and append a dev
suffix. Even if a version was released by accident, it is not possible to do so
as an official release.

## Issue & Feature Tracking

The Atlassian Bitbucket Issue Tracker is being used for tracking features and
issues.

All source code changes for features must be tracked in a Git branch
`feat/$ISSUE`, wheras `$ISSUE` is the id of the corresponding issue inside
the issue tracker. Bugs are tracked under `bugfix/$ISSUE` and hotfixes are
tracked under `hotfix/$ISSUE`.

## Documentation

```shell
$ python3 -m pipenv run htmldocgen
```

```shell
$ python3 -m pipenv run mddocgen
```

## Releasing

There currently is no release plan in place. Patches and hotfixes will be
integrated on a *have time, can do* basis.

Features and Bugfixes must be (squash) merged into the Git branch `dev` first.
Concluding a development interval as this program’s maintainer requires one to
create a `release/$SEMVER` Git branch and have the release tested by whoever
opened the issue, or feature. If bugs are found, they must be tracked inside
the issue tracker and once concluded must be integrated into the
`release/$SEMVER` Git branch and tested through whoever opened the bug. Once
the bug is resolved, the `release/$SEMVER` Git branch is (fast-forward)
merged into the `dev` branch. The release can only be concluded if the HEAD
of the `release/$SEMVER` branch is tagged with a SemVer version string.

Afterwards the `release/$SEMVER` branch is merged (no fast-forward) into
the `master` Git branch.

Each release (irrelevant of it being a major, minor, or patch release) must
have a dedicated changelog release note.

Copy the release note of the previous release from
`doc/changelogs/%Y%M%D %d.%d.%d.rst` and increment the date and version of
the filename, as well as chapter title. Next make sure to stick to the
Keep-A-Changelog format and describe the changes only through *Fixed*,
*Changed*, *Added* sections.

Afterwards, include the release note inside the root changelog
(`docs/CHANGELOG.rst`) and add a link to the web page of the Git repository
tag.

## Continouous Integration

There currently is no CI/CD automation through pipelines in place. However,
the build environment is properly virtualized to support simple pipelines, so
it will probably be part of a future release. It is still being evaluated on
how to operate Bitbucket Pipelines the cheapest. There are a multitude of
factors to consider. For the time being, the build environment has been
simplified enough as to avoid error-prone manual tasks.

```shell
$ python3 -m pipenv run tox
```

```shell
$ git commit -e
```

```shell
$ git tag "v$SEMVER"
```

```shell
$ python3 -m pipenv run tox
```

```shell
$ git diff --exit-code --quiet && echo "this is fine" || echo "this is not fine"
```

```shell
$ python3 -m pipenv run tox -e publish
```

```shell
$ git push -u origin HEAD "v$SEMVER"
```

```shell
$ python3 -m BITBUCKET_REPO_SLUG=py-aws-spitzel \
             python3 -m pipenv run tox -e publish-docs
```
