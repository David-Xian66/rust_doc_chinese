# 通用 rustdoc 翻译工具

跨 crate 复用的 audit/translate 脚本。每个 crate 目录（如 `rustls_pki_types/`）应只保留 crate-specific 的术语表和翻译 pairs，**所有通用逻辑都在这里**。

## 脚本列表

### `strict_audit.py`
检测某 crate 下所有 OWN method docblock（含 trait method impl）是否已翻译。

```bash
python _common_tools/strict_audit.py rustls_pki_types rustls_pki_types
```

输出每个未翻译 docblock 的 (file, anchor, text)。**0 个未翻译才算完成**。

注意 OWN 判定基于 src 链接是否包含 crate 名字（rustdoc 把 `impl Trait for X` 整个块的 src 指向 crate 文件）。

### `comprehensive_audit.py`
三段审计 — chrome 可见文本残留、OWN docblock、top-doc 描述。

```bash
python _common_tools/comprehensive_audit.py rustls_pki_types
```

### `final_verify.py`
行号污染 + 标签平衡 + CJK 总数。

```bash
python _common_tools/final_verify.py rustls_pki_types
```

### `chrome.py`
批量翻译所有 .html 的 lang/title/H1/sidebar/footer chrome 文本。

```bash
python _common_tools/chrome.py rustls_pki_types
```

长字符串优先匹配，幂等（已翻译的不重复替换）。

### `replace_in_files.py`
通用 (old, new) 批量替换。把翻译 pairs 存到 JSON 文件然后调用：

```bash
# dry-run (默认)
python _common_tools/replace_in_files.py rustls_pki_types --json rustls_pki_types/_pairs.json

# 真正替换
python _common_tools/replace_in_files.py rustls_pki_types --json rustls_pki_types/_pairs.json --apply
```

JSON 格式：`[["old1", "new1"], ["old2", "new2"]]`。脚本会按 old 长度降序匹配，避免子串冲突。

## 工作流示例

翻译一个新 crate（如 `foo`）：

```bash
# 1. 复制一份原始未译版本作 backup
cp -r foo foo_old/

# 2. 跑 chrome 翻译
python _common_tools/chrome.py foo

# 3. 翻译 crate-specific 的术语表 (写一个 _translate_foo.py)
#    该文件用 _common_tools/replace_in_files.py 加载翻译 pairs
python _translate_foo.py

# 4. 多轮 audit + 补译, 直到 0 个未翻译
python _common_tools/comprehensive_audit.py foo
python _translate_foo.py  # 补漏
# ... 重复 4 直到 clean

# 5. 最终验证
python _common_tools/final_verify.py foo
```

## 历史 bug 教训

这些工具之所以这样写，是因为以下 rustdoc 输出坑：

1. **docblock `<p>` vs 裸文本**：rustdoc 对 inherent method 用 `<div class="docblock"><p>text</p></div>`，对 trait method 用 `<div class='docblock'>text<a>Read more</a></div>`（裸文本 + 内嵌 `<a>`）。`strict_audit.py` 剥掉所有 HTML 标签后检查 CJK，避免漏判。

2. **单引号 vs 双引号 class 属性**：`<div class="docblock">` 和 `<div class='docblock'>` 都要匹配。regex 用 `class=['\"]docblock['\"]`。

3. **OWN vs STD 方法**：rustdoc 把 `impl Trait for X` 块（包括 STD 的 default docblock）的 src 设为 OWN crate 文件，但 docblock 文本本身仍是 STD 的。翻译策略：OWN-implemented trait method 的 docblock 翻译（即使 trait 来自 STD），因为它在用户 crate 的文档里显示。

4. **Section 标签属性顺序**：rustdoc 输出 `<section class='method trait-impl' id='method.X'>`（class 在前），regex 不能假设 id 在前。用 `<section[^>]*id=...class=...>` 让任意顺序都可匹配。

5. **`Read more` → `更多信息`**：rustdoc 给所有 STD lib 方法自动加 `Read more` 链接（跳转到 STD 文档）。中文版应改为 `更多信息`。