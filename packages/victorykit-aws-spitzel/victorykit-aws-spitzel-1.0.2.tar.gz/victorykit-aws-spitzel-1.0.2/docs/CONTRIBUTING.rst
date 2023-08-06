############
CONTRIBUTING
############

Releasing
=========

There currently is no release plan in place. Patches and hotfixes will be 
integrated on a *have time, can do* basis.

Continouous Integration
=======================

There currently is no CI/CD automation through pipelines in place. However, 
the build environment is properly virtualized to support simple pipelines, so
it will probably be part of a future release. It is still being evaluated on 
how to operate Bitbucket Pipelines the cheapest. There are a multitude of 
factors to consider. For the time being, the build environment has been 
simplified enough as to avoid error-prone manual tasks.

Versioning
==========

This project uses SemVer for software release versioning. Versioning of all 
release components is automated and can be controlled through a Git tag with
a prefixed SemVer version (e.g. ``v1.0.0``).

Should the Git HEAD have a tag with a SemVer string prefixed with v as a name, 
and the Git stage be empty, this version is then obliged to in all build 
processes. However should the Git stage not be empty, or the HEAD not being 
tagged, the automation system will increment the patch version and append a dev 
suffix. Even if a version was released by accident, it is not possible to do so 
as an official release.

Issue & Feature Tracking
========================

Ideally, Jira is being used. However, it has not been evaluated yet, if the 
publicity of Jira is good enough to have it as a public project management 
dashboard.