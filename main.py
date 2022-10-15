import typing as T
import asyncio
from glob import glob
import logging
import os
from pathlib import Path

logging.basicConfig()
DEFAULT_LOGGER = logging.getLogger(__name__)
DEFAULT_LOGGER.setLevel(logging.DEBUG)


async def run_subprocess(
    program: str | bytes | os.PathLike[str] | os.PathLike[bytes],
    *args: str | bytes | os.PathLike[str] | os.PathLike[bytes],
    logger: logging.Logger = None,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
) -> T.Tuple[asyncio.subprocess.Process, T.List[str]]:
    process = await asyncio.create_subprocess_exec(
        program,
        *args,
        stdout=stdout,
        stderr=stderr,
    )
    errors = []
    while process.stdout and process.stderr and process.returncode is None:
        await asyncio.sleep(0.5)
        async for line in process.stdout:
            logger.debug(line.decode("utf-8").rstrip())
        async for line in process.stderr:
            err = line.decode("utf-8").rstrip()
            errors.append(err)
            logger.debug(err)
    return process, errors


async def main(outdir: Path, logger: logging.Logger):
    for diagram_script in glob("input/*diagram.py"):
        logger.info(f"running {diagram_script}")
        process, _ = await run_subprocess(
            "python", diagram_script, outdir, logger=logger
        )
        if process.returncode != 0:
            logger.error(f"error running file '{diagram_script}'")
        else:
            logger.info(f"finished {diagram_script}")


if __name__ == "__main__":
    outdir = Path.cwd() / "output"
    if outdir_env := os.getenv("OUTDIR"):
        outdir = Path(outdir_env)
    asyncio.run(main(outdir=outdir, logger=DEFAULT_LOGGER))
