##################
Splunk Integration
##################

This is a reference implementation of a Splunk integration for AWS CloudTrail 
with *aws-spitzel*.

#. `Deploy an Evaluation Splunk Server`_
#. `Create a new Splunk Index`_
#. `Create a new Splunk HTTP event collector`_
#. `Create a Simple POSIX Shell Integration`_
#. `Create a Simple Python Integration`_


Deploy an Evaluation Splunk Server
==================================

This is just to show up a way of having an evaluatory Splunk server. Should you
already have a Splunk instance, you may skip this step.

.. code-block::

    $ docker run \
        -p 8000:8000 \
        -p 8088:8088 \
        -e "SPLUNK_PASSWORD=qwertz123" \
        -e "SPLUNK_START_ARGS=--accept-license" \
        -d \
        --name so1 \
        splunk/splunk:latest

Wait until the container has fully initialized (about 2 minutes), this is the 
case, once an Ansible playbook run summary is printed. You can tail the logs of 
the container

.. code-block:: shell

    $ docker logs -f so1

.. note::
    In one case, the container crashed after the first init, but worked fine 
    after being restarted. Once it is verified that the container is running, 
    open a shell inside the container.

Now, execute a shell inside the container.

.. code-block::

    $ docker exec -u splunk -it so1 bash

You are now on the Splunk server. Execute the following, so that you have an
authenticated session for every succeeding command and splunk can be found in
the command lookup paths.

.. code-block::

    $ export PATH="$PATH:/opt/splunk/bin"

.. code-block::

    splunk search 'index=_internal' -auth 'admin:qwertz123'

Create a new Splunk Index
=========================

You can create a new index, either through the Splunk web console or running 
the following Splunk CLI command

.. code-block::

    $ splunk add index aws-spitzel-sample
    WARNING: Server Certificate Hostname Validation is disabled. Please see server.conf/[sslConfig]/cliVerifyServerName for details.
    Index "aws-spitzel-sample" added.

Create a new Splunk HTTP event collector
========================================

.. note::
    Dear Splunk, is it true that less and less people are using your CLI for 
    managing Splunk servers? Otherwise, why is it so hard finding documentation
    about using your CLI? Thank you for not blocking archive.org from archiving
    your old documentation though, back in 2019 everything seemed fine... Here 
    is, what i found: `<https://web.archive.org/web/20190925024935/http://dev.splunk.com/view/event-collector/SP-CAAAE7C>`_


You can create a new index, either through the Splunk web console or running 
the following Splunk CLI command:

.. code-block::

    $ splunk http-event-collector create \
        aws-spitzel-sample \
        "Sample Collector for aws-spitzel" \
        -index aws-spitzel-sample \
        -uri "https://localhost:8089"
    WARNING: Server Certificate Hostname Validation is disabled. Please see server.conf/[sslConfig]/cliVerifyServerName for details.
    http://aws-spitzel-sample
            token=4047c5d8-b4af-437d-b0bc-eb2518a73342
            description=Sample Collector for aws-spitzel
            disabled=0
            index=aws-spitzel-sample
            indexes=
            source=
            sourcetype=
            outputgroup=
            use-ack=
            allow-query-string-auth=

Note the token value.

You've now created a new HTTP event collector. Make sure it works by sending 
a test event.

.. code-block:: shell

    $ HEC_TOKEN=4047c5d8-b4af-437d-b0bc-eb2518a73342
    $ curl https://localhost:8088/services/collector \
        --insecure \
        -H "Authorization: Splunk $HEC_TOKEN" -d '{"event": "hello world"}'
    {"text": "Success", "code": 0}

Verify the event exists.

.. code-block:: shell

    $ splunk search 'index=aws-spitze-sample'
    WARNING: Server Certificate Hostname Validation is disabled. Please see server.conf/[sslConfig]/cliVerifyServerName for details.
    hello world

Exit the container shell and run the *curl* test again in order to verify that
the HEC is also reachable from your Docker VM host.

Create a simple POSIX Shell Integration
=======================================

The following will write all existing ``s3:Get*`` event logs to Splunk by 
piping the output of *aws-spitzel*, to a wrapper program, which wraps the 
CloudTrail log event with a Splunk specific wrapper, then each line is treated
as a seperate splunk event and sent via CURL to Splunk asynchronously.

.. code-block:: shell

    aws-spitzel 's3:List' --last-minute 300 \
    | \
    python3 samples/splunk-integration/generic-wrapper.py \
    | \
    while read -r line; do

        curl https://localhost:8088/services/collector \
            --insecure \
            -H "Authorization: Splunk $HEC_TOKEN" -d "$line" \
        &
    done

    wait

.. note::
    There is no HTTP connection error handling in this sample, errors in curl
    would have to be treated in some way.


Create a Simple Python Integration
==================================

This uses nothing more than aws-spitzel and the Python standard library to
forward CloudTrail events to Splunk. It spawns a new thread spawning a new
connection for each event. 

Extend it as needed (e.g. adding client certificate support, etc.).

Use it as a you use aws-spitzel, but additionally you will have to provide
some more flags. Check out ``--help`` for more information.

What you will have to do when running this in production?

Running this on dual-core intel i5 makes it drop a few connections, or not be 
able to connect at all. Since the Splunk server is run as a Docker container on 
the same machine it is difficult to determine the root cause. Probably, one 
must throttle the creation of threads, so that less socket file descriptors are 
open.

`Feuer frei! <https://www.youtube.com/watch?v=ZkW-K5RQdzo>`_

The reference implementation is pretty fast, however can still be optimized by 
e.g. buffering multiple events first and then sending them via a single HTTP 
request. Therefore less threads and connections are used, this would be useful 
for running in less capable runtime environments. On the same dual-core intel 
i5 machine, running Splunk and aws-spitzel together was able to throughput 
~4000 CloudTrail events per minute to Splunk. On a more capable system and 
Splunk running on a different machine, reaching the maximum throughput of 6000 
Events per minute is feasible.

Btw. a CloudTrail event can be a maximum of 256KB in size. So, worst case, 
the aws-spitzel host must be able to handle a 200 Mbps downlink 
throughput (100 x 256KB events per second), if it want's to achieve an overall 
throughput of 6000 events per second.

This reference implementation can also serve as a basis for an AWS Lambda 
implementation triggered by 
`Amazon EventBridge on a schedule <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_
To avoid missing out on any events, make sure to store the actual timestamp of
the last function call as to be able to calculate a correction and setting 
``--from`` and ``--to`` date range inputs explicitly. It's doubtful, that all 
AWS services run on equally (NTP) time-synchronized systems, and that Amazon 
EventBridge will always trigger on the nanosecond dot. That's what the 
correction would be needed for. It should work like: "What time is it, when was 
i supposed to be triggered, and how much further do i have to go back in time to 
also get the events that wouldn't be covered by me if i actually followed the 
order of going back exactly 10 minutes from now?"

.. code-block:: shell

    $ python3 samples/splunk-integration/standalone.py "s3:*" \
        --splunk-hec-token $HEC_TOKEN \
        --splunk-hec-hostname localhost \
        --splunk-hec-port 8088