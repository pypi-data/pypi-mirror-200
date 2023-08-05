from setuptools import setup, find_packages
from pathlib import Path
import os

if __name__ == "__main__":
    with Path(Path(__file__).parent, "README.md").open(encoding="utf-8") as file:
        long_description = file.read()

    def _read_reqs(relpath):
        fullpath = os.path.join(os.path.dirname(__file__), relpath)
        with open(fullpath) as f:
            return [s.strip() for s in f.readlines() if (s.strip() and not s.startswith("#"))]

    REQUIREMENTS = _read_reqs("requirements.txt")

    setup(
        name="core",
        packages=find_packages(),
        include_package_data=True,
        version="0.0.2",
        license="MIT",
        description="ytt_utils",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Youssef Taktak",
        author_email="dz.youssef.taktak@gmail.com",
        url="https://github.com/dzertus/ytt_utils",
        data_files=[(".", ["README.md"])],
        keywords=["tools, scripts , helper"],
        install_requires=REQUIREMENTS,
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Topic :: Python utils modules",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.9",
        ],
    )