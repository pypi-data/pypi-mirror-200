import os
import shutil
import sys

import setuptools

VERSION = (0, 0, 6)


def clear(clear_dist_dir=False):
    if clear_dist_dir and os.path.exists("dist"):
        shutil.rmtree("dist", ignore_errors=True)
    if os.path.exists("build"):
        shutil.rmtree("build", ignore_errors=True)
    if os.path.exists("joeypan.egg-info"):
        shutil.rmtree("joeypan.egg-info", ignore_errors=True)
    for root, ds, fs in os.walk("joeypan"):
        for d in ds:
            if d == "__pycache__":
                shutil.rmtree(os.path.join(root, d))
        for f in fs:
            if f and f[-4:] == ".pyc":
                os.remove(os.path.join(root, f))


def build():
    clear(True)
    print("DELETE BUILD CACHE DONE")
    current_version = ".".join(str(item) for item in VERSION)
    md_name = current_version + ".md"
    doc_path = os.path.join(os.getcwd(), "release_note", md_name)
    if not os.path.exists(doc_path):
        print(f"RELEASE DOC NOT FOUND: {md_name}")
    with open(doc_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()

    setuptools.setup(
        name="joeypan",
        version=current_version,
        author="elijahxb",
        package_dir={"joeypan": "joeypan"},
        install_requires=["pydantic==1.10.6"],
        author_email="elijahxb@outlook.com",
        description="A small package for web framework",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="http://www.joeypan.cn:9830/Elijahxb/joeypan",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    )
    clear()
    print("BUILD SUCCESS")


def publish():
    build()
    python_path = sys.executable
    upload_cmd = f'"{python_path}" -m twine upload --repository pypi dist/*'
    try:
        import twine
        print(upload_cmd)
    except ImportError as _:
        os.system(f"{sys.executable} -m pip install twine")
        print("PUBLISH MODULE TO PYPI......")
        print(upload_cmd)


def dispatch():
    support_args = ["build", "publish"]
    if len(sys.argv) == 1:
        sys.argv.append("build")
    intent = str(sys.argv[1])
    if intent not in support_args:
        print("WARN: ONLY SUPPORT build/publish")
    if intent == "publish":
        args = " ".join(sys.argv)
        real_args = args.split("publish")
        real_args.insert(1, "build")
        sys.argv = sys.argv = [sys.argv[0], "sdist", "bdist_wheel"]
        publish()
    elif intent == "build":
        sys.argv = [sys.argv[0], "sdist", "bdist_wheel"]
        build()


dispatch()
