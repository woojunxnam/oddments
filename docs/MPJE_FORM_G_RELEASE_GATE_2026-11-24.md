# Form G release gate — 2026-11-24

Status: content/source review and structural gate passed; browser regression and deployment are separate pending gates. AI source-text review only; not independent pharmacy/legal expert certification or NABP psychometric validation.

- 120 questions, 600 choices/rationales, 22 competency quotas exact; areas {"1":26,"2":40,"3":29,"4":25}; types {"multi":44,"single":76}; difficulty {"scenario":66,"direct":30,"integrated":24}; 62 selected-option critical flags.
- Verified all question IDs, distinct normalized stems, rationale/key consistency, five choices, source URL presence, and incorrect-only critical flags. Previous full-form review documented zero exact stem/ID collisions against A–F; near-duplicate scoring is a screen, not proof of total conceptual independence.
- Targeted source recheck: NABP legacy statements through February 28, 2027; MA 2023-02 vaccine policy revised 9/4/2025, delivery advisory 1/9/2025, USP <797> official FAQ, Massachusetts statutes/CMR, applicable federal CFR/USC. Official PDF screenshots were unavailable for certain MA policies; official indexed text was available. Not all source URLs were individually re-opened. Full source links are attached to each item.
- Three refinements: G077 permission versus prohibition distinction and removed overbroad critical flag; G086 specifies the Orange Book listing pathway; G106 makes the requested oral suspension exceed the regulatory cap. No answer key changed.
- Fixed bank signature 2e1dcf0c, seeded fixed order, 150 minutes. No modifications to existing A–F question banks or histories. Public availability not established by this commit.

## CI follow-up — 2026-11-24
- Previous release-candidate SHA c7537c508e10eb33bf418458f1260bf3b7aed35a: Chapter 30 full-length and mixed-mock QA passed, including verify-form-g (mobile and desktop), verify-form-e, and A–D/mixes/history regression. Run https://github.com/woojunxnam/oddments/actions/runs/45440905524.
- Practice quality/chaos run https://github.com/woojunxnam/oddments/actions/runs/45440905402: 115 unit tests and source/build checks passed. Browser setup failed because ubuntu-latest resolved to unsupported Ubuntu 26.04 for pinned Playwright 1.57.0. HTTP and chaos browser checks therefore did not execute; this is an environment failure, not proof of application regression or success.
- Remediation: pin that workflow to Ubuntu 24.04 (same as passing Form G and existing Pages workflow); retain all tests. Add post-deploy public Form G asset-hash and browser verification to Pages workflow. No question, key, exam code or history changes. New CI and public deploy are still pending. Keep PR draft until release gates pass.
