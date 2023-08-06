from setuptools import setup

readme_content = None
with open("README.md") as f:
      readme_content = f.read()

setup(name='qtpip',
      version='0.0',
      description="A pip wrapper to install commercial Qt for Python wheels",
      url="https://qt.io/qt-for-python",
      license = "Qt Commercial",
      author = "Qt for Python Team",
      author_email = "pyside@qt-project.org",
      long_description = readme_content,
      long_description_content_type = "text/markdown")
