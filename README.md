# Adapt sigstore PyPI GitHub Action

<!--- BADGES: START --->
[![CI](https://github.com/trailofbits/gh-action-adapt-sigstore-pypi/actions/workflows/tests.yml/badge.svg)](https://github.com/trailofbits/gh-action-adapt-sigstore-pypi/actions/workflows/tests.yml)
<!--- BADGES: END --->

This action converts the Sigstore bundles generated by the [attest-build-provenance](https://github.com/actions/attest-build-provenance) GitHub action into PyPI attestations.

## Inputs

See [action.yml](https://github.com/trailofbits/gh-action-adapt-sigstore-pypi/blob/main/action.yml)

```yml
inputs:
  bundles:
    description: >-
      Sigstore bundles to convert. Accepts only .jsonl files.
      May contain a glob pattern or list of paths.
    required: true
  output-dir:
    description: >-
      Directory where to store the converted attestations.
      Optional, if omitted a new temporary directory will be
      created and returned as an output.
    required: false
```

## Outputs

| Name          | Description                                                          | Example           |
| ------------- | -------------------------------------------------------------------- | ------------------|
| `output-dir ` | Absolute path to the directory containing the converted attestations | `/tmp/aao23HKb2/` |

## Example usage

```yml
uses: trailofbits/gh-action-adapt-sigstore-pypi@v1
with:
  bundles: '<PATH TO JSONL FILE>'
```
