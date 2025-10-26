from typing import Any
import sys
import logging
import subprocess

logger = logging.getLogger(__name__)

def pip_install(*args: Any) -> None:
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", *args]
        )
    except subprocess.CalledProcessError as e:
        logger.error(str(e))