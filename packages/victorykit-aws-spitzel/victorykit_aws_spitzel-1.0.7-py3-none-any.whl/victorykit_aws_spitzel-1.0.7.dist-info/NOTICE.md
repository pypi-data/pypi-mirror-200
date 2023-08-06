# NOTICE

**NOTE**: Look for what’s to come in the future. *aws-spitzel* has the potential to
replace AWS Kinesis Data Stream as a log shipping solution for AWS
CloudTrail. That would mean an IAM role, Lambda layer and function,
instead of an IAM role, S3 bucket, Kinesis Data Stream, Lambda function and
layer. Remember, CloudTrail log events are present for 90 days, regardless
of whether a CloudTrail trail actually exists or not and they will arrive
up to 5 minutes late everytime anyway. Finally, not being on time makes
sense and is actually quite pleasant…

**NOTE**: This program is looking for a maintainer. Whether you despise, or admire
this program; Do something about it! Just contact
[py-aws-spitzel@victory-k.it](mailto:py-aws-spitzel@victory-k.it). As an example of transparent communication for
EU commissioner von der Leyen, communication is public, adapt your
discretion accordingly.

**Security Notices**

**WARNING**: The `jsonpath` third-party Python module uses `eval()` statements.
Restrict your local environment and AWS principal accordingly. If you are
unsure about the sanity of CloudTrail event JSON object values.

**WARNING**: This is, for a change, a positive security notice.
\* [upbeat pop-rock music playing](https://www.youtube.com/watch?v=ZHwVBirqD2s) \*
(open in separate tab). If you’re a developer and stumble upon the
ast.parse method `mode` attribute set to `eval`, don’t worry, this
isn’t equivalent to the built-in `eval()` method. The code is not being
interpreted and executed. Yes you can crash the process, cause excessive
CPU consumption , or denial of service, but nothing to be worried about
security-wise, unless somebodies live depended upon AWS CloudTrail log
delivery. You can find more information in the
[Python documentation chapter about the ast module](https://docs.python.org/3/library/ast.html#ast.literal_eval).
