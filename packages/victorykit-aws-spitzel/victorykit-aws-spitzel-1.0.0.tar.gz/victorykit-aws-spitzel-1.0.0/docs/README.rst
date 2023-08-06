.. argparse::
   :module: aws_spitzel.cli
   :func: get_parser
   :prog: aws-spitzel

Getting Started
###############

The following commands are required:

* :code:`python3`
* :code:`pip`
* :code:`pipenv` (Development)

Next, install and make sure the command is available.

.. code-block:: shell

    $ python3 -m pip install victorykit-aws-spitzel

.. code-block:: shell

    $ aws-spitzel --help


Usage Examples
##############

Make sure to configure the AWS API through setting the `well-known AWS CLI 
environment variables <https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html>`_.

The defaults are, to get all events within the last 5 hours

.. code-block:: shell

    $ aws-spitzel 's3:Get*' 'dynamodb:Get*'

same as

.. code-block:: shell

    $ aws-spitzel 's3:Get*' 'dynamodb:*' --last-minute 300

Alternatively, date ranges can be specified:

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