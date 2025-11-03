# Changelog

## [1.8.0](https://github.com/strmforge/vabhub/compare/v1.7.11...v1.8.0) (2025-11-03)


### Features

* release v1.5.0 - 多仓库版本管理优化和现代化UI系统集成 ([5968747](https://github.com/strmforge/vabhub/commit/596874727fa7fe18c2092c0052e1ef4ba8855b46))
* **release:** v1.6.0 complete - AI recommendation, caching, GraphQL, automation systems ([ddb513f](https://github.com/strmforge/vabhub/commit/ddb513fe98174d2357e227ae1e85e3beb1b9db79))


### Bug Fixes

* add BUILDKIT_CONTEXT_KEEP_GIT_DIR to fix Docker build context issue ([2099964](https://github.com/strmforge/vabhub/commit/209996427dc7b72db17d5e9cda3489e25495c999))
* add missing createFriendlyMessage export in errorHandler.js ([ea63962](https://github.com/strmforge/vabhub/commit/ea63962c53a2ae45cedf23db1d4be18cc4bf6b39))
* add missing useGlobalSettingsStore export to resolve build error ([f415c0d](https://github.com/strmforge/vabhub/commit/f415c0dbe7ef924fe7f36bf88ed505468d9bd5aa))
* add submodules checkout to GitHub Actions workflow ([51c1615](https://github.com/strmforge/vabhub/commit/51c161548a69087fba35d9abe33d684c68410768))
* add VabHub-* directories content to fix Docker build context issue ([3f61308](https://github.com/strmforge/vabhub/commit/3f61308f1fd9e29a541e2f21162f2b54111010c5))
* add VabHub-* directories to fix Docker build context issue ([73d17b0](https://github.com/strmforge/vabhub/commit/73d17b02be6b9c4a0cbe33fdeb0f5bbea6f31bc9))
* correct siteBundleApi import to use ApiService.siteBundle ([459342b](https://github.com/strmforge/vabhub/commit/459342b793bcbe137254230e4f31b85f437869a0))
* correct start.sh path in Dockerfile - use /app/deploy/start.sh instead of /app/start.sh ([f80e133](https://github.com/strmforge/vabhub/commit/f80e133cfb0c206b6b384793e2d7e5cdf08256b3))
* create missing @core/utils modules and fix import paths ([77c1737](https://github.com/strmforge/vabhub/commit/77c173786ecb37162dcf1075bf6a58d5dd46f0d9))
* create missing PWAInstallPrompt.vue component ([0517a23](https://github.com/strmforge/vabhub/commit/0517a23aadbbfb5973cc15d573aa7a0d10781e8e))
* create missing utils files to resolve build errors ([95f2261](https://github.com/strmforge/vabhub/commit/95f2261c6e0a785e30a79952a79843e281844e1e))
* remove duplicate COPY command for start.sh in Dockerfile ([d38b96c](https://github.com/strmforge/vabhub/commit/d38b96cf921dfa74ad57c9bc97c9b37f1ab7ff11))
* Remove MoviePilot references and fix Dockerfile build issues ([45d9826](https://github.com/strmforge/vabhub/commit/45d9826158fae11b468334291a94beb8bb745767))
* remove non-existent user store import from stores/index.ts ([c0ebccc](https://github.com/strmforge/vabhub/commit/c0ebccc835acac1723cd7cc2f44158d9aa76a7e8))
* remove submodules config from GitHub Actions workflow ([bba4c7c](https://github.com/strmforge/vabhub/commit/bba4c7cda2c974dae616bd8d35fcb3e68ffef306))
* remove vuetify dependency and replace with custom theme implementation ([33aa896](https://github.com/strmforge/vabhub/commit/33aa89626c519c2987791556c535db7a04f6d13d))
* replace JSX syntax in OnlineMusic.vue with standard Vue template syntax ([15b4435](https://github.com/strmforge/vabhub/commit/15b4435eeb484834f4989a9fb917d0ef7a5b7a3e))
* replace Magic icon with Star icon to resolve build error ([b2ef0f3](https://github.com/strmforge/vabhub/commit/b2ef0f3298a78645d4f5f738b246304c0eca9b21))
* replace non-existent el-loading-text with standard loading component ([c8226b8](https://github.com/strmforge/vabhub/commit/c8226b8840bed9a33770b4c222c404a220afa286))
* resolve Sass [@import](https://github.com/import) deprecation warnings and fix API import paths ([9635e8e](https://github.com/strmforge/vabhub/commit/9635e8e7b2ae86dcc064f52849ba906ee4f21602))
* update GitHub Actions cache paths and directory references ([1dea154](https://github.com/strmforge/vabhub/commit/1dea154751036cc96075884a0ba956b8d3466495))
* update GitHub Actions Docker build configurations ([c8e097b](https://github.com/strmforge/vabhub/commit/c8e097b53ee0ade950bd0bae1ddc1be924f330b6))
* update GitHub Actions Node.js cache configuration ([ce0c442](https://github.com/strmforge/vabhub/commit/ce0c4429fdc134c94b15764d3468445191d40683))
* update GitHub Actions release-please configuration for multi-repo structure ([af3e6a7](https://github.com/strmforge/vabhub/commit/af3e6a77c10e6f741a2a1422a1f65c6626f4b36b))
* 修复 Dependabot 配置路径错误，添加插件依赖更新配置 ([280e8dc](https://github.com/strmforge/vabhub/commit/280e8dc7ab0e58d6125c02f04b3719f59a989859))
* 修复 GitHub Actions 中 npm ci 命令错误，添加 package-lock.json 检查逻辑 ([5219834](https://github.com/strmforge/vabhub/commit/52198341c46c97c774ff84febf36164169cfff4e))
* 修复 GitHub Actions 中图标构建错误，创建缺失的 [@iconify](https://github.com/iconify) 目录和配置文件 ([39e9d5d](https://github.com/strmforge/vabhub/commit/39e9d5dfaae0c044805e1f8fb7803b194aa1ab1d))
* 修复 index.html 中的脚本路径引用 ([3b4f3c2](https://github.com/strmforge/vabhub/commit/3b4f3c201d21154d7848d533d800107ee25e7d71))
* 修复 vite.config.js 中的 ES 模块导入错误 ([3e426ed](https://github.com/strmforge/vabhub/commit/3e426ed02ab95e257e56d305e0c194813880e5d5))
* 修复前端构建错误 ([dc13469](https://github.com/strmforge/vabhub/commit/dc134694fbc28c4905c09df83adbd3440f194278))
* 删除 vite.config.js 中重复的 autoprefixer 导入语句 ([c68b6bc](https://github.com/strmforge/vabhub/commit/c68b6bc89cc49792dc4413bcdba21219a03d5891))
