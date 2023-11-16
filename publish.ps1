rm -r -fo .\dist\*
"Dist to ./dist ?"
pause
python setup.py sdist bdist_wheel
"Upload ?"
pause
python -m twine upload .\dist\*