import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Dict


def _global_venv_dir() -> str:
    """Get the directory where envless stores virtualenvs."""
    if sys.platform.startswith("win32"):
        root = os.path.join(os.path.expanduser("~"), "AppData", "Roaming")
    elif (
        sys.platform.startswith("darwin")
        and os.environ.get("ENVLESS_USE_LIBRARY") == "1"
    ):
        root = os.path.join(os.path.expanduser("~"), "Library", "Application Support")
    else:
        root = os.path.join(os.path.expanduser("~"), ".local", "share")

    return os.path.join(root, "envless", "virtualenvs")


def _env_for_venv(venv_dir: str) -> Dict[str, str]:
    """Construct a process environment with the provided venv active."""
    env = dict(os.environ)
    if (old_path := env.get("_OLD_VIRTUAL_PATH")) is not None:
        env["PATH"] = old_path
    env["VIRTUAL_ENV"] = venv_dir
    curr_path = env.get("PATH")
    if curr_path is not None:
        env["PATH"] = os.path.join(venv_dir, "bin") + os.pathsep + curr_path
    else:
        env["PATH"] = os.path.join(venv_dir, "bin")

    return env


def _find_pip() -> str:
    """Try to find pip next to the current python binary.

    Sometimes this is "pip" sometimes there's only "pip3", sometimes there's only a
    fully versioned one like "pip3.8".
    """
    python_bindir = os.path.dirname(sys.executable)

    plain_pip = os.path.join(python_bindir, "pip")
    if os.path.exists(plain_pip):
        return plain_pip

    pip3 = os.path.join(python_bindir, "pip3")
    if os.path.exists(pip3):
        return pip3

    pip_re = re.compile(r"pip[\d.]+")
    for item in os.listdir(python_bindir):
        if pip_re.match(item):
            return os.path.join(python_bindir, item)

    raise FileNotFoundError(
        "Unable to find pip next to your python interpreter. "
        f"(Checking in {python_bindir}.)"
    )


def script_dependencies(requirements: Dict[str, str], source_file: str) -> None:
    """Declare the dependencies of this script and re-exec python with them loaded.

    Args:
        requirements: a mapping from dependency name to accepted versions. The version
            can be specified in any form understood in a requirements.txt file.
        source_file: pass `__file__` from your script as this parameter
    """

    requirements_str = "\n".join(
        [f"{name} {version}" for name, version in requirements.items()]
    )
    with open(source_file) as f:
        script_contents = f.read()

    script_hash = hashlib.sha256()
    script_hash.update(script_contents.encode("utf-8"))
    script_hash.update(sys.version.encode("utf-8"))
    digest = script_hash.hexdigest()
    venv_name = digest[:16]
    venv_dir = os.path.join(_global_venv_dir(), venv_name)

    if os.environ.get("VIRTUAL_ENV") == venv_dir:
        # venv is already active, so we're done.
        return

    if not os.path.exists(venv_dir):
        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "venv",
                    venv_dir,
                ],
                check=True,
            )
            # We have to use `delete=False` and clean up manually because on Windows,
            # the pip process can't read from this file if we have it open in this one.
            reqs_txt = tempfile.NamedTemporaryFile(
                prefix="requirements_", suffix=".txt", mode="w+", delete=False
            )
            try:
                try:
                    reqs_txt.write(requirements_str)
                finally:
                    reqs_txt.close()
                subprocess.run(
                    [
                        _find_pip(),
                        "install",
                        "-r",
                        reqs_txt.name,
                    ],
                    check=True,
                    env=_env_for_venv(venv_dir),
                )
            finally:
                os.remove(reqs_txt.name)
        except Exception:
            if os.path.exists(venv_dir):
                shutil.rmtree(venv_dir)
            raise
    os.execve(
        sys.executable,
        [sys.executable, source_file, *sys.argv[1:]],
        _env_for_venv(venv_dir),
    )
