# Architecture

## SBOM Generation and Validation

### SPDX 3.0.1 Validation Status

Syft (v1.51.0) is capable of emitting SPDX 3.0.1 SBOMs using the `-o spdx-json@3` flag. However, as of 2026-08-24, there is no scriptable validator readily available in our pipeline that can read and validate SPDX 3.0.1 documents. Tools like `sbomqs`, `pyspdxtools`, and `protobom` either do not support SPDX 3.0.1 in their stable releases or are still in experimental stages for this specification. Therefore, while we can generate SPDX 3.0.1 SBOMs, we cannot currently perform automated validation within our CI pipeline.
