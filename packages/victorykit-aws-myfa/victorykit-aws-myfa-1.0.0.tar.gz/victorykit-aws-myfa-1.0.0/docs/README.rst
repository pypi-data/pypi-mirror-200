.. argparse::
   :module: aws_myfa.__main__
   :func: get_parser
   :prog: aws-myfa

Getting Started
###############

The following commands are required:

* :code:`python3`
* :code:`pip`
* :code:`pipenv` (Development)

Next, install and make sure the command is available.

.. code-block:: shell

    $ python3 -m pip install victorykit-aws-myfa

.. code-block:: shell

    $ aws-myfa --help

Alternatively, you can clone the repository and install via pipenv

.. code-block:: shell

    $ mkdir aws-myfa && cd $_ && git clone git@bitbucket.org:victorykit/py-aws-myfa.git .

.. code-block:: shell

    $ python3 -m pipenv install -d

.. code-block:: shell

    $ python3 -m pipenv run aws-myfa --help

The documentation can be built through the pipenv enironment

.. code-block:: shell

    $ python3 -m pipenv run htmldocgen

.. code-block:: shell

    $ python3 -m pipenv run mddocgen



Usage Examples
##############

A bad example:

.. code-block:: shell

    aws-mfa \
        --mfa-device-arn "arn:aws:iam::XXXXXXXXXXXX:mfa/me" \
        --yes

This will use your default profile and overwrite it. You'll have to get new 
AWS IAM user access keys afterwards.

Do this instead:

.. code-block:: shell

    aws-myfa \
        --mfa-device-arn 'arn:aws:iam::XXXXXXXXXXXX:mfa/me' \
        'my-new-mfa-authenticated-profile-name' \
        'my-mfa-device-owning-principal-profile-name' \

You will use the AWS CLI profile named 
``my-mfa-device-owning-principal-profile-name``  from your ~/.aws/config file 
to get an AWS STS session token and create or update a profile named 
``my-new-mfa-authenticated-profile-name``, which links to source profile in 
~/.aws/credentials named ``my-new-mfa-authenticated-profile-name``.

Add the ``--yes`` flag to acknowledge all yes/no prompts.

If you want to update an existing MFA profile you've already created, it is
sufficient to do the following:

.. code-block:: shell

    aws-myfa -y 'my-new-mfa-authenticated-profile-name'

View this help documentation:

.. code-block:: shell

    python3 aws-myfa --help

Create a system daemon or shell script (CRON, etc.) to do this recurrently, 
there is open-source software for virtual MFA devices to do this. Will your 
security officer be mad at you for doing this? Probably... The point of MFA is, 
to have multiple authentication factors from multiple systems. The greater the 
separation between the systems, the better. Having both, a password and a 
token-device on the same physical system is bad enough, but having it in the 
same software system (e.g. like 1Password, Bitwarden, etc.) is really bad... 
It's annoying sometimes, but there is no better option as of yet.

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