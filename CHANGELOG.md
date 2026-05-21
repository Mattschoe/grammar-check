# Changelog

## [1.2.1](https://github.com/Mattschoe/grammar-check/compare/v1.2.0...v1.2.1) (2026-05-21)


### Bug Fixes

* avoid retriggering action on PR rebasing ([bfcc1c7](https://github.com/Mattschoe/grammar-check/commit/bfcc1c705486aaad65635063115db7f5fee17af3))

## [1.2.0](https://github.com/Mattschoe/grammar-check/compare/v1.1.1...v1.2.0) (2026-05-18)


### Features

* add configurable max-output-tokens input ([8ee42e2](https://github.com/Mattschoe/grammar-check/commit/8ee42e2797703130629a1eb8b6caff6f0affa4e8))

## [1.1.1](https://github.com/Mattschoe/grammar-check/compare/v1.1.0...v1.1.1) (2026-05-18)


### Bug Fixes

* process changed files one-by-one to avoid response truncation ([1ebac32](https://github.com/Mattschoe/grammar-check/commit/1ebac32059170048ab8349d773cc3276e961354a))
* scope setup-uv cache-dependency-glob to the action path ([d7f5716](https://github.com/Mattschoe/grammar-check/commit/d7f571610b92c5c69c11ce8ba1b4aa9d791d6118))

## [1.1.0](https://github.com/Mattschoe/grammar-check/compare/v1.0.0...v1.1.0) (2026-05-18)


### Features

* surface run results in GitHub step summary ([eabaa30](https://github.com/Mattschoe/grammar-check/commit/eabaa3077f9c2332f39b64f4673fbcc82530285c))

## 1.0.0 (2026-05-18)


### Features

* add claude support ([60e8dd6](https://github.com/Mattschoe/grammar-check/commit/60e8dd6fc9e181f5f60406f3762b85466a440fab))
* add project ([60e8dd6](https://github.com/Mattschoe/grammar-check/commit/60e8dd6fc9e181f5f60406f3762b85466a440fab))
* add support for different filetypes ([e186d3a](https://github.com/Mattschoe/grammar-check/commit/e186d3a398a031833d53cfdadc977b512f2cd13c))
* composite github action ([8001078](https://github.com/Mattschoe/grammar-check/commit/80010781a935712a80cad5e35db1761ba2e89fa9))
* Create grammar.yml ([21ff3ff](https://github.com/Mattschoe/grammar-check/commit/21ff3ffc860cc12f01fd52c8cf26c404d6eaf29a))
* deepseek support ([8e3b145](https://github.com/Mattschoe/grammar-check/commit/8e3b1457dfc8515582e2fa9f04f0e836d3f51a42))
* support for different models per provider ([f8585f1](https://github.com/Mattschoe/grammar-check/commit/f8585f185c36b8408016794449d0770e63833dbe))


### Bug Fixes

* force push to PR branch ([4a861a1](https://github.com/Mattschoe/grammar-check/commit/4a861a1d6fdceeb30f73ae9ebea73bac58318848))
* grammar check whole files and not just diff ([5f7086c](https://github.com/Mattschoe/grammar-check/commit/5f7086cf95a9792fa20dedb5a07c15f2fa8e40b1))
* grammar checks all commits, not just newest ([ee828a5](https://github.com/Mattschoe/grammar-check/commit/ee828a5b01560bbca3fcfd5abbd3afcde48dd55b))
* only run script on .tex upload ([8e3b145](https://github.com/Mattschoe/grammar-check/commit/8e3b1457dfc8515582e2fa9f04f0e836d3f51a42))
* use gh action bot ([4a861a1](https://github.com/Mattschoe/grammar-check/commit/4a861a1d6fdceeb30f73ae9ebea73bac58318848))
