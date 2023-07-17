from setuptools import setup

setup(name='vsco',
      version="0.0.1",
      description="""A api wrapper for vsco.""",
      author="Quintin Dunn",
      author_email="dunnquintin07@gmail.com",
      url="",
      packages=['vsco'],
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Operating System :: Microsoft :: Windows :: Windows 10',
            'Programming Language :: Python :: 3',
      ],
      install_requires=["pillow", "requests"]
)
