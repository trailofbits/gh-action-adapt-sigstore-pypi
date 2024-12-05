# Adapt sigstore PyPI GitHub Action

This action converts the Sigstore bundles generated by the [attest-build-provenance](https://github.com/actions/attest-build-provenance) GitHub action into PyPI attestations.

## Inputs

## `bundles`

**Required** Sigstore bundles to convert. Accepts only .jsonl files. May contain a glob pattern or list of paths.

## Outputs

## `output-dir`

Directory containing the converted PyPI attestations.

## Example usage

uses: trailofbits/gh-action-adapt-sigstore-pypi@v1
with:
  bundles: '<PATH TO JSONL FILE>'