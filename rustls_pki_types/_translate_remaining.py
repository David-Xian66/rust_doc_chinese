"""rustls_pki_types 多阶段 chrome 补译 (stage 4-7).

通过 _common_tools/replace_in_files.py 应用。
"""

import os
import subprocess

BASE = 'D:/Administrator/Documents/Code/rust_doc_all/rustls_pki_types'

# Stage 4-7 累积的补译 pairs
PAIRS = [
    # all.html title + meta
    ('<title>List of all items in this crate</title>',
     '<title>本 crate 中的所有项</title>'),
    ('<meta name="description" content="List of all items in this crate">',
     '<meta name="description" content="本 crate 中的所有项">'),
    # Sidebar 'In crate' header
    ('>In crate rustls_<wbr>pki_<wbr>types<',
     '>在 crate rustls_<wbr>pki_<wbr>types 中<'),
    # Non-exhaustive variant disclaimer
    ('<span>This variant is marked as non-exhaustive</span>',
     '<span>此变体被标记为非穷尽（non-exhaustive）</span>'),
    ('Non-exhaustive enum variants could have additional fields added in future. Therefore, non-exhaustive enum variants cannot be constructed in external crates and cannot be matched against.',
     '非穷尽枚举变体在未来可能会增加更多字段。因此，非穷尽枚举变体无法在外部 crate 中构造，也不能在匹配中穷尽列举。'),
    # Stage 5/6 sidebar 锚点
    ('<h3><a href="#variants">Variants</a></h3>', '<h3><a href="#variants">变体</a></h3>'),
    ('<h3><a href="#fields">Fields</a></h3>', '<h3><a href="#fields">字段</a></h3>'),
    ('<h3><a href="#methods">Methods</a></h3>', '<h3><a href="#methods">方法</a></h3>'),
    ('<h3><a href="#trait-implementations">Trait Implementations</a></h3>',
     '<h3><a href="#trait-implementations">trait 实现</a></h3>'),
    ('<h3><a href="#synthetic-implementations">Auto Trait Implementations</a></h3>',
     '<h3><a href="#synthetic-implementations">自动 trait 实现</a></h3>'),
    ('<h3><a href="#blanket-implementations">Blanket Implementations</a></h3>',
     '<h3><a href="#blanket-implementations">blanket 实现</a></h3>'),
    ('<h3><a href="#aliased-type">Aliased Type</a></h3>',
     '<h3><a href="#aliased-type">别名类型</a></h3>'),
    ('<h3><a href="#dyn-compatibility">Dyn Compatibility</a></h3>',
     '<h3><a href="#dyn-compatibility">动态分发兼容性</a></h3>'),
    ('<h3><a href="#foreign-impls">Implementations on Foreign Types</a></h3>',
     '<h3><a href="#foreign-impls">外部类型上的实现</a></h3>'),
    ('<h3><a href="#implementors">Implementors</a></h3>',
     '<h3><a href="#implementors">实现者</a></h3>'),
    ('<h3><a href="#required-methods">Required Methods</a></h3>',
     '<h3><a href="#required-methods">必需方法</a></h3>'),
    ('<h3><a href="#provided-methods">Provided Methods</a></h3>',
     '<h3><a href="#provided-methods">提供方法</a></h3>'),
    # Sidebar sub-item labels
    ('<a href="#reexports" title="Re-exports">Re-exports</a>',
     '<a href="#reexports" title="Re-exports">再导出</a>'),
    ('<a href="#modules" title="Modules">Modules</a>',
     '<a href="#modules" title="Modules">模块</a>'),
    ('<a href="#macros" title="Macros">Macros</a>',
     '<a href="#macros" title="Macros">宏</a>'),
    ('<a href="#structs" title="Structs">Structs</a>',
     '<a href="#structs" title="Structs">结构体</a>'),
    ('<a href="#enums" title="Enums">Enums</a>',
     '<a href="#enums" title="Enums">枚举</a>'),
    ('<a href="#traits" title="Traits">Traits</a>',
     '<a href="#traits" title="Traits">特性</a>'),
    ('<a href="#types" title="Type Aliases">Type Aliases</a>',
     '<a href="#types" title="Type Aliases">类型别名</a>'),
    ('<a href="#functions" title="Functions">Functions</a>',
     '<a href="#functions" title="Functions">函数</a>'),
    ('<a href="#constants" title="Constants">Constants</a>',
     '<a href="#constants" title="Constants">常量</a>'),
    ('<a href="#statics" title="Statics">Statics</a>',
     '<a href="#statics" title="Statics">静态项</a>'),
    # Stage 6: h2/h3 + anchor long form
    ('Trait Implementations<a href="#trait-implementations"',
     'trait 实现<a href="#trait-implementations"'),
    ('Auto Trait Implementations<a href="#synthetic-implementations"',
     '自动 trait 实现<a href="#synthetic-implementations"'),
    ('Blanket Implementations<a href="#blanket-implementations"',
     'blanket 实现<a href="#blanket-implementations"'),
    ('Implementations on Foreign Types<a href="#foreign-impls"',
     '外部类型上的实现<a href="#foreign-impls"'),
    ('Provided Methods<a href="#provided-methods"',
     '提供方法<a href="#provided-methods"'),
    ('Required Methods<a href="#required-methods"',
     '必需方法<a href="#required-methods"'),
    ('Aliased Type<a href="#aliased-type"',
     '别名类型<a href="#aliased-type"'),
    ('Dyn Compatibility<a href="#dyn-compatibility"',
     '动态分发兼容性<a href="#dyn-compatibility"'),
    ('Implementors<a href="#implementors"',
     '实现者<a href="#implementors"'),
    ('Variants<a href="#variants"', '变体<a href="#variants"'),
    ('Fields<a href="#fields"', '字段<a href="#fields"'),
    ('Methods<a href="#methods"', '方法<a href="#methods"'),
    ('Re-exports<a href="#reexports"', '再导出<a href="#reexports"'),
    ('Modules<a href="#modules"', '模块<a href="#modules"'),
    ('Macros<a href="#macros"', '宏<a href="#macros"'),
    ('Structs<a href="#structs"', '结构体<a href="#structs"'),
    ('Enums<a href="#enums"', '枚举<a href="#enums"'),
    ('Traits<a href="#traits"', '特性<a href="#traits"'),
    ('Type Aliases<a href="#types"', '类型别名<a href="#types"'),
    ('Functions<a href="#functions"', '函数<a href="#functions"'),
    ('Constants<a href="#constants"', '常量<a href="#constants"'),
    ('Statics<a href="#statics"', '静态项<a href="#statics"'),
    ('Foreign Types<a href="#foreign-types"', '外部类型<a href="#foreign-types"'),
    ('Implementations<a href="#implementations"', '实现<a href="#implementations"'),
    # Stage 4 h4 + chrome
    ('<h3 id="enums">Enums</h3>', '<h3 id="enums">枚举</h3>'),
    ('<h3 id="structs">Structs</h3>', '<h3 id="structs">结构体</h3>'),
    ('<h3 id="traits">Traits</h3>', '<h3 id="traits">特性</h3>'),
    ('<h3 id="types">Type Aliases</h3>', '<h3 id="types">类型别名</h3>'),
    ('<h3 id="functions">Functions</h3>', '<h3 id="functions">函数</h3>'),
    ('<h3 id="constants">Constants</h3>', '<h3 id="constants">常量</h3>'),
    ('<h3 id="macros">Macros</h3>', '<h3 id="macros">宏</h3>'),
    ('<h3 id="modules">Modules</h3>', '<h3 id="modules">模块</h3>'),
    ('<h1>List of all items</h1>', '<h1>所有项列表</h1>'),
    ('<h4>Fields</h4>', '<h4>字段</h4>'),
    ('<p>An RSA private key</p>', '<p>一份 RSA 私钥</p>'),
    ('<p>A Sec1 private key</p>', '<p>一份 Sec1 私钥</p>'),
    ('<p>A PKCS#8 private key</p>', '<p>一份 PKCS#8 私钥</p>'),
    # Title suffix
    (' - Rust</title>', ' - rustls_pki_types</title>'),
]


def main():
    import json
    pairs_file = os.path.join(BASE, '_pairs_remaining.json')
    with open(pairs_file, 'w', encoding='utf-8') as f:
        json.dump(PAIRS, f, ensure_ascii=False)
    # Call common tool
    subprocess.run([
        'python', '_common_tools/replace_in_files.py', BASE,
        '--json', pairs_file, '--apply',
    ], check=True)


if __name__ == '__main__':
    main()