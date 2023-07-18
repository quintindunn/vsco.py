from setuptools import setup

VERSION = "0.0.2"
DESCRIPTION = "A Python API wrapper for VSCO."
LONG_DESCRIPTION = "A Python (unofficial) API wrapper for VSCO."

setup(name='vsco',
      version=VERSION,
      description=DESCRIPTION,
      long_description_content_type="text/markdown",
      long_description=LONG_DESCRIPTION,
      author="Quintin Dunn",
      author_email="dunnquintin07@gmail.com",
      url="https://github.com/quintindunn/vsco.py",
      packages=['vsco'],
      keywords=['social media', 'vsco', 'api', 'api wrapper'],
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Operating System :: Microsoft :: Windows :: Windows 10',
            'Programming Language :: Python :: 3',
      ],
      install_requires=["pillow", "requests"]
      )
