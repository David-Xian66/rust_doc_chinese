#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补译 tokio/fs/ 5 个 struct 文件的英文 docblock。"""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def read_bytes(rel):
    with open(os.path.join(ROOT, rel), 'rb') as f:
        return f.read()


def write_bytes(rel, data):
    with open(os.path.join(ROOT, rel), 'wb') as f:
        f.write(data)


def E(s):
    """Encode UTF-8 string to bytes."""
    return s.encode('utf-8')


def add(rel, pairs):
    PLAN.append((rel, pairs))


PLAN = []


# ============================================================
# fs/struct.DirBuilder.html (9 issues)
# ============================================================
add('fs/struct.DirBuilder.html', [
    (E('<p>Creates a new set of options with default mode/security settings for all\nplatforms and also non-recursive.</p>'),
     E('<p>使用所有平台的默认模式/安全设置创建一个新的选项集合，并且不递归。</p>')),
    (E('<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.DirBuilder.html#method.new" title="associated function std::fs::DirBuilder::new"><code>std::fs::DirBuilder::new</code></a>.</p>'),
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.DirBuilder.html#method.new" title="associated function std::fs::DirBuilder::new"><code>std::fs::DirBuilder::new</code></a> 的异步版本。</p>')),
    (E('<p>Indicates whether to create directories recursively (including all parent directories).\nParents that do not exist are created with the same security and permissions settings.</p>'),
     E('<p>指示是否递归地创建目录（包括所有父目录）。\n不存在的父目录将使用相同的安全性和权限设置创建。</p>')),
    (E('<p>This option defaults to <code>false</code>.</p>'),
     E('<p>此选项默认为 <code>false</code>。</p>')),
    (E('<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.DirBuilder.html#method.recursive" title="method std::fs::DirBuilder::recursive"><code>std::fs::DirBuilder::recursive</code></a>.</p>'),
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.DirBuilder.html#method.recursive" title="method std::fs::DirBuilder::recursive"><code>std::fs::DirBuilder::recursive</code></a> 的异步版本。</p>')),
    (E('<p>Creates the specified directory with the configured options.</p>'),
     E('<p>使用配置的选项创建指定的目录。</p>')),
    (E('<p>It is considered an error if the directory already exists unless\nrecursive mode is enabled.</p>'),
     E('<p>如果目录已经存在（除非启用了递归模式），\n则视为错误。</p>')),
    (E('<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.DirBuilder.html#method.create" title="method std::fs::DirBuilder::create"><code>std::fs::DirBuilder::create</code></a>.</p>'),
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.DirBuilder.html#method.create" title="method std::fs::DirBuilder::create"><code>std::fs::DirBuilder::create</code></a> 的异步版本。</p>')),
    (E('<p>An error will be returned under the following circumstances:</p>'),
     E('<p>在以下情况下将返回错误：</p>')),
])


# ============================================================
# fs/struct.DirEntry.html (11 issues)
# ============================================================
add('fs/struct.DirEntry.html', [
    (E('<p>Returns the full path to the file that this entry represents.</p>'),
     E('<p>返回此条目所代表的文件的完整路径。</p>')),
    (E('<p>The full path is created by joining the original path to <code>read_dir</code>\nwith the filename of this entry.</p>'),
     E('<p>完整路径是通过将传递给 <code>read_dir</code> 的原始路径与此条目的\r\n文件名连接起来创建的。</p>')),
    (E('<p>This prints output like:</p>'),
     E('<p>这将输出类似如下内容：</p>')),
    (E('<p>The exact text, of course, depends on what files you have in <code>.</code>.</p>'),
     E('<p>当然，确切的文本取决于 <code>.</code> 中有哪些文件。</p>')),
    (E('<p>Returns the bare file name of this directory entry without any other\nleading path component.</p>'),
     E('<p>返回此目录条目的裸文件名，不含任何其他\r\n前导路径组件。</p>')),
    (E('<p>Returns the metadata for the file that this entry points at.</p>'),
     E('<p>返回此条目所指向的文件的元数据。</p>')),
    (E('<p>This function will not traverse symlinks if this entry points at a\nsymlink.</p>'),
     E('<p>如果此条目指向符号链接，此函数不会遍历符号链接。</p>')),
    (E('<p>On Windows this function is cheap to call (no extra system calls\nneeded), but on Unix platforms this function is the equivalent of\ncalling <code>symlink_metadata</code> on the path.</p>'),
     E('<p>在 Windows 上调用此函数开销很小（无需额外的系统调用），\r\n但在 Unix 平台上，此函数等价于\r\n对该路径调用 <code>symlink_metadata</code>。</p>')),
    (E('<p>Returns the file type for the file that this entry points at.</p>'),
     E('<p>返回此条目所指向的文件的类型。</p>')),
    # p 9 same as p 6
    (E('<p>This function will not traverse symlinks if this entry points at a\nsymlink.</p>'),
     E('<p>如果此条目指向符号链接，此函数不会遍历符号链接。</p>')),
    (E('<p>On Windows and most Unix platforms this function is free (no extra\nsystem calls needed), but some Unix platforms may require the equivalent\ncall to <code>symlink_metadata</code> to learn about the target file type.</p>'),
     E('<p>在 Windows 和大多数 Unix 平台上，此函数无需任何代价（不需要额外\r\n的系统调用），但某些 Unix 平台可能需要\r\n通过等价的 <code>symlink_metadata</code> 调用来了解目标文件的类型。</p>')),
])


# ============================================================
# fs/struct.ReadDir.html (6 issues)
# ============================================================
add('fs/struct.ReadDir.html', [
    (E('<p>Returns the next entry in the directory stream.</p>'),
     E('<p>返回目录流中的下一个条目。</p>')),
    (E('<p>This method is cancellation safe.</p>'),
     E('<p>此方法是可取消安全的。</p>')),
    (E('<p>Polls for the next directory entry in the stream.</p>'),
     E('<p>轮询流中的下一个目录条目。</p>')),
    (E('<p>This method returns:</p>'),
     E('<p>此方法返回：</p>')),
    (E('<p>When the method returns <code>Poll::Pending</code>, the <code>Waker</code> in the provided\n<code>Context</code> is scheduled to receive a wakeup when the next directory entry\nbecomes available on the underlying IO resource.</p>'),
     E('<p>当方法返回 <code>Poll::Pending</code> 时，提供的\r\n<code>Context</code> 中的 <code>Waker</code> 会被安排为在底层 IO 资源上\r\n可获取下一个目录条目时收到唤醒。</p>')),
    (E('<p>Note that on multiple calls to <code>poll_next_entry</code>, only the <code>Waker</code> from\nthe <code>Context</code> passed to the most recent call is scheduled to receive a\nwakeup.</p>'),
     E('<p>请注意，在多次调用 <code>poll_next_entry</code> 时，只有\r\n传递给最近一次调用的 <code>Context</code> 中的 <code>Waker</code> 会被安排\r\n接收唤醒。</p>')),
])


# ============================================================
# fs/struct.File.html (43 issues)
# ============================================================
add('fs/struct.File.html', [
    (E('<p>Attempts to open a file in read-only mode.</p>'),
     E('<p>尝试以只读模式打开一个文件。</p>')),
    (E('<p>See <a href="struct.OpenOptions.html" title="struct tokio::fs::OpenOptions"><code>OpenOptions</code></a> for more details.</p>'),
     E('<p>更多详情请参阅 <a href="struct.OpenOptions.html" title="struct tokio::fs::OpenOptions"><code>OpenOptions</code></a>。</p>')),
    (E('<p>This function will return an error if called from outside of the Tokio\nruntime or if path does not already exist. Other errors may also be\nreturned according to <code>OpenOptions::open</code>.</p>'),
     E('<p>如果在 Tokio 运行时之外调用此函数，或者路径\r\n尚不存在，则此函数将返回错误。\r\n根据 <code>OpenOptions::open</code> 的定义，也可能会返回其他错误。</p>')),
    (E('<p>The <a href="../io/trait.AsyncReadExt.html#method.read_to_end" title="method tokio::io::AsyncReadExt::read_to_end"><code>read_to_end</code></a> method is defined on the <a href="../io/trait.AsyncReadExt.html" title="trait tokio::io::AsyncReadExt"><code>AsyncReadExt</code></a> trait.</p>'),
     E('<p><a href="../io/trait.AsyncReadExt.html#method.read_to_end" title="method tokio::io::AsyncReadExt::read_to_end"><code>read_to_end</code></a> 方法定义于 <a href="../io/trait.AsyncReadExt.html" title="trait tokio::io::AsyncReadExt"><code>AsyncReadExt</code></a> trait 上。</p>')),
    (E('<p>Opens a file in write-only mode.</p>'),
     E('<p>以只写模式打开一个文件。</p>')),
    (E('<p>This function will create a file if it does not exist, and will truncate\nit if it does.</p>'),
     E('<p>如果文件不存在，此函数将创建该文件；\r\n如果文件已存在，则会将其截断。</p>')),
    # p 6 same as p 1
    (E('<p>See <a href="struct.OpenOptions.html" title="struct tokio::fs::OpenOptions"><code>OpenOptions</code></a> for more details.</p>'),
     E('<p>更多详情请参阅 <a href="struct.OpenOptions.html" title="struct tokio::fs::OpenOptions"><code>OpenOptions</code></a>。</p>')),
    (E('<p>Results in an error if called from outside of the Tokio runtime or if\nthe underlying <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.File.html#method.create" title="associated function std::fs::File::create"><code>create</code></a> call results in an error.</p>'),
     E('<p>如果在 Tokio 运行时之外调用，或底层的\r\n<a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.File.html#method.create" title="associated function std::fs::File::create"><code>create</code></a> 调用导致错误，则\r\n会返回错误。</p>')),
    # p 8 same as p 3 layout (write_all)
    (E('<p>The <a href="../io/trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> method is defined on the <a href="../io/trait.AsyncWriteExt.html" title="trait tokio::io::AsyncWriteExt"><code>AsyncWriteExt</code></a> trait.</p>'),
     E('<p><a href="../io/trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> 方法定义于 <a href="../io/trait.AsyncWriteExt.html" title="trait tokio::io::AsyncWriteExt"><code>AsyncWriteExt</code></a> trait 上。</p>')),
    (E('<p>Opens a file in read-write mode.</p>'),
     E('<p>以读写模式打开一个文件。</p>')),
    (E('<p>This function will create a file if it does not exist, or return an error\nif it does. This way, if the call succeeds, the file returned is guaranteed\nto be new.</p>'),
     E('<p>如果文件不存在，此函数将创建该文件；如果文件已存在，\r\n则返回错误。这样，如果调用成功，则可以\r\n保证返回的文件是新建的。</p>')),
    (E('<p>This option is useful because it is atomic. Otherwise between checking\nwhether a file exists and creating a new one, the file may have been\ncreated by another process (a TOCTOU race condition / attack).</p>'),
     E('<p>此选项很有用，因为它是原子操作。否则，在检查\r\n文件是否存在和创建新文件之间，文件\r\n可能被另一个进程创建（TOCTOU 竞争条件 / 攻击）。</p>')),
    (E('<p>This can also be written using <code>File::options().read(true).write(true).create_new(true).open(...)</code>.</p>'),
     E('<p>这也可以通过 <code>File::options().read(true).write(true).create_new(true).open(...)</code> 来编写。</p>')),
    # p 13 same as p 1
    (E('<p>See <a href="struct.OpenOptions.html" title="struct tokio::fs::OpenOptions"><code>OpenOptions</code></a> for more details.</p>'),
     E('<p>更多详情请参阅 <a href="struct.OpenOptions.html" title="struct tokio::fs::OpenOptions"><code>OpenOptions</code></a>。</p>')),
    # p 14 same as p 8 (write_all again)
    (E('<p>The <a href="../io/trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> method is defined on the <a href="../io/trait.AsyncWriteExt.html" title="trait tokio::io::AsyncWriteExt"><code>AsyncWriteExt</code></a> trait.</p>'),
     E('<p><a href="../io/trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> 方法定义于 <a href="../io/trait.AsyncWriteExt.html" title="trait tokio::io::AsyncWriteExt"><code>AsyncWriteExt</code></a> trait 上。</p>')),
    (E('<p>Returns a new <a href="struct.OpenOptions.html" title="struct tokio::fs::OpenOptions"><code>OpenOptions</code></a> object.</p>'),
     E('<p>返回一个新的 <a href="struct.OpenOptions.html" title="struct tokio::fs::OpenOptions"><code>OpenOptions</code></a> 对象。</p>')),
    (E('<p>This function returns a new <code>OpenOptions</code> object that you can use to\nopen or create a file with specific options if <code>open()</code> or <code>create()</code>\nare not appropriate.</p>'),
     E('<p>此函数返回一个新的 <code>OpenOptions</code> 对象，如果 <code>open()</code>\r\n或 <code>create()</code> 不合适，你可以使用它以\r\n特定选项打开或创建文件。</p>')),
    (E('<p>It is equivalent to <code>OpenOptions::new()</code>, but allows you to write more\nreadable code. Instead of\n<code>OpenOptions::new().append(true).open("example.log")</code>,\nyou can write <code>File::options().append(true).open("example.log")</code>. This\nalso avoids the need to import <code>OpenOptions</code>.</p>'),
     E('<p>它等价于 <code>OpenOptions::new()</code>，但使你能够编写更\r\n易读的代码。与其写\r\n<code>OpenOptions::new().append(true).open("example.log")</code>，\r\n你可以写 <code>File::options().append(true).open("example.log")</code>。\r\n这样还可以避免导入 <code>OpenOptions</code>。</p>')),
    (E('<p>See the <a href="struct.OpenOptions.html#method.new" title="associated function tokio::fs::OpenOptions::new"><code>OpenOptions::new</code></a> function for more details.</p>'),
     E('<p>更多详情请参阅 <a href="struct.OpenOptions.html#method.new" title="associated function tokio::fs::OpenOptions::new"><code>OpenOptions::new</code></a> 函数。</p>')),
    (E('<p>Converts a <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.File.html" title="struct std::fs::File"><code>std::fs::File</code></a> to a <a href="struct.File.html" title="struct tokio::fs::File"><code>tokio::fs::File</code></a>.</p>'),
     E('<p>将 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.File.html" title="struct std::fs::File"><code>std::fs::File</code></a> 转换为 <a href="struct.File.html" title="struct tokio::fs::File"><code>tokio::fs::File</code></a>。</p>')),
    (E('<p>Attempts to sync all OS-internal metadata to disk.</p>'),
     E('<p>尝试将所有操作系统内部元数据同步到磁盘。</p>')),
    (E('<p>This function will attempt to ensure that all in-core data reaches the\nfilesystem before returning.</p>'),
     E('<p>此函数将尝试确保所有核心内数据在返回之前\r\n到达文件系统。</p>')),
    # p 22 same as p 8 (write_all)
    (E('<p>The <a href="../io/trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> method is defined on the <a href="../io/trait.AsyncWriteExt.html" title="trait tokio::io::AsyncWriteExt"><code>AsyncWriteExt</code></a> trait.</p>'),
     E('<p><a href="../io/trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> 方法定义于 <a href="../io/trait.AsyncWriteExt.html" title="trait tokio::io::AsyncWriteExt"><code>AsyncWriteExt</code></a> trait 上。</p>')),
    (E('<p>This function is similar to <code>sync_all</code>, except that it may not\nsynchronize file metadata to the filesystem.</p>'),
     E('<p>此函数与 <code>sync_all</code> 类似，只是它可能\r\n不会将文件元数据同步到文件系统。</p>')),
    (E('<p>This is intended for use cases that must synchronize content, but don’t\nneed the metadata on disk. The goal of this method is to reduce disk\noperations.</p>'),
     E('<p>此方法适用于必须同步内容，但不需要\r\n磁盘上的元数据的场景。该方法的目标是减少\r\n磁盘操作。</p>')),
    (E('<p>Note that some platforms may simply implement this in terms of <code>sync_all</code>.</p>'),
     E('<p>请注意，某些平台可能只是通过 <code>sync_all</code> 来实现此功能。</p>')),
    # p 26 same as p 8
    (E('<p>The <a href="../io/trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> method is defined on the <a href="../io/trait.AsyncWriteExt.html" title="trait tokio::io::AsyncWriteExt"><code>AsyncWriteExt</code></a> trait.</p>'),
     E('<p><a href="../io/trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> 方法定义于 <a href="../io/trait.AsyncWriteExt.html" title="trait tokio::io::AsyncWriteExt"><code>AsyncWriteExt</code></a> trait 上。</p>')),
    (E('<p>Truncates or extends the underlying file, updating the size of this file to become size.</p>'),
     E('<p>截断或扩展底层文件，将此文件的大小更新为指定的大小。</p>')),
    (E('<p>If the size is less than the current file’s size, then the file will be\nshrunk. If it is greater than the current file’s size, then the file\nwill be extended to size and have all of the intermediate data filled in\nwith 0s.</p>'),
     E('<p>如果该大小小于文件的当前大小，则\r\n文件将被缩减。如果大于文件的当前大小，\r\n则文件将扩展到该大小，并且\r\n中间的所有数据都将填充为 0。</p>')),
    (E('<p>This function will return an error if the file is not opened for\nwriting.</p>'),
     E('<p>如果文件没有以写入方式打开，\r\n此函数将返回错误。</p>')),
    # p 30 same as p 8
    (E('<p>The <a href="../io/trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> method is defined on the <a href="../io/trait.AsyncWriteExt.html" title="trait tokio::io::AsyncWriteExt"><code>AsyncWriteExt</code></a> trait.</p>'),
     E('<p><a href="../io/trait.AsyncWriteExt.html#method.write_all" title="method tokio::io::AsyncWriteExt::write_all"><code>write_all</code></a> 方法定义于 <a href="../io/trait.AsyncWriteExt.html" title="trait tokio::io::AsyncWriteExt"><code>AsyncWriteExt</code></a> trait 上。</p>')),
    (E('<p>Queries metadata about the underlying file.</p>'),
     E('<p>查询底层文件的元数据。</p>')),
    (E('<p>Creates a new <code>File</code> instance that shares the same underlying file handle\nas the existing <code>File</code> instance. Reads, writes, and seeks will affect both\nFile instances simultaneously.</p>'),
     E('<p>创建一个新的 <code>File</code> 实例，与现有的 <code>File</code> 实例\r\n共享相同的底层文件句柄。读、写和寻\r\n作会同时影响两个 File 实例。</p>')),
    (E('<p>Destructures <code>File</code> into a <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.File.html" title="struct std::fs::File"><code>std::fs::File</code></a>. This function is\nasync to allow any in-flight operations to complete.</p>'),
     E('<p>将 <code>File</code> 解构为 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.File.html" title="struct std::fs::File"><code>std::fs::File</code></a>。此函数是\r\n异步的，以便让任何进行中的\r\n操作完成。</p>')),
    (E('<p>Use <code>File::try_into_std</code> to attempt conversion immediately.</p>'),
     E('<p>使用 <code>File::try_into_std</code> 尝试立即转换。</p>')),
    (E('<p>Tries to immediately destructure <code>File</code> into a <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.File.html" title="struct std::fs::File"><code>std::fs::File</code></a>.</p>'),
     E('<p>尝试立即将 <code>File</code> 解构为 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.File.html" title="struct std::fs::File"><code>std::fs::File</code></a>。</p>')),
    (E('<p>This function will return an error containing the file if some\noperation is in-flight.</p>'),
     E('<p>如果有正在进行的操作，\r\n此函数将返回一个包含该文件的错误。</p>')),
    (E('<p>Changes the permissions on the underlying file.</p>'),
     E('<p>更改底层文件的权限。</p>')),
    (E('<p>This function currently corresponds to the <code>fchmod</code> function on Unix and\nthe <code>SetFileInformationByHandle</code> function on Windows. Note that, this\n<a href="https://doc.rust-lang.org/std/io/index.html#platform-specific-behavior">may change in the future</a>.</p>'),
     E('<p>此函数当前对应于 Unix 上的 <code>fchmod</code> 函数以及\r\nWindows 上的 <code>SetFileInformationByHandle</code> 函数。请注意，\r\n此<a href="https://doc.rust-lang.org/std/io/index.html#platform-specific-behavior">行为将来可能会改变</a>。</p>')),
    (E('<p>This function will return an error if the user lacks permission change\nattributes on the underlying file. It may also return an error in other\nos-specific unspecified cases.</p>'),
     E('<p>如果用户缺少对底层文件的权限更改\r\n权限，此函数将返回错误。在其他\r\n未明确说明的特定于操作系统的场景下，它也可能返回错误。</p>')),
    (E('<p>Set the maximum buffer size for the underlying <a href="../io/trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> / <a href="../io/trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> operation.</p>'),
     E('<p>设置底层 <a href="../io/trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> / <a href="../io/trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> 操作的最大缓冲区大小。</p>')),
    (E('<p>Although Tokio uses a sensible default value for this buffer size, this function would be\nuseful for changing that default depending on the situation.</p>'),
     E('<p>尽管 Tokio 为此缓冲区大小使用了合理的默认值，但根据不同\r\n情况，此函数可用于更改该默认值。</p>')),
    (E('<p>Get the maximum buffer size for the underlying <a href="../io/trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> / <a href="../io/trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> operation.</p>'),
     E('<p>获取底层 <a href="../io/trait.AsyncRead.html" title="trait tokio::io::AsyncRead"><code>AsyncRead</code></a> / <a href="../io/trait.AsyncWrite.html" title="trait tokio::io::AsyncWrite"><code>AsyncWrite</code></a> 操作的最大缓冲区大小。</p>')),
])


# ============================================================
# fs/struct.OpenOptions.html (49 issues)
# ============================================================
add('fs/struct.OpenOptions.html', [
    (E('<p>Creates a blank new set of options ready for configuration.</p>'),
     E('<p>创建一个准备好用于配置的空白选项集合。</p>')),
    (E('<p>All options are initially set to <code>false</code>.</p>'),
     E('<p>所有选项最初都设置为 <code>false</code>。</p>')),
    (E('<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.new" title="associated function std::fs::OpenOptions::new"><code>std::fs::OpenOptions::new</code></a></p>'),
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.new" title="associated function std::fs::OpenOptions::new"><code>std::fs::OpenOptions::new</code></a> 的异步版本</p>')),
    (E('<p>Sets the option for read access.</p>'),
     E('<p>设置读访问选项。</p>')),
    (E('<p>This option, when true, will indicate that the file should be\n<code>read</code>-able if opened.</p>'),
     E('<p>当该选项为 true 时，将指示文件在打开后\r\n应可 <code>read</code>。</p>')),
    (E('<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.read" title="method std::fs::OpenOptions::read"><code>std::fs::OpenOptions::read</code></a></p>'),
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.read" title="method std::fs::OpenOptions::read"><code>std::fs::OpenOptions::read</code></a> 的异步版本</p>')),
    (E('<p>Sets the option for write access.</p>'),
     E('<p>设置写访问选项。</p>')),
    (E('<p>This option, when true, will indicate that the file should be\n<code>write</code>-able if opened.</p>'),
     E('<p>当该选项为 true 时，将指示文件在打开后\r\n应可 <code>write</code>。</p>')),
    (E('<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.write" title="method std::fs::OpenOptions::write"><code>std::fs::OpenOptions::write</code></a></p>'),
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.write" title="method std::fs::OpenOptions::write"><code>std::fs::OpenOptions::write</code></a> 的异步版本</p>')),
    (E('<p>Sets the option for the append mode.</p>'),
     E('<p>设置追加模式选项。</p>')),
    (E('<p>This option, when true, means that writes will append to a file instead\nof overwriting previous contents.  Note that setting\n<code>.write(true).append(true)</code> has the same effect as setting only\n<code>.append(true)</code>.</p>'),
     E('<p>当该选项为 true 时，意味着写入将追加到文件末尾，\r\n而不是覆盖之前的内容。请注意，设置\r\n<code>.write(true).append(true)</code> 的效果与仅设置\r\n<code>.append(true)</code> 相同。</p>')),
    (E('<p>For most filesystems, the operating system guarantees that all writes are\natomic: no writes get mangled because another process writes at the same\ntime.</p>'),
     E('<p>对于大多数文件系统，操作系统保证所有\r\n写入操作都是原子的：不会因为\r\n另一个进程同时写入而导致写入失败。</p>')),
    (E('<p>One maybe obvious note when using append-mode: make sure that all data\nthat belongs together is written to the file in one operation. This\ncan be done by concatenating strings before passing them to <a href="../io/trait.AsyncWriteExt.html#method.write" title="method tokio::io::AsyncWriteExt::write"><code>write()</code></a>,\nor using a buffered writer (with a buffer of adequate size),\nand calling <a href="../io/trait.AsyncWriteExt.html#method.flush" title="method tokio::io::AsyncWriteExt::flush"><code>flush()</code></a> when the message is complete.</p>'),
     E('<p>使用追加模式时有一句话可能很明显但仍然要强调：\r\n确保属于一起的所有数据在一次操作中写入文件。\r\n可以通过在将字符串传递给 <a href="../io/trait.AsyncWriteExt.html#method.write" title="method tokio::io::AsyncWriteExt::write"><code>write()</code></a> 之前连接字符串来实现，\r\n或者使用缓冲写入器（缓冲区大小合适），\r\n并在消息完成时调用 <a href="../io/trait.AsyncWriteExt.html#method.flush" title="method tokio::io::AsyncWriteExt::flush"><code>flush()</code></a>。</p>')),
    (E('<p>If a file is opened with both read and append access, beware that after\nopening, and after every write, the position for reading may be set at the\nend of the file. So, before writing, save the current position (using\n<a href="../io/trait.AsyncSeekExt.html#method.seek" title="method tokio::io::AsyncSeekExt::seek"><code>seek</code></a><code>(</code><a href="https://doc.rust-lang.org/1.95.0/std/io/enum.SeekFrom.html" title="enum std::io::SeekFrom"><code>SeekFrom</code></a><code>::</code><a href="https://doc.rust-lang.org/1.95.0/std/io/enum.SeekFrom.html#variant.Current" title="variant std::io::SeekFrom::Current"><code>Current</code></a><code>(0))</code>), and restore it before the next read.</p>'),
     E('<p>如果文件以读和追加访问同时打开，请注意在打开之后以及\r\n每次写入之后，用于读取的位置\r\n可能会被设置在文件末尾。因此，在写入之前，\r\n保存当前位置（使用\r\n<a href="../io/trait.AsyncSeekExt.html#method.seek" title="method tokio::io::AsyncSeekExt::seek"><code>seek</code></a><code>(</code><a href="https://doc.rust-lang.org/1.95.0/std/io/enum.SeekFrom.html" title="enum std::io::SeekFrom"><code>SeekFrom</code></a><code>::</code><a href="https://doc.rust-lang.org/1.95.0/std/io/enum.SeekFrom.html#variant.Current" title="variant std::io::SeekFrom::Current"><code>Current</code></a><code>(0))</code>），并在下次读取前恢复它。</p>')),
    (E('<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.append" title="method std::fs::OpenOptions::append"><code>std::fs::OpenOptions::append</code></a></p>'),
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.append" title="method std::fs::OpenOptions::append"><code>std::fs::OpenOptions::append</code></a> 的异步版本</p>')),
    (E('<p>This function doesn’t create the file if it doesn’t exist. Use the <a href="struct.OpenOptions.html#method.create" title="method tokio::fs::OpenOptions::create"><code>create</code></a>\nmethod to do so.</p>'),
     E('<p>如果文件不存在，此函数不会创建它。使用 <a href="struct.OpenOptions.html#method.create" title="method tokio::fs::OpenOptions::create"><code>create</code></a>\r\n方法可以做到这一点。</p>')),
    (E('<p>Sets the option for truncating a previous file.</p>'),
     E('<p>设置截断现有文件的选项。</p>')),
    (E('<p>If a file is successfully opened with this option set it will truncate\nthe file to 0 length if it already exists.</p>'),
     E('<p>如果设置此选项后成功打开文件，\r\n将在文件已存在时将其截断为 0 长度。</p>')),
    (E('<p>The file must be opened with write access for truncate to work.</p>'),
     E('<p>要使截断生效，必须以写入访问打开文件。</p>')),
    (E('<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.truncate" title="method std::fs::OpenOptions::truncate"><code>std::fs::OpenOptions::truncate</code></a></p>'),
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.truncate" title="method std::fs::OpenOptions::truncate"><code>std::fs::OpenOptions::truncate</code></a> 的异步版本</p>')),
    (E('<p>Sets the option for creating a new file.</p>'),
     E('<p>设置创建新文件的选项。</p>')),
    (E('<p>This option indicates whether a new file will be created if the file\ndoes not yet already exist.</p>'),
     E('<p>此选项指示在文件尚不存在时是否\r\n将创建新文件。</p>')),
    (E('<p>In order for the file to be created, <a href="struct.OpenOptions.html#method.write" title="method tokio::fs::OpenOptions::write"><code>write</code></a> or <a href="struct.OpenOptions.html#method.append" title="method tokio::fs::OpenOptions::append"><code>append</code></a> access must\nbe used.</p>'),
     E('<p>要创建文件，必须使用 <a href="struct.OpenOptions.html#method.write" title="method tokio::fs::OpenOptions::write"><code>write</code></a> 或 <a href="struct.OpenOptions.html#method.append" title="method tokio::fs::OpenOptions::append"><code>append</code></a> 访问。</p>')),
    (E('<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.create" title="method std::fs::OpenOptions::create"><code>std::fs::OpenOptions::create</code></a></p>'),
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.create" title="method std::fs::OpenOptions::create"><code>std::fs::OpenOptions::create</code></a> 的异步版本</p>')),
    (E('<p>Sets the option to always create a new file.</p>'),
     E('<p>设置始终创建新文件的选项。</p>')),
    (E('<p>This option indicates whether a new file will be created.  No file is\nallowed to exist at the target location, also no (dangling) symlink.</p>'),
     E('<p>此选项指示是否将创建新文件。在目标位置\r\n不允许存在任何文件，也不允许（悬空）符号链接。</p>')),
    # p 26 same as create_new p 11 in File.html (atomic)
    (E('<p>This option is useful because it is atomic. Otherwise between checking\nwhether a file exists and creating a new one, the file may have been\ncreated by another process (a TOCTOU race condition / attack).</p>'),
     E('<p>此选项很有用，因为它是原子操作。否则，在检查\r\n文件是否存在和创建新文件之间，文件\r\n可能被另一个进程创建（TOCTOU 竞争条件 / 攻击）。</p>')),
    (E('<p>If <code>.create_new(true)</code> is set, <a href="struct.OpenOptions.html#method.create" title="method tokio::fs::OpenOptions::create"><code>.create()</code></a> and <a href="struct.OpenOptions.html#method.truncate" title="method tokio::fs::OpenOptions::truncate"><code>.truncate()</code></a> are\nignored.</p>'),
     E('<p>如果设置了 <code>.create_new(true)</code>，<a href="struct.OpenOptions.html#method.create" title="method tokio::fs::OpenOptions::create"><code>.create()</code></a> 和 <a href="struct.OpenOptions.html#method.truncate" title="method tokio::fs::OpenOptions::truncate"><code>.truncate()</code></a>\r\n将被忽略。</p>')),
    (E('<p>The file must be opened with write or append access in order to create a\nnew file.</p>'),
     E('<p>要创建新文件，必须以写或追加访问方式打开文件。</p>')),
    (E('<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.create_new" title="method std::fs::OpenOptions::create_new"><code>std::fs::OpenOptions::create_new</code></a></p>'),
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.create_new" title="method std::fs::OpenOptions::create_new"><code>std::fs::OpenOptions::create_new</code></a> 的异步版本</p>')),
    (E('<p>Opens a file at <code>path</code> with the options specified by <code>self</code>.</p>'),
     E('<p>使用 <code>self</code> 指定的选项在 <code>path</code> 打开一个文件。</p>')),
    (E('<p>This is an async version of <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.open" title="method std::fs::OpenOptions::open"><code>std::fs::OpenOptions::open</code></a></p>'),
     E('<p>这是 <a href="https://doc.rust-lang.org/1.95.0/std/fs/struct.OpenOptions.html#method.open" title="method std::fs::OpenOptions::open"><code>std::fs::OpenOptions::open</code></a> 的异步版本</p>')),
    (E('<p>This function will return an error under a number of different\ncircumstances. Some of these error conditions are listed here, together\nwith their <a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html" title="enum std::io::error::ErrorKind"><code>ErrorKind</code></a>. The mapping to <a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html" title="enum std::io::error::ErrorKind"><code>ErrorKind</code></a>s is not part of\nthe compatibility contract of the function, especially the <code>Other</code> kind\nmight change to more specific kinds in the future.</p>'),
     E('<p>此函数在许多不同情况下会返回错误。此处列出了部分\r\n错误情况及其 <a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html" title="enum std::io::error::ErrorKind"><code>ErrorKind</code></a>。到 <a href="https://doc.rust-lang.org/1.95.0/std/io/error/enum.ErrorKind.html" title="enum std::io::error::ErrorKind"><code>ErrorKind</code></a> 的映射\r\n不属于该函数的兼容性约定，尤其 <code>Other</code> 种类\r\n将来可能会更改为更具体的种类。</p>')),
    (E('<p>On Linux, you can also use <code>io_uring</code> for executing system calls.\nTo enable <code>io_uring</code>, you need to specify the <code>--cfg tokio_unstable</code>\nflag at compile time, enable the <code>io-uring</code> cargo feature, and set the\n<code>Builder::enable_io_uring</code> runtime option.</p>'),
     E('<p>在 Linux 上，你还可以使用 <code>io_uring</code> 来执行系统调用。\r\n要启用 <code>io_uring</code>，需要在编译时指定\r\n<code>--cfg tokio_unstable</code> 标志，启用 <code>io-uring</code> cargo 特性，\r\n并设置 <code>Builder::enable_io_uring</code> 运行时选项。</p>')),
    (E('<p>Support for <code>io_uring</code> is currently experimental, so its behavior may\nchange or it may be removed in future versions.</p>'),
     E('<p><code>io_uring</code> 支持目前是实验性的，因此其行为\r\n将来版本中可能会改变或被删除。</p>')),
    (E('<p>Overrides the <code>dwDesiredAccess</code> argument to the call to <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea"><code>CreateFile</code></a>\nwith the specified value.</p>'),
     E('<p>将调用 <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea"><code>CreateFile</code></a> 时的\r\n<code>dwDesiredAccess</code> 参数覆盖为指定值。</p>')),
    (E('<p>This will override the <code>read</code>, <code>write</code>, and <code>append</code> flags on the\n<code>OpenOptions</code> structure. This method provides fine-grained control over\nthe permissions to read, write and append data, attributes (like hidden\nand system), and extended attributes.</p>'),
     E('<p>这将覆盖 <code>OpenOptions</code> 结构上的 <code>read</code>、<code>write</code>、<code>append</code>\r\n标志。此方法提供对读写和追加数据、属性（如隐藏\r\n和系统）以及扩展属性的精细控制。</p>')),
    (E('<p>Overrides the <code>dwShareMode</code> argument to the call to <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea"><code>CreateFile</code></a> with\nthe specified value.</p>'),
     E('<p>将调用 <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea"><code>CreateFile</code></a> 时的\r\n<code>dwShareMode</code> 参数覆盖为指定值。</p>')),
    (E('<p>By default <code>share_mode</code> is set to\n<code>FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE</code>. This allows\nother processes to read, write, and delete/rename the same file\nwhile it is open. Removing any of the flags will prevent other\nprocesses from performing the corresponding operation until the file\nhandle is closed.</p>'),
     E('<p>默认情况下，<code>share_mode</code> 设置为\r\n<code>FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE</code>。这允许\r\n其他进程在文件打开时对同一文件进行读、\r\n写和删除 / 重命名操作。删除任何\r\n标志都会阻止其他进程执行相应的操作，\r\n直到文件句柄关闭为止。</p>')),
    (E('<p>Sets extra flags for the <code>dwFileFlags</code> argument to the call to\n<a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfile2"><code>CreateFile2</code></a> to the specified value (or combines it with\n<code>attributes</code> and <code>security_qos_flags</code> to set the <code>dwFlagsAndAttributes</code>\nfor <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea"><code>CreateFile</code></a>).</p>'),
     E('<p>将调用 <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfile2"><code>CreateFile2</code></a> 时的\r\n<code>dwFileFlags</code> 参数的附加标志设置为指定值（或将其与 <code>attributes</code> 和\r\n<code>security_qos_flags</code> 组合，为 <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea"><code>CreateFile</code></a> 设置 <code>dwFlagsAndAttributes</code>）。</p>')),
    (E('<p>Custom flags can only set flags, not remove flags set by Rust’s options.\nThis option overwrites any previously set custom flags.</p>'),
     E('<p>自定义标志只能设置标志，不能移除 Rust 选项设置的\r\n标志。此选项会覆盖任何\r\n先前设置的自定义标志。</p>')),
    (E('<p>Sets the <code>dwFileAttributes</code> argument to the call to <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfile2"><code>CreateFile2</code></a> to\nthe specified value (or combines it with <code>custom_flags</code> and\n<code>security_qos_flags</code> to set the <code>dwFlagsAndAttributes</code> for\n<a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea"><code>CreateFile</code></a>).</p>'),
     E('<p>将调用 <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfile2"><code>CreateFile2</code></a> 时的\r\n<code>dwFileAttributes</code> 参数设置为指定值（或将其与 <code>custom_flags</code> 和\r\n<code>security_qos_flags</code> 组合，为 <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea"><code>CreateFile</code></a> 设置 <code>dwFlagsAndAttributes</code>）。</p>')),
    (E('<p>If a <em>new</em> file is created because it does not yet exist and\n<code>.create(true)</code> or <code>.create_new(true)</code> are specified, the new file is\ngiven the attributes declared with <code>.attributes()</code>.</p>'),
     E('<p>如果因为文件尚不存在而\r\n创建<em>新</em>文件，并且指定了 <code>.create(true)</code> 或\r\n<code>.create_new(true)</code>，则\r\n新文件将具有通过 <code>.attributes()</code> 声明的属性。</p>')),
    (E('<p>If an <em>existing</em> file is opened with <code>.create(true).truncate(true)</code>, its\nexisting attributes are preserved and combined with the ones declared\nwith <code>.attributes()</code>.</p>'),
     E('<p>如果以 <code>.create(true).truncate(true)</code> 打开<em>现有</em>文件，\r\n其现有属性会保留，并与通过 <code>.attributes()</code> 声明的属性组合。</p>')),
    (E('<p>In all other cases the attributes get ignored.</p>'),
     E('<p>在所有其他情况下，属性将被忽略。</p>')),
    (E('<p>Sets the <code>dwSecurityQosFlags</code> argument to the call to <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfile2"><code>CreateFile2</code></a> to\nthe specified value (or combines it with <code>custom_flags</code> and <code>attributes</code>\nto set the <code>dwFlagsAndAttributes</code> for <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea"><code>CreateFile</code></a>).</p>'),
     E('<p>将调用 <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfile2"><code>CreateFile2</code></a> 时的\r\n<code>dwSecurityQosFlags</code> 参数设置为指定值（或将其与 <code>custom_flags</code> 和\r\n<code>attributes</code> 组合，为 <a href="https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea"><code>CreateFile</code></a> 设置 <code>dwFlagsAndAttributes</code>）。</p>')),
    (E('<p>By default <code>security_qos_flags</code> is not set. It should be specified when\nopening a named pipe, to control to which degree a server process can\nact on behalf of a client process (security impersonation level).</p>'),
     E('<p>默认情况下，<code>security_qos_flags</code> 未设置。在打开\r\n命名管道时应指定它，以控制服务器进程可以\r\n代表客户端进程执行操作的程度（安全模拟级别）。</p>')),
    (E('<p>When <code>security_qos_flags</code> is not set, a malicious program can gain the\nelevated privileges of a privileged Rust process when it allows opening\nuser-specified paths, by tricking it into opening a named pipe. So\narguably <code>security_qos_flags</code> should also be set when opening arbitrary\npaths. However the bits can then conflict with other flags, specifically\n<code>FILE_FLAG_OPEN_NO_RECALL</code>.</p>'),
     E('<p>当 <code>security_qos_flags</code> 未设置时，恶意程序\r\n可能会诱使特权 Rust 进程打开用户指定的路径（通过让其打开命名管道），\r\n从而获得该特权进程的提升权限。因此有人认为\r\n在打开任意路径时也应设置 <code>security_qos_flags</code>。然而这些位\r\n可能与其他标志冲突，特别是 <code>FILE_FLAG_OPEN_NO_RECALL</code>。</p>')),
    (E('<p>For information about possible values, see <a href="https://docs.microsoft.com/en-us/windows/win32/api/winnt/ne-winnt-security_impersonation_level">Impersonation Levels</a> on the\nWindows Dev Center site. The <code>SECURITY_SQOS_PRESENT</code> flag is set\nautomatically when using this method.</p>'),
     E('<p>有关可能的取值，请参阅 Windows 开发人员中心站点上的\r\n<a href="https://docs.microsoft.com/en-us/windows/win32/api/winnt/ne-winnt-security_impersonation_level">模拟级别</a>。\r\n使用此方法时，<code>SECURITY_SQOS_PRESENT</code> 标志\r\n会自动设置。</p>')),
])


def main():
    """Apply all pairs to files."""
    total_replacements = 0
    files_modified = 0

    for rel, pairs in PLAN:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            print(f'NOT FOUND: {path}')
            continue
        try:
            original = read_bytes(rel)
        except Exception as e:
            print(f'ERROR reading {path}: {e}')
            continue

        content = original
        local_replacements = 0
        unmatched = []

        for en_b, zh_b in pairs:
            if en_b in content:
                count = content.count(en_b)
                local_replacements += count
                content = content.replace(en_b, zh_b)
            else:
                unmatched.append(en_b[:80])

        if content != original:
            write_bytes(rel, content)
            files_modified += 1
            print(f'{rel}: {local_replacements} replacements' + (f' ({len(unmatched)} unmatched patterns!)' if unmatched else ''))
            if unmatched:
                for u in unmatched:
                    print(f'   UNMATCHED: {u!r}...')
        else:
            print(f'{rel}: NO changes' + (f' ({len(unmatched)} unmatched patterns!)' if unmatched else ''))
            if unmatched:
                for u in unmatched:
                    print(f'   UNMATCHED: {u!r}...')

        total_replacements += local_replacements

    print(f'\nTotal: {total_replacements} replacements across {files_modified} files')


if __name__ == '__main__':
    main()
