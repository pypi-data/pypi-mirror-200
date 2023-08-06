import sys
from setuptools import setup, find_packages

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False


except ImportError:
    bdist_wheel = None

if sys.version_info < (3, 0):
    sys.exit("Sorry, Python < 3.0 is not supported")

requirements = ["numpy", "tqdm", "requests", "portalocker"]
if sys.platform == "darwin":
    requirements.append("opencv-python")
else:
    # Newer versions of opencv don't have wheels for i686
    requirements.append("opencv-python<=4.5.1.48")

setup(
    name="daisykit",
    version="0.3.0.0",
    author="vietanhdev",
    author_email="vietanh.dev@gmail.com",
    maintainer="vietanhdev",
    maintainer_email="vietanh.dev@gmail.com",
    description="Toolkit for software engineers to Deploy AI Systems Yourself (DAISY). DaisyKit SDK is the core of models and algorithms, which can be used to develop wrappers and applications for different platforms: mobile, embedded or web browsers.",
    url="https://daisykit.org/",
    classifiers=[
        "Programming Language :: C++",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    license="Apache License 2.0",
    python_requires=">=3.6",
    packages=find_packages(),
    package_dir={"": "."},
    package_data={"daisykit": ["daisykit.cpython-311-darwin.so"]},
    install_requires=requirements,
    cmdclass={"bdist_wheel": bdist_wheel},
)
