import setuptools

setuptools.setup(
    name = "PolyglotIQ",
    version = "0.0.8",
    author = "ArtanisTheOne",
    author_email = "ledragio@gmail.com",
    description = "A language identification package which is backed by the mT5 Neural Network",
    long_description = "Language detection library built for RitaBot which uses a finetuned version of mT5 (multilingual t5), a seq-to-seq model, to predict the language of a given text. Model is supported using CTranslate2, an efficient engine for Transformer models for CPU/GPU.",
    long_description_content_type = "text/markdown",
    url = "https://pypi.org/project/PolyglotIQ/",
    classifiers = [
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
    ],
    packages = setuptools.find_packages(exclude=["tests", "scripts"]),
    python_requires = ">=3.7"
)