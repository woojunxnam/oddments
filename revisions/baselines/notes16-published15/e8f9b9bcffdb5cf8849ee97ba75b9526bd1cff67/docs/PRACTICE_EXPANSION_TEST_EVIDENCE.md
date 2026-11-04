# Practice draft addition: execution evidence

## Successful checked import

https://github.com/woojunxnam/oddments/actions/runs/40024586060

The successful import ran 35 tests: the original 27 structural/content-mapping tests plus eight integration tests. It also ran the reader with real HTTP and file navigation, including real localStorage reload persistence, answer handling, filtering, export/import, all 1,024 desktop renders and all 1,024 question views at 320 pixels. Main-to-status and return navigation, metadata-only status behavior and 320/390/768/1440 layouts passed. This is a software execution record, not an independent legal or realism audit.

The first import run failed its 320-pixel overflow assertion. The reader CSS was repaired to wrap long tokens and constrain flex/grid controls; the assertion was not removed. The second run passed. Question content, keys, explanations and per-question hashes were not changed.

All pre-existing tracked files except `README.md` and `site/index.html` were byte-compared before/after import. Data, audits, notes, release policy and quiz scripts were unchanged. The final diff removes the temporary import workflow and retains read-only continuous QA.

## Existing notes-reader regression

The PR's existing notes-reader browser check initially failed because `.notes-entry-primary` now selected two styled entry buttons. The test now identifies the notes button by its exact `href="notes/"`, explicitly asserts exactly one match, clicks it and retains the destination assertion. No test case was skipped and no notes or quiz application code was modified. `scripts/verify_notes_browser.py` is therefore one additional existing file changed after the import, solely to make its navigation selector destination-specific. The new practice navigation has its own separate browser test.

Local execution of the entire repository test suite exceeded the local command timeout; it is not recorded as a passed full-suite run. Repository-wide QA and notes-reader rerun status are reported separately by their existing GitHub workflows. Physical iOS/Android devices, Safari and independent legal completeness remain untested. Production Pages deployment is a separate step from the successful feature-branch import.
