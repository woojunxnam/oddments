"""Reviewed trust-root constants, not JSON approval flags.

Entries may be added only after actual immutable-base guard results and exact
current native audits/content/code have been reviewed. No production admission
or base replay proof has been enrolled by this infrastructure change.
This file is deliberately excluded from manifests' code-hash graphs: it is the
reviewed trust root and must be exact committed HEAD bytes, not its own child.
"""
APPROVED_BASE_GUARD_PROOFS = {}
APPROVED_ADMISSIONS = {}

# Actual public UI delivery quarantine; this does not change canonical status.
DELIVERY_HOLD_FLOOR = {
    "source_commit": "c7d5162fa8deb75d61f17ec02159e69634ffcbd7",
    "source_path": "site/verified-law/delivery-holds.json",
    "source_sha256": "75cc99ba2bff3df34f6cc96a0b85ba63383baf7d14588076fad92d3efd18d376",
    "question_hashes": {
        "MA-Q-0011": "ebe1d835c312f6005f85c60c457f5e6ffe57f0dc0af24ddb78418ceb67a15afe",
        "MA-Q-0026": "c010bd60091aed3e827f9d221983fdbcc309b0ec0a7e1f1c29d1d2491a5add4c",
        "MA-Q-0033": "12319f3c6f138a1711785d4f18d2a698dabf20b3fc8bac00e795ab3b7f931d22",
        "MA-Q-0062": "d689835851608165324d2104a19bd1f7fbbc0e1100241b3ffcf3dafa2f839fe1",
        "MA-Q-0085": "4242afd488898b81b6b20314a53bf15deb891d5b4a0a496de2524ae690f2cf65",
        "MA-Q-0284": "7993637f11360613a8fb57ea5f4417f830eb01464fea66238095ff108354696d",
        "MA-Q-0087": "c90855cd857f822660f75bb99bd7ffd10fd12964ceb6268bdc2ba3d009969629",
        "MA-Q-0162": "901384da8c92b9eadeecb4cffd811dc3dee110cea1c6971627c71b7d67cbdcb5",
        "MA-Q-0052": "6cad7b064f77c9c526477be70c140c631dc04bb4533a7eb59c5f5c7567eb3311",
        "MA-Q-0051": "bda8b80a0f41674ce51f748a5371410e942666696d309e5d3ff26f3a51a27e7b",
        "MA-Q-0088": "051e6db2f7336da361ec59ce595f16fb81e57e56e8622a81223a15d6c74aaa3c",
        "MA-Q-0060": "fa78d8ed09ab0980614cacfb3d9854362d5080424478d8b33940d9ef1af0b8ed",
        "MA-Q-0437": "392ae83b7052255b4320e7a170ebeefb21f2b41be0c09420422af9b495fe0449",
        "MA-Q-0380": "b50917b53eef342c76c3e66bc0be4ddbe882b3decd34e27e8ce1e85c5088f4ec",
        "MA-Q-0058": "27edefb5d9f7bbaa4d7d73fb17adf514ddbd1064a66c05f98fac202636134959",
        "MA-Q-0227": "e4366cb456fcb126e4a96988320d32dcf0258d432acb1df73ecca7bee3c2065e",
        "MA-Q-0020": "84d0756bdfda1b813fa7e569d58cf5e2d2364dca0e2d467fba93229129fb6799",
        "MA-Q-0424": "72c0b6b15250e00dcd2d56dd1aad837f678853a94a841020bbf8ac51756d26c6",
        "MA-Q-0397": "bc197ca3617e7bb10e510dcf7d6403d88d997429aff55895fd26c7b137d6ea28"
    }
}
