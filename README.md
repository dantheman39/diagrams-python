# diagrams-python

This image includes python, the python package [diagrams](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwi3_7re-eL6AhXOD1kFHcdRDz8QFnoECBMQAQ&url=https%3A%2F%2Fgithub.com%2Fmingrammer%2Fdiagrams&usg=AOvVaw30cWNpLcVUe2aRYdCDEqpx)
and [graphviz](https://www.graphviz.org/), a dependency of the diagrams package.
I made this image to make it easy for my non-python colleagues to build diagrams
without having to fuss with conda / mamba / pipenv etc, and to be able to build
diagrams in CI.

# Quickstart

The idea is that you mount a local directory to "/app/input" and to "/app/output",
and the python script here will search for python files in "/app/input" ending in `diagram.py`,
and call them.

To easily get your output files, each of your input files should accept a command-line
argument that indicates the output directory, because the main.py file here will
call each file with "/app/output" (this makes it so your script still works if not running
in Docker). If you've mounted a local folder to /app/output, then
your diagrams will appear there. For example, here's a file `goodstuff_diagram.py`:

```python
from pathlib import Path
import sys

from diagrams import Diagram
from diagrams.gcp.storage import Storage


def create_diagram(output_dir: Path) -> None:
    outfile = Path(output_dir, "goodstuff")
    with Diagram("Good Stuff", show=False, filename=str(outfile)):
        Storage("Bucket")

 
if __name__ == "__main__":
    output_dir = Path(__file__).parent
    if len(sys.argv) > 1:
        output_dir = Path(sys.argv[1])
    create_diagram(output_dir=output_dir)
```

Sample command:

```shell
docker run -it \
  --volume "/some/input/folder:/app/input" \
  --volume "/some/output/folder:/app/output" \
  dantheman39/diagrams-python
```

See the docker-compose file. If the volumes are written correctly, it's
as simple as `docker-compose up`.