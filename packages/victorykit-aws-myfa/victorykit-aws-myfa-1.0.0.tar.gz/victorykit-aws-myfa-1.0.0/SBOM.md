# SOFTWARE BILL OF MATERIALS

```ini
[metadata]
name = victorykit-aws-myfa
author = Tiara Rodney (victory-k.it)
author_email = py-aws-mfa@victoryk.it
description = Convenience wrapper for MFA-authenticated AWS STS sessions
long_description = file: README.md
long_description_content_type = text/markdown
url = https://victorykit.bitbucket.io/py-aws-myfa
project_urls = 
	Bug Tracker = https://bitbucket.org/victorykit/py-aws-myfa/jira
classifiers = 
	Development Status :: 4 - Beta
	Environment :: Other Environment
	Intended Audience :: Developers
	Topic :: Utilities
    Topic :: Security
	Programming Language :: Python :: 3.7
	Programming Language :: Python :: 3.8
	Programming Language :: Python :: 3.9
	Operating System :: OS Independent
	License :: Other/Proprietary License

[options]
zip_safe = true
package_dir = 
	=src
python_requires = >=3.7
test_suite = test
packages = find:

[options.entry_points]
console_scripts = 
	aws-myfa = aws_myfa.__main__:main

[options.packages.find]
where = src
```

```ini
[[source]]
url = 'https://pypi.python.org/simple'
verify_ssl = true
name = 'pypi'

[requires]
python_version = '3'

[scripts]
"docgen" = "tox"
"htmldocgen" = "tox -e htmldocgen"
"mddocgen" = "tox -e mddocgen"
"pdfdocgen" = "tox -e pdfdocgen"

[dev-packages]
tox                    = '==3.23.0'

[packages]
aws-myfa = {editable = true, path = "."}
```

```ini
[tox]
skipsdist = true
minversion = 3.7.0
isolated_build = True
envlist = lint, mddocgen, build, htmldocgen


[testenv:lint]
description = lint with pylint
setenv = PYTHONPATH = {toxinidir}/src
deps =
    {toxinidir}
    pylint >= 2.12.2, < 3
commands =
    python3 -m pylint {toxinidir}/src {posargs}


[testenv:format]
description = format code
basepython = python3
deps =
    autopep8 >= 1.6.0, < 2
commands =
    python3 -m autopep8 -v src/ {posargs}


[testenv:build]
description = build and package
basepython = python3
setenv = PYTHONPATH = {toxinidir}/src
deps = 
    build >= 0.5.1, < 1
commands =
    python3 -m build {posargs}


[testenv:htmldocgen]
description = build HTML documentation
basepython = python3
allowlist_externals =
    sphinx-build
deps = 
    sphinx >= 4.3.2, < 5
    furo
    sphinx-argparse
    {toxinidir}
setenv = 
    PLANTUML_LIMIT_SIZE=20000
commands =
    sphinx-build -d "{toxinidir}/build/docs/_tree/html" docs "build/docs/html" --color -W -bhtml {posargs}


[testenv:mddocgen]
description = build markdown repository documentation
basepython = python3
allowlist_externals =
    sphinx-build
deps = 
    sphinx >= 4.3.2, < 5
    sphinx-markdown-builder >= 0.5.4, < 1
    sphinx-argparse
    {toxinidir}
commands =
    sphinx-build -d "{toxinidir}/build/docs/_tree/_" docs {toxinidir} --color -W -bmarkdown -treadme {posargs}


[testenv:pdfdocgen]
description = build single PDF document documentation
basepython = python3
allowlist_externals =
    sphinx-build
deps = 
    sphinx >= 4.3.2, < 5
    furo
    sphinx-argparse
    rst2pdf >= 0.100, < 1
    {toxinidir}
commands =
    sphinx-build -d "{toxinidir}/build/docs/_tree/_" docs "dist/docs/pdf" --color -W -bpdf -tpdf {posargs}


[testenv:publish]
description = publish to pypi repository
passenv =
    #https://twine.readthedocs.io/en/stable/#environment-variables
    TWINE_USERNAME
    TWINE_PASSWORD
    TWINE_REPOSITORY
    TWINE_REPOSITORY_URL
    TWINE_CERT
    TWINE_NON_INTERACTIVE
deps = 
    twine
commands =
    python3 -m twine upload "dist/*"


[testenv:publish-docs]
description = publish documentation
setenv =
    tmppath = {envdir}/git/vicytorykit.bitbucket.io
passenv =
    #https://support.atlassian.com/bitbucket-cloud/docs/variables-and-secrets/
    BITBUCKET_REPO_SLUG
allowlist_externals =
    /bin/sh
    /bin/rm
    /bin/cp
    /bin/mkdir
    /usr/bin/git
commands =
    python3 -c "exec('import os\nif \'BITBUCKET_REPO_SLUG\' not in os.environ.keys(): exit(1)')"
    rm -rf {env:tmppath}
    git clone git@bitbucket.org:victorykit/victorykit.bitbucket.io.git {env:tmppath}
    mkdir -p "{env:tmppath}/{env:BITBUCKET_REPO_SLUG}"
    cp -r build/docs/html/. "{env:tmppath}/{env:BITBUCKET_REPO_SLUG}"
    sh -c "cd {env:tmppath}; git add {env:BITBUCKET_REPO_SLUG}"
    sh -c "cd {env:tmppath}; git -c 'user.name=victoryk.it Bot' -c 'user.email=commits-noreply@victoryk.it' commit -m 'updated {env:BITBUCKET_REPO_SLUG}'"
    sh -c "cd {env:tmppath}; git push"
```
