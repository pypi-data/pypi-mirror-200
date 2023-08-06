import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="posco-lp", # Replace with your own username
    version="1.0.8",
    author="Duhwan Kim",
    author_email="hrdkdh@naver.com",
    description="POSCO Learning Platform Crawling Code Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hrdkdh",
    project_urls={
        "Bug Tracker": "https://github.com/hrdkdh",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages = setuptools.find_packages(exclude = ["docs", "tests*", "dev*"]),
    python_requires=">=3.6",
    install_requires = [
        "requests",
        "urllib3",
        "numpy",
        "pandas",
        "pyautogui",
        "bs4"
    ],
    keywords = ["POSCO", "learning platform", "lp"],
)