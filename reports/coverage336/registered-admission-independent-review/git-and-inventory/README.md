# Independent registered-admission hardening addendum

The original R1–R4 reproductions are fixed at current module SHA `d56f1c64fa57df30f89b42fed8aa7b4adbeb6cbfafd7104e92f3b326398138a6`. The100 focused tests passed in6.52 seconds. The prior sealed review is unchanged.

**Still not ready for admission.** Three residual P2 findings remain: untracked publishable UI source is accepted; M/N/E metadata need not exist in the committed HEAD; and the public registered coverage API can return caller fields without matching the cached native K. Exact registry hashes remain required, and no present production authorization bypass or real enrollment is claimed.

**H1: A post-validation handle still permits an untracked publishable UI file**

require_context now rejects dirty tracked files and new protected inventory, but site/verified-law/unlisted.js is untracked and outside the enumerated source maps. It is accepted with unchanged HEAD/code/known seals. publish_practice.py copies the entire site tree, so that extra disk source is publishable despite not being part of reviewed Git content.

Reject untracked nonignored source, with only the exact computed coverage K as an explicit validated exception. Also compare the entire publishable site disk inventory and bytes against HEAD so ignored publishable additions cannot evade the check.

Probe limit: A test-only already-valid-token fixture was used with the actual inventory function. No production token was minted and no site generation/publication occurred.

**H2: Manifest, notes context and enrollment are not required to be committed HEAD blobs**

The new whole-delta helper uses subset allowlists. A HEAD containing only the registry change passes while exact M/N/E JSON files exist solely as untracked disk inputs. Current-source hash checks bind those bytes to registry hashes, but no later check binds them to HEAD regular blobs. The registry can therefore claim a registered context that a clean clone of that HEAD cannot reconstruct.

Require all M/N/E paths to exist as regular HEAD blobs with exact raw bytes equal to the reviewed/current bindings. Validate the exact required post-content path set, retaining K only as a separately calculated optional output.

Probe limit: Actual Git-delta/current-reader helpers were exercised; the production registry remains empty and no complete native registration was run. Exact SHA authorization is not bypassed.

**H3: The public registered coverage API can return caller data as current native coverage**

coverage_snapshot checks selected counts through _coverage_value, then copies the caller coverage object into current_native_coverage. A caller-added field survives and the returned K can differ from context._expected_coverage. The actual artifact producer path recomputes correctly, and a later existing-K consumer check rejects the forged value; those do not bind the public API return itself.

Only return registered coverage when the full supplied coverage, guide and payload match the actual producer values cached at mint. Keep the internal producer calculation path separate from public caller-input validation and unchanged legacy defaults.

Probe limit: An explicit setup mock stands in for the already-validated context to test the actual public API value predicate only. This does not obtain registry authorization, native PASS, admission or release.

The new DERIVED4 before/after and actual-producer comparison logic is present; all four exact comparison predicates reject forged values. The K hash direction avoids a manifest self-cycle, and its consumer rejects a mismatched existing file. These are code/predicate checks, not a successful real30–40 admission.

Production registry is empty. CI routing, historical fixed-count integration, positive registered E2E and later context lifecycle remain unfinished. No source edits, whole native/1781/full-pytest/regeneration run, commit, push, admission, audit, CI or release credit.

Exact11 file hashes and source copies are in review-addendum.json and reviewed-source/.
