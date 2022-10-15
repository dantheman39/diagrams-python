FROM condaforge/mambaforge:4.14.0-0

WORKDIR /app

COPY environment.yml ./
RUN mamba env update -n base --file environment.yml --quiet && conda clean -afy

COPY pyproject.toml ./
COPY poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction

RUN mkdir input
RUN mkdir output
COPY main.py ./
CMD ["python", "main.py"]

