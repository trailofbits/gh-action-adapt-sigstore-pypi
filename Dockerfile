FROM ghcr.io/astral-sh/uv:0.5-python3.13-bookworm-slim

COPY convert-attestations.py /convert-attestations.py

ENTRYPOINT ["uv", "run", "--prerelease=allow", "/convert-attestations.py"]
