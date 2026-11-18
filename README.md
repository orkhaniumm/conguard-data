# ConGuard reviewed public pool

This local candidate is `release-1fc73de07cc8`, prepared from shipped commit
`432dc7148e03464f70f0742f8bd30c2dcfada2cf`. It has not been published or selected
by the extension's production data pin.

The pool contains 106 global records and 230 country lists. The 15 countries
using global coverage are AQ, CC, CX, GS, HM, IO, KP, NF, NU, PN, TF, TK, UM, VA
and WF. `coverage-modes.json` records that distinction; no substitute country
lists are generated for those countries.

`manifest.json` binds every payload hash and the curated fallback generation.
`summary.json` records selection and review decisions. See [ATTRIBUTION](ATTRIBUTION)
for the frozen CrUX, Majestic and curated inputs, source hashes and licence notices.
The generator and source recipe remain in the
[ConGuard source repository](https://github.com/orkhaniumm/conguard/blob/2415f6fa9caa92c3062305fc12aecd3326c51a55/docs/public-pool-source-recipe.md).
That source-recipe link will resolve only once the reviewed revision is pushed.

The old Radar generator, its dependencies and scheduled update workflow are
removed. Updates require a separately reviewed generation and explicit publication;
this draft introduces no publishing automation.
