test pyvows:
	@PYTHONPATH=.:$$PYTHONPATH pyvows -v --profile --cover --cover_package=derpconf --cover_threshold=90 vows/
