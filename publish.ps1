Remove-Item -r -fo .\dist\*
"Dist ?"
pause
python -m build
"Upload ?"
pause
python -m twine upload .\dist\*