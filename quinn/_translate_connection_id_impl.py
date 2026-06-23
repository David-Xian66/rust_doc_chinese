"""Translate all impl-section method docblocks in quinn/struct.ConnectionId.html."""

import re
import sys
sys.path.insert(0, 'D:/Administrator/Documents/Code/rust_doc_all/quinn')
from _connection_id_blocks import BLOCKS as ORIGINAL_BLOCKS

PATH = 'D:/Administrator/Documents/Code/rust_doc_all/quinn/struct.ConnectionId.html'

# Mapping of name -> new Chinese docblock (without [EXAMPLE] placeholders)
TRANSLATIONS = {
    'new': '<p>从字节数组构造一个 cid</p>',
    'is_ascii': '<p>检查此切片中的所有字节是否都在 ASCII 范围内。</p>\n<p>空切片返回 <code>true</code>。</p>',
    'as_ascii_unchecked': '<p>将此字节切片转换为 ASCII 字符切片，但不检查它们是否合法。</p>\n<h5 id="safety"><a class="doc-anchor" href="#safety">§</a>安全性</h5>\n<p>切片中的每个字节都必须位于 <code>0..=127</code>，否则属于未定义行为。</p>',
    'eq_ignore_ascii_case': '<p>检查两个切片是否在不区分 ASCII 大小写的情况下相等。</p>\n<p>等价于 <code>to_ascii_lowercase(a) == to_ascii_lowercase(b)</code>，但无需分配并复制临时变量。</p>',
    'make_ascii_uppercase': '<p>将此切片就地转换为对应的大写 ASCII 形式。</p>\n<p>ASCII 字母 <code>a</code> 到 <code>z</code> 会被映射为 <code>A</code> 到 <code>Z</code>，但非 ASCII 字母保持不变。</p>\n<p>若希望返回一个新的全大写副本而不修改原切片，请使用 <a href="#method.to_ascii_uppercase"><code>to_ascii_uppercase</code></a>。</p>',
    'make_ascii_lowercase': '<p>将此切片就地转换为对应的小写 ASCII 形式。</p>\n<p>ASCII 字母 <code>A</code> 到 <code>Z</code> 会被映射为 <code>a</code> 到 <code>z</code>，但非 ASCII 字母保持不变。</p>\n<p>若希望返回一个新的全小写副本而不修改原切片，请使用 <a href="#method.to_ascii_lowercase"><code>to_ascii_lowercase</code></a>。</p>',
    'escape_ascii': '<p>返回一个迭代器，产出此切片的转义形式，按 ASCII 字符串处理。</p>\n<h5 id="examples"><a class="doc-anchor" href="#examples">§</a>示例</h5>\n[EXAMPLE]',
    'trim_ascii_start': '<p>返回一个移除了开头 ASCII 空白字节的字节切片。</p>\n<p>“空白”采用 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.u8.html#method.is_ascii_whitespace" title="method u8::is_ascii_whitespace"><code>u8::is_ascii_whitespace</code></a> 的定义。</p>\n<h5 id="examples-1"><a class="doc-anchor" href="#examples-1">§</a>示例</h5>\n[EXAMPLE]',
    'trim_ascii_end': '<p>返回一个移除了末尾 ASCII 空白字节的字节切片。</p>\n<p>“空白”采用 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.u8.html#method.is_ascii_whitespace" title="method u8::is_ascii_whitespace"><code>u8::is_ascii_whitespace</code></a> 的定义。</p>\n<h5 id="examples-2"><a class="doc-anchor" href="#examples-2">§</a>示例</h5>\n[EXAMPLE]',
    'trim_ascii': '<p>返回一个同时移除了开头和末尾 ASCII 空白字节的字节切片。</p>\n<p>“空白”采用 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.u8.html#method.is_ascii_whitespace" title="method u8::is_ascii_whitespace"><code>u8::is_ascii_whitespace</code></a> 的定义。</p>\n<h5 id="examples-3"><a class="doc-anchor" href="#examples-3">§</a>示例</h5>\n[EXAMPLE]',
    'len': '<p>返回切片中的元素数量。</p>\n<h5 id="examples-4"><a class="doc-anchor" href="#examples-4">§</a>示例</h5>\n[EXAMPLE]',
    'is_empty': '<p>如果切片长度为 0 则返回 <code>true</code>。</p>\n<h5 id="examples-5"><a class="doc-anchor" href="#examples-5">§</a>示例</h5>\n[EXAMPLE]',
    'is_not_empty': '<p>如果切片长度不为 0 则返回 <code>true</code>。</p>\n<h5 id="examples-6"><a class="doc-anchor" href="#examples-6">§</a>示例</h5>\n[EXAMPLE]',
    'first': '<p>返回切片中的第一个元素，若切片为空则返回 <code>None</code>。</p>\n<h5 id="examples-7"><a class="doc-anchor" href="#examples-7">§</a>示例</h5>\n[EXAMPLE]',
    'first_chunk': '<p>返回切片开头的前 <code>N</code> 个元素。</p>\n<h5 id="examples-8"><a class="doc-anchor" href="#examples-8">§</a>示例</h5>\n[EXAMPLE]',
    'first_mut': '<p>返回切片中第一个元素的可变引用，若切片为空则返回 <code>None</code>。</p>\n<h5 id="examples-9"><a class="doc-anchor" href="#examples-9">§</a>示例</h5>\n[EXAMPLE]',
    'split_first': '<p>返回切片的第一个元素及剩余切片，若切片为空则返回 <code>None</code>。</p>\n<h5 id="examples-10"><a class="doc-anchor" href="#examples-10">§</a>示例</h5>\n[EXAMPLE]',
    'split_first_mut': '<p>返回切片的第一个元素及剩余切片的可变引用，若切片为空则返回 <code>None</code>。</p>\n<h5 id="examples-11"><a class="doc-anchor" href="#examples-11">§</a>示例</h5>\n[EXAMPLE]',
    'split_last': '<p>返回切片的最后一个元素及剩余切片，若切片为空则返回 <code>None</code>。</p>\n<h5 id="examples-12"><a class="doc-anchor" href="#examples-12">§</a>示例</h5>\n[EXAMPLE]',
    'split_last_mut': '<p>返回切片的最后一个元素及剩余切片的可变引用，若切片为空则返回 <code>None</code>。</p>\n<h5 id="examples-13"><a class="doc-anchor" href="#examples-13">§</a>示例</h5>\n[EXAMPLE]',
    'last': '<p>返回切片中的最后一个元素，若切片为空则返回 <code>None</code>。</p>\n<h5 id="examples-14"><a class="doc-anchor" href="#examples-14">§</a>示例</h5>\n[EXAMPLE]',
    'last_mut': '<p>返回切片中最后一个元素的可变引用，若切片为空则返回 <code>None</code>。</p>\n<h5 id="examples-15"><a class="doc-anchor" href="#examples-15">§</a>示例</h5>\n[EXAMPLE]',
    'get': '<p>返回位于给定索引处的元素，或在越界时返回 <code>None</code>。</p>\n<h5 id="examples-16"><a class="doc-anchor" href="#examples-16">§</a>示例</h5>\n[EXAMPLE]',
    'get_mut': '<p>返回位于给定索引处的元素的可变引用，或在越界时返回 <code>None</code>。</p>\n<h5 id="examples-17"><a class="doc-anchor" href="#examples-17">§</a>示例</h5>\n[EXAMPLE]',
    'as_ptr': '<p>返回指向切片起始地址的裸指针。</p>\n<p>调用方必须确保切片存活，且不能通过该指针在 <code>self</code> 范围之外访问内存。</p>',
    'as_mut_ptr': '<p>返回指向切片起始地址的可写裸指针。</p>\n<p>调用方必须确保切片存活，且不能通过该指针在 <code>self</code> 范围之外访问内存。</p>',
    'as_ptr_range': '<p>返回包含切片中所有有效索引的“指针范围”。</p>',
    'swap_unchecked': '<p>交换切片中的两个元素，无需进行边界检查。</p>\n<h5 id="safety"><a class="doc-anchor" href="#safety">§</a>安全性</h5>\n<p>调用方必须确保 <code>a</code> 和 <code>b</code> 均小于切片长度，否则属于未定义行为。</p>',
    'as_array': '<p>将切片转换为共享引用，指向底层数组。</p>\n<p>若切片长度正好等于数组长度，则返回 <code>Some</code>；否则返回 <code>None</code>。</p>',
    'as_mut_array': '<p>将可变切片转换为可变引用，指向底层数组。</p>\n<p>若切片长度正好等于数组长度，则返回 <code>Some</code>；否则返回 <code>None</code>。</p>',
    'assume_init': '<p>移除切片初始化状态的标记，封装出一个元素类型已初始化的新切片。</p>\n<p>这是一种 unsafe 的“信任我”操作，旨在支持延迟初始化。</p>\n<h5 id="safety"><a class="doc-anchor" href="#safety">§</a>安全性</h5>\n<p>调用方必须确保数组中的所有元素确实已初始化。</p>',
    'as_slice': '<p>返回包含整个数组的 <code>&amp;[T]</code>。</p>',
    'as_mut_slice': '<p>返回包含整个数组的 <code>&amp;mut [T]</code>。</p>',
    'as_flattened': '<p>取一个由数组组成的切片，展平后返回该切片所组成的数组的 <code>&amp;[T]</code>。</p>',
    'as_flattened_mut': '<p>取一个由可变数组组成的切片，展平后返回该切片所组成的数组的 <code>&amp;mut [T]</code>。</p>',
    'sort': '<p>对切片进行原地排序。</p>\n<p>此排序是稳定的（即不重排相等元素的相对顺序），最坏情况的时间复杂度为 <code>O(n * log(n))</code>，空间复杂度为 <code>O(1)</code>。</p>',
    'sort_unstable': '<p>对切片进行原地排序。</p>\n<p>此排序不稳定，相等的元素相对顺序可能被打乱；平均与最坏情况时间复杂度均为 <code>O(n * log(n))</code>，空间复杂度为 <code>O(1)</code>。</p>',
    'sort_by': '<p>使用给定的比较函数对切片进行原地稳定排序。</p>\n<p>此排序是稳定的，最坏情况时间复杂度为 <code>O(n * log(n))</code>，空间复杂度为 <code>O(1)</code>。</p>',
    'sort_by_key': '<p>使用从元素派生的键对切片进行原地稳定排序。</p>',
    'sort_by_cached_key': '<p>使用从元素派生的键对切片进行原地稳定排序，键只计算一次。</p>',
    'sort_unstable_by': '<p>使用给定的比较函数对切片进行原地不稳定排序。</p>',
    'sort_unstable_by_key': '<p>使用从元素派生的键对切片进行原地不稳定排序。</p>',
    'rotate_left': '<p>将切片在原地旋转，使切片开头的 <code>mid</code> 个元素移到末尾。</p>\n<p>要求 <code>mid &lt;= self.len()</code>。复杂度为 <code>O(1)</code>。</p>',
    'rotate_right': '<p>将切片在原地旋转，使切片末尾的 <code>k</code> 个元素移到开头。</p>\n<p>要求 <code>k &lt;= self.len()</code>。复杂度为 <code>O(1)</code>。</p>',
    'fill': '<p>用 <code>value</code> 填充切片中的所有元素。</p>',
    'fill_with': '<p>用 <code>f</code> 生成的元素填充切片。</p>',
    'clone_from': '<p>从 <code>src</code> 拷贝元素到本切片。</p>\n<p>两个切片长度可以不同；旧的元素会被覆盖（这与赋值行为一致）；若需要保留原有元素，应使用 <code>copy_from_slice</code> 之类的 API。</p>',
    'copy_from_slice': '<p>将 <code>src</code> 中的元素拷贝到 <code>self</code>。</p>\n<p>两个切片必须等长。复杂度为 <code>O(n)</code>。</p>',
    'copy_to_slice': '<p>将本切片中的元素拷贝到 <code>dst</code>。</p>\n<p>两个切片必须等长。复杂度为 <code>O(n)</code>。</p>',
    'swap_with_slice': '<p>将本切片与 <code>other</code> 切片中的元素互换。</p>\n<p>两个切片必须等长。复杂度为 <code>O(1)</code>。</p>',
    'iter': '<p>返回一个遍历切片的迭代器。</p>',
    'iter_mut': '<p>返回一个可变迭代器，允许修改每个元素。</p>',
    'windows': '<p>返回一个长度为 <code>size</code> 的重叠窗口上的迭代器。</p>\n<p>若切片短于 <code>size</code>，迭代器不产生任何元素。复杂度为 <code>O(n)</code>。</p>',
    'chunks': '<p>返回一个非重叠块上的迭代器，每个块长度为 <code>chunk_size</code>。</p>',
    'chunks_mut': '<p>返回一个非重叠可变块上的迭代器，每个块长度为 <code>chunk_size</code>。</p>',
    'chunks_exact': '<p>返回一个非重叠块上的迭代器，每个块长度为 <code>chunk_size</code>，最后一个块可能较短。</p>',
    'chunks_exact_mut': '<p>返回一个非重叠可变块上的迭代器，每个块长度为 <code>chunk_size</code>，最后一个块可能较短。</p>',
    'rchunks': '<p>返回一个非重叠块上的迭代器，从切片末尾开始向前，每个块长度为 <code>chunk_size</code>。</p>',
    'rchunks_mut': '<p>返回一个非重叠可变块上的迭代器，从切片末尾开始向前，每个块长度为 <code>chunk_size</code>。</p>',
    'rchunks_exact': '<p>返回一个非重叠块上的迭代器，从切片末尾开始向前，每个块长度为 <code>chunk_size</code>，最前面的块可能较短。</p>',
    'rchunks_exact_mut': '<p>返回一个非重叠可变块上的迭代器，从切片末尾开始向前，每个块长度为 <code>chunk_size</code>，最前面的块可能较短。</p>',
    'chunk_by': '<p>返回一个从切片开头开始、按相邻相等元素分组的迭代器。</p>',
    'chunk_by_mut': '<p>返回一个从切片开头开始、按相邻相等元素分组的可变迭代器。</p>',
    'split_at': '<p>将切片在给定索引处一分为二。</p>',
    'split_at_mut': '<p>将可变切片在给定索引处一分为二。</p>',
    'split': '<p>返回一个由 <code>pat</code> 匹配的所有子切片组成的迭代器（可为 <code>&amp;T</code>、<code>&amp;[T]</code>，或用于单分隔符匹配的 <code>FnMut(&amp;T) -&gt; bool</code>）。</p>',
    'split_mut': '<p>返回一个由 <code>pat</code> 匹配的所有可变子切片组成的迭代器。</p>',
    'split_inclusive': '<p>返回一个迭代器，产出由 <code>pat</code> 匹配的子切片，以及这些匹配项之前的所有内容。</p>',
    'split_inclusive_mut': '<p>返回一个迭代器，产出由 <code>pat</code> 匹配的可变子切片，以及这些匹配项之前的所有内容。</p>',
    'splitn': '<p>返回一个迭代器，至多产出 <code>n</code> 个由 <code>pat</code> 匹配的子切片。</p>',
    'splitn_mut': '<p>返回一个迭代器，至多产出 <code>n</code> 个由 <code>pat</code> 匹配的可变子切片。</p>',
    'rsplitn': '<p>返回一个从右端开始的迭代器，至多产出 <code>n</code> 个由 <code>pat</code> 匹配的子切片。</p>',
    'rsplitn_mut': '<p>返回一个从右端开始的迭代器，至多产出 <code>n</code> 个由 <code>pat</code> 匹配的可变子切片。</p>',
    'contains': '<p>如果切片包含给定元素则返回 <code>true</code>。</p>',
    'starts_with': '<p>如果切片以 <code>needle</code> 开头则返回 <code>true</code>。</p>',
    'ends_with': '<p>如果切片以 <code>needle</code> 结尾则返回 <code>true</code>。</p>',
    'strip_prefix': '<p>如果切片以 <code>prefix</code> 开头则返回去掉前缀后的子切片，否则返回 <code>None</code>。</p>',
    'strip_suffix': '<p>如果切片以 <code>suffix</code> 结尾则返回去掉后缀后的子切片，否则返回 <code>None</code>。</p>',
    'binary_search': '<p>二分查找切片中等于给定元素的索引。</p>',
    'binary_search_by': '<p>二分查找切片，使用给定的比较函数。</p>',
    'binary_search_by_key': '<p>二分查找切片，给定一个可以从元素派生的搜索键。</p>',
    'sort_floats': '<p>对浮点数切片进行原地排序。</p>\n<p>排序后非 NaN 的元素保持稳定的顺序，NaN 元素被排到末尾。该方法的唯一目的是作为 <code>sort_unstable</code> 的浮点特化版本。</p>',
    'to_vec_in': '<p>将本切片拷贝到一个 <code>Vec</code> 中，复用 <code>allocator</code> 的内存分配。</p>',
    'repeat': '<p>创建一个长度为 <code>n</code> 的向量，其中每个元素都是给定值的一份拷贝。</p>',
    'concat_ref': '<p>将所有切片按顺序连接成一个新的切片。</p>',
    'join_ref': '<p>使用 <code>sep</code> 作为分隔符，按顺序连接所有切片。</p>',
    'as_chunks': '<p>尝试将切片拆分为 <code>N</code>-元素数组的切片，余数切片长度严格小于 <code>N</code>。</p>',
    'as_chunks_mut': '<p>与 <a href="#method.as_chunks"><code>as_chunks</code></a> 类似，但产生的是可变切片。</p>',
    'as_rchunks': '<p>从切片末尾开始，将切片拆分为 <code>N</code>-元素数组的切片，余数切片长度严格小于 <code>N</code>。</p>',
    'as_chunks_unchecked': '<p>将切片拆分为 <code>N</code>-元素数组的切片，假定不存在余数。</p>',
    'as_chunks_unchecked_mut': '<p>将切片拆分为 <code>N</code>-元素数组的切片，假定不存在余数（可变版本）。</p>',
    'get_unchecked': '<p>返回对一个元素或子切片的引用，不进行边界检查。</p>\n<p>如需安全版本，请参阅 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.get" title="method slice::get"><code>get</code></a>。</p>\n<h5 id="safety-1"><a class="doc-anchor" href="#safety-1">§</a>安全性</h5>\n<p>即便不使用所得到的引用，使用越界索引调用本方法也属于<em><a href="https://doc.rust-lang.org/reference/behavior-considered-undefined.html">未定义行为</a></em>。</p>\n<p>你可以把它理解为 <code>.get(index).unwrap_unchecked()</code>。调用 <code>.get_unchecked(len)</code> 即便立即转换成指针也是 UB；同理，调用 <code>.get_unchecked(..len + 1)</code>、<code>.get_unchecked(..=len)</code> 等也是 UB。</p>\n<h5 id="examples-24"><a class="doc-anchor" href="#examples-24">§</a>示例</h5>\n[EXAMPLE]',
    'get_unchecked_mut': '<p>返回对一个元素或子切片的可变引用，不进行边界检查。</p>\n<p>如需安全版本，请参阅 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.get_mut" title="method slice::get_mut"><code>get_mut</code></a>。</p>\n<h5 id="safety-2"><a class="doc-anchor" href="#safety-2">§</a>安全性</h5>\n<p>即便不使用所得到的引用，使用越界索引调用本方法也属于<em><a href="https://doc.rust-lang.org/reference/behavior-considered-undefined.html">未定义行为</a></em>。</p>\n<p>你可以把它理解为 <code>.get_mut(index).unwrap_unchecked()</code>。调用 <code>.get_unchecked_mut(len)</code> 即便立即转换成指针也是 UB；同理，调用 <code>.get_unchecked_mut(..len + 1)</code>、<code>.get_unchecked_mut(..=len)</code> 等也是 UB。</p>\n<h5 id="examples-25"><a class="doc-anchor" href="#examples-25">§</a>示例</h5>\n[EXAMPLE]',
    'as_mut_ptr_range': '<p>返回覆盖该切片范围的两个不安全的可变指针。</p>\n<p>返回的范围是半开区间，意思是结束指针指向切片最后一个元素<em>之后</em>的位置。这样一来，空切片由两个相等的指针表示，而两指针之差就是切片的长度。</p>\n<p>关于使用这些指针时的注意事项，请参阅 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.as_mut_ptr" title="method slice::as_mut_ptr"><code>as_mut_ptr</code></a>。结束指针需要额外小心，因为它并不指向切片中的有效元素。</p>\n<p>本函数适用于与使用两个指针表示内存中一段元素的外部接口（常见于 C++）交互。</p>',
    'swap': '<p>交换切片中的两个元素。</p>\n<p>若 <code>a</code> 等于 <code>b</code>，则保证元素值不会改变。</p>\n<h5 id="arguments"><a class="doc-anchor" href="#arguments">§</a>参数</h5>\n<ul>\n<li>a — 第一个元素的索引</li>\n<li>b — 第二个元素的索引</li>\n</ul>\n<h5 id="panics"><a class="doc-anchor" href="#panics">§</a>Panics</h5>\n<p>若 <code>a</code> 或 <code>b</code> 越界则 panic。</p>\n<h5 id="examples-28"><a class="doc-anchor" href="#examples-28">§</a>示例</h5>\n[EXAMPLE]',
    'reverse': '<p>将切片中的元素顺序原地反转。</p>\n<h5 id="examples-30"><a class="doc-anchor" href="#examples-30">§</a>示例</h5>\n[EXAMPLE]',
    'as_rchunks_mut': '<p>将切片拆分为一个由 <code>N</code>-元素数组组成的切片（从切片末尾开始）以及一个长度严格小于 <code>N</code> 的余数切片。</p>\n<p>余数部分在除法意义下是有意义的。给定 <code>let (remainder, chunks) = slice.as_rchunks_mut()</code>，那么：</p>\n<ul>\n<li><code>remainder.len()</code> 等于 <code>slice.len() % N</code>，</li>\n<li><code>chunks.len()</code> 等于 <code>slice.len() / N</code>，</li>\n<li><code>slice.len()</code> 等于 <code>chunks.len() * N + remainder.len()</code>。</li>\n</ul>\n<p>可以使用 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.as_flattened_mut" title="method slice::as_flattened_mut"><code>as_flattened_mut</code></a> 把 chunks 重新展平为 <code>T</code> 切片。</p>\n<h5 id="panics-9"><a class="doc-anchor" href="#panics-9">§</a>Panics</h5>\n<p>若 <code>N</code> 为零则 panic。</p>\n<p>注意此检查针对的是 const 泛型参数而非运行时值，因此某一具体单态化要么总是 panic、要么从不 panic。</p>\n<h5 id="examples-43"><a class="doc-anchor" href="#examples-43">§</a>示例</h5>\n[EXAMPLE]',
    'array_windows': '<p>返回一个迭代器，按长度为 <code>N</code> 的重叠窗口遍历切片，从切片开头开始。</p>\n<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.windows" title="method slice::windows"><code>windows</code></a> 的 const 泛型等价物。</p>\n<p>若 <code>N</code> 大于切片大小，则不返回任何窗口。</p>\n<h5 id="panics-10"><a class="doc-anchor" href="#panics-10">§</a>Panics</h5>\n<p>若 <code>N</code> 为零则 panic。</p>\n<p>注意此检查针对的是 const 泛型参数而非运行时值，因此某一具体单态化要么总是 panic、要么从不 panic。</p>\n<h5 id="examples-44"><a class="doc-anchor" href="#examples-44">§</a>示例</h5>\n[EXAMPLE]',
    'split_at_unchecked': '<p>在某个索引处将切片一分为二，不进行边界检查。</p>\n<p>第一部分包含区间 <code>[0, mid)</code> 中的所有索引（不含 <code>mid</code> 本身），第二部分包含 <code>[mid, len)</code> 中的所有索引（不含 <code>len</code> 本身）。</p>\n<p>如需安全版本，请参阅 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.split_at" title="method slice::split_at"><code>split_at</code></a>。</p>\n<h5 id="safety-6"><a class="doc-anchor" href="#safety-6">§</a>安全性</h5>\n<p>即便不使用所得到的引用，使用越界索引调用本方法也属于<em><a href="https://doc.rust-lang.org/reference/behavior-considered-undefined.html">未定义行为</a></em>。调用方必须保证 <code>0 &lt;= mid &lt;= self.len()</code>。</p>\n<h5 id="examples-53"><a class="doc-anchor" href="#examples-53">§</a>示例</h5>\n[EXAMPLE]',
    'split_at_mut_unchecked': '<p>在某个索引处将可变切片一分为二，不进行边界检查。</p>\n<p>第一部分包含区间 <code>[0, mid)</code> 中的所有索引（不含 <code>mid</code> 本身），第二部分包含 <code>[mid, len)</code> 中的所有索引（不含 <code>len</code> 本身）。</p>\n<p>如需安全版本，请参阅 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.split_at_mut" title="method slice::split_at_mut"><code>split_at_mut</code></a>。</p>\n<h5 id="safety-7"><a class="doc-anchor" href="#safety-7">§</a>安全性</h5>\n<p>即便不使用所得到的引用，使用越界索引调用本方法也属于<em><a href="https://doc.rust-lang.org/reference/behavior-considered-undefined.html">未定义行为</a></em>。调用方必须保证 <code>0 &lt;= mid &lt;= self.len()</code>。</p>\n<h5 id="examples-54"><a class="doc-anchor" href="#examples-54">§</a>示例</h5>\n[EXAMPLE]',
    'split_once': '<p>在第一个满足给定谓词的元素处将切片一分为二。</p>\n<p>若切片中存在匹配的元素，则返回该匹配项之前的前缀和之后的后缀。匹配项本身不在结果中。若没有任何元素匹配，则返回 <code>None</code>。</p>\n<h5 id="examples-67"><a class="doc-anchor" href="#examples-67">§</a>示例</h5>\n[EXAMPLE]',
    'rsplit_once': '<p>在最后一个满足给定谓词的元素处将切片一分为二。</p>\n<p>若切片中存在匹配的元素，则返回该匹配项之前的前缀和之后的后缀。匹配项本身不在结果中。若没有任何元素匹配，则返回 <code>None</code>。</p>\n<h5 id="examples-68"><a class="doc-anchor" href="#examples-68">§</a>示例</h5>\n[EXAMPLE]',
    'strip_circumfix': '<p>返回一个去除了前缀和后缀的子切片。</p>\n<p>若切片以 <code>prefix</code> 开头且以 <code>suffix</code> 结尾，则返回介于前缀之后、后缀之前的那段子切片，并包装在 <code>Some</code> 中返回。</p>\n<p>若切片不以 <code>prefix</code> 开头或不以 <code>suffix</code> 结尾，则返回 <code>None</code>。</p>\n<h5 id="examples-74"><a class="doc-anchor" href="#examples-74">§</a>示例</h5>\n[EXAMPLE]',
    'trim_prefix': '<p>返回一个去除了可选前缀的子切片。</p>\n<p>若切片以 <code>prefix</code> 开头，则返回去掉该前缀后的子切片。若 <code>prefix</code> 为空或切片不以 <code>prefix</code> 开头，则直接返回原切片。若 <code>prefix</code> 与原切片相等，则返回空切片。</p>\n<h5 id="examples-75"><a class="doc-anchor" href="#examples-75">§</a>示例</h5>\n[EXAMPLE]',
    'trim_suffix': '<p>返回一个去除了可选后缀的子切片。</p>\n<p>若切片以 <code>suffix</code> 结尾，则返回去掉该后缀后的子切片。若 <code>suffix</code> 为空或切片不以 <code>suffix</code> 结尾，则直接返回原切片。若 <code>suffix</code> 与原切片相等，则返回空切片。</p>\n<h5 id="examples-76"><a class="doc-anchor" href="#examples-76">§</a>示例</h5>\n[EXAMPLE]',
    'partition_dedup': '<p>依据 <a href="https://doc.rust-lang.org/1.95.0/core/cmp/trait.PartialEq.html" title="trait core::cmp::PartialEq"><code>PartialEq</code></a> trait 的实现，将切片中所有连续重复的元素移到末尾。</p>\n<p>返回两个切片。第一个不含任何连续重复元素；第二个包含所有重复项（顺序未指定）。</p>\n<p>若切片是已排序的，那么第一个返回的切片不含任何重复项。</p>\n<h5 id="examples-89"><a class="doc-anchor" href="#examples-89">§</a>示例</h5>\n[EXAMPLE]',
    'partition_dedup_by': '<p>依据给定的相等性关系，将切片中除第一个外、连续的元素都移到末尾。</p>\n<p>返回两个切片。第一个不含任何连续重复元素；第二个包含所有重复项（顺序未指定）。</p>\n<p><code>same_bucket</code> 函数接收切片中两个元素的引用，必须判断它们是否相等。两个元素按其切片中顺序的相反顺序传入，因此若 <code>same_bucket(a, b)</code> 返回 <code>true</code>，<code>a</code> 会被移到切片末尾。</p>\n<p>若切片是已排序的，那么第一个返回的切片不含任何重复项。</p>\n<h5 id="examples-90"><a class="doc-anchor" href="#examples-90">§</a>示例</h5>\n[EXAMPLE]',
    'partition_dedup_by_key': '<p>将切片中除第一个外、连续的元素中具有相同键的元素移到末尾。</p>\n<p>返回两个切片。第一个不含任何连续重复元素；第二个包含所有重复项（顺序未指定）。</p>\n<p>若切片是已排序的，那么第一个返回的切片不含任何重复项。</p>\n<h5 id="examples-91"><a class="doc-anchor" href="#examples-91">§</a>示例</h5>\n[EXAMPLE]',
    'clone_from_slice': '<p>将 <code>src</code> 中的元素拷贝到 <code>self</code>。</p>\n<p><code>src</code> 的长度必须与 <code>self</code> 相同。</p>\n<h5 id="panics-28"><a class="doc-anchor" href="#panics-28">§</a>Panics</h5>\n<p>若两个切片长度不同则 panic。</p>\n<h5 id="examples-98"><a class="doc-anchor" href="#examples-98">§</a>示例</h5>\n<p>从一个切片中克隆两个元素到另一个切片：</p>\n[EXAMPLE]',
    'copy_within': '<p>使用 memmove 将切片的一部分拷贝到另一部分。</p>\n<p><code>src</code> 是要拷贝的源区间（在 <code>self</code> 内）。<code>dest</code> 是目标区间的起始索引（在 <code>self</code> 内），其长度与 <code>src</code> 相同。两个区间可以重叠。两区间的端点都必须小于等于 <code>self.len()</code>。</p>\n<h5 id="panics-30"><a class="doc-anchor" href="#panics-30">§</a>Panics</h5>\n<p>若任一区间超出切片末尾，或 <code>src</code> 的终点早于起点，则 panic。</p>\n<h5 id="examples-100"><a class="doc-anchor" href="#examples-100">§</a>示例</h5>\n<p>在切片内拷贝四个字节：</p>\n[EXAMPLE]',
    'align_to': '<p>将该切片转换为另一种类型的切片，并保证类型的对齐得到保持。</p>\n<p>本方法将切片拆分为三段：前缀、类型正确对齐的中间切片以及后缀切片。在给定的对齐约束和元素大小下，中间段会被尽可能地拉长。</p>\n<p>当输入元素 <code>T</code> 或输出元素 <code>U</code> 是零大小类型时，本方法无意义，会原样返回原切片，不做任何拆分。</p>\n<h5 id="safety-8"><a class="doc-anchor" href="#safety-8">§</a>安全性</h5>\n<p>对返回的中间切片中的元素而言，本方法本质上等同于 <code>transmute</code>，因此 <code>transmute::&lt;T, U&gt;</code> 的所有常见注意事项在这里同样适用。</p>\n<h5 id="examples-101"><a class="doc-anchor" href="#examples-101">§</a>示例</h5>\n<p>基本用法：</p>\n[EXAMPLE]',
    'align_to_mut': '<p>将该可变切片转换为另一种类型的可变切片，并保证类型的对齐得到保持。</p>\n<p>本方法将切片拆分为三段：前缀、类型正确对齐的中间切片以及后缀切片。在给定的对齐约束和元素大小下，中间段会被尽可能地拉长。</p>\n<p>当输入元素 <code>T</code> 或输出元素 <code>U</code> 是零大小类型时，本方法无意义，会原样返回原切片，不做任何拆分。</p>\n<h5 id="safety-9"><a class="doc-anchor" href="#safety-9">§</a>安全性</h5>\n<p>对返回的中间切片中的元素而言，本方法本质上等同于 <code>transmute</code>，因此 <code>transmute::&lt;T, U&gt;</code> 的所有常见注意事项在这里同样适用。</p>\n<h5 id="examples-102"><a class="doc-anchor" href="#examples-102">§</a>示例</h5>\n<p>基本用法：</p>\n[EXAMPLE]',
    'as_simd': '<p>将切片拆分为一个前缀、一个对齐好的 SIMD 类型中间段以及一个后缀。</p>\n<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.align_to" title="method slice::align_to"><code>slice::align_to</code></a> 的安全包装，因此继承该方法的所有保证。</p>\n<h5 id="panics-32"><a class="doc-anchor" href="#panics-32">§</a>Panics</h5>\n<p>若 SIMD 类型的大小与 <code>LANES</code> 倍标量类型大小不同，则 panic。</p>\n<p>撰写本文档时，<code>Simd&lt;T, LANES&gt;</code> 上的 trait 约束使得这种情况不会发生——只支持 2 的幂次个 lane。未来这些约束若被解除，则可能在 <code>LANES == 3</code> 之类的情况下从此方法看到 panic。</p>\n<h5 id="examples-103"><a class="doc-anchor" href="#examples-103">§</a>示例</h5>\n[EXAMPLE]',
    'as_simd_mut': '<p>将可变切片拆分为一个可变前缀、一个对齐好的 SIMD 类型中间段以及一个可变后缀。</p>\n<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.align_to_mut" title="method slice::align_to_mut"><code>slice::align_to_mut</code></a> 的安全包装，因此继承该方法的所有保证。</p>\n<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.as_simd" title="method slice::as_simd"><code>slice::as_simd</code></a> 的可变版本；示例请参阅后者。</p>\n<h5 id="panics-33"><a class="doc-anchor" href="#panics-33">§</a>Panics</h5>\n<p>若 SIMD 类型的大小与 <code>LANES</code> 倍标量类型大小不同，则 panic。</p>\n<p>撰写本文档时，<code>Simd&lt;T, LANES&gt;</code> 上的 trait 约束使得这种情况不会发生——只支持 2 的幂次个 lane。未来这些约束若被解除，则可能在 <code>LANES == 3</code> 之类的情况下从此方法看到 panic。</p>',
    'is_sorted': '<p>检查切片中的元素是否已排序。</p>\n<p>也就是说，对每个元素 <code>a</code> 及其后继元素 <code>b</code>，必须满足 <code>a &lt;= b</code>。若切片恰好产出零或一个元素，则返回 <code>true</code>。</p>\n<p>注意，若 <code>Self::Item</code> 只实现了 <code>PartialOrd</code> 而未实现 <code>Ord</code>，那么按上述定义，一旦出现任意两个相邻项不可比较的情况，本函数就会返回 <code>false</code>。</p>\n<h5 id="examples-104"><a class="doc-anchor" href="#examples-104">§</a>示例</h5>\n[EXAMPLE]',
    'is_sorted_by': '<p>使用给定的比较函数检查切片中的元素是否已排序。</p>\n<p>本函数不使用 <code>PartialOrd::partial_cmp</code>，而是使用给定的 <code>compare</code> 函数来判断两个元素是否可视为处于已排序顺序中。</p>\n<h5 id="examples-105"><a class="doc-anchor" href="#examples-105">§</a>示例</h5>\n[EXAMPLE]',
    'is_sorted_by_key': '<p>使用给定的键提取函数检查切片中的元素是否已排序。</p>\n<p>本函数并不直接比较切片元素，而是按 <code>f</code> 所决定的键进行比较。除此之外与 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.is_sorted" title="method slice::is_sorted"><code>is_sorted</code></a> 等价；更多信息请参阅该方法的文档。</p>\n<h5 id="examples-106"><a class="doc-anchor" href="#examples-106">§</a>示例</h5>\n[EXAMPLE]',
    'partition_point': '<p>依据给定的谓词返回切分点的索引（即第二个分区的首元素索引）。</p>\n<p>切片假定已按给定谓词切分，意味着所有谓词返回 true 的元素位于切片开头，所有返回 false 的元素位于切片末尾。例如，<code>[7, 15, 3, 5, 4, 12, 6]</code> 在谓词 <code>x % 2 != 0</code> 下就是切分好的（所有奇数在前、所有偶数在后）。</p>\n<p>若切片并未真正切分，则返回结果是未指定且无意义的，因为本方法本质上是一种二分查找。</p>\n<p>另请参阅 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.binary_search" title="method slice::binary_search"><code>binary_search</code></a>、<a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.binary_search_by" title="method slice::binary_search_by"><code>binary_search_by</code></a> 与 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.binary_search_by_key" title="method slice::binary_search_by_key"><code>binary_search_by_key</code></a>。</p>\n<h5 id="examples-107"><a class="doc-anchor" href="#examples-107">§</a>示例</h5>\n[EXAMPLE]',
    'split_off': '<p>移除对应给定范围的子切片，并返回它的引用。</p>\n<p>若给定范围越界，则返回 <code>None</code> 且不修改切片。</p>\n<p>注意，本方法只接受单边区间（如 <code>2..</code> 或 <code>..6</code>），不接受 <code>2..6</code>。</p>\n<h5 id="examples-108"><a class="doc-anchor" href="#examples-108">§</a>示例</h5>\n<p>切下切片的前三个元素：</p>\n[EXAMPLE]',
    'split_off_mut': '<p>移除对应给定范围的子切片，并返回它的可变引用。</p>\n<p>若给定范围越界，则返回 <code>None</code> 且不修改切片。</p>\n<p>注意，本方法只接受单边区间（如 <code>2..</code> 或 <code>..6</code>），不接受 <code>2..6</code>。</p>\n<h5 id="examples-109"><a class="doc-anchor" href="#examples-109">§</a>示例</h5>\n<p>切下切片的前三个元素：</p>\n[EXAMPLE]',
    'split_off_first': '<p>移除切片的第一个元素并返回它的引用。</p>\n<p>若切片为空则返回 <code>None</code>。</p>\n<h5 id="examples-110"><a class="doc-anchor" href="#examples-110">§</a>示例</h5>\n[EXAMPLE]',
    'split_off_first_mut': '<p>移除切片的第一个元素并返回它的可变引用。</p>\n<p>若切片为空则返回 <code>None</code>。</p>\n<h5 id="examples-111"><a class="doc-anchor" href="#examples-111">§</a>示例</h5>\n[EXAMPLE]',
    'split_off_last': '<p>移除切片的最后一个元素并返回它的引用。</p>\n<p>若切片为空则返回 <code>None</code>。</p>\n<h5 id="examples-112"><a class="doc-anchor" href="#examples-112">§</a>示例</h5>\n[EXAMPLE]',
    'split_off_last_mut': '<p>移除切片的最后一个元素并返回它的可变引用。</p>\n<p>若切片为空则返回 <code>None</code>。</p>\n<h5 id="examples-113"><a class="doc-anchor" href="#examples-113">§</a>示例</h5>\n[EXAMPLE]',
    'get_disjoint_unchecked_mut': '<p>一次性返回对多个索引的可变引用，不做任何检查。</p>\n<p>索引可以是 <code>usize</code>、<a href="https://doc.rust-lang.org/1.95.0/core/ops/range/struct.Range.html" title="struct core::ops::range::Range"><code>Range</code></a> 或 <a href="https://doc.rust-lang.org/1.95.0/core/ops/range/struct.RangeInclusive.html" title="struct core::ops::range::RangeInclusive"><code>RangeInclusive</code></a>。注意本方法接收的是一个数组，因此所有索引类型必须一致；若传入的是 <code>usize</code> 数组，则返回的是对单个元素的可变引用数组；若传入的是区间数组，则返回的是对子切片的可变引用数组。</p>\n<p>如需安全版本，请参阅 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.get_disjoint_mut" title="method slice::get_disjoint_mut"><code>get_disjoint_mut</code></a>。</p>\n<h5 id="safety-10"><a class="doc-anchor" href="#safety-10">§</a>安全性</h5>\n<p>即便不使用所得到的引用，使用重叠或越界的索引调用本方法也属于<em><a href="https://doc.rust-lang.org/reference/behavior-considered-undefined.html">未定义行为</a></em>。</p>\n<h5 id="examples-114"><a class="doc-anchor" href="#examples-114">§</a>示例</h5>\n[EXAMPLE]',
    'get_disjoint_mut': '<p>一次性返回对多个索引的可变引用。</p>\n<p>索引可以是 <code>usize</code>、<a href="https://doc.rust-lang.org/1.95.0/core/ops/range/struct.Range.html" title="struct core::ops::range::Range"><code>Range</code></a> 或 <a href="https://doc.rust-lang.org/1.95.0/core/ops/range/struct.RangeInclusive.html" title="struct core::ops::range::RangeInclusive"><code>RangeInclusive</code></a>。注意本方法接收的是一个数组，因此所有索引类型必须一致；若传入的是 <code>usize</code> 数组，则返回的是对单个元素的可变引用数组；若传入的是区间数组，则返回的是对子切片的可变引用数组。</p>\n<p>若任一索引越界或存在重叠索引则返回错误。空区间若位于另一区间的开头或末尾不被视为重叠，但位于中间则视为重叠。</p>\n<p>本方法以 O(n²) 的开销检查索引之间没有重叠，因此传入大量索引时请注意。</p>\n<h5 id="examples-115"><a class="doc-anchor" href="#examples-115">§</a>示例</h5>\n[EXAMPLE]',
    'element_offset': '<p>返回某元素引用所指向的索引。</p>\n<p>若 <code>element</code> 并不指向切片中某个元素的起点，则返回 <code>None</code>。</p>\n<p>本方法对于扩展诸如 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.split" title="method slice::split"><code>slice::split</code></a> 这样的切片迭代器非常有用。</p>\n<p>注意本方法使用了指针算术，<strong>并不比较元素</strong>。若要通过比较查找元素索引，请改用 <a href="https://doc.rust-lang.org/1.95.0/core/iter/traits/iterator/trait.Iterator.html#method.position" title="method core::iter::traits::iterator::Iterator::position"><code>.iter().position()</code></a>。</p>\n<h5 id="panics-34"><a class="doc-anchor" href="#panics-34">§</a>Panics</h5>\n<p>若 <code>T</code> 是零大小类型则 panic。</p>\n<h5 id="examples-116"><a class="doc-anchor" href="#examples-116">§</a>示例</h5>\n<p>基本用法：</p>\n[EXAMPLE]',
    'subslice_range': '<p>返回某子切片所对应的索引区间。</p>\n<p>若 <code>subslice</code> 不指向切片内部，或未与切片中元素对齐，则返回 <code>None</code>。</p>\n<p>本方法<strong>不比较元素</strong>，而是找出 <code>subslice</code> 在切片中所源自的位置。若要通过比较查找子切片的索引，请改用 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.windows" title="method slice::windows"><code>.windows()</code></a><a href="https://doc.rust-lang.org/1.95.0/core/iter/traits/iterator/trait.Iterator.html#method.position" title="method core::iter::traits::iterator::Iterator::position"><code>.position()</code></a>。</p>\n<p>本方法对于扩展诸如 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.split" title="method slice::split"><code>slice::split</code></a> 这样的切片迭代器非常有用。</p>\n<p>若 <code>subslice</code> 长度为 0 并指向另一段独立切片的开头或结尾，则可能返回误报（即 <code>Some(0..0)</code> 或 <code>Some(self.len()..self.len())</code>）。</p>\n<h5 id="panics-35"><a class="doc-anchor" href="#panics-35">§</a>Panics</h5>\n<p>若 <code>T</code> 是零大小类型则 panic。</p>\n<h5 id="examples-117"><a class="doc-anchor" href="#examples-117">§</a>示例</h5>\n<p>基本用法：</p>\n[EXAMPLE]',
    'utf8_chunks': '<p>在此切片上创建一个迭代器，遍历连续的合法 UTF-8 区间及其之间的非 UTF-8 片段。</p>\n<p>迭代器所产出项的文档请参阅 <a href="https://doc.rust-lang.org/1.95.0/core/str/lossy/struct.Utf8Chunk.html" title="struct core::str::lossy::Utf8Chunk"><code>Utf8Chunk</code></a>。</p>\n<h5 id="examples-118"><a class="doc-anchor" href="#examples-118">§</a>示例</h5>\n<p>本函数可将任意（但主要是 UTF-8 的）字节格式化为形如 <code>c"..."</code> 的 C 字符串字面量。</p>\n[EXAMPLE]',
    'to_ascii_uppercase': '<p>返回一个包含本切片副本的向量，其中每个字节都被映射为对应的 ASCII 大写形式。</p>\n<p>ASCII 字母 <code>a</code> 到 <code>z</code> 会被映射为 <code>A</code> 到 <code>Z</code>，但非 ASCII 字母保持不变。</p>\n<p>若希望就地大写化，请使用 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.make_ascii_uppercase" title="method slice::make_ascii_uppercase"><code>make_ascii_uppercase</code></a>。</p>',
    'to_ascii_lowercase': '<p>返回一个包含本切片副本的向量，其中每个字节都被映射为对应的 ASCII 小写形式。</p>\n<p>ASCII 字母 <code>A</code> 到 <code>Z</code> 会被映射为 <code>a</code> 到 <code>z</code>，但非 ASCII 字母保持不变。</p>\n<p>若希望就地小写化，请使用 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.make_ascii_lowercase" title="method slice::make_ascii_lowercase"><code>make_ascii_lowercase</code></a>。</p>',
    'partial_sort_unstable': '<p>对切片中的指定区间进行不稳定的部分排序。</p>\n<p>完成后，对指定区间 <code>start..end</code> 保证：</p>\n<ol>\n<li><code>self[..start]</code> 中的每个元素都小于等于</li>\n<li><code>self[start..end]</code> 中的每个元素（已排序），并且后者小于等于</li>\n<li><code>self[end..]</code> 中的每个元素。</li>\n</ol>\n<p>此部分排序是不稳定的，意味着指定区间内的相等元素顺序可能被重排。指定区间外的元素顺序也可能被重排，但上述保证依然成立。</p>\n<p>此部分排序是原地（不分配）的，最坏复杂度为 <em>O</em>(<em>n</em> + <em>k</em> * log(<em>k</em>))，其中 <em>n</em> 为切片长度，<em>k</em> 为指定区间长度。</p>\n<p>实现细节请参阅 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.sort_unstable" title="method slice::sort_unstable"><code>sort_unstable</code></a> 的文档。</p>\n<h5 id="panics-20"><a class="doc-anchor" href="#panics-20">§</a>Panics</h5>\n<p>当 <a href="https://doc.rust-lang.org/1.95.0/core/cmp/trait.Ord.html" title="trait core::cmp::Ord"><code>Ord</code></a> 的实现并非全序、或其实现本身 panic、或指定区间越界时，可能 panic。</p>\n<h5 id="examples-83"><a class="doc-anchor" href="#examples-83">§</a>示例</h5>\n[EXAMPLE]',
    'partial_sort_unstable_by': '<p>使用给定的比较函数对切片中的指定区间进行不稳定的部分排序。</p>\n<p>完成后，对指定区间 <code>start..end</code> 保证：</p>\n<ol>\n<li><code>self[..start]</code> 中的每个元素都小于等于</li>\n<li><code>self[start..end]</code> 中的每个元素（已排序），并且后者小于等于</li>\n<li><code>self[end..]</code> 中的每个元素。</li>\n</ol>\n<p>此部分排序是不稳定的，意味着指定区间内的相等元素顺序可能被重排。指定区间外的元素顺序也可能被重排，但上述保证依然成立。</p>\n<p>此部分排序是原地（不分配）的，最坏复杂度为 <em>O</em>(<em>n</em> + <em>k</em> * log(<em>k</em>))，其中 <em>n</em> 为切片长度，<em>k</em> 为指定区间长度。</p>\n<p>实现细节请参阅 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.sort_unstable_by" title="method slice::sort_unstable_by"><code>sort_unstable_by</code></a> 的文档。</p>\n<h5 id="panics-21"><a class="doc-anchor" href="#panics-21">§</a>Panics</h5>\n<p>当 <code>compare</code> 不是全序、或其本身 panic、或指定区间越界时，可能 panic。</p>\n<h5 id="examples-84"><a class="doc-anchor" href="#examples-84">§</a>示例</h5>\n[EXAMPLE]',
    'partial_sort_unstable_by_key': '<p>使用给定的键提取函数对切片中的指定区间进行不稳定的部分排序。</p>\n<p>完成后，对指定区间 <code>start..end</code> 保证：</p>\n<ol>\n<li><code>self[..start]</code> 中的每个元素都小于等于</li>\n<li><code>self[start..end]</code> 中的每个元素（已按对应键排序），并且后者小于等于</li>\n<li><code>self[end..]</code> 中的每个元素。</li>\n</ol>\n<p>此部分排序是不稳定的，意味着指定区间内的相等元素顺序可能被重排。指定区间外的元素顺序也可能被重排，但上述保证依然成立。</p>\n<p>此部分排序是原地（不分配）的，最坏复杂度为 <em>O</em>(<em>n</em> + <em>k</em> * log(<em>k</em>))，其中 <em>n</em> 为切片长度，<em>k</em> 为指定区间长度。</p>\n<p>实现细节请参阅 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.sort_unstable_by_key" title="method slice::sort_unstable_by_key"><code>sort_unstable_by_key</code></a> 的文档。</p>\n<h5 id="panics-22"><a class="doc-anchor" href="#panics-22">§</a>Panics</h5>\n<p>当键提取函数的实现并非全序、或其本身 panic、或指定区间越界时，可能 panic。</p>\n<h5 id="examples-85"><a class="doc-anchor" href="#examples-85">§</a>示例</h5>\n[EXAMPLE]',
    'select_nth_unstable': '<p>对切片中的指定区间进行不稳定的选择排序，使区间内的某个元素被放到正确排序位置。</p>\n<p>完成后，保证：</p>\n<ol>\n<li><code>self[..start]</code> 中的每个元素都小于等于</li>\n<li><code>self[start..end]</code> 中的每个元素（已部分排序），并且后者小于等于</li>\n<li><code>self[end..]</code> 中的每个元素。</li>\n</ol>\n<p>特别地，<code>self[k]</code> 等于排序后该位置的元素。</p>\n<p>此排序是不稳定的。区间外的元素顺序也可能被重排，但上述保证依然成立。</p>\n<p>此操作是原地（不分配）的；其最坏、平均与最佳时间复杂度均为 <em>O</em>(<em>n</em>)；空间复杂度为 <em>O</em>(1)。</p>\n<p>实现细节请参阅 <a href="https://doc.rust-lang.org/1.95.0/std/primitive.slice.html#method.select_nth_unstable_by" title="method slice::select_nth_unstable_by"><code>select_nth_unstable_by</code></a> 的文档。</p>\n<h5 id="panics-23"><a class="doc-anchor" href="#panics-23">§</a>Panics</h5>\n<p>当 <a href="https://doc.rust-lang.org/1.95.0/core/cmp/trait.Ord.html" title="trait core::cmp::Ord"><code>Ord</code></a> 的实现并非全序、或其实现本身 panic、或指定区间越界时，可能 panic。</p>\n<h5 id="examples-86"><a class="doc-anchor" href="#examples-86">§</a>示例</h5>\n[EXAMPLE]',
    'select_nth_unstable_by': '<p>使用给定的比较函数对切片中的指定区间进行不稳定的选择排序，使区间内某元素被放到正确排序位置。</p>\n<p>完成后，保证：</p>\n<ol>\n<li><code>self[..start]</code> 中的每个元素都小于等于</li>\n<li><code>self[start..end]</code> 中的每个元素（已部分排序），并且后者小于等于</li>\n<li><code>self[end..]</code> 中的每个元素。</li>\n</ol>\n<p>特别地，<code>self[k]</code> 等于排序后该位置的元素。</p>\n<p>此排序是不稳定的。区间外的元素顺序也可能被重排，但上述保证依然成立。</p>\n<p>此操作是原地（不分配）的；其最坏、平均与最佳时间复杂度均为 <em>O</em>(<em>n</em>)；空间复杂度为 <em>O</em>(1)。</p>\n<h5 id="panics-24"><a class="doc-anchor" href="#panics-24">§</a>Panics</h5>\n<p>当 <code>compare</code> 不是全序、或其本身 panic、或指定区间越界时，可能 panic。</p>\n<h5 id="examples-87"><a class="doc-anchor" href="#examples-87">§</a>示例</h5>\n[EXAMPLE]',
    'select_nth_unstable_by_key': '<p>使用给定的键提取函数对切片中的指定区间进行不稳定的选择排序。</p>\n<p>完成后，保证：</p>\n<ol>\n<li><code>self[..start]</code> 中的每个元素都小于等于</li>\n<li><code>self[start..end]</code> 中的每个元素（已部分排序），并且后者小于等于</li>\n<li><code>self[end..]</code> 中的每个元素。</li>\n</ol>\n<p>特别地，<code>self[k]</code> 等于排序后该位置的元素。</p>\n<p>此排序是不稳定的。区间外的元素顺序也可能被重排，但上述保证依然成立。</p>\n<p>此操作是原地（不分配）的；其最坏、平均与最佳时间复杂度均为 <em>O</em>(<em>n</em>)；空间复杂度为 <em>O</em>(1)。</p>\n<h5 id="panics-25"><a class="doc-anchor" href="#panics-25">§</a>Panics</h5>\n<p>当键提取函数不是全序、或其本身 panic、或指定区间越界时，可能 panic。</p>\n<h5 id="examples-88"><a class="doc-anchor" href="#examples-88">§</a>示例</h5>\n[EXAMPLE]',
}


def main():
    with open(PATH, 'r', encoding='utf-8') as f:
        c = f.read()

    found = 0
    missed_blocks = []
    for name, old in ORIGINAL_BLOCKS:
        if name not in TRANSLATIONS:
            missed_blocks.append(name)
            continue
        # Need to restore [EXAMPLE] from old to find the actual location.
        # Build the full old block as it appears in file.
        full_old = '<div class="docblock">' + old + '</div>'
        # Find the new block
        new_inner = TRANSLATIONS[name]
        full_new = '<div class="docblock">' + new_inner + '</div>'

        if full_old in c:
            c = c.replace(full_old, full_new)
            found += 1
        else:
            missed_blocks.append(name)

    with open(PATH, 'w', encoding='utf-8') as f:
        f.write(c)

    cjk = re.findall(r'[一-鿿]', c)
    print(f'Found: {found}/{len(ORIGINAL_BLOCKS)} docblocks')
    print(f'CJK: {len(cjk)}')
    if missed_blocks:
        print('Missed blocks:')
        for n in missed_blocks:
            print(f'  {n}')


if __name__ == '__main__':
    main()