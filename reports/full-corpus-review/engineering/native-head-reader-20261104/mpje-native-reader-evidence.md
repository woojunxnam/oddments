Candidate: 612af5ebc252838748d5069bf2fd07f74414d2b7
Branch/worktree: perf/native-head-reader / /workspace/mpje-native-head-reader
Base: 4583316eb77eb35167fdd6b6a87b7c594b4c34cb
Data tree used only for reads: /workspace/mpje-pr193-qa at 2a7f76e5a2cb785a60cf78dc125bd4a7715f4f7a

Change: extract closure.head_bytes_match; reuse the same exact-HEAD blob-index comparison in census.disk_reader and metadata.committed; enclose load_metadata in the existing head_snapshot. Preserve safe_path/output validation, raw-SHA checks, census SHA-before-HEAD ordering, record/claim/evidence validation, and existing metadata raw-byte capture cache. No verdict, migration, mtime, or guard cache was added.

Actual native metadata comparison (metadata result plus every captured source binding):
- Original QA code: 227.783457376 seconds; git show 22,343; rev-parse 2; ls-tree 1.
- Candidate code: 89.564827569 seconds; git show 302; rev-parse 2; ls-tree 1.
- Wall speedup 2.5432x under concurrent workloads; git show calls reduced 98.6483%.
- Both result files have 483,277 bytes and SHA256 5473b1053fe0d609d2080f745b9c73bcd86019df7b3efca93e595c8bf5f3aa58; cmp returned 0.
- Metrics/results: /workspace/scratch/mpje-native-reader-metadata-{before,after}.{metrics,result}.json
- Harness: /workspace/scratch/mpje-native-reader-benchmark.py. Calls native functions; only writes its output in scratch.

Verification:
- Final new regression module: 13 passed in 0.84s. Includes preserved-mtime/size disk mutation, caller-supplied altered SHA, wrong SHA, same-content symlink, HEAD advance, nested snapshot reuse, cross-root isolation, fallback exact-HEAD check, metadata result/source-binding equivalence.
- Existing native-focused synthetic suites: census 25, body 51, inactive 40, sibling 2, closure 32, held 17 = 167 passed.
- Broad run included earlier 11 new tests (178 passed overall) and 11 metadata fixture setup errors: all FileNotFoundError for immutable preimages excluded by sparse checkout. Four actual-root tests deselected. No test assertion failed.
- Broad run JUnit: /workspace/scratch/mpje-native-head-reader-focused.xml
- Candidate worktree is clean; main/QA were not edited by this candidate task.

Native expected_migration against exact QA2a7 completed in 699.005082185s. Its complete value equals the committed revisions/notes/protected-migration-held-n1.json manifest, including all 1,721 source_bindings. Canonical result: 285,161 bytes, SHA256 f187bc788812a4cff112e4e50c19342fc2f2950b33068ec538e18052cff05918. Parent-process Git calls: rev-parse2 / ls-tree1 / show1933 (subprocess calls inside children are not counted). This exact-data-root computation invoked unmodified QA build_full_corpus_review.py and build_representative_rewrites.py children, so its full wall time is conservative and does not measure the complete integrated candidate path. Result/metrics: /workspace/scratch/mpje-native-reader-migration-after.{result,metrics}.json.
