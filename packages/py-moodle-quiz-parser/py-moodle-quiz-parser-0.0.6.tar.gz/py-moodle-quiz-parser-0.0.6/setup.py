from setuptools import setup

from MoodleQuizParser import __version__

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setup(
    version=__version__,
    name='py-moodle-quiz-parser',
    description='Package for parsing moodle quiz HTML documents',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/Kononenko-Daniil/py-moodle-quiz-parser',
    author='Daniil Kononenko',
    package_dir={'MoodleQuizParser': 'MoodleQuizParser', 'MoodleQuizParser.Models': 'MoodleQuizParser/Models'},
    packages=['MoodleQuizParser', 'MoodleQuizParser.Models'],
    install_requires=['beautifulsoup4'],
    license="MIT",
    project_urls={
        "Documentation": "https://py-moodle-quiz-parser.readthedocs.io/en/latest/",
        "Source": "https://github.com/Kononenko-Daniil/py-moodle-quiz-parser"
    }
)
