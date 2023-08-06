from setuptools import find_packages, setup

with open('requirements.txt') as f:
    requires = f.read().splitlines()

setup(
    name="beauris",
    version='0.1',
    description="BEAURIS: an automated system for the creation of genome portals",
    author="BEAURIS team",
    author_email="gogepp@inrae.fr",
    url="https://gitlab.com/beaur1s/beauris",
    install_requires=requires,
    packages=find_packages(exclude=['*tests*']),
    license='MIT',
    platforms="Posix",
    entry_points="",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3.9",
    ],
    scripts=[
        'scripts/beauris_check_env',
        'scripts/beauris_commit_lockfiles',
        'scripts/beauris_diff_lockfiles',
        'scripts/beauris_run_on_touched_orgs',
        'scripts/beauris_fetch_locked_artifacts',
    ],
    include_package_data=True,
    package_data={
        'beauris.validation': ['template/schema.yaml'],
        'beauris.workflows': ['*/*sh', 'ansible/**'],
    }
)
