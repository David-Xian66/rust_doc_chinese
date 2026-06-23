# rust_doc_chinese — Rust 文档中文化

> 把流行的 Rust crate 的 `cargo doc` 生成的 HTML 文档**逐字翻译成中文**，部署在 Cloudflare Pages 上，提供双引擎搜索（原生 rustdoc + MiniSearch 中文索引）。

**在线访问**：[https://rust-doc-chinese.pages.dev](https://rust-doc-chinese.pages.dev) （部署到 Cloudflare Pages 后生效）

**GitHub 仓库**：[David-Xian66/rust_doc_chinese](https://github.com/David-Xian66/rust_doc_chinese)

---

## 已翻译 crate 状态（12 个）

| Crate | 类型 | 状态 | 文件数 | 说明 |
| --- | --- | --- | --- | --- |
| `coarsetime` | 时间测量 | ✅ 完成 | 14 | 2026-06 翻译；专注于速度的时钟/时刻/时长 |
| `enigo` | 跨平台键鼠模拟 | ✅ 完成 | 25 | |
| `rdev` | 键鼠监听/模拟 | ✅ 完成 | 20 | |
| `quinn` | QUIC 协议实现 | ✅ 完成 | 133 | 2026-06 完成 |
| `tokio` | 异步运行时 | ✅ 完成 | 200+ | 2026-06 完成 |
| `rustls_pki_types` | X.509 / PEM 类型 | ✅ 完成 | 60 | 2026-06 完成 |
| `ffmpeg_next` | FFmpeg Rust 绑定 | 🟡 部分 | 1 | 仅 `index.html` 描述已译 |
| `ffmpeg_sys_next` | FFmpeg 底层绑定 | 🟡 部分 | 1 | 同上 |
| `windows_capture` | Windows 屏幕捕获 | 🟡 部分 | 50+ | `capture/`、`d3d11/`、`dxgi_duplication_api/` 已译 |
| `scrap` | 屏幕捕获 | ❌ 未译 | 30+ | |
| `windows` | Windows API 绑定 | ❌ 未译 | 1000+ | 体积巨大 |
| `windows_core` | Windows 核心 | ❌ 未译 | 100+ | |

> 每个已翻译 crate 都有一份未译副本 `<crate>_old/` 作回滚备份。

---

## 部署架构

```
┌─────────────────┐    cargo doc    ┌──────────────────┐
│  Rust 源码      │ ──────────────▶ │ demo_sc/target/  │
│  (12 crates)    │                 │      doc/        │
└─────────────────┘                 └────────┬─────────┘
                                              │
                       ┌──────────────────────┼──────────────────────┐
                       │                      │                      │
                       ▼                      ▼                      ▼
            ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
            │ copy_doc_        │  │ HTML in-place    │  │ chrome.py /      │
            │ artifacts.py     │  │ 翻译 (中文)      │  │ _translate_      │
            │ → search.index/  │  │ → <crate>/*.html │  │ traits.py        │
            │ → src/           │  └────────┬─────────┘  └────────┬─────────┘
            │ → crates.js      │           │                    │
            └────────┬─────────┘           ▼                    │
                     │           ┌──────────────────┐           │
                     │           │ build_chinese_   │           │
                     │           │ index.py         │           │
                     │           │ → static.files/  │           │
                     │           │   chinese-index/ │           │
                     │           └────────┬─────────┘           │
                     │                    │                    │
                     │                    ▼                    ▼
                     │           ┌──────────────────┐ ┌──────────────────┐
                     │           │ inject_chinese_  │ │ inject_search_   │
                     │           │ search.py        │ │ button.py        │
                     │           └────────┬─────────┘ └────────┬─────────┘
                     │                    │                    │
                     └────────────────────┼────────────────────┘
                                          ▼
                              ┌──────────────────────┐
                              │ rust_doc_chinese     │
                              │ 仓库根（推送 GitHub）│
                              └──────────┬───────────┘
                                         │ git push
                                         ▼
                              ┌──────────────────────┐
                              │ GitHub               │
                              │ David-Xian66/        │
                              │ rust_doc_chinese     │
                              └──────────┬───────────┘
                                         │ Cloudflare Pages
                                         ▼
                              ┌──────────────────────┐
                              │ 生产站点             │
                              │ • 原生搜索           │
                              │ • 中文 MiniSearch    │
                              └──────────────────────┘
```

### Cloudflare Pages 配置

仓库根直接作为输出目录，无需 build step。两个关键文件：

- **`_redirects`**：显式屏蔽 `*_old/` 备份目录（避免部署到生产）
- **`_headers`**：缓存策略
  - `/static.files/*.{woff2,js,css,svg,png}` → `max-age=31536000, immutable`（哈希命名文件永久缓存）
  - `/*.html` → `max-age=0, must-revalidate`（HTML 总是重新校验）
  - `/search.index/*` → `max-age=3600`
  - `/static.files/chinese-index/*.json` → `max-age=3600`
  - `/src/*` → `max-age=300`

---

## 搜索系统（双引擎）

| 引擎 | 索引位置 | 体积 | 功能 |
| --- | --- | --- | --- |
| **原生 rustdoc** | `search.index/` | ~1.6 MB | 搜类型名、方法名、字段名（英文/标识符） |
| **中文 MiniSearch** | `static.files/chinese-index/` | ~150 KB / crate | 搜中文注释、模块说明、详细描述 |

### 中文搜索的特性

- 过滤掉纯英文 docblock（避免 stdlib trait 默认模板污染）
- 默认只加载当前 crate 索引，切换"所有 crates"时再加载 `all.json`（~1 MB）
- 索引存 `sessionStorage`，重复访问不重复 fetch
- 由 `static.files/chinese-search.js` + `minisearch.min.js` 驱动

### 触发方式

按 `S` 键或 `/` 键触发搜索。顶部右侧两个按钮：
- **搜索**（原生 rustdoc）
- **搜索文档**（中文 MiniSearch）

---

## 本地预览

```bash
# 启动本地 HTTP 服务
python -m http.server 8080

# 访问任一翻译过的 crate
open http://localhost:8080/coarsetime/index.html
open http://localhost:8080/quinn/index.html
open http://localhost:8080/tokio/index.html
```

或使用任意静态文件服务器（如 `npx serve`、`caddy file-server`）。

---

## 翻译工作流（7 步）

新 crate 翻译的标准流程：

```bash
# 1. 备份：复制一份原始未译版本
cp -r newcrate/ newcrate_old/

# 2. 基础 chrome 翻译（lang/title/H1/sidebar）
python _common_tools/chrome.py newcrate

# 3. 写 crate-specific 术语表（只放该 crate 特有翻译对）
#    编辑 newcrate/_translate_terms.py 或 _translate_pairs.json

# 4. 应用术语表 + 通用 trait method 翻译
python _common_tools/replace_in_files.py newcrate \
    --json newcrate/_translate_pairs.json --apply
python _common_tools/_translate_traits.py newcrate

# 5. 多轮 audit + 补译直到 0 个未译
python _common_tools/comprehensive_audit.py newcrate
python _common_tools/_strict_p_audit.py newcrate
# ... 重复直到全部为 0

# 6. 检查并修复坏链接
python _common_tools/check_links.py newcrate newcrate

# 7. 最终验证
python _common_tools/final_verify.py newcrate
```

### 部署（新增 crate 后）

```bash
# 复制 rustdoc 产物（search.index/src/crates.js）
python _common_tools/copy_doc_artifacts.py

# 重新生成中文搜索索引
python _common_tools/build_chinese_index.py

# 注入搜索按钮（幂等，已注入则跳过）
python _common_tools/inject_search_button.py

# 注入中文搜索脚本（幂等）
python _common_tools/inject_chinese_search.py

# 提交并推送
git add -A
git commit -m "translate newcrate + deploy artifacts"
git push origin main
```

---

## 关键陷阱

### ⚠️ 绝不可用 `Read` 工具读 HTML

`Read` 工具以 `cat -n` 格式输出（每行带 `数字+\t` 行号前缀），若复制粘贴回写，行号会污染文件，页面上出现大量无意义连续序号。

**正确做法**：用 Python 直接读写：

```python
with open('file.html', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('English text', '中文翻译')
with open('file.html', 'w', encoding='utf-8') as f:
    f.write(content)
```

### ⚠️ 源文件含非 ASCII 字符需用 `bytes` 模式

rustdoc HTML 中常含 `'`（U+2019，右单引号）、`–`（U+2013）等字符。若替换串里这些字符被规范成 `'`、`-`，匹配会失败。

```python
# 用 'rb' / 'wb' 字节模式
old = b'<p>If you\xe2\x80\x99d rather...</p>'
new = '<p>中文翻译</p>'.encode('utf-8')
with open(path, 'rb') as f: raw = f.read()
raw = raw.replace(old, new)
with open(path, 'wb') as f: f.write(raw)
```

### ⚠️ 行尾与 docblock 换行

- quinn / windows_capture 等用 rustdoc 在 Windows 生成的 HTML 是 **CRLF 行尾**
- Python 文本模式会自动规范 `\r\n` ↔ `\n`
- bytes 模式必须保留原始 `\r\n`
- 长段 docblock 的换行位置必须严格匹配源文件

### ⚠️ 多阶段补译

chrome 翻译不是一次到位。常见阶段：
1. 基础 chrome（lang/title/H1）
2. `<h4>` 子标题
3. sidebar 锚点
4. trait method docblock（裸文本 + `<a>Read more</a>`）
5. per-`<p>` 漏译

每阶段完成后跑一次 audit，按 HTML 模式分类补译。

### ⚠️ rustdoc 源链接占位符

某些 rustdoc 版本（特别是 nightly）会留下未解析的 intra-doc link 占位符：
- `href="method@Self::xxx"` → `#method.xxx`
- `href="struct@Foo"` → `Foo.html`
- `href="Type::method"` → `#method.method`

使用 `python _common_tools/check_links.py <crate> <crate>` 扫描并修复。

---

## 目录结构

```
rust_doc_chinese/
├── README.md                          # 本文件
├── CLAUDE.md                          # 给 AI 助手的项目说明
├── crates.js                          # 跨 crate 列表（rustdoc 漏生成，手动补）
├── _redirects                         # Cloudflare Pages 重定向
├── _headers                           # Cloudflare Pages 缓存策略
├── index.html                         # 站点根
├── help.html                          # rustdoc 标准帮助页
│
├── static.files/                      # 共享静态资源（字体/CSS/JS）— 切勿修改
│   ├── chinese-search.js              # 中文 MiniSearch 实现
│   ├── minisearch.min.js              # MiniSearch 库
│   └── chinese-index/                 # 中文搜索索引（按 crate 划分）
│       ├── coarsetime.json
│       ├── quinn.json
│       └── ...
│
├── search.index/                      # 原生 rustdoc 搜索碎片（按需从 cargo doc 复制）
│
├── src/                               # 源代码 HTML（解决 ../src/... 死链）
│
├── _common_tools/                     # 通用翻译/审计/部署脚本
│   ├── README.md                      # 工具说明
│   ├── chrome.py                      # 基础 chrome 翻译
│   ├── _translate_traits.py           # 通用 trait method + chrome 标签
│   ├── replace_in_files.py            # 通用 (old, new) 批量替换
│   ├── comprehensive_audit.py         # 三段审计（chrome/OWN/top-doc）
│   ├── _strict_p_audit.py             # per-<p> 严格审计
│   ├── strict_audit.py                # 旧版严格审计
│   ├── check_links.py                 # 坏链接扫描
│   ├── final_verify.py                # 最终验证
│   ├── copy_doc_artifacts.py          # 部署：复制 cargo doc 产物
│   ├── build_chinese_index.py         # 部署：生成中文搜索索引
│   ├── inject_search_button.py        # 部署：注入原生搜索按钮
│   └── inject_chinese_search.py       # 部署：注入中文搜索脚本
│
├── coarsetime/                        # ✅ 已翻译
├── coarsetime_old/                    # 原始未译版本（备份）
├── enigo/                             # ✅ 已翻译
├── enigo_old/                         # 备份
├── rdev/                              # ✅ 已翻译
├── rdev_old/                          # 备份
├── quinn/                             # ✅ 已翻译（133 文件）
├── quinn_old/                         # 备份
├── tokio/                             # ✅ 已翻译（200+ 文件）
├── tokio_old/                         # 备份
├── rustls_pki_types/                  # ✅ 已翻译（60 文件）
├── rustls_pki_types_old/              # 备份
├── ffmpeg_next/                       # 🟡 部分翻译
├── ffmpeg_next_old/                   # 备份
├── ffmpeg_sys_next/                   # 🟡 部分翻译
├── ffmpeg_sys_next_old/               # 备份
├── windows_capture/                   # 🟡 部分翻译
├── scrap/                             # ❌ 未翻译
├── windows/                           # ❌ 未翻译
└── windows_core/                      # ❌ 未翻译
```

---

## 仓库约束

- **不要触碰 `static.files/`** — 所有子目录共享同一份静态资产
- **不要翻译 `sidebar-items.js`** — 它是 JSON 标识符
- **不要翻译 `index.html` / `all.html` 的 H1 标题类型名** — 只翻译类型种类（Struct/Enum/Trait/...）
- **保留 HTML 中的 `<wbr>`** — rustdoc 自动分词按需插入，不要重排
- **不要把 `*_old/` 目录搬到生产** — 即使 `_redirects` 屏蔽了 404，体积也会膨胀 + 索引污染
- **不要凭空删除坏链接的 `<code>` 包裹文本** — 保留可见标识符，只改外层 `<a>` 的 `href`

---

## 已知不修的坏链接类型

- `attr.main.html` / `macro.select.html` 等 rustdoc 漏生成的 .html 文件
- `../src/...` 全部 404（源文件未打包；本仓库通过 `copy_doc_artifacts.py` 复制 `src/` 部分缓解）
- **跨 crate 链接**（quinn 指向 `tracing`/`rustls`/`ring`/`bytes` 等依赖；ffmpeg_next 指向 `bitflags`/`either`/`crossbeam`）— 用户不需要翻译也不阅读这些依赖的文档
- Windows 反斜杠在 `src/` 路径里（与 src 404 同时存在）

---

## 致谢

- 翻译基于各 crate 维护者提供的英文 rustdoc 文档
- 搜索系统使用 [MiniSearch](https://github.com/lucaong/minisearch) 库
- 部署由 [Cloudflare Pages](https://pages.cloudflare.com/) 提供
- 所有翻译以"合理使用"为前提，仅供学习参考

---

## 许可

本仓库的翻译文件按各上游 crate 的许可发布。原始 rustdoc HTML 由各 crate 作者生成，版权归原作者所有。

如果你是某 crate 的维护者并希望撤回翻译，请开 [Issue](https://github.com/David-Xian66/rust_doc_chinese/issues)。
