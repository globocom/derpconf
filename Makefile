test pyvows:
	@PYTHONPATH=.:$$PYTHONPATH pyvows -v --profile --cover --cover-package=derpconf --cover-threshold=90 vows/

tox:
	@PATH=$$PATH:~/.pythonbrew/pythons/Python-2.7.*/bin/:~/.pythonbrew/pythons/Python-3.0.*/bin/:~/.pythonbrew/pythons/Python-3.1.*/bin/:~/.pythonbrew/pythons/Python-3.2.3/bin/:~/.pythonbrew/pythons/Python-3.3.0/bin/ tox

setup:
	@pip install -Ue .\[tests\]


