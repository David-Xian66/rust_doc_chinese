#!/usr/bin/env python3
"""Translate tokio/net/ docblocks to Chinese.

Uses bytes mode (rb/wb) to preserve CRLF and UTF-8 characters.
Each PAIRS entry is (en_bytes, zh_bytes). Apply via .replace().
"""
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

# Each pair: (en_text_bytes, zh_text_bytes). Replace long patterns first.
PAIRS = [
    # ===== tokio/net/index.html =====
    (
        b"<p>TCP/UDP/Unix bindings for tokio.</p>\n<p>This module contains the TCP/UDP/Unix networking types, similar to the standard\nlibrary, which can be used to implement networking protocols.</p>\n<p>For IO resources not available in tokio::net, you can use AsyncFd.</p>",
        "<p>tokio 的 TCP/UDP/Unix 绑定。</p>\n<p>本模块包含 TCP/UDP/Unix 网络类型，类似于标准库中的类型，可用于实现网络协议。</p>\n<p>对于 tokio::net 中没有提供的 IO 资源，可以使用 AsyncFd。</p>".encode("utf-8")
    ),
    # ===== tokio/net/trait.ToSocketAddrs.html =====
    (
        b"<p>Converts or resolves without blocking to one or more SocketAddr values.</p>\n<p>Implementations of ToSocketAddrs for string types require a DNS lookup.</p>\n<p>Currently, this trait is only used as an argument to Tokio functions that\nneed to reference a target socket address. To perform a SocketAddr\nconversion directly, use lookup_host().</p>\n<p>This trait is sealed and is intended to be opaque. The details of the trait\nwill change. Stabilization is pending enhancements to the Rust language.</p>",
        "<p>非阻塞地转换或解析为一个或多个 SocketAddr 值。</p>\n<p>对于字符串类型的 ToSocketAddrs 实现需要 DNS 查询。</p>\n<p>目前，该 trait 仅作为需要引用目标套接字地址的 Tokio 函数的参数使用。要直接执行 SocketAddr 转换，请使用 lookup_host()。</p>\n<p>该 trait 是封闭的，该意为不透明。trait 的细节会改变。稳定化在等待 Rust 语言的增强。</p>".encode("utf-8")
    ),
    # ===== tokio/net/fn.lookup_host.html =====
    (
        b"<p>Performs a DNS resolution.</p>\n<p>The returned iterator may not actually yield any values depending on the\noutcome of any resolution performed.</p>\n<p>This API is not intended to cover all DNS use cases. Anything beyond the\nbasic use case should be done with a specialized library.</p>\n<p>To resolve a DNS entry:",
        "<p>执行 DNS 解析。</p>\n<p>根据所执行解析的结果，返回的迭代器可能并不会实际产生任何值。</p>\n<p>此 API 并不能覆盖所有 DNS 使用场景。超出基本使用场景之外的任何事项都应该使用专门的库来完成。</p>\n<p>要解析 DNS 条目：".encode("utf-8")
    ),
    # ===== tokio/net/tcp/index.html =====
    (
        b"<p>TCP utility types.</p>",
        "<p>TCP 工具类型。</p>".encode("utf-8")
    ),
    # ===== tokio/net/windows/index.html =====
    (
        b"<p>Windows specific network types.</p>",
        "<p>Windows 专用的网络类型。</p>".encode("utf-8")
    ),
    # ===== tokio/net/windows/named_pipe/index.html =====
    (
        b"<p>Tokio support for Windows named pipes.</p>",
        "<p>Tokio 对 Windows 命名管道的支持。</p>".encode("utf-8")
    ),
    # ===== tokio/net/tcp/struct.ReuniteError.html =====
    (
        b"<p>Error indicating that two halves were not from the same socket, and thus could\nnot be reunited.</p>",
        "<p>表示两个半部分不来自同一套接字，因此无法重新合并的错误。</p>".encode("utf-8")
    ),
    # ===== tokio/net/struct.TcpListener.html =====
    (
        b"<p>A TCP socket server, listening for connections.</p>\n<p>You can accept a new connection by using the <a href=\"struct.TcpListener.html#method.accept\" title=\"method tokio::net::TcpListener::accept\"><code>accept</code></a>\nmethod.</p>\n<p>A <code>TcpListener</code> can be turned into a <code>Stream</code> with <a href=\"https://docs.rs/tokio-stream/0.1/tokio_stream/wrappers/struct.TcpListenerStream.html\"><code>TcpListenerStream</code></a>.</p>\n<p>The socket will be closed when the value is dropped.</p>",
        "<p>TCP 套接字服务器，用于监听连接。</p>\n<p>可以使用 <a href=\"struct.TcpListener.html#method.accept\" title=\"method tokio::net::TcpListener::accept\"><code>accept</code></a>\n方法接受新的连接。</p>\n<p>可以使用 <a href=\"https://docs.rs/tokio-stream/0.1/tokio_stream/wrappers/struct.TcpListenerStream.html\"><code>TcpListenerStream</code></a> 将 <code>TcpListener</code> 转换为 <code>Stream</code>。</p>\n<p>当该值被释放时，套接字将被关闭。</p>".encode("utf-8")
    ),
    (
        b"<p>Note that accepting a connection can lead to various errors and not all\nof them are necessarily fatal \xe2\x80\x92 for example having too many open file\ndescriptors or the other side closing the connection while it waits in\nan accept queue. These would terminate the stream if not handled in any\nway.</p>",
        "<p>请注意，接受连接可能产生各种错误，并不所有错误都一定是致命的 \xe2\x80\x92 例如，打开的文件描述符太多，或对端在等待接受队列中关闭了连接。如果以任何方式不处理，这些情况会终止该流。</p>".encode("utf-8")
    ),
    (
        b"<p>Using <code>accept</code>:</p>",
        "<p>使用 <code>accept</code>：</p>".encode("utf-8")
    ),
    (
        b"<p>Creates a new <code>TcpListener</code>, which will be bound to the specified address.</p>",
        "<p>创建一个新的 <code>TcpListener</code>，它将绑定到指定的地址。</p>".encode("utf-8")
    ),
    (
        b"<p>The returned listener is ready for accepting connections.</p>",
        "<p>返回的监听器可以接受连接。</p>".encode("utf-8")
    ),
    (
        b"<p>Binding with a port number of 0 will request that the OS assigns a port\nto this listener. The port allocated can be queried via the <code>local_addr</code>\nmethod.</p>",
        "<p>使用端口号 0 进行绑定时，会要求操作系统为该监听器分配一个端口。分配的端口可以通过 <code>local_addr</code> 方法查询。</p>".encode("utf-8")
    ),
    (
        b"<p>This function sets the <code>SO_REUSEADDR</code> option on the socket on Unix.</p>",
        "<p>该函数会在 Unix 上为套接字设置 <code>SO_REUSEADDR</code> 选项。</p>".encode("utf-8")
    ),
    (
        b"<p>To configure the socket before binding, you can use the <a href=\"struct.TcpSocket.html\" title=\"struct tokio::net::TcpSocket\"><code>TcpSocket</code></a>\ntype.</p>",
        "<p>要在绑定前配置套接字，可以使用 <a href=\"struct.TcpSocket.html\" title=\"struct tokio::net::TcpSocket\"><code>TcpSocket</code></a>\n类型。</p>".encode("utf-8")
    ),
    (
        b"<p>Accepts a new incoming connection from this listener.</p>",
        "<p>从该监听器接受一个新的传入连接。</p>".encode("utf-8")
    ),
    (
        b"<p>This function will yield once a new TCP connection is established. When\nestablished, the corresponding <a href=\"struct.TcpStream.html\" title=\"struct tokio::net::TcpStream\"><code>TcpStream</code></a> and the remote peer\xe2\x80\x99s\naddress will be returned.</p>",
        "<p>该函数会在新的 TCP 连接建立时返回。连接建立后，将返回对应的 <a href=\"struct.TcpStream.html\" title=\"struct tokio::net::TcpStream\"><code>TcpStream</code></a> 以及远端对端地址。</p>".encode("utf-8")
    ),
    (
        b"<p>This method is cancel safe. If the method is used as the event in a\n<a href=\"../macro.select.html\" title=\"macro tokio::select\"><code>tokio::select!</code></a> statement and some other branch\ncompletes first, then it is guaranteed that no new connections were\naccepted by this method.</p>",
        "<p>此方法可安全取消。如果该方法作为 <a href=\"../macro.select.html\" title=\"macro tokio::select\"><code>tokio::select!</code></a> 语句中的事件，且某个其他分支先完成，则可以保证此方法未接受任何新连接。</p>".encode("utf-8")
    ),
    (
        b"<p>Polls to accept a new incoming connection to this listener.</p>",
        "<p>Poll 以接受一个新的传入连接到该监听器。</p>".encode("utf-8")
    ),
    (
        b"<p>If there is no connection to accept, <code>Poll::Pending</code> is returned and the\ncurrent task will be notified by a waker.  Note that on multiple calls\nto <code>poll_accept</code>, only the <code>Waker</code> from the <code>Context</code> passed to the most\nrecent call is scheduled to receive a wakeup.</p>",
        "<p>如果没有可接受的连接，则返回 <code>Poll::Pending</code>，并会通过 waker 通知当前任务。注意，对于多次调用 <code>poll_accept</code>，仅会调度传递给最近一次调用的 <code>Context</code> 中的 <code>Waker</code> 接收唤醒。</p>".encode("utf-8")
    ),
    (
        b"<p>Creates new <code>TcpListener</code> from a <code>std::net::TcpListener</code>.</p>",
        "<p>从 <code>std::net::TcpListener</code> 创建新的 <code>TcpListener</code>。</p>".encode("utf-8")
    ),
    (
        b"<p>This function is intended to be used to wrap a TCP listener from the\nstandard library in the Tokio equivalent.</p>",
        "<p>该函数用于将标准库中的 TCP 监听器包装为 Tokio 的对应类型。</p>".encode("utf-8")
    ),
    (
        b"<p>This API is typically paired with the <code>socket2</code> crate and the <code>Socket</code>\ntype to build up and customize a listener before it\xe2\x80\x99s shipped off to the\nbacking event loop. This allows configuration of options like\n<code>SO_REUSEPORT</code>, binding to multiple addresses, etc.</p>",
        "<p>此 API 通常与 <code>socket2</code> 框架及 <code>Socket</code> 类型配合使用，以在它被提交给后端事件循环之前构建并定制监听器。这使得可以配置类似 <code>SO_REUSEPORT</code>、绑定多个地址等选项。</p>".encode("utf-8")
    ),
    (
        b"<p>The caller is responsible for ensuring that the listener is in\nnon-blocking mode. Otherwise all I/O operations on the listener\nwill block the thread, which will cause unexpected behavior.\nNon-blocking mode can be set using <a href=\"https://doc.rust-lang.org/1.95.0/std/net/tcp/struct.TcpListener.html#method.set_nonblocking\" title=\"method std::net::tcp::TcpListener::set_nonblocking\"><code>set_nonblocking</code></a>.</p>",
        "<p>调用者负责确保监听器处于非阻塞模式。否则，监听器上的所有 I/O 操作都会阻塞线程，这将导致意外行为。可以使用 <a href=\"https://doc.rust-lang.org/1.95.0/std/net/tcp/struct.TcpListener.html#method.set_nonblocking\" title=\"method std::net::tcp::TcpListener::set_nonblocking\"><code>set_nonblocking</code></a> 设置非阻塞模式。</p>".encode("utf-8")
    ),
    (
        b"<p>Passing a listener in blocking mode is always erroneous,\nand the behavior in that case may change in the future.\nFor example, it could panic.</p>",
        "<p>传递一个阻塞模式的监听器始终是错误的，该情形下的行为可能会在未来发生变化。例如，可能会引发 panic。</p>".encode("utf-8")
    ),
    (
        b"<p>This function panics if it is not called from within a runtime with\nIO enabled.</p>",
        "<p>如果该函数不是在启用了 IO 的运行时中调用，则会引发 panic。</p>".encode("utf-8")
    ),
    (
        b"<p>The runtime is usually set implicitly when this function is called\nfrom a future driven by a tokio runtime, otherwise runtime can be set\nexplicitly with Runtime::enter function.</p>",
        "<p>运行时通常会在从由 tokio 运行时驱动的未来中调用此函数时隐式设置，否则可以使用 Runtime::enter 函数显式设置。</p>".encode("utf-8")
    ),
    (
        b"<p>Turns a <a href=\"struct.TcpListener.html\" title=\"struct tokio::net::TcpListener\"><code>tokio::net::TcpListener</code></a> into a <a href=\"https://doc.rust-lang.org/1.95.0/std/net/tcp/struct.TcpListener.html\" title=\"struct std::net::tcp::TcpListener\"><code>std::net::TcpListener</code></a>.</p>",
        "<p>将 <a href=\"struct.TcpListener.html\" title=\"struct tokio::net::TcpListener\"><code>tokio::net::TcpListener</code></a> 转换为 <a href=\"https://doc.rust-lang.org/1.95.0/std/net/tcp/struct.TcpListener.html\" title=\"struct std::net::tcp::TcpListener\"><code>std::net::TcpListener</code></a>。</p>".encode("utf-8")
    ),
    (
        b"<p>The returned <a href=\"https://doc.rust-lang.org/1.95.0/std/net/tcp/struct.TcpListener.html\" title=\"struct std::net::tcp::TcpListener\"><code>std::net::TcpListener</code></a> will have nonblocking mode set as\n<code>true</code>.  Use <a href=\"https://doc.rust-lang.org/1.95.0/std/net/tcp/struct.TcpListener.html#method.set_nonblocking\" title=\"method std::net::tcp::TcpListener::set_nonblocking\"><code>set_nonblocking</code></a> to change the blocking mode if needed.</p>",
        "<p>返回的 <a href=\"https://doc.rust-lang.org/1.95.0/std/net/tcp/struct.TcpListener.html\" title=\"struct std::net::tcp::TcpListener\"><code>std::net::TcpListener</code></a> 的非阻塞模式将被设置为\n<code>true</code>。如有需要，可使用 <a href=\"https://doc.rust-lang.org/1.95.0/std/net/tcp/struct.TcpListener.html#method.set_nonblocking\" title=\"method std::net::tcp::TcpListener::set_nonblocking\"><code>set_nonblocking</code></a> 修改阻塞模式。</p>".encode("utf-8")
    ),
    (
        b"<p>Returns the local address that this listener is bound to.</p>",
        "<p>返回该监听器绑定的本地地址。</p>".encode("utf-8")
    ),
    (
        b"<p>This can be useful, for example, when binding to port 0 to figure out\nwhich port was actually bound.</p>",
        "<p>这在某些场景下很有用，例如绑定到端口 0 时，可以查看实际绑定到了哪个端口。</p>".encode("utf-8")
    ),
    (
        b"<p>Gets the value of the <code>IP_TTL</code> option for this socket.</p>",
        "<p>获取该套接字的 <code>IP_TTL</code> 选项值。</p>".encode("utf-8")
    ),
    (
        b"<p>For more information about this option, see <a href=\"struct.TcpListener.html#method.set_ttl\" title=\"method tokio::net::TcpListener::set_ttl\"><code>set_ttl</code></a>.</p>",
        "<p>关于此选项的更多信息，请参见 <a href=\"struct.TcpListener.html#method.set_ttl\" title=\"method tokio::net::TcpListener::set_ttl\"><code>set_ttl</code></a>。</p>".encode("utf-8")
    ),
    (
        b"<p>Sets the value for the <code>IP_TTL</code> option on this socket.</p>",
        "<p>为该套接字设置 <code>IP_TTL</code> 选项的值。</p>".encode("utf-8")
    ),
    (
        b"<p>This value sets the time-to-live field that is used in every packet sent\nfrom this socket.</p>",
        "<p>此值设置了从该套接字发出的每个数据包中使用的生存时间字段。</p>".encode("utf-8")
    ),
    (
        b"<p>Consumes stream, returning the tokio I/O object.</p>",
        "<p>消耗流，返回 tokio 的 I/O 对象。</p>".encode("utf-8")
    ),
    (
        b"<p>This is equivalent to\n<a href=\"struct.TcpListener.html#method.from_std\" title=\"associated function tokio::net::TcpListener::from_std\"><code>TcpListener::from_std(stream)</code></a>.</p>",
        "<p>这等同于\n<a href=\"struct.TcpListener.html#method.from_std\" title=\"associated function tokio::net::TcpListener::from_std\"><code>TcpListener::from_std(stream)</code></a>。</p>".encode("utf-8")
    ),
    # ===== tokio/net/windows/named_pipe/enum.PipeEnd.html =====
    (
        b"<p>Indicates the end of a named pipe.</p>",
        "<p>表示命名管道的一端。</p>".encode("utf-8")
    ),
    (
        b"<p>The named pipe refers to the client end of a named pipe instance.</p>",
        "<p>该命名管道是某个命名管道实例的客户端。</p>".encode("utf-8")
    ),
    (
        b"<p>Corresponds to PIPE_CLIENT_END.</p>",
        "<p>对应 PIPE_CLIENT_END。</p>".encode("utf-8")
    ),
    (
        b"<p>The named pipe refers to the server end of a named pipe instance.</p>",
        "<p>该命名管道是某个命名管道实例的服务器端。</p>".encode("utf-8")
    ),
    (
        b"<p>Corresponds to PIPE_SERVER_END.</p>",
        "<p>对应 PIPE_SERVER_END。</p>".encode("utf-8")
    ),
    # ===== tokio/net/windows/named_pipe/enum.PipeMode.html =====
    (
        b"<p>The pipe mode of a named pipe.</p>\n<p>Set through ServerOptions::pipe_mode.</p>",
        "<p>命名管道的管道模式。</p>\n<p>通过 ServerOptions::pipe_mode 设置。</p>".encode("utf-8")
    ),
    (
        b"<p>Data is written to the pipe as a stream of bytes. The pipe does not\ndistinguish bytes written during different write operations.</p>",
        "<p>数据以字节流的形式写入管道。管道不区分不同写入操作期间写入的字节。</p>".encode("utf-8")
    ),
    (
        b"<p>Corresponds to PIPE_TYPE_BYTE.</p>",
        "<p>对应 PIPE_TYPE_BYTE。</p>".encode("utf-8")
    ),
    (
        b"<p>Data is written to the pipe as a stream of messages. The pipe treats the\nbytes written during each write operation as a message unit. Any reading\non a named pipe returns ERROR_MORE_DATA when a message is not read\ncompletely.</p>",
        "<p>数据以消息流的形式写入管道。管道将每次写入操作写入的字节作为一个消息单元。如果某个消息未被完全读取，命名管道上的任何读取都会返回 ERROR_MORE_DATA。</p>".encode("utf-8")
    ),
    (
        b"<p>Corresponds to PIPE_TYPE_MESSAGE.</p>",
        "<p>对应 PIPE_TYPE_MESSAGE。</p>".encode("utf-8")
    ),
    # ===== tokio/net/windows/named_pipe/struct.PipeInfo.html =====
    (
        b"<p>Information about a named pipe.</p>\n<p>Constructed through NamedPipeServer::info or NamedPipeClient::info.</p>",
        "<p>命名管道的信息。</p>\n<p>通过 NamedPipeServer::info 或 NamedPipeClient::info 构造。</p>".encode("utf-8")
    ),
    (
        b"<p>Indicates the mode of a named pipe.</p>",
        "<p>表示命名管道的模式。</p>".encode("utf-8")
    ),
    (
        b"<p>Indicates the end of a named pipe.</p>",
        "<p>表示命名管道的一端。</p>".encode("utf-8")
    ),
    (
        b"<p>The maximum number of instances that can be created for this pipe.</p>",
        "<p>可为该管道创建的最大实例数。</p>".encode("utf-8")
    ),
    (
        b"<p>The number of bytes to reserve for the output buffer.</p>",
        "<p>为输出缓冲区预留的字节数。</p>".encode("utf-8")
    ),
    (
        b"<p>The number of bytes to reserve for the input buffer.</p>",
        "<p>为输入缓冲区预留的字节数。</p>".encode("utf-8")
    ),
    # ===== tokio/net/struct.TcpStream.html =====
    (
        b"<p>A TCP stream between a local and a remote socket.</p>",
        "<p>本地套接字与远端套接字之间的 TCP 流。</p>".encode("utf-8")
    ),
    (
        b"<p>A TCP stream can either be created by connecting to an endpoint, via the\nconnect method, or by accepting a connection from a listener. A\nTCP stream can also be created via the TcpSocket type.</p>",
        "<p>TCP 流可以通过 connect 方法连接到端点创建，也可以通过监听器接受连接创建。TCP 流还可以通过 TcpSocket 类型创建。</p>".encode("utf-8")
    ),
    (
        b"<p>Reading and writing to a TcpStream is usually done using the\nconvenience methods found on the AsyncReadExt and AsyncWriteExt\ntraits.</p>",
        "<p>对 TcpStream 的读写通常使用 AsyncReadExt 和 AsyncWriteExt trait 上的便捷方法完成。</p>".encode("utf-8")
    ),
    (
        b"<p>Opens a TCP connection to a remote host.</p>",
        "<p>打开到远程主机的 TCP 连接。</p>".encode("utf-8")
    ),
    (
        b"<p>addr is an address of the remote host. Anything which implements the\nToSocketAddrs trait can be supplied as the address.  If addr\nyields multiple addresses, connect will be attempted with each of the\naddresses until a connection is successful. If none of the addresses\nresult in a successful connection, the error returned from the last\nconnection attempt (the last address) is returned.</p>",
        "<p>addr 是远程主机的地址。任何实现了 ToSocketAddrs trait 的类型都可以作为地址提供。如果 addr 产生多个地址，将依次尝试每个地址进行连接，直到连接成功。如果所有地址都未能成功建立连接，则返回最后一次连接尝试（即最后一个地址）的错误。</p>".encode("utf-8")
    ),
    (
        b"<p>To configure the socket before connecting, you can use the TcpSocket\ntype.</p>",
        "<p>要在连接前配置套接字，可以使用 TcpSocket 类型。</p>".encode("utf-8")
    ),
    (
        b"<p>Creates new TcpStream from a std::net::TcpStream.</p>",
        "<p>从 std::net::TcpStream 创建新的 TcpStream。</p>".encode("utf-8")
    ),
    (
        b"<p>This function is intended to be used to wrap a TCP stream from the\nstandard library in the Tokio equivalent.</p>",
        "<p>该函数用于将标准库中的 TCP 流包装为 Tokio 的对应类型。</p>".encode("utf-8")
    ),
    (
        b"<p>The caller is responsible for ensuring that the stream is in\nnon-blocking mode. Otherwise all I/O operations on the stream\nwill block the thread, which will cause unexpected behavior.\nNon-blocking mode can be set using set_nonblocking.</p>",
        "<p>调用者负责确保流处于非阻塞模式。否则，流上的所有 I/O 操作都会阻塞线程，这将导致意外行为。可以使用 set_nonblocking 设置非阻塞模式。</p>".encode("utf-8")
    ),
    (
        b"<p>Passing a listener in blocking mode is always erroneous,\nand the behavior in that case may change in the future.\nFor example, it could panic.</p>",
        "<p>传递一个阻塞模式的监听器始终是错误的，该情形下的行为可能会在未来发生变化。例如，可能会引发 panic。</p>".encode("utf-8")
    ),
    (
        b"<p>This function panics if it is not called from within a runtime with\nIO enabled.</p>",
        "<p>如果该函数不是在启用了 IO 的运行时中调用，则会引发 panic。</p>".encode("utf-8")
    ),
    (
        b"<p>The runtime is usually set implicitly when this function is called\nfrom a future driven by a tokio runtime, otherwise runtime can be set\nexplicitly with Runtime::enter function.</p>",
        "<p>运行时通常会在从由 tokio 运行时驱动的未来中调用此函数时隐式设置，否则可以使用 Runtime::enter 函数显式设置。</p>".encode("utf-8")
    ),
    (
        b"<p>Turns a tokio::net::TcpStream into a std::net::TcpStream.</p>",
        "<p>将 tokio::net::TcpStream 转换为 std::net::TcpStream。</p>".encode("utf-8")
    ),
    (
        b"<p>The returned std::net::TcpStream will have nonblocking mode set as true.\nUse set_nonblocking to change the blocking mode if needed.</p>",
        "<p>返回的 std::net::TcpStream 的非阻塞模式将被设置为 true。如有需要，可使用 set_nonblocking 修改阻塞模式。</p>".encode("utf-8")
    ),
    (
        b"<p>Returns the local address that this stream is bound to.</p>",
        "<p>返回该流绑定的本地地址。</p>".encode("utf-8")
    ),
    (
        b"<p>Returns the remote address that this stream is connected to.</p>",
        "<p>返回该流连接到的远端地址。</p>".encode("utf-8")
    ),
    (
        b"<p>Attempts to receive data on the socket, without removing that data from\nthe queue, registering the current task for wakeup if data is not yet\navailable.</p>",
        "<p>尝试在套接字上接收数据，但不会从队列中移除该数据。如果数据尚不可用，则注册当前任务以便稍后唤醒。</p>".encode("utf-8")
    ),
    (
        b"<p>Note that on multiple calls to poll_peek, poll_read or\npoll_read_ready, only the Waker from the Context passed to the\nmost recent call is scheduled to receive a wakeup. (However,\npoll_write retains a second, independent waker.)</p>",
        "<p>请注意，对于 poll_peek、poll_read 或 poll_read_ready 的多次调用，仅会调度传递给最近一次调用的 Context 中的 Waker 接收唤醒。（不过 poll_write 仍保留一个独立的 waker。）</p>".encode("utf-8")
    ),
    (
        b"<p>This function may encounter any standard I/O error except WouldBlock.</p>",
        "<p>该函数可能会遇到除 WouldBlock 之外的任何标准 I/O 错误。</p>".encode("utf-8")
    ),
    (
        b"<p>Waits for any of the requested ready states.</p>",
        "<p>等待任意一个所请求的就绪状态。</p>".encode("utf-8")
    ),
    (
        b"<p>This function is usually paired with try_read() or try_write(). It\ncan be used to concurrently read / write to the same socket on a single\ntask without splitting the socket.</p>",
        "<p>该函数通常与 try_read() 或 try_write() 配合使用。它可以在不拆分套接字的情况下，让单个任务同时对该套接字进行读 / 写。</p>".encode("utf-8")
    ),
    (
        b"<p>The function may complete without the socket being ready. This is a\nfalse-positive and attempting an operation will return with\nio::ErrorKind::WouldBlock. The function can also return with an empty\nReady set, so you should always check the returned value and possibly\nwait again if the requested states are not set.</p>",
        "<p>函数可能在套接字尚未就绪时完成。这是误报情况，尝试进行操作时会返回 io::ErrorKind::WouldBlock。函数也可能返回空的 Ready 集合，因此应始终检查返回值，若请求的状态尚未设置则可能需要再次等待。</p>".encode("utf-8")
    ),
    (
        b"<p>This method is cancel safe. Once a readiness event occurs, the method\nwill continue to return immediately until the readiness event is\nconsumed by an attempt to read or write that fails with WouldBlock or\nPoll::Pending.</p>",
        "<p>此方法可安全取消。一旦发生就绪事件，该方法会继续立即返回，直到就绪事件被读取或写入操作消费（这些操作以 WouldBlock 或 Poll::Pending 失败）。</p>".encode("utf-8")
    ),
    (
        b"<p>Concurrently read and write to the stream on the same task without\nsplitting.</p>",
        "<p>在不拆分的情况下，在同一任务上同时对流进行读写。</p>".encode("utf-8")
    ),
    (
        b"<p>Waits for the socket to become readable.</p>",
        "<p>等待套接字变为可读。</p>".encode("utf-8")
    ),
    (
        b"<p>This function is equivalent to ready(Interest::READABLE) and is usually\npaired with try_read().</p>",
        "<p>该函数等同于 ready(Interest::READABLE)，通常与 try_read() 配合使用。</p>".encode("utf-8")
    ),
    (
        b"<p>This method is cancel safe. Once a readiness event occurs, the method\nwill continue to return immediately until the readiness event is\nconsumed by an attempt to read that fails with WouldBlock or\nPoll::Pending.</p>",
        "<p>此方法可安全取消。一旦发生就绪事件，该方法会继续立即返回，直到就绪事件被读取操作消费（这些操作以 WouldBlock 或 Poll::Pending 失败）。</p>".encode("utf-8")
    ),
    (
        b"<p>Polls for read readiness.</p>",
        "<p>Poll 读取就绪状态。</p>".encode("utf-8")
    ),
    (
        b"<p>If the tcp stream is not currently ready for reading, this method will\nstore a clone of the Waker from the provided Context. When the tcp\nstream becomes ready for reading, Waker::wake will be called on the\nwaker.</p>",
        "<p>如果 tcp 流当前尚未准备好读取，此方法会存储提供的 Context 中 Waker 的一个克隆。当 tcp 流变为可读时，会在该 waker 上调用 Waker::wake。</p>".encode("utf-8")
    ),
    (
        b"<p>Note that on multiple calls to poll_read_ready, poll_read or\npoll_peek, only the Waker from the Context passed to the most\nrecent call is scheduled to receive a wakeup. (However,\npoll_write_ready retains a second, independent waker.)</p>",
        "<p>请注意，对于 poll_read_ready、poll_read 或 poll_peek 的多次调用，仅会调度传递给最近一次调用的 Context 中的 Waker 接收唤醒。（不过 poll_write_ready 仍保留一个独立的 waker。）</p>".encode("utf-8")
    ),
    (
        b"<p>This function is intended for cases where creating and pinning a future\nvia readable is not feasible. Where possible, using readable is\npreferred, as this supports polling from multiple tasks at once.</p>",
        "<p>该函数用于不便通过 readable 创建并固定一个 future 的场景。在条件允许时，建议使用 readable，因为它支持同时从多个任务进行 poll。</p>".encode("utf-8")
    ),
    (
        b"<p>Tries to read data from the stream into the provided buffer, returning how\nmany bytes were read.</p>",
        "<p>尝试从流读取数据到所提供的缓冲区中，返回读取的字节数。</p>".encode("utf-8")
    ),
    (
        b"<p>Receives any pending data from the socket but does not wait for new data\nto arrive. On success, returns the number of bytes read. Because\ntry_read() is non-blocking, the buffer does not have to be stored by\nthe async task and can exist entirely on the stack.</p>",
        "<p>从套接字接收所有待处理的数据，但不会等待新数据的到达。成功时返回读取的字节数。由于 try_read() 是非阻塞的，缓冲区不必由异步任务存储，可以完全存在于栈上。</p>".encode("utf-8")
    ),
    (
        b"<p>Usually, readable() or ready() is used with this function.</p>",
        "<p>通常，readable() 或 ready() 与该函数配合使用。</p>".encode("utf-8")
    ),
    (
        b"<p>If data is successfully read, Ok(n) is returned, where n is the\nnumber of bytes read. If n is 0, then it can indicate one of two scenarios:</p>",
        "<p>如果数据读取成功，则返回 Ok(n)，其中 n 是读取的字节数。如果 n 为 0，则可能表示以下两种情况之一：</p>".encode("utf-8")
    ),
    (
        b"<p>If the stream is not ready to read data,\nErr(io::ErrorKind::WouldBlock) is returned.</p>",
        "<p>如果流尚未准备好读取数据，则返回 Err(io::ErrorKind::WouldBlock)。</p>".encode("utf-8")
    ),
    (
        b"<p>Tries to read data from the stream into the provided buffers, returning\nhow many bytes were read.</p>",
        "<p>尝试从流读取数据到所提供的缓冲区中，返回读取的字节数。</p>".encode("utf-8")
    ),
    (
        b"<p>Data is copied to fill each buffer in order, with the final buffer\nwritten to possibly being only partially filled. This method behaves\nequivalently to a single call to try_read() with concatenated\nbuffers.</p>",
        "<p>数据按顺序复制以填充每个缓冲区，最后一个缓冲区可能仅被部分填充。此方法的行为等同于对拼接后的缓冲区调用一次 try_read()。</p>".encode("utf-8")
    ),
    (
        b"<p>Receives any pending data from the socket but does not wait for new data\nto arrive. On success, returns the number of bytes read. Because\ntry_read_vectored() is non-blocking, the buffer does not have to be\nstored by the async task and can exist entirely on the stack.</p>",
        "<p>从套接字接收所有待处理的数据，但不会等待新数据的到达。成功时返回读取的字节数。由于 try_read_vectored() 是非阻塞的，缓冲区不必由异步任务存储，可以完全存在于栈上。</p>".encode("utf-8")
    ),
    (
        b"<p>If data is successfully read, Ok(n) is returned, where n is the\nnumber of bytes read. Ok(0) indicates the stream\xe2\x80\x99s read half is closed\nand will no longer yield data. If the stream is not ready to read data\nErr(io::ErrorKind::WouldBlock) is returned.</p>",
        "<p>如果数据读取成功，则返回 Ok(n)，其中 n 是读取的字节数。Ok(0) 表示流的读取端已关闭，不再产生数据。如果流尚未准备好读取数据，则返回 Err(io::ErrorKind::WouldBlock)。</p>".encode("utf-8")
    ),
    (
        b"<p>Tries to read data from the stream into the provided buffer, advancing the\nbuffer\xe2\x80\x99s internal cursor, returning how many bytes were read.</p>",
        "<p>尝试从流读取数据到所提供的缓冲区中，并推进缓冲区的内部游标，返回读取的字节数。</p>".encode("utf-8")
    ),
    (
        b"<p>Receives any pending data from the socket but does not wait for new data\nto arrive. On success, returns the number of bytes read. Because\ntry_read_buf() is non-blocking, the buffer does not have to be stored by\nthe async task and can exist entirely on the stack.</p>",
        "<p>从套接字接收所有待处理的数据，但不会等待新数据的到达。成功时返回读取的字节数。由于 try_read_buf() 是非阻塞的，缓冲区不必由异步任务存储，可以完全存在于栈上。</p>".encode("utf-8")
    ),
    (
        b"<p>Waits for the socket to become writable.</p>",
        "<p>等待套接字变为可写。</p>".encode("utf-8")
    ),
    (
        b"<p>This function is equivalent to ready(Interest::WRITABLE) and is usually\npaired with try_write().</p>",
        "<p>该函数等同于 ready(Interest::WRITABLE)，通常与 try_write() 配合使用。</p>".encode("utf-8")
    ),
    (
        b"<p>This method is cancel safe. Once a readiness event occurs, the method\nwill continue to return immediately until the readiness event is\nconsumed by an attempt to write that fails with WouldBlock or\nPoll::Pending.</p>",
        "<p>此方法可安全取消。一旦发生就绪事件，该方法会继续立即返回，直到就绪事件被写入操作消费（这些操作以 WouldBlock 或 Poll::Pending 失败）。</p>".encode("utf-8")
    ),
    (
        b"<p>Polls for write readiness.</p>",
        "<p>Poll 写入就绪状态。</p>".encode("utf-8")
    ),
    (
        b"<p>If the tcp stream is not currently ready for writing, this method will\nstore a clone of the Waker from the provided Context. When the tcp\nstream becomes ready for writing, Waker::wake will be called on the\nwaker.</p>",
        "<p>如果 tcp 流当前尚未准备好写入，此方法会存储提供的 Context 中 Waker 的一个克隆。当 tcp 流变为可写时，会在该 waker 上调用 Waker::wake。</p>".encode("utf-8")
    ),
    (
        b"<p>Note that on multiple calls to poll_write_ready or poll_write, only\nthe Waker from the Context passed to the most recent call is\nscheduled to receive a wakeup. (However, poll_read_ready retains a\nsecond, independent waker.)</p>",
        "<p>请注意，对于 poll_write_ready 或 poll_write 的多次调用，仅会调度传递给最近一次调用的 Context 中的 Waker 接收唤醒。（不过 poll_read_ready 仍保留一个独立的 waker。）</p>".encode("utf-8")
    ),
    (
        b"<p>This function is intended for cases where creating and pinning a future\nvia writable is not feasible. Where possible, using writable is\npreferred, as this supports polling from multiple tasks at once.</p>",
        "<p>该函数用于不便通过 writable 创建并固定一个 future 的场景。在条件允许时，建议使用 writable，因为它支持同时从多个任务进行 poll。</p>".encode("utf-8")
    ),
    (
        b"<p>Try to write a buffer to the stream, returning how many bytes were\nwritten.</p>",
        "<p>尝试将缓冲区写入流，返回写入的字节数。</p>".encode("utf-8")
    ),
    (
        b"<p>The function will attempt to write the entire contents of buf, but\nonly part of the buffer may be written.</p>",
        "<p>函数将尝试写入 buf 的全部内容，但可能仅写入缓冲区的一部分。</p>".encode("utf-8")
    ),
    (
        b"<p>This function is usually paired with writable().</p>",
        "<p>该函数通常与 writable() 配合使用。</p>".encode("utf-8")
    ),
    (
        b"<p>If data is successfully written, Ok(n) is returned, where n is the\nnumber of bytes written. If the stream is not ready to write data,\nErr(io::ErrorKind::WouldBlock) is returned.</p>",
        "<p>如果数据写入成功，则返回 Ok(n)，其中 n 是写入的字节数。如果流尚未准备好写入数据，则返回 Err(io::ErrorKind::WouldBlock)。</p>".encode("utf-8")
    ),
    (
        b"<p>Tries to write several buffers to the stream, returning how many bytes\nwere written.</p>",
        "<p>尝试将多个缓冲区写入流，返回写入的字节数。</p>".encode("utf-8")
    ),
    (
        b"<p>Data is written from each buffer in order, with the final buffer read\nfrom possibly being only partially consumed. This method behaves\nequivalently to a single call to try_write() with concatenated\nbuffers.</p>",
        "<p>数据按顺序从每个缓冲区写入，最后一个缓冲区可能仅被部分消费。此方法的行为等同于对拼接后的缓冲区调用一次 try_write()。</p>".encode("utf-8")
    ),
    (
        b"<p>Tries to read or write from the socket using a user-provided IO operation.</p>",
        "<p>尝试使用用户提供的 IO 操作对套接字进行读写。</p>".encode("utf-8")
    ),
    (
        b"<p>If the socket is ready, the provided closure is called. The closure\nshould attempt to perform IO operation on the socket by manually\ncalling the appropriate syscall. If the operation fails because the\nsocket is not actually ready, then the closure should return a\nWouldBlock error and the readiness flag is cleared. The return value\nof the closure is then returned by try_io.</p>",
        "<p>如果套接字就绪，则调用所提供的闭包。闭包应通过手动调用适当的系统调用来尝试对套接字执行 IO 操作。如果由于套接字实际上未就绪而导致操作失败，则闭包应返回 WouldBlock 错误，并清除就绪标志。然后 try_io 返回闭包的返回值。</p>".encode("utf-8")
    ),
    (
        b"<p>If the socket is not ready, then the closure is not called\nand a WouldBlock error is returned.</p>",
        "<p>如果套接字未就绪，则不会调用闭包，并返回 WouldBlock 错误。</p>".encode("utf-8")
    ),
    (
        b"<p>The closure should only return a WouldBlock error if it has performed\nan IO operation on the socket that failed due to the socket not being\nready. Returning a WouldBlock error in any other situation will\nincorrectly clear the readiness flag, which can cause the socket to\nbehave incorrectly.</p>",
        "<p>闭包仅应在已对套接字执行 IO 操作且该操作因套接字未就绪而失败时返回 WouldBlock 错误。在任何其他情况下返回 WouldBlock 错误都会错误地清除就绪标志，从而可能导致套接字行为异常。</p>".encode("utf-8")
    ),
    (
        b"<p>The closure should not perform the IO operation using any of the methods\ndefined on the Tokio TcpStream type, as this will mess with the\nreadiness flag and can cause the socket to behave incorrectly.</p>",
        "<p>闭包不应使用 Tokio TcpStream 类型上定义的任何方法来执行 IO 操作，因为这会干扰就绪标志，并可能导致套接字行为异常。</p>".encode("utf-8")
    ),
    (
        b"<p>This method is not intended to be used with combined interests.\nThe closure should perform only one type of IO operation, so it should not\nrequire more than one ready state. This method may panic or sleep forever\nif it is called with a combined interest.</p>",
        "<p>该方法不应与组合的 interest 一起使用。闭包应仅执行一种 IO 操作，因此不应需要多于一个就绪状态。如果使用组合的 interest 调用此方法，它可能会 panic 或永远睡眠。</p>".encode("utf-8")
    ),
    (
        b"<p>Usually, readable(), writable() or ready() is used with this function.</p>",
        "<p>通常，readable()、writable() 或 ready() 与该函数配合使用。</p>".encode("utf-8")
    ),
    (
        b"<p>Reads or writes from the socket using a user-provided IO operation.</p>",
        "<p>使用用户提供的 IO 操作对套接字进行读写。</p>".encode("utf-8")
    ),
    (
        b"<p>The readiness of the socket is awaited and when the socket is ready,\nthe provided closure is called. The closure should attempt to perform\nIO operation on the socket by manually calling the appropriate syscall.\nIf the operation fails because the socket is not actually ready,\nthen the closure should return a WouldBlock error. In such case the\nreadiness flag is cleared and the socket readiness is awaited again.\nThis loop is repeated until the closure returns an Ok or an error\nother than WouldBlock.</p>",
        "<p>等待套接字就绪，一旦套接字就绪，则调用所提供的闭包。闭包应通过手动调用适当的系统调用来尝试对套接字执行 IO 操作。如果由于套接字实际上未就绪而导致操作失败，则闭包应返回 WouldBlock 错误。在这种情况下，会清除就绪标志并再次等待套接字就绪。该循环会重复进行，直到闭包返回 Ok 或除 WouldBlock 之外的错误。</p>".encode("utf-8")
    ),
    (
        b"<p>This method is not intended to be used with combined interests.\nThe closure should perform only one type of IO operation, so it should not\nrequire more than one ready state. This method may panic or sleep forever\nif it is called with a combined interest.</p>\n",
        "<p>该方法不应与组合的 interest 一起使用。闭包应仅执行一种 IO 操作，因此不应需要多于一个就绪状态。如果使用组合的 interest 调用此方法，它可能会 panic 或永远睡眠。</p>\n".encode("utf-8")
    ),
    (
        b"<p>Receives data on the socket from the remote address to which it is\nconnected, without removing that data from the queue. On success,\nreturns the number of bytes peeked.</p>",
        "<p>从套接字所连接的远端地址接收数据，但不会从队列中移除该数据。成功时返回已窥视的字节数。</p>".encode("utf-8")
    ),
    (
        b"<p>Successive calls return the same data. This is accomplished by passing\nMSG_PEEK as a flag to the underlying recv system call.</p>",
        "<p>连续调用会返回相同的数据。这是通过在底层的 recv 系统调用中传入 MSG_PEEK 标志来实现的。</p>".encode("utf-8")
    ),
    (
        b"<p>This method is cancel safe. If the method is used as the event in a\ntokio::select! statement and some other branch\ncompletes first, then it is guaranteed that no peek was performed, and\nthat buf has not been modified.</p>",
        "<p>此方法可安全取消。如果该方法作为 tokio::select! 语句中的事件，且某个其他分支先完成，则可以保证未执行任何 peek 操作，且 buf 未被修改。</p>".encode("utf-8")
    ),
    (
        b"<p>Gets the value of the TCP_NODELAY option on this socket.</p>",
        "<p>获取该套接字上 TCP_NODELAY 选项的值。</p>".encode("utf-8")
    ),
    (
        b"<p>For more information about this option, see set_nodelay.</p>",
        "<p>关于此选项的更多信息，请参见 set_nodelay。</p>".encode("utf-8")
    ),
    (
        b"<p>Sets the value of the TCP_NODELAY option on this socket.</p>",
        "<p>设置该套接字上 TCP_NODELAY 选项的值。</p>".encode("utf-8")
    ),
    (
        b"<p>If set, this option disables the Nagle algorithm. This means that\nsegments are always sent as soon as possible, even if there is only a\nsmall amount of data. When not set, data is buffered until there is a\nsufficient amount to send out, thereby avoiding the frequent sending of\nsmall packets.</p>",
        "<p>如果设置，此选项将禁用 Nagle 算法。这意味着总是尽快发送段，即使只有少量数据。如果未设置，则会对数据进行缓冲，直到累积足够多的数据再发送，从而避免频繁发送小数据包。</p>".encode("utf-8")
    ),
    (
        b"<p>Reads the linger duration for this socket by getting the SO_LINGER\noption.</p>",
        "<p>通过获取 SO_LINGER 选项来读取该套接字的 linger 时间。</p>".encode("utf-8")
    ),
    (
        b"<p>For more information about this option, see set_zero_linger and set_linger.</p>",
        "<p>关于此选项的更多信息，请参见 set_zero_linger 和 set_linger。</p>".encode("utf-8")
    ),
    (
        b"<p>Sets the linger duration of this socket by setting the SO_LINGER option.</p>",
        "<p>通过设置 SO_LINGER 选项来设置该套接字的 linger 时间。</p>".encode("utf-8")
    ),
    (
        b"<p>This option controls the action taken when a stream has unsent messages and the stream is\nclosed. If SO_LINGER is set, the system shall block the process until it can transmit the\ndata or until the time expires.</p>",
        "<p>该选项控制当流存在未发送消息且流已关闭时采取的操作。如果设置了 SO_LINGER，系统将阻塞该进程，直到能够传输数据或时间到期。</p>".encode("utf-8")
    ),
    (
        b"<p>If SO_LINGER is not specified, and the stream is closed, the system handles the call in a\nway that allows the process to continue as quickly as possible.</p>",
        "<p>如果未指定 SO_LINGER，并且流已关闭，系统会以使进程尽可能快地继续运行的方式处理该调用。</p>".encode("utf-8")
    ),
    (
        b"<p>This option is deprecated because setting SO_LINGER on a socket used with Tokio is\nalways incorrect as it leads to blocking the thread when the socket is closed. For more\ndetails, please see:</p>",
        "<p>此选项已废弃，因为在用于 Tokio 的套接字上设置 SO_LINGER 始终是不正确的，会导致在关闭套接字时阻塞线程。更多细节，请参见：</p>".encode("utf-8")
    ),
    (
        b"<p>Volumes of communications have been devoted to the intricacies of SO_LINGER versus\nnon-blocking (O_NONBLOCK) sockets. From what I can tell, the final word is: don\xe2\x80\x99t\ndo it. Rely on the shutdown()-followed-by-read()-eof technique instead.</p>",
        "<p>大量的讨论都致力于 SO_LINGER 与非阻塞（O_NONBLOCK）套接字之间的复杂性。据我所知，最终结论是：不要这样做。请改用 shutdown()-后跟-read()-eof 的技术。</p>".encode("utf-8")
    ),
    (
        b"<p>Although this method is deprecated, it will not be removed from Tokio.</p>",
        "<p>尽管此方法已废弃，但不会从 Tokio 中移除。</p>".encode("utf-8")
    ),
    (
        b"<p>Note that the special case of setting SO_LINGER to zero does not lead to blocking.\nTokio provides set_zero_linger for this purpose.</p>",
        "<p>请注意，将 SO_LINGER 设置为零的特殊情况并不会导致阻塞。Tokio 提供了 set_zero_linger 以用于此目的。</p>".encode("utf-8")
    ),
    (
        b"<p>Sets a linger duration of zero on this socket by setting the SO_LINGER option.</p>",
        "<p>通过设置 SO_LINGER 选项，将该套接字的 linger 时间设置为零。</p>".encode("utf-8")
    ),
    (
        b"<p>This causes the connection to be forcefully aborted (\xe2\x80\x9cabortive close\xe2\x80\x9d) when the socket is\ndropped or closed. Instead of the normal TCP shutdown handshake (FIN/ACK), a TCP RST\n(reset) segment is sent to the peer, and the socket immediately discards any unsent data\nresiding in the socket send buffer. This prevents the socket from entering the TIME_WAIT\nstate after closing it.</p>",
        "<p>当套接字被丢弃或关闭时，这会导致连接被强制中止（“abortive close”）。不会执行正常的 TCP 关闭握手（FIN/ACK），而是向对端发送一个 TCP RST（重置）段，并且套接字立即丢弃驻留在套接字发送缓冲区中的任何未发送数据。这可以防止套接字在关闭后进入 TIME_WAIT 状态。</p>".encode("utf-8")
    ),
    (
        b"<p>This is a destructive action. Any data currently buffered by the OS but not yet\ntransmitted will be lost. The peer will likely receive a \xe2\x80\x9cConnection Reset\xe2\x80\x9d error\nrather than a clean end-of-stream.</p>",
        "<p>这是一个具有破坏性的操作。操作系统中当前已缓冲但尚未传输的任何数据都将丢失。对端可能会收到一个“Connection Reset”错误，而不是一个干净的流结束。</p>".encode("utf-8")
    ),
    (
        b"<p>See the documentation for set_linger for additional details on\nhow SO_LINGER works.</p>",
        "<p>有关 SO_LINGER 工作原理的更多详细信息，请参阅 set_linger 的文档。</p>".encode("utf-8")
    ),
    (
        b"<p>Gets the value of the IP_TTL option for this socket.</p>",
        "<p>获取该套接字的 IP_TTL 选项值。</p>".encode("utf-8")
    ),
    (
        b"<p>For more information about this option, see set_ttl.</p>",
        "<p>关于此选项的更多信息，请参见 set_ttl。</p>".encode("utf-8")
    ),
    (
        b"<p>Sets the value for the IP_TTL option on this socket.</p>",
        "<p>为该套接字设置 IP_TTL 选项的值。</p>".encode("utf-8")
    ),
    (
        b"<p>This value sets the time-to-live field that is used in every packet sent\nfrom this socket.</p>",
        "<p>此值设置了从该套接字发出的每个数据包中使用的生存时间字段。</p>".encode("utf-8")
    ),
    (
        b"<p>Splits a TcpStream into a read half and a write half, which can be used\nto read and write the stream concurrently.</p>",
        "<p>将 TcpStream 拆分为读取端和写入端，可用于同时读写该流。</p>".encode("utf-8")
    ),
    (
        b"<p>This method is more efficient than into_split, but the halves cannot be\nmoved into independently spawned tasks.</p>",
        "<p>此方法比 into_split 更高效，但拆分后的两半不能移到独立 spawn 的任务中。</p>".encode("utf-8")
    ),
    (
        b"<p>Splits a TcpStream into a read half and a write half, which can be used\nto read and write the stream concurrently.</p>\n<p>Unlike split, the owned halves can be moved to separate tasks, however\nthis comes at the cost of a heap allocation.</p>",
        "<p>将 TcpStream 拆分为读取端和写入端，可用于同时读写该流。</p>\n<p>与 split 不同，拥有的两端可以移动到不同的任务中，但这是以一次堆分配为代价的。</p>".encode("utf-8")
    ),
    (
        b"<p>Note: Dropping the write half will shut down the write half of the TCP\nstream. This is equivalent to calling shutdown() on the TcpStream.</p>",
        "<p>注意：释放写入端将关闭 TCP 流的写入端。这等同于在 TcpStream 上调用 shutdown()。</p>".encode("utf-8")
    ),
    (
        b"<p>Consumes stream, returning the tokio I/O object.</p>",
        "<p>消耗流，返回 tokio 的 I/O 对象。</p>".encode("utf-8")
    ),
    (
        b"<p>This is equivalent to\nTcpStream::from_std(stream).</p>",
        "<p>这等同于\nTcpStream::from_std(stream)。</p>".encode("utf-8")
    ),
    # ===== tokio/net/struct.UdpSocket.html =====
    (
        b"<p>A UDP socket.</p>",
        "<p>UDP 套接字。</p>".encode("utf-8")
    ),
    (
        b"<p>UDP is \xe2\x80\x9cconnectionless\xe2\x80\x9d, unlike TCP. Meaning, regardless of what address you\xe2\x80\x99ve bound to, a UdpSocket\nis free to communicate with many different remotes. In tokio there are basically two main ways to use UdpSocket:</p>",
        "<p>与 TCP 不同，UDP 是“无连接”的。这意味着，无论你绑定到哪个地址，UdpSocket 都可以与许多不同的远端通信。在 tokio 中，使用 UdpSocket 的方式主要有两种：</p>".encode("utf-8")
    ),
    (
        b"<p>This type does not provide a split method, because this functionality\ncan be achieved by instead wrapping the socket in an Arc. Note that\nyou do not need a Mutex to share the UdpSocket \xe2\x80\x94 an Arc&lt;UdpSocket&gt;\nis enough. This is because all of the methods take &amp;self instead of\n&amp;mut self. Once you have wrapped it in an Arc, you can call\n.clone() on the Arc&lt;UdpSocket&gt; to get multiple shared handles to the\nsame socket. An example of such usage can be found further down.</p>",
        "<p>此类型不提供 split 方法，因为此功能可以通过将套接字包装在 Arc 中来实现。请注意，你不需要 Mutex 来共享 UdpSocket \xe2\x80\x94 一个 Arc&lt;UdpSocket&gt; 就足够了。这是因为所有方法都使用 &amp;self 而不是 &amp;mut self。一旦将其包装在 Arc 中，就可以对 Arc&lt;UdpSocket&gt; 调用 .clone() 以获得指向同一套接字的多个共享句柄。这种用法的示例可以在下面找到。</p>".encode("utf-8")
    ),
    (
        b"<p>If you need to listen over UDP and produce a Stream, you can look\nat UdpFramed.</p>",
        "<p>如果你需要通过 UDP 监听并生成一个 Stream，可以查看 UdpFramed。</p>".encode("utf-8")
    ),
    (
        b"<p>Using bind we can create a simple echo server that sends and recv\xe2\x80\x99s with many different clients:</p>",
        "<p>使用 bind 可以创建一个简单的 echo 服务器，它与许多不同的客户端发送和接收数据：</p>".encode("utf-8")
    ),
    (
        b"<p>Or using connect we can echo with a single remote address using send and recv:</p>",
        "<p>或者使用 connect，我们可以通过 send 和 recv 与单个远端地址进行回显：</p>".encode("utf-8")
    ),
    (
        b"<p>Because send_to and recv_from take &amp;self. It\xe2\x80\x99s perfectly alright\nto use an Arc&lt;UdpSocket&gt; and share the references to multiple tasks.\nHere is a similar \xe2\x80\x9cecho\xe2\x80\x9d example that supports concurrent\nsending/receiving:</p>",
        "<p>由于 send_to 和 recv_from 接受 &amp;self。使用 Arc&lt;UdpSocket&gt; 并将对它的引用共享给多个任务是完全可以的。下面是一个支持并发发送/接收的类似“echo”示例：</p>".encode("utf-8")
    ),
    (
        b"<p>This function will create a new UDP socket and attempt to bind it to\nthe addr provided.</p>",
        "<p>该函数将创建一个新的 UDP 套接字，并尝试将其绑定到所提供的 addr。</p>".encode("utf-8")
    ),
    (
        b"<p>Binding with a port number of 0 will request that the OS assigns a port\nto this listener. The port allocated can be queried via the local_addr\nmethod.</p>",
        "<p>使用端口号 0 进行绑定时，会要求操作系统为该监听器分配一个端口。分配的端口可以通过 local_addr 方法查询。</p>".encode("utf-8")
    ),
    (
        b"<p>Creates new UdpSocket from a previously bound std::net::UdpSocket.</p>",
        "<p>从之前绑定的 std::net::UdpSocket 创建新的 UdpSocket。</p>".encode("utf-8")
    ),
    (
        b"<p>This function is intended to be used to wrap a UDP socket from the\nstandard library in the Tokio equivalent.</p>",
        "<p>该函数用于将标准库中的 UDP 套接字包装为 Tokio 的对应类型。</p>".encode("utf-8")
    ),
    (
        b"<p>This can be used in conjunction with socket2\xe2\x80\x99s Socket interface to\nconfigure a socket before it\xe2\x80\x99s handed off, such as setting options like\nreuse_address or binding to multiple addresses.</p>",
        "<p>这可以与 socket2 的 Socket 接口配合使用，以便在套接字移交之前对其进行配置，例如设置 reuse_address 等选项或绑定到多个地址。</p>".encode("utf-8")
    ),
    (
        b"<p>This function panics if thread-local runtime is not set.</p>",
        "<p>如果未设置线程局部运行时，该函数会引发 panic。</p>".encode("utf-8")
    ),
    (
        b"<p>Turns a tokio::net::UdpSocket into a std::net::UdpSocket.</p>",
        "<p>将 tokio::net::UdpSocket 转换为 std::net::UdpSocket。</p>".encode("utf-8")
    ),
    (
        b"<p>The returned std::net::UdpSocket will have nonblocking mode set as\ntrue.  Use set_nonblocking to change the blocking mode if needed.</p>",
        "<p>返回的 std::net::UdpSocket 的非阻塞模式将被设置为 true。如有需要，可使用 set_nonblocking 修改阻塞模式。</p>".encode("utf-8")
    ),
    (
        b"<p>Returns the local address that this socket is bound to.</p>",
        "<p>返回该套接字绑定的本地地址。</p>".encode("utf-8")
    ),
    (
        b"<p>Returns the socket address of the remote peer this socket was connected to.</p>",
        "<p>返回该套接字连接到的远端对端的套接字地址。</p>".encode("utf-8")
    ),
    (
        b"<p>Connects the UDP socket setting the default destination for send() and\nlimiting packets that are read via recv from the address specified in\naddr.</p>",
        "<p>连接 UDP 套接字，为 send() 设置默认的目标地址，并限制通过 recv 读取的包来源地址为 addr 中指定的地址。</p>".encode("utf-8")
    ),
    (
        b"<p>This function is usually paired with try_recv() or try_send(). It\ncan be used to concurrently recv / send to the same socket on a single\ntask without splitting the socket.</p>",
        "<p>该函数通常与 try_recv() 或 try_send() 配合使用。它可以在不拆分套接字的情况下，让单个任务同时对该套接字进行 recv / send。</p>".encode("utf-8")
    ),
    (
        b"<p>Concurrently receive from and send to the socket on the same task\nwithout splitting.</p>",
        "<p>在不拆分的情况下，在同一任务上同时对套接字进行接收和发送。</p>".encode("utf-8")
    ),
    (
        b"<p>This function is equivalent to ready(Interest::WRITABLE) and is\nusually paired with try_send() or try_send_to().</p>",
        "<p>该函数等同于 ready(Interest::WRITABLE)，通常与 try_send() 或 try_send_to() 配合使用。</p>".encode("utf-8")
    ),
    (
        b"<p>The function may complete without the socket being writable. This is a\nfalse-positive and attempting a try_send() will return with\nio::ErrorKind::WouldBlock.</p>",
        "<p>函数可能在套接字尚未可写时完成。这是误报情况，尝试进行 try_send() 时将返回 io::ErrorKind::WouldBlock。</p>".encode("utf-8")
    ),
    (
        b"<p>Polls for write/send readiness.</p>",
        "<p>Poll 写入/发送就绪状态。</p>".encode("utf-8")
    ),
    (
        b"<p>If the udp stream is not currently ready for sending, this method will\nstore a clone of the Waker from the provided Context. When the udp\nstream becomes ready for sending, Waker::wake will be called on the\nwaker.</p>",
        "<p>如果 udp 流当前尚未准备好发送，此方法会存储提供的 Context 中 Waker 的一个克隆。当 udp 流变为可发送时，会在该 waker 上调用 Waker::wake。</p>".encode("utf-8")
    ),
    (
        b"<p>Note that on multiple calls to poll_send_ready or poll_send, only\nthe Waker from the Context passed to the most recent call is\nscheduled to receive a wakeup. (However, poll_recv_ready retains a\nsecond, independent waker.)</p>",
        "<p>请注意，对于 poll_send_ready 或 poll_send 的多次调用，仅会调度传递给最近一次调用的 Context 中的 Waker 接收唤醒。（不过 poll_recv_ready 仍保留一个独立的 waker。）</p>".encode("utf-8")
    ),
    (
        b"<p>Sends data on the socket to the remote address that the socket is\nconnected to.</p>",
        "<p>通过套接字向其连接的远端地址发送数据。</p>".encode("utf-8")
    ),
    (
        b"<p>The connect method will connect this socket to a remote address.\nThis method will fail if the socket is not connected.</p>",
        "<p>connect 方法会将该套接字连接到远端地址。如果套接字尚未连接，此方法将失败。</p>".encode("utf-8")
    ),
    (
        b"<p>This method may fail with a ConnectionRefused error if the remote\naddress has replied with ICMP Unreachable to a previously sent packet.\nHowever, this behavior depends on the OS.</p>",
        "<p>如果远端地址已对之前发送的数据包回复了 ICMP Unreachable，此方法可能会因 ConnectionRefused 错误而失败。不过，这种行为取决于操作系统。</p>".encode("utf-8")
    ),
    (
        b"<p>On success, the number of bytes sent is returned, otherwise, the\nencountered error is returned.</p>",
        "<p>成功时返回发送的字节数，否则返回所遇到的错误。</p>".encode("utf-8")
    ),
    (
        b"<p>This method is cancel safe. If send is used as the event in a\ntokio::select! statement and some other branch\ncompletes first, then it is guaranteed that the message was not sent.</p>",
        "<p>此方法可安全取消。如果 send 作为 tokio::select! 语句中的事件，且某个其他分支先完成，则可以保证消息未被发送。</p>".encode("utf-8")
    ),
    (
        b"<p>Attempts to send data on the socket to the remote address to which it\nwas previously connected.</p>",
        "<p>尝试通过套接字向先前连接的远端地址发送数据。</p>".encode("utf-8")
    ),
    (
        b"<p>Note that on multiple calls to a poll_* method in the send direction,\nonly the Waker from the Context passed to the most recent call will\nbe scheduled to receive a wakeup.</p>",
        "<p>请注意，对于发送方向上 poll_* 方法的多次调用，仅会调度传递给最近一次调用的 Context 中的 Waker 接收唤醒。</p>".encode("utf-8")
    ),
    (
        b"<p>Tries to send data on the socket to the remote address to which it is\nconnected.</p>",
        "<p>尝试通过套接字向其连接的远端地址发送数据。</p>".encode("utf-8")
    ),
    (
        b"<p>When the socket buffer is full, Err(io::ErrorKind::WouldBlock) is\nreturned. This function is usually paired with writable().</p>",
        "<p>当套接字缓冲区已满时，返回 Err(io::ErrorKind::WouldBlock)。该函数通常与 writable() 配合使用。</p>".encode("utf-8")
    ),
    (
        b"<p>If successful, Ok(n) is returned, where n is the number of bytes\nsent. If the socket is not ready to send data,\nErr(ErrorKind::WouldBlock) is returned.</p>",
        "<p>如果成功，则返回 Ok(n)，其中 n 是发送的字节数。如果套接字尚未准备好发送数据，则返回 Err(ErrorKind::WouldBlock)。</p>".encode("utf-8")
    ),
    (
        b"<p>Waits for the socket to become readable.</p>",
        "<p>等待套接字变为可读。</p>".encode("utf-8")
    ),
    (
        b"<p>This function is equivalent to ready(Interest::READABLE) and is usually\npaired with try_recv().</p>",
        "<p>该函数等同于 ready(Interest::READABLE)，通常与 try_recv() 配合使用。</p>".encode("utf-8")
    ),
    (
        b"<p>The function may complete without the socket being readable. This is a\nfalse-positive and attempting a try_recv() will return with\nio::ErrorKind::WouldBlock.</p>",
        "<p>函数可能在套接字尚未可读时完成。这是误报情况，尝试进行 try_recv() 时将返回 io::ErrorKind::WouldBlock。</p>".encode("utf-8")
    ),
    (
        b"<p>Polls for read/receive readiness.</p>",
        "<p>Poll 读取/接收就绪状态。</p>".encode("utf-8")
    ),
    (
        b"<p>If the udp stream is not currently ready for receiving, this method will\nstore a clone of the Waker from the provided Context. When the udp\nsocket becomes ready for reading, Waker::wake will be called on the\nwaker.</p>",
        "<p>如果 udp 流当前尚未准备好接收，此方法会存储提供的 Context 中 Waker 的一个克隆。当 udp 套接字变为可读时，会在该 waker 上调用 Waker::wake。</p>".encode("utf-8")
    ),
    (
        b"<p>Note that on multiple calls to poll_recv_ready, poll_recv or\npoll_peek, only the Waker from the Context passed to the most\nrecent call is scheduled to receive a wakeup. (However,\npoll_send_ready retains a second, independent waker.)</p>",
        "<p>请注意，对于 poll_recv_ready、poll_recv 或 poll_peek 的多次调用，仅会调度传递给最近一次调用的 Context 中的 Waker 接收唤醒。（不过 poll_send_ready 仍保留一个独立的 waker。）</p>".encode("utf-8")
    ),
    (
        b"<p>Receives a single datagram message on the socket from the remote address\nto which it is connected. On success, returns the number of bytes read.</p>",
        "<p>从套接字所连接的远端地址接收单个数据报消息。成功时返回读取的字节数。</p>".encode("utf-8")
    ),
    (
        b"<p>The function must be called with valid byte array buf of sufficient\nsize to hold the message bytes. If a message is too long to fit in the\nsupplied buffer, excess bytes may be discarded.</p>",
        "<p>调用此函数时必须传入大小足够容纳消息字节的有效字节数组 buf。如果消息过长而无法放入所提供的缓冲区，则可能丢弃多余的字节。</p>".encode("utf-8")
    ),
    (
        b"<p>This method is cancel safe. If recv is used as the event in a\ntokio::select! statement and some other branch\ncompletes first, it is guaranteed that no messages were received on this\nsocket.</p>",
        "<p>此方法可安全取消。如果 recv 作为 tokio::select! 语句中的事件，且某个其他分支先完成，则可以保证此套接字未接收到任何消息。</p>".encode("utf-8")
    ),
    (
        b"<p>Attempts to receive a single datagram message on the socket from the remote\naddress to which it is connected.</p>",
        "<p>尝试从套接字所连接的远端地址接收单个数据报消息。</p>".encode("utf-8")
    ),
    (
        b"<p>The connect method will connect this socket to a remote address. This method\nresolves to an error if the socket is not connected.</p>",
        "<p>connect 方法会将该套接字连接到远端地址。如果套接字尚未连接，此方法会解析为错误。</p>".encode("utf-8")
    ),
    (
        b"<p>Note that on multiple calls to a poll_* method in the recv direction, only the\nWaker from the Context passed to the most recent call will be scheduled to\nreceive a wakeup.</p>",
        "<p>请注意，对于接收方向上 poll_* 方法的多次调用，仅会调度传递给最近一次调用的 Context 中的 Waker 接收唤醒。</p>".encode("utf-8")
    ),
    (
        b"<p>Tries to receive a single datagram message on the socket from the remote\naddress to which it is connected. On success, returns the number of\nbytes read.</p>",
        "<p>尝试从套接字所连接的远端地址接收单个数据报消息。成功时返回读取的字节数。</p>".encode("utf-8")
    ),
    (
        b"<p>This method must be called with valid byte array buf of sufficient size\nto hold the message bytes. If a message is too long to fit in the\nsupplied buffer, excess bytes may be discarded.</p>",
        "<p>调用此方法时必须传入大小足够容纳消息字节的有效字节数组 buf。如果消息过长而无法放入所提供的缓冲区，则可能丢弃多余的字节。</p>".encode("utf-8")
    ),
    (
        b"<p>When there is no pending data, Err(io::ErrorKind::WouldBlock) is\nreturned. This function is usually paired with readable().</p>",
        "<p>当没有待处理的数据时，返回 Err(io::ErrorKind::WouldBlock)。该函数通常与 readable() 配合使用。</p>".encode("utf-8")
    ),
    (
        b"<p>Tries to read data from the stream into the provided buffer, advancing the\nbuffer\xe2\x80\x99s internal cursor, returning how many bytes were read.</p>",
        "<p>尝试从流读取数据到所提供的缓冲区中，并推进缓冲区的内部游标，返回读取的字节数。</p>".encode("utf-8")
    ),
    (
        b"<p>This method can be used even if buf is uninitialized.</p>",
        "<p>即使 buf 未初始化，也可以使用此方法。</p>".encode("utf-8")
    ),
    (
        b"<p>Receives a single datagram message on the socket from the remote address\nto which it is connected, advancing the buffer\xe2\x80\x99s internal cursor,\nreturning how many bytes were read.</p>",
        "<p>从套接字所连接的远端地址接收单个数据报消息，并推进缓冲区的内部游标，返回读取的字节数。</p>".encode("utf-8")
    ),
    (
        b"<p>Tries to receive a single datagram message on the socket. On success,\nreturns the number of bytes read and the origin.</p>",
        "<p>尝试从套接字接收单个数据报消息。成功时返回读取的字节数及来源地址。</p>".encode("utf-8")
    ),
    (
        b"<p>Note that the socket address cannot be implicitly trusted, because it is relatively\ntrivial to send a UDP datagram with a spoofed origin in a packet injection attack.\nBecause UDP is stateless and does not validate the origin of a packet,\nthe attacker does not need to be able to intercept traffic in order to interfere.\nIt is important to be aware of this when designing your application-level protocol.</p>",
        "<p>请注意，套接字地址不能被隐式信任，因为在数据包注入攻击中以伪造的源地址发送 UDP 数据报相对容易。由于 UDP 是无状态的，且不验证数据包的来源，攻击者无需能够拦截流量即可进行干扰。在设计应用层协议时，请务必了解这一点。</p>".encode("utf-8")
    ),
    (
        b"<p>Receives a single datagram message on the socket, advancing the\nbuffer\xe2\x80\x99s internal cursor, returning how many bytes were read and the origin.</p>",
        "<p>从套接字接收单个数据报消息，并推进缓冲区的内部游标，返回读取的字节数及来源地址。</p>".encode("utf-8")
    ),
    (
        b"<p>Sends data on the socket to the given address. On success, returns the\nnumber of bytes written.</p>",
        "<p>通过套接字向给定地址发送数据。成功时返回写入的字节数。</p>".encode("utf-8")
    ),
    (
        b"<p>Address type can be any implementor of ToSocketAddrs trait. See its\ndocumentation for concrete examples.</p>",
        "<p>地址类型可以是 ToSocketAddrs trait 的任何实现者。具体示例请参阅其文档。</p>".encode("utf-8")
    ),
    (
        b"<p>It is possible for addr to yield multiple addresses, but send_to\nwill only send data to the first address yielded by addr.</p>",
        "<p>addr 可能会产生多个地址，但 send_to 只会将数据发送到 addr 产生的第一个地址。</p>".encode("utf-8")
    ),
    (
        b"<p>This will return an error when the IP version of the local socket does\nnot match that returned from ToSocketAddrs.</p>",
        "<p>当本地套接字的 IP 版本与 ToSocketAddrs 返回的版本不匹配时，将返回错误。</p>".encode("utf-8")
    ),
    (
        b"<p>Attempts to send data on the socket to a given address.</p>",
        "<p>尝试通过套接字向给定地址发送数据。</p>".encode("utf-8")
    ),
    (
        b"<p>Tries to send data on the socket to the given address, but if the send is\nblocked this will return right away.</p>",
        "<p>尝试通过套接字向给定地址发送数据，但如果发送被阻塞，则会立即返回。</p>".encode("utf-8")
    ),
    (
        b"<p>If successful, returns the number of bytes sent</p>",
        "<p>如果成功，则返回发送的字节数。</p>".encode("utf-8")
    ),
    (
        b"<p>Users should ensure that when the remote cannot receive, the\nErrorKind::WouldBlock is properly handled. An error can also occur\nif the IP version of the socket does not match that of target.</p>",
        "<p>用户应确保在远端无法接收时正确处理 ErrorKind::WouldBlock。如果套接字的 IP 版本与目标的版本不匹配，也可能发生错误。</p>".encode("utf-8")
    ),
    (
        b"<p>Receives a single datagram message on the socket. On success, returns\nthe number of bytes read and the origin.</p>",
        "<p>从套接字接收单个数据报消息。成功时返回读取的字节数及来源地址。</p>".encode("utf-8")
    ),
    (
        b"<p>This method is cancel safe. If recv_from is used as the event in a\ntokio::select! statement and some other branch\ncompletes first, it is guaranteed that no messages were received on this\nsocket.</p>",
        "<p>此方法可安全取消。如果 recv_from 作为 tokio::select! 语句中的事件，且某个其他分支先完成，则可以保证此套接字未接收到任何消息。</p>".encode("utf-8")
    ),
    (
        b"<p>Attempts to receive a single datagram on the socket.</p>",
        "<p>尝试从套接字接收单个数据报。</p>".encode("utf-8")
    ),
    (
        b"<p>Tries to receive a single datagram message on the socket. On success,\nreturns the number of bytes read and the origin.</p>",
        "<p>尝试从套接字接收单个数据报消息。成功时返回读取的字节数及来源地址。</p>".encode("utf-8")
    ),
    (
        b"<p>Tries to read or write from the socket using a user-provided IO operation.</p>",
        "<p>尝试使用用户提供的 IO 操作对套接字进行读写。</p>".encode("utf-8")
    ),
    (
        b"<p>If the socket is ready, the provided closure is called. The closure\nshould attempt to perform IO operation on the socket by manually\ncalling the appropriate syscall. If the operation fails because the\nsocket is not actually ready, then the closure should return a\nWouldBlock error and the readiness flag is cleared. The return value\nof the closure is then returned by try_io.</p>",
        "<p>如果套接字就绪，则调用所提供的闭包。闭包应通过手动调用适当的系统调用来尝试对套接字执行 IO 操作。如果由于套接字实际上未就绪而导致操作失败，则闭包应返回 WouldBlock 错误，并清除就绪标志。然后 try_io 返回闭包的返回值。</p>".encode("utf-8")
    ),
    (
        b"<p>If the socket is not ready, then the closure is not called\nand a WouldBlock error is returned.</p>",
        "<p>如果套接字未就绪，则不会调用闭包，并返回 WouldBlock 错误。</p>".encode("utf-8")
    ),
    (
        b"<p>The closure should only return a WouldBlock error if it has performed\nan IO operation on the socket that failed due to the socket not being\nready. Returning a WouldBlock error in any other situation will\nincorrectly clear the readiness flag, which can cause the socket to\nbehave incorrectly.</p>",
        "<p>闭包仅应在已对套接字执行 IO 操作且该操作因套接字未就绪而失败时返回 WouldBlock 错误。在任何其他情况下返回 WouldBlock 错误都会错误地清除就绪标志，从而可能导致套接字行为异常。</p>".encode("utf-8")
    ),
    (
        b"<p>The closure should not perform the IO operation using any of the methods\ndefined on the Tokio UdpSocket type, as this will mess with the\nreadiness flag and can cause the socket to behave incorrectly.</p>",
        "<p>闭包不应使用 Tokio UdpSocket 类型上定义的任何方法来执行 IO 操作，因为这会干扰就绪标志，并可能导致套接字行为异常。</p>".encode("utf-8")
    ),
    (
        b"<p>This method is not intended to be used with combined interests.\nThe closure should perform only one type of IO operation, so it should not\nrequire more than one ready state. This method may panic or sleep forever\nif it is called with a combined interest.</p>\n<p>Usually, readable(), writable() or ready() is used with this function.</p>",
        "<p>该方法不应与组合的 interest 一起使用。闭包应仅执行一种 IO 操作，因此不应需要多于一个就绪状态。如果使用组合的 interest 调用此方法，它可能会 panic 或永远睡眠。</p>\n<p>通常，readable()、writable() 或 ready() 与该函数配合使用。</p>".encode("utf-8")
    ),
    (
        b"<p>Reads or writes from the socket using a user-provided IO operation.</p>",
        "<p>使用用户提供的 IO 操作对套接字进行读写。</p>".encode("utf-8")
    ),
    (
        b"<p>The readiness of the socket is awaited and when the socket is ready,\nthe provided closure is called. The closure should attempt to perform\nIO operation on the socket by manually calling the appropriate syscall.\nIf the operation fails because the socket is not actually ready,\nthen the closure should return a WouldBlock error. In such case the\nreadiness flag is cleared and the socket readiness is awaited again.\nThis loop is repeated until the closure returns an Ok or an error\nother than WouldBlock.</p>",
        "<p>等待套接字就绪，一旦套接字就绪，则调用所提供的闭包。闭包应通过手动调用适当的系统调用来尝试对套接字执行 IO 操作。如果由于套接字实际上未就绪而导致操作失败，则闭包应返回 WouldBlock 错误。在这种情况下，会清除就绪标志并再次等待套接字就绪。该循环会重复进行，直到闭包返回 Ok 或除 WouldBlock 之外的错误。</p>".encode("utf-8")
    ),
    (
        b"<p>The closure should only return a WouldBlock error if it has performed\nan IO operation on the socket that failed due to the socket not being\nready. Returning a WouldBlock error in any other situation will\nincorrectly clear the readiness flag, which can cause the socket to\nbehave incorrectly.</p>",
        "<p>闭包仅应在已对套接字执行 IO 操作且该操作因套接字未就绪而失败时返回 WouldBlock 错误。在任何其他情况下返回 WouldBlock 错误都会错误地清除就绪标志，从而可能导致套接字行为异常。</p>".encode("utf-8")
    ),
    (
        b"<p>The closure should not perform the IO operation using any of the methods\ndefined on the Tokio UdpSocket type, as this will mess with the\nreadiness flag and can cause the socket to behave incorrectly.</p>",
        "<p>闭包不应使用 Tokio UdpSocket 类型上定义的任何方法来执行 IO 操作，因为这会干扰就绪标志，并可能导致套接字行为异常。</p>".encode("utf-8")
    ),
    (
        b"<p>This method is not intended to be used with combined interests.\nThe closure should perform only one type of IO operation, so it should not\nrequire more than one ready state. This method may panic or sleep forever\nif it is called with a combined interest.</p>\n",
        "<p>该方法不应与组合的 interest 一起使用。闭包应仅执行一种 IO 操作，因此不应需要多于一个就绪状态。如果使用组合的 interest 调用此方法，它可能会 panic 或永远睡眠。</p>\n".encode("utf-8")
    ),
    (
        b"<p>Receives a single datagram from the connected address without removing it from the queue.\nOn success, returns the number of bytes read from whence the data came.</p>",
        "<p>从已连接地址接收单个数据报，但不会从队列中移除。成功时返回读取的字节数以及数据来源。</p>".encode("utf-8")
    ),
    (
        b"<p>On Windows, if the data is larger than the buffer specified, the buffer\nis filled with the first part of the data, and peek returns the error\nWSAEMSGSIZE(10040). The excess data is lost.\nMake sure to always use a sufficiently large buffer to hold the\nmaximum UDP packet size, which can be up to 65536 bytes in size.</p>",
        "<p>在 Windows 上，如果数据大于指定的缓冲区，则缓冲区将填充数据的第一部分，peek 会返回错误 WSAEMSGSIZE(10040)。多余的数据会丢失。请务必始终使用足够大的缓冲区来容纳最大的 UDP 数据包大小，最大可达 65536 字节。</p>".encode("utf-8")
    ),
    (
        b"<p>MacOS will return an error if you pass a zero-sized buffer.</p>",
        "<p>如果你传入零大小的缓冲区，MacOS 将返回错误。</p>".encode("utf-8")
    ),
    (
        b"<p>If you\xe2\x80\x99re merely interested in learning the sender of the data at the head of the queue,\ntry peek_sender.</p>",
        "<p>如果你只想了解队列头部数据的发送者，请尝试 peek_sender。</p>".encode("utf-8")
    ),
    (
        b"<p>Receives data from the connected address, without removing it from the input queue.</p>",
        "<p>从已连接地址接收数据，但不会从输入队列中移除。</p>".encode("utf-8")
    ),
    (
        b"<p>Note that on multiple calls to a poll_* method in the recv direction, only the\nWaker from the Context passed to the most recent call will be scheduled to\nreceive a wakeup</p>",
        "<p>请注意，对于接收方向上 poll_* 方法的多次调用，仅会调度传递给最近一次调用的 Context 中的 Waker 接收唤醒。</p>".encode("utf-8")
    ),
    (
        b"<p>If you\xe2\x80\x99re merely interested in learning the sender of the data at the head of the queue,\ntry poll_peek_sender.</p>",
        "<p>如果你只想了解队列头部数据的发送者，请尝试 poll_peek_sender。</p>".encode("utf-8")
    ),
    (
        b"<p>Tries to receive data on the connected address without removing it from the input queue.\nOn success, returns the number of bytes read.</p>",
        "<p>尝试从已连接地址接收数据，但不会从输入队列中移除。成功时返回读取的字节数。</p>".encode("utf-8")
    ),
    (
        b"<p>If you\xe2\x80\x99re merely interested in learning the sender of the data at the head of the queue,\ntry try_peek_sender.</p>",
        "<p>如果你只想了解队列头部数据的发送者，请尝试 try_peek_sender。</p>".encode("utf-8")
    ),
    (
        b"<p>Receives data from the socket, without removing it from the input queue.\nOn success, returns the number of bytes read and the address from whence\nthe data came.</p>",
        "<p>从套接字接收数据，但不会从输入队列中移除。成功时返回读取的字节数以及数据来源地址。</p>".encode("utf-8")
    ),
    (
        b"<p>On Windows, if the data is larger than the buffer specified, the buffer\nis filled with the first part of the data, and peek_from returns the error\nWSAEMSGSIZE(10040). The excess data is lost.\nMake sure to always use a sufficiently large buffer to hold the\nmaximum UDP packet size, which can be up to 65536 bytes in size.</p>",
        "<p>在 Windows 上，如果数据大于指定的缓冲区，则缓冲区将填充数据的第一部分，peek_from 会返回错误 WSAEMSGSIZE(10040)。多余的数据会丢失。请务必始终使用足够大的缓冲区来容纳最大的 UDP 数据包大小，最大可达 65536 字节。</p>".encode("utf-8")
    ),
    (
        b"<p>If you\xe2\x80\x99re merely interested in learning the sender of the data at the head of the queue,\ntry peek_sender.</p>\n",
        "<p>如果你只想了解队列头部数据的发送者，请尝试 peek_sender。</p>\n".encode("utf-8")
    ),
    (
        b"<p>Receives data from the socket, without removing it from the input queue.\nOn success, returns the sending address of the datagram.</p>",
        "<p>从套接字接收数据，但不会从输入队列中移除。成功时返回数据报的发送地址。</p>".encode("utf-8")
    ),
    (
        b"<p>Tries to receive data on the socket without removing it from the input queue.\nOn success, returns the number of bytes read and the sending address of the\ndatagram.</p>",
        "<p>尝试从套接字接收数据，但不会从输入队列中移除。成功时返回读取的字节数以及数据报的发送地址。</p>".encode("utf-8")
    ),
    (
        b"<p>Retrieve the sender of the data at the head of the input queue, waiting if empty.</p>",
        "<p>检索输入队列头部数据的发送者，如果队列为空则等待。</p>".encode("utf-8")
    ),
    (
        b"<p>This is equivalent to calling peek_from with a zero-sized buffer,\nbut suppresses the WSAEMSGSIZE error on Windows and the \xe2\x80\x9cinvalid argument\xe2\x80\x9d error on macOS.</p>",
        "<p>这相当于使用零大小的缓冲区调用 peek_from，但会抑制 Windows 上的 WSAEMSGSIZE 错误以及 macOS 上的“invalid argument”错误。</p>".encode("utf-8")
    ),
    (
        b"<p>Retrieve the sender of the data at the head of the input queue,\nscheduling a wakeup if empty.</p>",
        "<p>检索输入队列头部数据的发送者，如果队列为空则调度一次唤醒。</p>".encode("utf-8")
    ),
    (
        b"<p>This is equivalent to calling poll_peek_from with a zero-sized buffer,\nbut suppresses the WSAEMSGSIZE error on Windows and the \xe2\x80\x9cinvalid argument\xe2\x80\x9d error on macOS.</p>",
        "<p>这相当于使用零大小的缓冲区调用 poll_peek_from，但会抑制 Windows 上的 WSAEMSGSIZE 错误以及 macOS 上的“invalid argument”错误。</p>".encode("utf-8")
    ),
    (
        b"<p>Note that on multiple calls to a poll_* method in the recv direction, only the\nWaker from the Context passed to the most recent call will be scheduled to\nreceive a wakeup.</p>",
        "<p>请注意，对于接收方向上 poll_* 方法的多次调用，仅会调度传递给最近一次调用的 Context 中的 Waker 接收唤醒。</p>".encode("utf-8")
    ),
    (
        b"<p>Try to retrieve the sender of the data at the head of the input queue.</p>",
        "<p>尝试检索输入队列头部数据的发送者。</p>".encode("utf-8")
    ),
    (
        b"<p>Gets the value of the SO_BROADCAST option for this socket.</p>",
        "<p>获取该套接字的 SO_BROADCAST 选项值。</p>".encode("utf-8")
    ),
    (
        b"<p>For more information about this option, see set_broadcast.</p>",
        "<p>关于此选项的更多信息，请参见 set_broadcast。</p>".encode("utf-8")
    ),
    (
        b"<p>Sets the value of the SO_BROADCAST option for this socket.</p>",
        "<p>设置该套接字的 SO_BROADCAST 选项值。</p>".encode("utf-8")
    ),
    (
        b"<p>When enabled, this socket is allowed to send packets to a broadcast\naddress.</p>",
        "<p>启用后，此套接字可以向广播地址发送数据包。</p>".encode("utf-8")
    ),
    (
        b"<p>Gets the value of the IP_MULTICAST_LOOP option for this socket.</p>",
        "<p>获取该套接字的 IP_MULTICAST_LOOP 选项值。</p>".encode("utf-8")
    ),
    (
        b"<p>For more information about this option, see set_multicast_loop_v4.</p>",
        "<p>关于此选项的更多信息，请参见 set_multicast_loop_v4。</p>".encode("utf-8")
    ),
    (
        b"<p>Sets the value of the IP_MULTICAST_LOOP option for this socket.</p>",
        "<p>设置该套接字的 IP_MULTICAST_LOOP 选项值。</p>".encode("utf-8")
    ),
    (
        b"<p>If enabled, multicast packets will be looped back to the local socket.</p>",
        "<p>如果启用，多播数据包将被回环到本地套接字。</p>".encode("utf-8")
    ),
    (
        b"<p>This may not have any effect on IPv6 sockets.</p>",
        "<p>这对 IPv6 套接字可能没有任何效果。</p>".encode("utf-8")
    ),
    (
        b"<p>Gets the value of the IP_MULTICAST_TTL option for this socket.</p>",
        "<p>获取该套接字的 IP_MULTICAST_TTL 选项值。</p>".encode("utf-8")
    ),
    (
        b"<p>For more information about this option, see set_multicast_ttl_v4.</p>",
        "<p>关于此选项的更多信息，请参见 set_multicast_ttl_v4。</p>".encode("utf-8")
    ),
    (
        b"<p>Sets the value of the IP_MULTICAST_TTL option for this socket.</p>",
        "<p>设置该套接字的 IP_MULTICAST_TTL 选项值。</p>".encode("utf-8")
    ),
    (
        b"<p>Indicates the time-to-live value of outgoing multicast packets for\nthis socket. The default value is 1 which means that multicast packets\ndon\xe2\x80\x99t leave the local network unless explicitly requested.</p>",
        "<p>指示此套接字对外发送多播数据包的生存时间值。默认值为 1，这意味着多播数据包不会离开本地网络，除非显式请求。</p>".encode("utf-8")
    ),
    (
        b"<p>Gets the value of the IPV6_MULTICAST_LOOP option for this socket.</p>",
        "<p>获取该套接字的 IPV6_MULTICAST_LOOP 选项值。</p>".encode("utf-8")
    ),
    (
        b"<p>For more information about this option, see set_multicast_loop_v6.</p>",
        "<p>关于此选项的更多信息，请参见 set_multicast_loop_v6。</p>".encode("utf-8")
    ),
    (
        b"<p>Sets the value of the IPV6_MULTICAST_LOOP option for this socket.</p>",
        "<p>设置该套接字的 IPV6_MULTICAST_LOOP 选项值。</p>".encode("utf-8")
    ),
    (
        b"<p>Controls whether this socket sees the multicast packets it sends itself.</p>",
        "<p>控制此套接字是否能看到自身发送的多播数据包。</p>".encode("utf-8")
    ),
    (
        b"<p>This may not have any effect on IPv4 sockets.</p>",
        "<p>这对 IPv4 套接字可能没有任何效果。</p>".encode("utf-8")
    ),
    (
        b"<p>Gets the value of the IP_TTL option for this socket.</p>",
        "<p>获取该套接字的 IP_TTL 选项值。</p>".encode("utf-8")
    ),
    (
        b"<p>For more information about this option, see set_ttl.</p>",
        "<p>关于此选项的更多信息，请参见 set_ttl。</p>".encode("utf-8")
    ),
    (
        b"<p>Sets the value for the IP_TTL option on this socket.</p>",
        "<p>为该套接字设置 IP_TTL 选项的值。</p>".encode("utf-8")
    ),
    (
        b"<p>This value sets the time-to-live field that is used in every packet sent\nfrom this socket.</p>",
        "<p>此值设置了从该套接字发出的每个数据包中使用的生存时间字段。</p>".encode("utf-8")
    ),
    (
        b"<p>Gets the value of the IP_TOS option for this socket.</p>",
        "<p>获取该套接字的 IP_TOS 选项值。</p>".encode("utf-8")
    ),
    (
        b"<p>For more information about this option, see set_tos_v4.</p>",
        "<p>关于此选项的更多信息，请参见 set_tos_v4。</p>".encode("utf-8")
    ),
    (
        b"<p>Sets the value for the IP_TOS option on this socket.</p>",
        "<p>为该套接字设置 IP_TOS 选项的值。</p>".encode("utf-8")
    ),
    (
        b"<p>This value sets the type-of-service field that is used in every packet\nsent from this socket.</p>",
        "<p>此值设置了从该套接字发出的每个数据包中使用的服务类型字段。</p>".encode("utf-8")
    ),
    (
        b"<p>Executes an operation of the IP_ADD_MEMBERSHIP type.</p>",
        "<p>执行 IP_ADD_MEMBERSHIP 类型的操作。</p>".encode("utf-8")
    ),
    (
        b"<p>This function specifies a new multicast group for this socket to join.\nThe address must be a valid multicast address, and interface is the\naddress of the local interface with which the system should join the\nmulticast group. If it\xe2\x80\x99s equal to INADDR_ANY then an appropriate\ninterface is chosen by the system.</p>",
        "<p>该函数为该套接字指定一个新的多播组以加入。地址必须是有效的多播地址，interface 是系统应通过其加入多播组的本地接口的地址。如果它等于 INADDR_ANY，则由系统选择合适的接口。</p>".encode("utf-8")
    ),
    (
        b"<p>Executes an operation of the IPV6_ADD_MEMBERSHIP type.</p>",
        "<p>执行 IPV6_ADD_MEMBERSHIP 类型的操作。</p>".encode("utf-8")
    ),
    (
        b"<p>This function specifies a new multicast group for this socket to join.\nThe address must be a valid multicast address, and interface is the\nindex of the interface to join/leave (or 0 to indicate any interface).</p>",
        "<p>该函数为该套接字指定一个新的多播组以加入。地址必须是有效的多播地址，interface 是要加入/离开的接口的索引（或 0，表示任意接口）。</p>".encode("utf-8")
    ),
    (
        b"<p>Executes an operation of the IP_DROP_MEMBERSHIP type.</p>",
        "<p>执行 IP_DROP_MEMBERSHIP 类型的操作。</p>".encode("utf-8")
    ),
    (
        b"<p>For more information about this option, see join_multicast_v4.</p>",
        "<p>关于此选项的更多信息，请参见 join_multicast_v4。</p>".encode("utf-8")
    ),
    (
        b"<p>Executes an operation of the IPV6_DROP_MEMBERSHIP type.</p>",
        "<p>执行 IPV6_DROP_MEMBERSHIP 类型的操作。</p>".encode("utf-8")
    ),
    (
        b"<p>For more information about this option, see join_multicast_v6.</p>",
        "<p>关于此选项的更多信息，请参见 join_multicast_v6。</p>".encode("utf-8")
    ),
    (
        b"<p>Returns the value of the SO_ERROR option.</p>",
        "<p>返回 SO_ERROR 选项的值。</p>".encode("utf-8")
    ),
    (
        b"<p>Consumes stream, returning the tokio I/O object.</p>",
        "<p>消耗流，返回 tokio 的 I/O 对象。</p>".encode("utf-8")
    ),
    (
        b"<p>This is equivalent to\nUdpSocket::from_std(stream).</p>",
        "<p>这等同于\nUdpSocket::from_std(stream)。</p>".encode("utf-8")
    ),
]

print(f"Stage 1: {len(PAIRS)} pairs defined.")
print("Apply with: python tokio/_translate_subagent_net.py apply")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "apply":
        # Apply pairs to all net/ files
        net_dir = "tokio/net"
        total_files = 0
        total_replacements = 0
        for root, dirs, files in os.walk(net_dir):
            for f in files:
                if not f.endswith(".html"):
                    continue
                fpath = os.path.join(root, f)
                with open(fpath, "rb") as f:
                    data = f.read()
                original = data
                file_replacements = 0
                for en, zh in PAIRS:
                    if en in data:
                        count = data.count(en)
                        data = data.replace(en, zh)
                        file_replacements += count
                if data != original:
                    with open(fpath, "wb") as f:
                        f.write(data)
                    total_files += 1
                    total_replacements += file_replacements
                    print(f"  {fpath}: {file_replacements} replacements")
        print(f"\nTotal: {total_replacements} replacements across {total_files} files")