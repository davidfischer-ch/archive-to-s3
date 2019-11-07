#!/usr/bin/env bash

warning()
{
    echo "[WARNING] $1" 1>&2
    echo 'press enter to continue or ctrl+c to exit ...'
    read a
}

error()
{
    echo "[ERROR] $1" 1>&2
    exit $2
}

version=$(cat 'archive_to_s3/__init__.py' | grep '__version__ = ' | cut -d'=' -f2 | sed "s:'::g;s: ::g")
echo "Release version $version, press enter to continue ..."
read a

git push || error 'Unable to push to GitHub' 1
git tag "$version" && git push origin "$version" || error 'Unable to add release tag' 2

rm -rf dist/ 2>/dev/null
python3 setup.py sdist bdist_wheel || error 'Unable to build for Python 3' 3
twine upload dist/* --skip-existing || error 'Unable to upload to PyPI' 4
