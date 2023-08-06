.. note::
    * Repository: https://bitbucket.org/victorykit/py-aws-spitzel
    * Documentation: https://victorykit.bitbucket.io/py-aws-spitzel
    * Issue Tracker: https://bitbucket.org/victorykit/py-aws-spitzel/issues
    * Mailing List: https://groups.google.com/a/victory-k.it/g/py-aws-spitzel

.. argparse::
   :module: aws_spitzel.cli
   :func: get_parser
   :prog: aws-spitzel

About
#####

Things currently change a lot and sometimes they break features, and routines 
that have been previously established. It's noisy, but one gets to a point
of true system resilience much quicker. After the migration to a different IAM
scheme, a project suffered from the loss of access to an AWS service. The 
project manager claimed that an AWS service isn't accessible anymore, but was 
so in the past. The new IAM scheme restricts access to more AWS services, so it 
might be possible to accidentally have restricted access to the service 
mentioned by the project manager. All services accessed by projects were 
regarded when defining the new IAM scheme. According to the compliance criteria 
of the German BSI C5 catalogue for operating certifiable cloud services in 
accordance with German data privacy protection regulations, events like these 
still fall under the security incident management requirements. These are just 
the *nice* kind of security incidents, where somebody accidentally get's locked 
out. Unpleasant for the principal affected, but to quote the great Elton John:
"I'm still standing...". However, it would still  be required to properly 
classify this incident accordingly (BSI C5 SIM-02). Depending on the 
correctness of the project managers statements, remediation actions may be 
postponed.

It is obvious which actions, and services are applicable as CloudTrail events 
and when they should have occured, however this would mean joining multiple 
queries against the AWS CloudTrail API ``LookupEvent`` action, since it 
currently allows only 1 query attribute at a time. One needs some more advanced 
query utility in order to do that. Amazon Athena is a perfect fit for that, 
since it supports SQL and advanced JSON-oriented queries. However, it is a 
giant and has rather extensive requirements, like an already existing S3 bucket 
populated with CloudTrail trail log events, even though CloudTrail is storing 
all events in the Nirvana for 90 days, regardless of somebody proactively 
creating a CloudTrail trail. The effort of getting the Amazon Athena 
functionality wasn't worth it, because this program is what came up in the 
meantime. Besides some JSON-oriented query the only real operations required 
are some basic comparisons and regular expresssion substring evaluations. There 
is XPath for XML queries, and now there is JSONPath for JSON queries. The 
Python standard library itself  (ast - abstract syntax tree for parsing strings 
as definitions of Python built-in types) and a custom basic tokenizer for 
parsing the tokens of an operand-operation-operand expression built on top of 
it can deliver the rest.

System interchange is possible through line-delimited JSON streaming via stdout.
The program routine is parallelized through multi-threading, making it fast 
enough to keep up with the AWS API throttling threshold.

Due to the AWS CloudTrail API ``LookupEvents`` throttling threshold (100 
events, across 2 requests per principal, per second) this program is optimized 
for single-core execution. Multi-core execution makes sense, when more than two 
access keys for the same AWS environment are being used, therefore doubling the 
networking throughput. An implementation for that will be covered in the 
future, when support for CloudTrail trails with S3 backends has been 
established by this program. This is currently planned for the middle of Q2 in 
2023.

How It Works
############

A main thread spawns a handler thread. The handler executes 
``cloudtrail:LookupEvents`` requests in a loop indefinetly until a 
pagination token is no longer provided. Meanwhile, each paginated API response 
will spawn a worker thread, which are registered inside the handler thread. 
Each worker thread will loop through the list of events of the API response, 
and match each list item against one or multiple JSONPath expressions. Any 
matching item will then be compared against a specified Python built-in type, 
or regular expression.

.. warning::
    This program uses a 
    `quasi-port of the original Javascript JSONPath reference implementation <http://www.ultimate.com/phil/python/#jsonpath>`_. 
    Expect resolution as described in 
    `IETF draft-goessner-dispatch-jsonpath-00 <https://datatracker.ietf.org/doc/draft-goessner-dispatch-jsonpath/>`_.

.. note::
    Supported filter expression operators:

    * `==`: equal comparison to int, str, dict, bool, None, tuple, or list values
    * `!=`: not equal comparison to int, str, dict, bool, None, tuple, or list values
    * `regex`: compare by matching against a regular expression (only supported 
      for str built-in types)

.. note::
    ECMAScript behaviour of non-existing object properties being of type 
    ``undefined`` is being emulated through get() method on dictionaries, so 
    that JSONPath expressions not matching against any items can be compared 
    to ``None`` (e.g. ``$.errorCode != None``).

Should the item match, it will be pushed onto a priority queue as a queue item. 
After the thread looped over the entire event list, it will return.

The main thread loops over the priority queue indefinetly. Each time it 
retrieves a lookup match item from the queue, it will yield the item. Should it 
receive a stop signal, it will set the queue item retrieval timeout, so that
the main thread's loop will be broken, should there be no more items to be 
expected coming from the queue.

Getting Started
###############

Get familiarized with the 
`CloudTrail event format <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-examples.html#error-code-and-error-message>`_
and configure API access to the AWS environment in question (`<https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html>`_.
).

The following is a sample AWS CloudTrail event

