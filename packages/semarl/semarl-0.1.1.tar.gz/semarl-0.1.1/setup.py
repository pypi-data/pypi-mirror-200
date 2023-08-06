import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
	description = fh.read()

setuptools.setup(
	name="semarl",
	version="0.1.1",
	author="Hanz",
	author_email="hanz@godot.id",
	description="Magically turns your semantic git logs to release summary, helpful for release maintainers.",
	description_long=description,
	long_description_content_type="text/markdown",
	url="https://github.com/HanzHaxors/ReleaseSummaryGenerator",
	packages = ["semarl"],
	entry_points={
		"console_scripts": [
			"semarl = semarl.main:run",
		]
	},
	classifiers=[
		"Development Status :: 4 - Beta",
		"Environment :: Console",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: The Unlicense (Unlicense)",
		"Topic :: Documentation",
		"Topic :: Software Development :: Libraries :: Python Modules",
		"Topic :: Software Development :: Version Control :: Git"
	],
	excluded=[
	],
	install_requires=[
		"GitPython==3.1.27"
	],
	python_requires=">=3.6"
)
