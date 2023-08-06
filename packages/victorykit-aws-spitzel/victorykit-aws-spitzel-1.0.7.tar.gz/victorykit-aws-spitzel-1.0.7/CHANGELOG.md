# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased


* support logical `and`, and `or` operations for matchers/filters


* remove redundant imports


* log shipping usage example (Splunk)


* AWS Lambda layer distribution


* basic unit tests


* ### stdin Input Handling

In addition to using the AWS CloudTrail API as an input, it is planned to
support input from stdin as new-line delimited JSON object streaming and
optionaly [HTTP multipart/byterange MIME type](https://datatracker.ietf.org/doc/html/rfc7233#section-5.4.1),
where the byterange represents a single line JSON object stream (the Python
standard library can support that).

One can basically just stream whatever CloudTrail events into stdin, wheras
*aws-spitzel* will act as a proxy. Should the capabilities of a single
*aws-spitzel* not suffice, one can then just chain multiple *aws-spitzel*
together and achieve a higher query complexity.

### Lambda layer distribution

lambda layer distributions will be made available with each release in the
future. Additionally, the build tools for the lambda layer distribution will be
part of the repository. This will be a milestone, since *aws-spitzel* has the
potential to replace the (rather difficult to maintain at large) AWS solution
of streaming CloudTrail log events with Kinesis Data streams. Instead,
*aws-spitzel* can be used as an interval log-shipper. AWS CloudTrail log
delivery is delayed by 5 minutes anyway. It is not necessary to put an
event-driven architecture in place for that. Sometimes logs may not even have
to be delivered as fast as possible (performance-oriented logs). Amazon Kinesis
just feels too mighty for the task, if one can basically built an adequate
solution with AWS Lambda, the Python standard library, and a single, compact
third-party Python module for JSONPath. Luckily the API’s of log management
solutions aren’t too complicated because of the quantitative requirements they
have. The more complex their interface, the slower the throughput. It should
be fairly easy to extend *aws-spitzel* to a full AWS CloudTrail log shipping
solution (for e.g. Splunk). Private networking requirements could be fulfilled
through AWS Lambda VPC networking (which AWS Kinesis Data Stream can’t).

### support for `and` and `or` operators in expressions

Advanced Input Handling has higher precedence, since you could achieve *and*,
and *or* logic through shell piping, however it would be nice to work on this,
since it would require the expression tokenizer to be hardened as to support
escaping reserved characters.

## v1.0.7 - 2023-04-03

**Changed**


* added throttling support for standalone Splunk integration reference
implementation


* added timestamp and source to Splunk integration reference implementation


* updated documentation

## v1.0.6 - 2023-04-02

**Changed**


* documentation on Splunk Integration reference implementation

## v1.0.5 - 2023-04-02

**Added**


* Splunk reference implementation

**Changed**


* refactored cli interface


* refactory main Python interface

## v1.0.4 - 2023-04-02

**Added**


* documentation hint for CloudTrail format in README


* documentation hint for AWS CLI configuration in README

**Changed**


* description of *Releasing* in Contribution Guidelines to match updated build
tools

## v1.0.3 - 2023-04-02

**Added**


* Python module documentation

**Changed**


* updated build tools interface


* documentation wording and order

## v1.0.2 - 2023-04-02

**Changed**


* updated documentation

## v1.0.1 - 2023-04-01

**Fixed**


* fixed documentation workflow

**Changed**


* updated docs

## v1.0.0 - 2023-04-01

**Added**


* initial commits

**[unreleased]**: [https://bitbucket.org/victorykit/py-aws-spitzel/src/dev/](https://bitbucket.org/victorykit/py-aws-spitzel/src/dev/)

**[1.0.7]**: [https://bitbucket.org/victorykit/py-aws-spitzel/src/v1.0.7/](https://bitbucket.org/victorykit/py-aws-spitzel/src/v1.0.7/)

**[1.0.6]**: [https://bitbucket.org/victorykit/py-aws-spitzel/src/v1.0.6/](https://bitbucket.org/victorykit/py-aws-spitzel/src/v1.0.6/)

**[1.0.5]**: [https://bitbucket.org/victorykit/py-aws-spitzel/src/v1.0.5/](https://bitbucket.org/victorykit/py-aws-spitzel/src/v1.0.5/)

**[1.0.4]**: [https://bitbucket.org/victorykit/py-aws-spitzel/src/v1.0.4/](https://bitbucket.org/victorykit/py-aws-spitzel/src/v1.0.4/)

**[1.0.3]**: [https://bitbucket.org/victorykit/py-aws-spitzel/src/v1.0.3/](https://bitbucket.org/victorykit/py-aws-spitzel/src/v1.0.3/)

**[1.0.2]**: [https://bitbucket.org/victorykit/py-aws-spitzel/src/v1.0.2/](https://bitbucket.org/victorykit/py-aws-spitzel/src/v1.0.2/)

**[1.0.1]**: [https://bitbucket.org/victorykit/py-aws-spitzel/src/v1.0.1/](https://bitbucket.org/victorykit/py-aws-spitzel/src/v1.0.1/)

**[1.0.0]**: [https://bitbucket.org/victorykit/py-aws-spitzel/src/v1.0.0/](https://bitbucket.org/victorykit/py-aws-spitzel/src/v1.0.0/)
