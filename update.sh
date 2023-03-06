# removing distribution files
rm -rf dist
# generate new distribution file
python3 setup.py sdist
# upload to pypi
python3 -m twine upload --repository pypi dist/*