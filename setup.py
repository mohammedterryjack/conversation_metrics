import os

from setuptools import setup


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths


setup(
    name="conversation_metrics",
    version="1.0.3",
    description="Automatic Evaluation of Conversation Quality",
    author="Mohammed Terry-Jack; Anh Phuong Le",
    author_email="m.jack@oxolo.com; a.phuong@oxolo.com",
    packages=["conversation_metrics"],
    package_data={"conversation_metrics": package_files("conversation_metrics")},
    install_requires=[
        "transformers",
        "torch",
        "matplotlib",
        "scipy",
        "spacy",
    ],
)
