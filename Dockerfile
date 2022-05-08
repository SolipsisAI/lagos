FROM python:3.10 as builder

# install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# copy files
COPY pyproject.toml pdm.lock README.md /project/
COPY lagos/ /project/lagos

# install dependencies and project
WORKDIR /project
RUN pdm install --prod --no-lock --no-editable

# run stage
FROM python:3.10

# retrieve packages from build stage
ENV PYTHONPATH=/app/pkgs
COPY --from=builder /project/__pypackages__/3.10/lib /app/pkgs

WORKDIR /app