import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="my-chat-analytic",
    version="0.1.0",
    author="Emre Tasar",
    author_email="emre@example.com",
    description="Zero-Shot sentiment and intent analysis for an iPhone14 purchase conversation, plus conversational expansions (Task 2).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/detasar/my-chat-analytic",
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "transformers>=4.0.0",
        "torch>=1.9.0",
        "sqlalchemy[asyncio]>=1.4.0",
        "configparser>=5.0.0",
        "jupyter>=1.0.0",
        "aiosqlite"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="nlp zero-shot classification sentiment intent bart mnli conversational",
)
