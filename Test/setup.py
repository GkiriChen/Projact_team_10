from setuptools import setup, find_namespace_packages

setup(name='Assistant',
      version='1.0',
      description='Assistant bot',
      url='https://github.com/GkiriChen/Projact_team_10',
      author='project participants',
      license='MIT',
      packages=find_namespace_packages(),
      include_package_data=True,
      python_requires='>=3.6',
      entry_points={'console_scripts': ['Assistant=start_page.clean:main']}
)s
