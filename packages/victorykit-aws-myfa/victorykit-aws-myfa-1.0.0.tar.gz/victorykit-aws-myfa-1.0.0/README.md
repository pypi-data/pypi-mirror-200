Create and maintain AWS CLI profiles requiring MFA-authenticated STS sessions
with ease.

If you don’t know what this script is for, don’t waste your time, you’ll 
probably won’t need it.

A bad example:

> python3 aws-mfa-profile.py 

>     –mfa-device-arn “arn:aws:iam::XXXXXXXXXXXX:mfa/me”         –yes

This will use your default profile and overwrite it. You’ll have to get new 
AWS IAM user access keys afterwards.

Do this instead:

> python3 aws-mfa-profile.py 

>     ”my-new-mfa-authenticated-profile-name” “my-mfa-device-owning-principal-profile-name” –mfa-device-arn “arn:aws:iam::XXXXXXXXXXXX:mfa/me”

You will use the AWS CLI profile named 
`my-mfa-device-owning-principal-profile-name`  from your ~/.aws/config file 
to get an AWS STS session token and create or update a profile named 
`my-new-mfa-authenticated-profile-name`, which links to source profile in 
~/.aws/credentials named `my-new-mfa-authenticated-profile-name`.

Add the `--yes` flag to acknowledge all yes/no prompts.

If you want to update an existing MFA profile you’ve already created, it is
sufficient to do the following:

> python3 aws-mfa-profile.py -y “my-new-mfa-authenticated-profile-name”

View this help documentation:

```shell
python3 aws-mfa-profile.py --help
```

Create a system daemon or shell script (CRON, etc.) to do this recurrently, 
there is open-source software for virtual MFA devices to do this. Will your 
security officer be mad at you for doing this? Probably… The point of MFA is, 
to have multiple authentication factors from multiple systems. The greater the 
separation between the systems, the better. Having both, a password and a 
token-device on the same physical system is bad enough, but having it in the 
same software system (e.g. like 1Password, Bitwarden, etc.) is really bad… 
It’s annoying sometimes, but there is no better option as of yet.

Use it at your own discretion, but try not to automate too much of the 
authentication process, PLEASE!

Want to extend the functionality? Make main() small again!


```default
usage: aws-myfa [-h] [--config FILE] [--yes] [--mfa-device-arn FILE] [--mfa-token-code TOKEN_CODE] [--credentials FILE] TARGET_PROFILE [PRINCIPAL_PROFILE]
```

# Positional Arguments

# Named Arguments

Your current AWS CLI profiles will be retained.


# Getting Started

The following commands are required:


* `python3`


* `pip`


* `pipenv` (Development)

Next, install and make sure the command is available.

```shell
$ python3 -m pip install victorykit-aws-myfa
```

```shell
$ aws-myfa --help
```

Alternatively, you can clone the repository and install via pipenv

```shell
$ mkdir aws-myfa && cd $_ && git clone git@bitbucket.org:victorykit/py-aws-myfa.git .
```

```shell
$ python3 -m pipenv install -d
```

```shell
$ python3 -m pipenv run aws-myfa --help
```

The documentation can be built through the pipenv enironment

```shell
$ python3 -m pipenv run htmldocgen
```

```shell
$ python3 -m pipenv run mddocgen
```

# Usage Examples

A bad example:

```shell
aws-mfa \
    --mfa-device-arn "arn:aws:iam::XXXXXXXXXXXX:mfa/me" \
    --yes
```

This will use your default profile and overwrite it. You’ll have to get new
AWS IAM user access keys afterwards.

Do this instead:

```shell
aws-myfa \
    --mfa-device-arn 'arn:aws:iam::XXXXXXXXXXXX:mfa/me' \
    'my-new-mfa-authenticated-profile-name' \
    'my-mfa-device-owning-principal-profile-name' \
```

You will use the AWS CLI profile named
`my-mfa-device-owning-principal-profile-name`  from your ~/.aws/config file
to get an AWS STS session token and create or update a profile named
`my-new-mfa-authenticated-profile-name`, which links to source profile in
~/.aws/credentials named `my-new-mfa-authenticated-profile-name`.

Add the `--yes` flag to acknowledge all yes/no prompts.

If you want to update an existing MFA profile you’ve already created, it is
sufficient to do the following:

```shell
aws-myfa -y 'my-new-mfa-authenticated-profile-name'
```

View this help documentation:

```shell
python3 aws-myfa --help
```

Create a system daemon or shell script (CRON, etc.) to do this recurrently,
there is open-source software for virtual MFA devices to do this. Will your
security officer be mad at you for doing this? Probably… The point of MFA is,
to have multiple authentication factors from multiple systems. The greater the
separation between the systems, the better. Having both, a password and a
token-device on the same physical system is bad enough, but having it in the
same software system (e.g. like 1Password, Bitwarden, etc.) is really bad…
It’s annoying sometimes, but there is no better option as of yet.

# License

```default
DL-DE->BY-2.0

Datenlizenz Deutschland – Namensnennung – Version 2.0

(1) Jede Nutzung ist unter den Bedingungen dieser „Datenlizenz Deutschland – Namensnennung – Version 2.0" zulässig.

Die bereitgestellten Daten und Metadaten dürfen für die kommerzielle und nicht kommerzielle Nutzung insbesondere

vervielfältigt, ausgedruckt, präsentiert, verändert, bearbeitet sowie an Dritte übermittelt werden;
mit eigenen Daten und Daten Anderer zusammengeführt und zu selbständigen neuen Datensätzen verbunden werden;
in interne und externe Geschäftsprozesse, Produkte und Anwendungen in öffentlichen und nicht öffentlichen elektronischen Netzwerken eingebunden werden.

(2) Bei der Nutzung ist sicherzustellen, dass folgende Angaben als Quellenvermerk enthalten sind:

Bezeichnung des Bereitstellers nach dessen Maßgabe,
der Vermerk „Datenlizenz Deutschland – Namensnennung – Version 2.0" oder „dl-de/by-2-0" mit Verweis auf den Lizenztext unter www.govdata.de/dl-de/by-2-0 sowie
einen Verweis auf den Datensatz (URI).
Dies gilt nur soweit die datenhaltende Stelle die Angaben 1. bis 3. zum Quellenvermerk bereitstellt.

(3) Veränderungen, Bearbeitungen, neue Gestaltungen oder sonstige Abwandlungen sind im Quellenvermerk mit dem Hinweis zu versehen, dass die Daten geändert wurden.

Data licence Germany – attribution – version 2.0

(1) Any use will be permitted provided it fulfils the requirements of this "Data licence Germany – attribution – Version 2.0".

The data and meta-data provided may, for commercial and non-commercial use, in particular

be copied, printed, presented, altered, processed and transmitted to third parties;
be merged with own data and with the data of others and be combined to form new and independent datasets;
be integrated in internal and external business processes, products and applications in public and non-public electronic networks.

(2) The user must ensure that the source note contains the following information:

the name of the provider,
the annotation "Data licence Germany – attribution – Version 2.0" or "dl-de/by-2-0" referring to the licence text available at www.govdata.de/dl-de/by-2-0, and
a reference to the dataset (URI).
This applies only if the entity keeping the data provides the pieces of information 1-3 for the source note.

(3) Changes, editing, new designs or other amendments must be marked as such in the source note.

URL: http://www.govdata.de/dl-de/by-2-0
```
