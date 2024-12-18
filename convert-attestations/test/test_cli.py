"""Testing module for CLI."""

import filecmp
import os
from pathlib import Path

import pytest

from convert_attestations._cli import main

ARG_ERROR_CODE = 2
_ASSETS = (Path(__file__).parent / "assets").resolve()
assert _ASSETS.is_dir()

# Contains the attestation for pypi_attestations-0.0.18.tar.gz
gh_output_single_attestation = _ASSETS / "gh-output-single-attestation.jsonl"
# Contains the attestations for pypi_attestations-0.0.18.tar.gz and
# pypi_attestations-0.0.18-py3-none-any.whl
gh_output_two_attestations = _ASSETS / "gh-output-two-attestations.jsonl"

# Known good conversions
converted_slsa_attestation_1 = (
    _ASSETS / "pypi_attestations-0.0.18-py3-none-any.whl.slsa.attestation"
)
converted_slsa_attestation_2 = _ASSETS / "pypi_attestations-0.0.18.tar.gz.slsa.attestation"


def test_run_show_help() -> None:
    with pytest.raises(SystemExit) as e:
        main(["--help"])
    assert e.value.code == 0


def test_run_no_arguments_error() -> None:
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == ARG_ERROR_CODE


def test_run_with_single_attestation_in_jsonl(
    capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    main([str(gh_output_single_attestation), "--output-dir", str(tmp_path)])
    captures = capsys.readouterr()
    assert captures.out.startswith("OK: 1 attestations converted and written to")

    files = list(tmp_path.iterdir())
    assert len(files) == 1
    assert filecmp.cmp(files[0], converted_slsa_attestation_2, shallow=False)


def test_run_with_multiple_attestations_in_jsonl(
    capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    expected_len_attestations = 2
    main([str(gh_output_two_attestations), "--output-dir", str(tmp_path)])
    captures = capsys.readouterr()
    assert captures.out.startswith(
        f"OK: {expected_len_attestations} attestations converted and written to "
    )

    files = sorted(tmp_path.iterdir())
    assert len(files) == expected_len_attestations
    assert filecmp.cmp(files[0], converted_slsa_attestation_1, shallow=False)
    assert filecmp.cmp(files[1], converted_slsa_attestation_2, shallow=False)


def test_run_with_non_extant_file(caplog: pytest.LogCaptureFixture) -> None:
    with pytest.raises(SystemExit) as e:
        main(["missing_file.jsonl"])
    assert e.value.code == 1
    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.msg == "Specified file does not exist: missing_file.jsonl"


def test_run_with_invalid_json(caplog: pytest.LogCaptureFixture, tmp_path: Path) -> None:
    invalid_jsonl = tmp_path / "invalid.jsonl"
    with invalid_jsonl.open("w+") as f:
        f.write("notjson")

    with pytest.raises(SystemExit) as e:
        main([str(invalid_jsonl)])
    assert e.value.code == 1

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.msg.startswith("Error while parsing the bundle:")


def test_run_with_unsupported_file(caplog: pytest.LogCaptureFixture) -> None:
    with pytest.raises(SystemExit) as e:
        main([str(converted_slsa_attestation_1)])
    assert e.value.code == 1

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.msg.endswith("Only jsonl files are currently supported")


def test_run_with_unsupported_bundle(caplog: pytest.LogCaptureFixture) -> None:
    unsupported_bundle = _ASSETS / "multiple-signatures.jsonl"

    with pytest.raises(SystemExit) as e:
        main([str(unsupported_bundle)])
    assert e.value.code == 1

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.msg.startswith("Error while converting the bundle to a PyPI attestation")


def test_run_missing_subject_in_attestation(caplog: pytest.LogCaptureFixture) -> None:
    missing_subject_path = _ASSETS / "missing-subject.jsonl"

    with pytest.raises(SystemExit) as e:
        main([str(missing_subject_path)])
    assert e.value.code == 1

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.msg.endswith("expected 'subject' field present in the in-toto statement")


def test_run_invalid_multiple_subjects_in_attestation(caplog: pytest.LogCaptureFixture) -> None:
    multiple_subjects_path = _ASSETS / "multiple-subjects.jsonl"

    with pytest.raises(SystemExit) as e:
        main([str(multiple_subjects_path)])
    assert e.value.code == 1

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.msg.endswith("expected only one subject in the in-toto statement")


def test_run_missing_name_in_subject(caplog: pytest.LogCaptureFixture) -> None:
    no_name_subject_path = _ASSETS / "no-name-subject.jsonl"

    with pytest.raises(SystemExit) as e:
        main([str(no_name_subject_path)])
    assert e.value.code == 1

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.msg.endswith("expected 'name' field present in the in-toto subject")


def test_gha_set_outputs(tmp_path: Path) -> None:
    env_file = tmp_path / "env_file"
    os.environ["GITHUB_ENV"] = str(env_file)
    output_path = tmp_path / "output_dir"
    output_path.mkdir()

    main([str(gh_output_single_attestation), "--output-dir", str(output_path)])

    assert env_file.read_text() == f"output-dir={output_path!s}"