.. code-block:: json

    {
        "eventVersion": "1.04",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "EX_PRINCIPAL_ID",
            "arn": "arn:aws:iam::123456789012:user/Alice",
            "accountId": "123456789012",
            "accessKeyId": "EXAMPLE_KEY_ID",
            "userName": "AliceIsNotBob"
        },
        "eventTime": "2016-07-14T19:15:45Z",
        "eventSource": "cloudtrail.amazonaws.com",
        "eventName": "UpdateTrail",
        "awsRegion": "us-east-2",
        "sourceIPAddress": "205.251.233.182",
        "userAgent": "aws-cli/1.10.32 Python/2.7.9 Windows/7 botocore/1.4.22",
        "errorCode": "TrailNotFoundException",
        "errorMessage": "Unknown trail: myTrail2 for the user: 123456789012",
        "requestParameters": {"name": "myTrail2"},
        "responseElements": null,
        "requestID": "5d40662a-49f7-11e6-97e4-d9cb6ff7d6a3",
        "eventID": "b7d4398e-b2f0-4faa-9c76-e2d316a8d67f",
        "eventType": "AwsApiCall",
        "recipientAccountId": "123456789012"
    }

With aws-spitzel, it is possible to query any attribute with a JSONPath query 
(e.g. ``$.userIdentity.userName``) and compare it to a string, or number

.. code-block:: shell

    $ aws-spitzel 'cloudtrail:Update*' \
        --match '$.userIdentity.userName == "AliceIsNotBob"'

.. code-block:: shell

    $ aws-spitzel 'cloudtrail:Update*' \
        --match '$.userIdentity.userName != "AliceIsNotBob"'

You can also execute a regular expression substring search

.. code-block:: shell

    $ aws-spitzel 'cloudtrail:Update*' \
        --match '$.userIdentity.userName regex "AliceIsNot.*"'

.. note::
    operations occur on each single CloudTrail event, any JSON container 
    objects (e.g. ``Records`` arrays) will not be available.

The following commands are required:

* :code:`python3`
* :code:`pip`
* :code:`pipenv` (Development)

Next, install and make sure the command is available.

.. code-block:: shell

    $ python3 -m pip install victorykit-aws-spitzel

.. code-block:: shell

    $ aws-spitzel --help

Alternatively, you can clone the repository

.. code-block:: shell

    $ mkdir py-aws-spitzel && cd $_ && git clone https://bitbucket.org/victorykit/py-aws-spitzel.git .

install via pipenv (development)

.. code-block:: shell

    $ python3 -m pipenv install -d

.. code-block:: shell

    $ python3 -m pipenv run aws-spitzel --help

or pip

.. code-block:: shell

    $ python3 -m pipenv install .

.. code-block:: shell

    $ aws-spitzel --help


More information in the :doc:`Contribution Guidelines </CONTRIBUTING>`

Usage Examples
##############

Make sure to configure the AWS API through setting the `well-known AWS CLI 
environment variables <https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html>`_.

The defaults are, to get all events within the last 90 days

.. code-block:: shell

    $ aws-spitzel 's3:Get*' 'dynamodb:Get*'

There is a shorthand for *the last x minutes*

.. code-block:: shell

    $ aws-spitzel 's3:Get*' 'dynamodb:*' --last-minute 300

Also, date ranges can be explicitly specified and will default to *now* and *90 
days before now*:

.. code-block:: shell

    $ aws-spitzel \
        --from '2023-03-31 14:00:12' \
        --to '2023-04-01 00:00:00' \
        's3:Get*' \
        'dynamodb:*'

The following example finds all CloudTrail events of the AWS Transfer Family 
API, not made by AWS IAM user ``Alice`` existing in AWS account ``000000000000`` 
that we're not denied and came from the host ``147.161.171.112``. Strange 
query, but hopefully the point comes across.

.. code-block:: shell

    $ aws-spitzel \
        --match '$.errorCode == "AccessDenied"' \
        --match '$.userIdentity.principalId regex ".*:^((?!Alice).)"' \
        --match '$.userIdentity.accountId == "060862059283"' \
        --match '$.sourceIPAddress == "147.161.171.112"' \
        "transfer:List*"

The next example gets all *Get* events on S3 and DynamoDB API calls in the last 
3 hours, which were denied for an IAM user *MyUser* from the principal account 
*060862059283*, that assumed the role *MyRole* in the target account.

.. code-block:: shell

    $ aws-spitzel \
        --match '$.errorCode == "AccessDenied"' \
        --match '$.userIdentity.arn regex ".*/MyRole/MyUser"' \
        --match '$.userIdentity.accountId == "060862059283"' \
        --match ''
        --last-minute 300 \
        's3:Get*' \
        'dynamodb:Get*' \

Piping is supported (warnings and errors are written to *stderr*)

.. code-block:: shell

    while [ 1 -eq 1 ]; do

        echo "getting CloudTrail"

        aws-spitzel \
            --match '$.errorCode != "AccessDenied"' \
            --last-minute 300 \
            "s3:*Acl" \
            "ssm:List*" \
        | \
        jq '.'

        echo "waiting for CloudTrail (3000 seconds)"

        sleep 3000
    done

License
#######

.. literalinclude:: ../LICENSE

.. only:: readme

    .. toctree::
        :hidden:
        :maxdepth: 1

        CHANGELOG

.. only:: not readme

    .. toctree::
        :hidden:
        :maxdepth: 1

        CONTRIBUTING
        SBOM
        NOTICE

.. toctree::
    :hidden:

    samples/index