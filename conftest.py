"""Collect live suites; verify retained publication trees through closure guards."""

# Published Git trees contain historical copies of the same test modules.
# Dedicated closure suites and the reconstructed old guards validate these bytes.
collect_ignore = ["revisions/baselines"]
