# Independent consumer hardening review

H1–H3 original reproducers are fixed at module SHA `2b7af2165ce0f2cba103d32aa1a643d237889f3a1d5f5cd2971de84d8995c3c8`. The103 focused tests passed in7.25 seconds. Eleven independent tiny consumer probes confirm untracked/ignored UI rejection, committed M/N/E bytes, full coverage/payload/guide value matching, deepcopy and computed-K checks.

One P2 remains: Git index assume-unchanged/skip-worktree flags hide tracked UI byte changes from git diff. The current helper checks only disk path membership against HEAD and therefore accepts changed site/app.js bytes; skip-worktree also permits a symlink at that tracked path. The real synthetic Git/helper reproducer is saved separately. Compare direct regular disk preimages with immutable HEAD blob bytes, rejecting every symlink component, rather than treating Git index dirty reporting as content authentication.

No current production registry authorization bypass was demonstrated. Production registry is empty and actual status is NO_ENROLLED_ADMISSION. Actual30–40 positive E2E, CI routing and future context lifecycle remain unverified, so NOT_READY. No source edits, whole native/1781/full pytest/regeneration run, commit, push, admission or release action. The prior addendum and sealed files remain unchanged.
