#!/usr/bin/env python3
"""Translate 14 encoder HTML files from English to Chinese."""
from pathlib import Path
import re

# === General translations ===
# Order matters: longer phrases first to avoid partial matches

# lang attribute
LANG_REPL = ('<html lang="en"', '<html lang="zh"')

# UI strings
UI_REPL = [
    ('title="Drag to resize sidebar"', 'title="拖动以调整侧边栏大小"'),
    ('title="Copy item path to clipboard"', 'title="复制条目路径到剪贴板"'),
    ('id="copy-path" title="Copy item path to clipboard"', 'id="copy-path" title="复制条目路径到剪贴板"'),
]

# Standard library blanket impl docblock text
STDLIB_REPL = [
    # IntoEither - method docblock
    ('Converts <code>self</code> into a <a href="../../either/enum.Either.html#variant.Left" title="variant either::Either::Left"><code>Left</code></a> variant of <a href="../../either/enum.Either.html" title="enum either::Either"><code>Either&lt;Self, Self&gt;</code></a>\nif <code>into_left</code> is <code>true</code>.\nConverts <code>self</code> into a <a href="../../either/enum.Either.html#variant.Right" title="variant either::Either::Right"><code>Right</code></a> variant of <a href="../../either/enum.Either.html" title="enum either::Either"><code>Either&lt;Self, Self&gt;</code></a>\notherwise. <a href="../../either/into_either/trait.IntoEither.html#method.into_either">Read more</a>',
     '当 <code>into_left</code> 为 <code>true</code> 时，将 <code>self</code> 转换为 <a href="../../either/enum.Either.html" title="enum either::Either"><code>Either&lt;Self, Self&gt;</code></a> 的 <a href="../../either/enum.Either.html#variant.Left" title="variant either::Either::Left"><code>Left</code></a> 变体。\n否则将 <code>self</code> 转换为 <a href="../../either/enum.Either.html" title="enum either::Either"><code>Either&lt;Self, Self&gt;</code></a> 的 <a href="../../either/enum.Either.html#variant.Right" title="variant either::Either::Right"><code>Right</code></a> 变体。<a href="../../either/into_either/trait.IntoEither.html#method.into_either">阅读更多</a>'),

    ('Converts <code>self</code> into a <a href="../../either/enum.Either.html#variant.Left" title="variant either::Either::Left"><code>Left</code></a> variant of <a href="../../either/enum.Either.html" title="enum either::Either"><code>Either&lt;Self, Self&gt;</code></a>\nif <code>into_left(&amp;self)</code> returns <code>true</code>.\nConverts <code>self</code> into a <a href="../../either/enum.Either.html#variant.Right" title="variant either::Either::Right"><code>Right</code></a> variant of <a href="../../either/enum.Either.html" title="enum either::Either"><code>Either&lt;Self, Self&gt;</code></a>\notherwise. <a href="../../either/into_either/trait.IntoEither.html#method.into_either_with">Read more</a>',
     '当 <code>into_left(&amp;self)</code> 返回 <code>true</code> 时，将 <code>self</code> 转换为 <a href="../../either/enum.Either.html" title="enum either::Either"><code>Either&lt;Self, Self&gt;</code></a> 的 <a href="../../either/enum.Either.html#variant.Left" title="variant either::Either::Left"><code>Left</code></a> 变体。\n否则将 <code>self</code> 转换为 <a href="../../either/enum.Either.html" title="enum either::Either"><code>Either&lt;Self, Self&gt;</code></a> 的 <a href="../../either/enum.Either.html#variant.Right" title="variant either::Either::Right"><code>Right</code></a> 变体。<a href="../../either/into_either/trait.IntoEither.html#method.into_either_with">阅读更多</a>'),

    # PartialEq / Eq docblock
    ('Tests for <code>!=</code>. The default implementation is almost always sufficient, and should not be overridden without very good reason.',
     '测试 <code>!=</code>。默认实现几乎总是足够的，除非有非常充分的理由，否则不应被覆盖。'),
    ('Tests for <code>self</code> and <code>other</code> values to be equal, and is used by <code>==</code>.',
     '测试 <code>self</code> 和 <code>other</code> 值是否相等，由 <code>==</code> 使用。'),
    ('The resulting type after obtaining ownership.',
     '获取所有权后的结果类型。'),
]

# Audio settings subtype translations
AUDIO_REPL = [
    ('Audio encoder subtypes.', '音频编码器子类型。'),
    ('Advanced Audio Coding (AAC).', '高级音频编码 (AAC)。'),
    ('Dolby Digital (AC-3).', '杜比数字 (AC-3)。'),
    ('AAC framed with ADTS headers.', '使用 ADTS 头封装的 AAC 帧。'),
    ('AAC with HDCP protection.', '带 HDCP 保护的 AAC。'),
    ('AC-3 over S/PDIF.', '通过 S/PDIF 传输的 AC-3。'),
    ('AC-3 with HDCP protection.', '带 HDCP 保护的 AC-3。'),
    ('ADTS (Audio Data Transport Stream).', 'ADTS（音频数据传输流）。'),
    ('Apple Lossless Audio Codec (ALAC).', 'Apple 无损音频编解码器 (ALAC)。'),
    ('Adaptive Multi-Rate Narrowband (AMR-NB).', '自适应多速率窄带 (AMR-NB)。'),
    ('Adaptive Multi-Rate Wideband (AMR-WB).', '自适应多速率宽带 (AMR-WB)。'),
    ('DTS audio.', 'DTS 音频。'),
    ('Enhanced AC-3 (E-AC-3).', '增强型 AC-3 (E-AC-3)。'),
    ('Free Lossless Audio Codec (FLAC).', '自由无损音频编解码器 (FLAC)。'),
    ('32-bit floating-point PCM.', '32 位浮点 PCM。'),
    ('MPEG-1/2 Layer III (MP3).', 'MPEG-1/2 Layer III (MP3)。'),
    ('Generic MPEG audio.', '通用 MPEG 音频。'),
    ('Opus audio.', 'Opus 音频。'),
    ('Pulse-code modulation (PCM).', '脉冲编码调制 (PCM)。'),
    ('Windows Media Audio 8.', 'Windows Media 音频 8。'),
    ('Windows Media Audio 9.', 'Windows Media 音频 9。'),
    ('Vorbis audio.', 'Vorbis 音频。'),
    ('Returns the Windows Media subtype identifier string for this <a class="enum" href="enum.AudioSettingsSubType.html" title="enum windows_capture::encoder::AudioSettingsSubType">AudioSettingsSubType</a>.',
     '返回此 <a class="enum" href="enum.AudioSettingsSubType.html" title="enum windows_capture::encoder::AudioSettingsSubType">AudioSettingsSubType</a> 的 Windows Media 子类型标识符字符串。'),
]

# Container settings subtype translations
CONTAINER_REPL = [
    ('Container subtypes.', '容器子类型。'),
    ('Advanced Systems Format (ASF).', '高级系统格式 (ASF)。'),
    ('Raw MP3 container.', '原始 MP3 容器。'),
    ('MPEG-4 container (e.g., MP4).', 'MPEG-4 容器（例如 MP4）。'),
    ('Audio Video Interleave (AVI).', '音频视频交错 (AVI)。'),
    ('MPEG-2 container.', 'MPEG-2 容器。'),
    ('WAVE (WAV) container.', 'WAVE (WAV) 容器。'),
    ('AAC ADTS stream.', 'AAC ADTS 流。'),
    ('ADTS container.', 'ADTS 容器。'),
    ('3GP container.', '3GP 容器。'),
    ('AMR container.', 'AMR 容器。'),
    ('FLAC container.', 'FLAC 容器。'),
    ('Returns the Windows Media container subtype identifier string for this\n<a class="enum" href="enum.ContainerSettingsSubType.html" title="enum windows_capture::encoder::ContainerSettingsSubType">ContainerSettingsSubType</a>.',
     '返回此 <a class="enum" href="enum.ContainerSettingsSubType.html" title="enum windows_capture::encoder::ContainerSettingsSubType">ContainerSettingsSubType</a> 的 Windows Media 容器子类型标识符字符串。'),
]

# Image encoder pixel format translations
PIXEL_FORMAT_REPL = [
    ('Pixel formats supported by the Windows API for image encoding.', 'Windows API 支持的图像编码像素格式。'),
    ('16-bit floating-point RGBA format.', '16 位浮点 RGBA 格式。'),
    ('8-bit unsigned integer BGRA format.', '8 位无符号整数 BGRA 格式。'),
    ('8-bit unsigned integer RGBA format.', '8 位无符号整数 RGBA 格式。'),
]

# Image format translations
IMAGE_FORMAT_REPL = [
    ('Supported output image formats for <a class="struct" href="struct.ImageEncoder.html" title="struct windows_capture::encoder::ImageEncoder"><code>ImageEncoder</code></a>.',
     '<a class="struct" href="struct.ImageEncoder.html" title="struct windows_capture::encoder::ImageEncoder"><code>ImageEncoder</code></a> 支持的输出图像格式。'),
    ('JPEG (lossy).', 'JPEG（有损）。'),
    ('PNG (lossless).', 'PNG（无损）。'),
    ('GIF (palette-based).', 'GIF（基于调色板）。'),
    ('TIFF (Tagged Image File Format).', 'TIFF（标签图像文件格式）。'),
    ('BMP (Bitmap).', 'BMP（位图）。'),
    ('JPEG XR (HD Photo).', 'JPEG XR（HD 照片）。'),
]

# Video encoder error translations
VIDEO_ERR_REPL = [
    ('Errors emitted by <a class="struct" href="struct.VideoEncoder.html" title="struct windows_capture::encoder::VideoEncoder"><code>VideoEncoder</code></a> during configuration, streaming, or finalization.',
     '在配置、流式传输或最终化过程中由 <a class="struct" href="struct.VideoEncoder.html" title="struct windows_capture::encoder::VideoEncoder"><code>VideoEncoder</code></a> 发出的错误。'),
    ('A Windows Runtime/Win32 API call failed.', 'Windows Runtime/Win32 API 调用失败。'),
    ('Wraps <a class="struct" href="https://doc.rust-lang.org/1.95.0/windows/core/struct.Error.html" title="struct windows::core::Error">windows::core::Error</a>.',
     '包装了 <a class="struct" href="https://doc.rust-lang.org/1.95.0/windows/core/struct.Error.html" title="struct windows::core::Error">windows::core::Error</a>。'),
    ('Failed to send a video sample into the internal pipeline.', '将视频样本发送到内部管线失败。'),
    ('Typically indicates the internal channel is closed.', '通常表示内部通道已关闭。'),
    ('Failed to send an audio sample into the internal pipeline.', '将音频样本发送到内部管线失败。'),
    ('Video encoding was disabled via <a class="associatedfunction" href="struct.VideoSettingsBuilder.html#method.disabled" title="associated function windows_capture::encoder::VideoSettingsBuilder::disabled">VideoSettingsBuilder::disabled</a>.',
     '视频编码已通过 <a class="associatedfunction" href="struct.VideoSettingsBuilder.html#method.disabled" title="associated function windows_capture::encoder::VideoSettingsBuilder::disabled">VideoSettingsBuilder::disabled</a> 禁用。'),
    ('Audio encoding was disabled via <a class="associatedfunction" href="struct.AudioSettingsBuilder.html#method.disabled" title="associated function windows_capture::encoder::AudioSettingsBuilder::disabled">AudioSettingsBuilder::disabled</a>.',
     '音频编码已通过 <a class="associatedfunction" href="struct.AudioSettingsBuilder.html#method.disabled" title="associated function windows_capture::encoder::AudioSettingsBuilder::disabled">AudioSettingsBuilder::disabled</a> 禁用。'),
    ('An I/O error occurred during file creation or writing.', '在文件创建或写入过程中发生 I/O 错误。'),
    ('The provided frame color format is unsupported by the encoder path.', '提供的帧颜色格式不被编码器路径支持。'),
    ('See <a class="enum" href="../settings/enum.ColorFormat.html" title="enum windows_capture::settings::ColorFormat"><code>ColorFormat</code></a>.',
     '参见 <a class="enum" href="../settings/enum.ColorFormat.html" title="enum windows_capture::settings::ColorFormat"><code>ColorFormat</code></a>。'),
]

# Image encoder error translations (already partially done, just touch up)
IMAGE_ERR_REPL = [
    ('<p>Wraps <a class="struct" href="https://doc.rust-lang.org/1.95.0/std/io/struct.Error.html" title="struct std::io::Error">std::io::Error</a>.</p>', '<p>包装了 <a class="struct" href="https://doc.rust-lang.org/1.95.0/std/io/struct.Error.html" title="struct std::io::Error">std::io::Error</a>。</p>'),
    ('<p>Wraps <a class="struct" href="https://doc.rust-lang.org/1.95.0/std/num/struct.TryFromIntError.html" title="struct std::num::TryFromIntError">std::num::TryFromIntError</a>.</p>', '<p>包装了 <a class="struct" href="https://doc.rust-lang.org/1.95.0/std/num/struct.TryFromIntError.html" title="struct std::num::TryFromIntError">std::num::TryFromIntError</a>。</p>'),
]

# Video settings subtype translations
VIDEO_SUBTYPE_REPL = [
    ('Video encoder subtypes.', '视频编码器子类型。'),
    ('Uncompressed 32-bit ARGB (8:8:8:8).', '未压缩的 32 位 ARGB (8:8:8:8)。'),
    ('Uncompressed 32-bit BGRA (8:8:8:8).', '未压缩的 32 位 BGRA (8:8:8:8)。'),
    ('16-bit depth format.', '16 位深度格式。'),
    ('H.263 video.', 'H.263 视频。'),
    ('H.264/AVC video.', 'H.264/AVC 视频。'),
    ('H.264 elementary stream.', 'H.264 基本流。'),
    ('H.265/HEVC video.', 'H.265/HEVC 视频。'),
    ('H.265/HEVC elementary stream.', 'H.265/HEVC 基本流。'),
    ('Planar YUV 4:2:0 (IYUV).', '平面 YUV 4:2:0 (IYUV)。'),
    ('8-bit luminance (grayscale).', '8 位亮度（灰度）。'),
    ('16-bit luminance (grayscale).', '16 位亮度（灰度）。'),
    ('Motion JPEG.', '运动 JPEG。'),
    ('NV12 YUV 4:2:0 (semi-planar).', 'NV12 YUV 4:2:0（半平面）。'),
    ('MPEG-1 video.', 'MPEG-1 视频。'),
    ('MPEG-2 video.', 'MPEG-2 视频。'),
    ('24-bit RGB.', '24 位 RGB。'),
    ('32-bit RGB.', '32 位 RGB。'),
    ('Windows Media Video 9 (WMV3).', 'Windows Media Video 9 (WMV3)。'),
    ('Windows Media Video Advanced Profile (VC-1).', 'Windows Media Video 高级配置 (VC-1)。'),
    ('VP9 video.', 'VP9 视频。'),
    ('Packed YUY2 4:2:2.', '打包的 YUY2 4:2:2。'),
    ('Planar YV12 4:2:0.', '平面 YV12 4:2:0。'),
    ('Returns the Windows Media subtype identifier string for this <a class="enum" href="enum.VideoSettingsSubType.html" title="enum windows_capture::encoder::VideoSettingsSubType">VideoSettingsSubType</a>.',
     '返回此 <a class="enum" href="enum.VideoSettingsSubType.html" title="enum windows_capture::encoder::VideoSettingsSubType">VideoSettingsSubType</a> 的 Windows Media 子类型标识符字符串。'),
]

# AudioSettingsBuilder docblock
AUDIO_BUILDER_REPL = [
    ('Builder for configuring audio encoder settings.', '用于配置音频编码器设置的构建器。'),
    ('Constructs a new <a class="struct" href="struct.AudioSettingsBuilder.html" title="struct windows_capture::encoder::AudioSettingsBuilder">AudioSettingsBuilder</a> with common defaults.',
     '使用常用默认值构造一个新的 <a class="struct" href="struct.AudioSettingsBuilder.html" title="struct windows_capture::encoder::AudioSettingsBuilder">AudioSettingsBuilder</a>。'),
    ('Sets audio bitrate in bits per second.', '设置音频比特率（比特/秒）。'),
    ('Sets number of interleaved channels.', '设置交错声道数。'),
    ('Sets sample rate in Hz.', '设置采样率（赫兹）。'),
    ('Sets bits per sample.', '设置每样本位数。'),
    ('Sets audio codec/subtype (e.g., <a class="variant" href="enum.AudioSettingsSubType.html#variant.AAC" title="variant windows_capture::encoder::AudioSettingsSubType::AAC">AudioSettingsSubType::AAC</a>).',
     '设置音频编解码器/子类型（例如 <a class="variant" href="enum.AudioSettingsSubType.html#variant.AAC" title="variant windows_capture::encoder::AudioSettingsSubType::AAC">AudioSettingsSubType::AAC</a>）。'),
    ('Disables or enables audio encoding.', '禁用或启用音频编码。'),
]

# ContainerSettingsBuilder docblock
CONTAINER_BUILDER_REPL = [
    ('Builder for configuring container settings.', '用于配置容器设置的构建器。'),
    ('Constructs a new <a class="struct" href="struct.ContainerSettingsBuilder.html" title="struct windows_capture::encoder::ContainerSettingsBuilder">ContainerSettingsBuilder</a>.',
     '构造一个新的 <a class="struct" href="struct.ContainerSettingsBuilder.html" title="struct windows_capture::encoder::ContainerSettingsBuilder">ContainerSettingsBuilder</a>。'),
    ('Default subtype: <a class="variant" href="enum.ContainerSettingsSubType.html#variant.MPEG4" title="variant windows_capture::encoder::ContainerSettingsSubType::MPEG4">ContainerSettingsSubType::MPEG4</a>.',
     '默认子类型：<a class="variant" href="enum.ContainerSettingsSubType.html#variant.MPEG4" title="variant windows_capture::encoder::ContainerSettingsSubType::MPEG4">ContainerSettingsSubType::MPEG4</a>。'),
    ('Sets the container subtype (e.g., <a class="variant" href="enum.ContainerSettingsSubType.html#variant.MPEG4" title="variant windows_capture::encoder::ContainerSettingsSubType::MPEG4">ContainerSettingsSubType::MPEG4</a>).',
     '设置容器子类型（例如 <a class="variant" href="enum.ContainerSettingsSubType.html#variant.MPEG4" title="variant windows_capture::encoder::ContainerSettingsSubType::MPEG4">ContainerSettingsSubType::MPEG4</a>）。'),
]

# ImageEncoder docblock
IMAGE_ENCODER_REPL = [
    ('Encodes raw image buffers into encoded bytes for common formats.', '将原始图像缓冲区编码为通用格式的编码字节。'),
    ('Supports saving as PNG, JPEG, GIF, TIFF, BMP, and JPEG XR when the input\ncolor format is compatible.', '当输入颜色格式兼容时，支持保存为 PNG、JPEG、GIF、TIFF、BMP 和 JPEG XR。'),
    ('Constructs a new <a class="struct" href="struct.ImageEncoder.html" title="struct windows_capture::encoder::ImageEncoder">ImageEncoder</a>.',
     '构造一个新的 <a class="struct" href="struct.ImageEncoder.html" title="struct windows_capture::encoder::ImageEncoder">ImageEncoder</a>。'),
    ('Encodes the provided pixel buffer into the configured output <a class="enum" href="enum.ImageFormat.html" title="enum windows_capture::encoder::ImageFormat">ImageFormat</a>.',
     '将提供的像素缓冲区编码为配置的输出 <a class="enum" href="enum.ImageFormat.html" title="enum windows_capture::encoder::ImageFormat">ImageFormat</a>。'),
    ('The input buffer must match the specified source <a class="enum" href="../settings/enum.ColorFormat.html" title="enum windows_capture::settings::ColorFormat">ColorFormat</a>\nand dimensions. For packed 8-bit formats (e.g., <a class="variant" href="../settings/enum.ColorFormat.html#variant.Bgra8" title="variant windows_capture::settings::ColorFormat::Bgra8">ColorFormat::Bgra8</a>),\nthe buffer length should be <code>width * height * 4</code>.',
     '输入缓冲区必须与指定的源 <a class="enum" href="../settings/enum.ColorFormat.html" title="enum windows_capture::settings::ColorFormat">ColorFormat</a> 和尺寸匹配。对于 8 位打包格式（例如 <a class="variant" href="../settings/enum.ColorFormat.html#variant.Bgra8" title="variant windows_capture::settings::ColorFormat::Bgra8">ColorFormat::Bgra8</a>），\n缓冲区长度应为 <code>width * height * 4</code>。'),
    ('The buffer length should be width * \nheight * 4.', '缓冲区长度应为 width * height * 4。'),
    ('image encoders (e.g., <a class="enum" href="../settings/enum.ColorFormat.html#variant.Rgba16F" title="variant windows_capture::settings::ColorFormat::Rgba16F">ColorFormat::Rgba16F</a>)',
     '图像编码器（例如 <a class="enum" href="../settings/enum.ColorFormat.html#variant.Rgba16F" title="variant windows_capture::settings::ColorFormat::Rgba16F">ColorFormat::Rgba16F</a>)'),
]

# VideoSettingsBuilder docblock
VIDEO_BUILDER_REPL = [
    ('Builder for configuring video encoder settings.', '用于配置视频编码器设置的构建器。'),
    ('Constructs a new <a class="struct" href="struct.VideoSettingsBuilder.html" title="struct windows_capture::encoder::VideoSettingsBuilder">VideoSettingsBuilder</a> with the given dimensions.',
     '使用给定尺寸构造一个新的 <a class="struct" href="struct.VideoSettingsBuilder.html" title="struct windows_capture::encoder::VideoSettingsBuilder">VideoSettingsBuilder</a>。'),
    ('Sets video codec/subtype (e.g., <a class="variant" href="enum.VideoSettingsSubType.html#variant.HEVC" title="variant windows_capture::encoder::VideoSettingsSubType::HEVC">VideoSettingsSubType::HEVC</a>).',
     '设置视频编解码器/子类型（例如 <a class="variant" href="enum.VideoSettingsSubType.html#variant.HEVC" title="variant windows_capture::encoder::VideoSettingsSubType::HEVC">VideoSettingsSubType::HEVC</a>）。'),
    ('Sets target bitrate in bits per second.', '设置目标比特率（比特/秒）。'),
    ('Sets target frame width in pixels.', '设置目标帧宽度（像素）。'),
    ('Sets target frame height in pixels.', '设置目标帧高度（像素）。'),
    ('Sets target frame rate (fps). The denominator is fixed to 1.', '设置目标帧率（fps）。分母固定为 1。'),
    ('Sets pixel aspect ratio. 1:1 preserves square pixels.', '设置像素宽高比。1:1 保持正方形像素。'),
    ('Disables or enables video encoding.', '禁用或启用视频编码。'),
    ('When <code>true</code>, the encoder drops frames that arrive faster than the configured frame rate.', '当为 <code>true</code> 时，编码器将丢弃到达速度快于所配置帧率的帧。'),
]

# AudioEncoderSource / VideoEncoderSource common
SOURCE_REPL = [
    ('Audio sources used by <a class="struct" href="struct.VideoEncoder.html" title="struct windows_capture::encoder::VideoEncoder"><code>VideoEncoder</code></a>. The encoder takes ownership of the bytes.',
     '<a class="struct" href="struct.VideoEncoder.html" title="struct windows_capture::encoder::VideoEncoder"><code>VideoEncoder</code></a> 使用的音频源。编码器获取这些字节的所有权。'),
    ('Interleaved PCM bytes.', '交错的 PCM 字节。'),
    ('Video sources used by <a class="struct" href="struct.VideoEncoder.html" title="struct windows_capture::encoder::VideoEncoder"><code>VideoEncoder</code></a>.',
     '<a class="struct" href="struct.VideoEncoder.html" title="struct windows_capture::encoder::VideoEncoder"><code>VideoEncoder</code></a> 使用的视频源。'),
    ('A Direct3D surface sample.', 'Direct3D 表面样本。'),
    ('A raw BGRA sample buffer.', '原始 BGRA 样本缓冲区。'),
]

# VideoEncoder docblock
VIDEO_ENCODER_REPL = [
    ('Encodes video frames (and optional audio) and writes them to a file or stream.', '编码视频帧（和可选音频）并将其写入文件或流。'),
    ('Frames are provided as Direct3D surfaces or raw BGRA buffers. Audio can be pushed\nas interleaved PCM bytes.', '帧以 Direct3D 表面或原始 BGRA 缓冲区的形式提供。音频可以以交错 PCM 字节的形式推送。'),
    ('Constructs a new <a class="struct" href="struct.VideoEncoder.html" title="struct windows_capture::encoder::VideoEncoder">VideoEncoder</a> that writes to a file path.',
     '构造一个新的写入文件路径的 <a class="struct" href="struct.VideoEncoder.html" title="struct windows_capture::encoder::VideoEncoder">VideoEncoder</a>。'),
    ('Constructs a new <a class="struct" href="struct.VideoEncoder.html" title="struct windows_capture::encoder::VideoEncoder">VideoEncoder</a> that writes to the given stream.',
     '构造一个新的写入给定流的 <a class="struct" href="struct.VideoEncoder.html" title="struct windows_capture::encoder::VideoEncoder">VideoEncoder</a>。'),
    ('Unlike <a class="fn" href="struct.VideoEncoder.html#method.new" title="associated function windows_capture::encoder::VideoEncoder::new">VideoEncoder::new</a>, which writes directly to a file, this constructor writes\nencoded output into any [IRandomAccessStream]. Use [InMemoryRandomAccessStream] to\nkeep the encoded video in memory (e.g., for network streaming or further processing).',
     '与直接写入文件的 <a class="fn" href="struct.VideoEncoder.html#method.new" title="associated function windows_capture::encoder::VideoEncoder::new">VideoEncoder::new</a> 不同，此构造函数将编码输出写入任何 [IRandomAccessStream]。使用 [InMemoryRandomAccessStream] 将编码后的视频保留在内存中（例如用于网络流式传输或进一步处理）。'),
    ('Unlike <a class="fn" href="struct.VideoEncoder.html#method.new" title="associated function windows_capture::encoder::VideoEncoder::new">VideoEncoder::new</a>, which writes directly to a file, this constructor writes encoded output into any <a href="https://doc.rust-lang.org/1.95.0/windows.Storage.Streams/struct.IRandomAccessStream.html">[IRandomAccessStream]</a>. Use <a href="https://doc.rust-lang.org/1.95.0/windows.Storage.Streams/struct.InMemoryRandomAccessStream.html">[InMemoryRandomAccessStream]</a> to keep the encoded video in memory (e.g., for network streaming or further processing).',
     '与直接写入文件的 <a class="fn" href="struct.VideoEncoder.html#method.new" title="associated function windows_capture::encoder::VideoEncoder::new">VideoEncoder::new</a> 不同，此构造函数将编码输出写入任何 <a href="https://doc.rust-lang.org/1.95.0/windows.Storage.Streams/struct.IRandomAccessStream.html">[IRandomAccessStream]</a>。使用 <a href="https://doc.rust-lang.org/1.95.0/windows.Storage.Streams/struct.InMemoryRandomAccessStream.html">[InMemoryRandomAccessStream]</a> 将编码后的视频保留在内存中（例如用于网络流式传输或进一步处理）。'),
    ('Sends a video frame (DirectX). Returns immediately.', '发送一帧视频（DirectX）。立即返回。'),
    ('Sends a video frame with an audio buffer; the encoder takes ownership of the bytes and\nfinishes when all frames are sent or <a class="fn" href="struct.VideoEncoder.html#method.finish" title="associated function windows_capture::encoder::VideoEncoder::finish">finish</a> is called.',
     '发送一帧带音频缓冲区的视频；编码器获取这些字节的所有权，并在所有帧发送完毕或调用 <a class="fn" href="struct.VideoEncoder.html#method.finish" title="associated function windows_capture::encoder::VideoEncoder::finish">finish</a> 时结束。'),
    ('Sends a frame of raw data; the encoder takes ownership. For the GPU path, the Windows\nallocator handles BGRA and row-major memory layout.', '发送一帧原始数据；编码器获取所有权。对于 GPU 路径，Windows 分配器处理 BGRA 和行主序内存布局。'),
    ('Sends an audio buffer; the encoder takes ownership. Note: the timestamp is ignored;\nuse only when pairing with video frames sent earlier.', '发送一个音频缓冲区；编码器获取所有权。注意：时间戳被忽略；仅在与之前发送的视频帧配对时使用。'),
    ('Finalizes encoding and performs any necessary cleanup.', '完成编码并执行任何必要的清理。'),
]

# Additional replacements for untranslated text
ADDITIONAL_REPL = [
    # PartialEq impl with line break
    ('Tests for <code>!=</code>. The default implementation is almost always sufficient,\nand should not be overridden without very good reason.',
     '测试 <code>!=</code>。默认实现几乎总是足够的，除非有非常充分的理由，否则不应被覆盖。'),

    # VideoEncoder - new_from_stream with regular brackets
    ('Unlike <a class="fn" href="struct.VideoEncoder.html#method.new" title="associated function windows_capture::encoder::VideoEncoder::new">VideoEncoder::new</a>, which writes directly to a file, this constructor writes encoded output into any [ IRandomAccessStream ]. Use [ InMemoryRandomAccessStream ] to keep the encoded video in memory (e.g., for network streaming or further processing).',
     '与直接写入文件的 <a class="fn" href="struct.VideoEncoder.html#method.new" title="associated function windows_capture::encoder::VideoEncoder::new">VideoEncoder::new</a> 不同，此构造函数将编码输出写入任何 [IRandomAccessStream]。使用 [InMemoryRandomAccessStream] 将编码后的视频保留在内存中（例如用于网络流式传输或进一步处理）。'),

    # Defaults: text
    ('Defaults:', '默认值：'),

    # Mojibake text - half-width chars converted to full-width by previous translation
    # These have full-width parens/full-width period from previous work
    ('Dolby Digital（AC-3）。', '杜比数字（AC-3）。'),
    ('MPEG-1/2 Layer III (MP3)。', 'MPEG-1/2 Layer III (MP3)。'),
    ('MPEG-1/2 Layer III (MP3)。', 'MPEG-1/2 Layer III (MP3)。'),
    ('Motion JPEG。', '运动 JPEG。'),
    ('Windows Media Video 9 (WMV3)。', 'Windows Media Video 9 (WMV3)。'),
    ('Windows Media Audio 8。', 'Windows Media 音频 8。'),
    ('Windows Media Audio 9。', 'Windows Media 音频 9。'),
    ('Windows Media Video Advanced Profile (VC-1)。', 'Windows Media Video 高级配置 (VC-1)。'),
    ('Apple Lossless Audio Codec (ALAC)。', 'Apple 无损音频编解码器 (ALAC)。'),
    ('Generic MPEG audio。', '通用 MPEG 音频。'),
    ('Pulse-code modulation (PCM)。', '脉冲编码调制 (PCM)。'),
    ('32-bit floating-point PCM。', '32 位浮点 PCM。'),
    ('Opus audio。', 'Opus 音频。'),
    ('Vorbis audio。', 'Vorbis 音频。'),
    ('DTS audio。', 'DTS 音频。'),
    ('Free Lossless Audio Codec (FLAC)。', '自由无损音频编解码器 (FLAC)。'),
    ('AAC ADTS stream。', 'AAC ADTS 流。'),
    ('3GP container。', '3GP 容器。'),
    ('ADTS container。', 'ADTS 容器。'),
    ('AMR container。', 'AMR 容器。'),
    ('FLAC container。', 'FLAC 容器。'),
    ('Advanced Systems Format (ASF)。', '高级系统格式 (ASF)。'),
    ('Raw MP3 container。', '原始 MP3 容器。'),
    ('MPEG-2 container。', 'MPEG-2 容器。'),
    ('WAVE (WAV) container。', 'WAVE (WAV) 容器。'),
    ('Audio Video Interleave (AVI)。', '音频视频交错 (AVI)。'),
    ('MPEG-4 container (e.g., MP4)。', 'MPEG-4 容器（例如 MP4）。'),
    ('Advanced Audio Coding (AAC)。', '高级音频编码 (AAC)。'),
    ('AAC framed with ADTS headers。', '使用 ADTS 头封装的 AAC 帧。'),
    ('AAC with HDCP protection。', '带 HDCP 保护的 AAC。'),
    ('AC-3 over S/PDIF。', '通过 S/PDIF 传输的 AC-3。'),
    ('AC-3 with HDCP protection。', '带 HDCP 保护的 AC-3。'),
    ('ADTS (Audio Data Transport Stream)。', 'ADTS（音频数据传输流）。'),
    ('Enhanced AC-3 (E-AC-3)。', '增强型 AC-3 (E-AC-3)。'),
    ('Adaptive Multi-Rate Narrowband (AMR-NB)。', '自适应多速率窄带 (AMR-NB)。'),
    ('Adaptive Multi-Rate Wideband (AMR-WB)。', '自适应多速率宽带 (AMR-WB)。'),
    ('H.263 video。', 'H.263 视频。'),
    ('H.264/AVC video。', 'H.264/AVC 视频。'),
    ('H.264 elementary stream。', 'H.264 基本流。'),
    ('H.265/HEVC video。', 'H.265/HEVC 视频。'),
    ('H.265/HEVC elementary stream。', 'H.265/HEVC 基本流。'),
    ('Planar YUV 4:2:0 (IYUV)。', '平面 YUV 4:2:0 (IYUV)。'),
    ('8-bit luminance (grayscale)。', '8 位亮度（灰度）。'),
    ('16-bit luminance (grayscale)。', '16 位亮度（灰度）。'),
    ('NV12 YUV 4:2:0 (semi-planar)。', 'NV12 YUV 4:2:0（半平面）。'),
    ('MPEG-1 video。', 'MPEG-1 视频。'),
    ('MPEG-2 video。', 'MPEG-2 视频。'),
    ('24-bit RGB。', '24 位 RGB。'),
    ('32-bit RGB。', '32 位 RGB。'),
    ('VP9 video。', 'VP9 视频。'),
    ('Packed YUY2 4:2:2。', '打包的 YUY2 4:2:2。'),
    ('Planar YV12 4:2:0。', '平面 YV12 4:2:0。'),
    ('16-bit depth format。', '16 位深度格式。'),
    ('Uncompressed 32-bit ARGB (8:8:8:8)。', '未压缩的 32 位 ARGB (8:8:8:8)。'),
    ('Uncompressed 32-bit BGRA (8:8:8:8)。', '未压缩的 32 位 BGRA (8:8:8:8)。'),
    ('JPEG (lossy)。', 'JPEG（有损）。'),
    ('PNG (lossless)。', 'PNG（无损）。'),
    ('GIF (palette-based)。', 'GIF（基于调色板）。'),
    ('TIFF (Tagged Image File Format)。', 'TIFF（标签图像文件格式）。'),
    ('BMP (Bitmap)。', 'BMP（位图）。'),
    ('JPEG XR (HD Photo)。', 'JPEG XR（HD 照片）。'),
    ('16-bit floating-point RGBA format。', '16 位浮点 RGBA 格式。'),
    ('8-bit unsigned integer BGRA format。', '8 位无符号整数 BGRA 格式。'),
    ('8-bit unsigned integer RGBA format。', '8 位无符号整数 RGBA 格式。'),
    ('Pixel formats supported by the Windows API for image encoding。', 'Windows API 支持的图像编码像素格式。'),
    ('Container subtypes。', '容器子类型。'),
    ('Audio encoder subtypes。', '音频编码器子类型。'),
    ('Video encoder subtypes。', '视频编码器子类型。'),
    ('Interleaved PCM bytes。', '交错的 PCM 字节。'),
    ('A Direct3D surface sample。', 'Direct3D 表面样本。'),
    ('A raw BGRA sample buffer。', '原始 BGRA 样本缓冲区。'),

    # VideoEncoder method docblocks
    ('Sends a video frame (DirectX). Returns immediately.', '发送一帧视频（DirectX）。立即返回。'),
    ('Sends a video frame with an audio buffer; the encoder takes ownership of the bytes and\nfinishes when all frames are sent or <a class="fn" href="struct.VideoEncoder.html#method.finish" title="associated function windows_capture::encoder::VideoEncoder::finish">finish</a> is called.',
     '发送一帧带音频缓冲区的视频；编码器获取这些字节的所有权，并在所有帧发送完毕或调用 <a class="fn" href="struct.VideoEncoder.html#method.finish" title="associated function windows_capture::encoder::VideoEncoder::finish">finish</a> 时结束。'),
    ('Sends a frame of raw data; the encoder takes ownership. For the GPU path, the Windows\nallocator handles BGRA and row-major memory layout.',
     '发送一帧原始数据；编码器获取所有权。对于 GPU 路径，Windows 分配器处理 BGRA 和行主序内存布局。'),
    ('Sends an audio buffer; the encoder takes ownership. Note: the timestamp is ignored;\nuse only when pairing with video frames sent earlier.',
     '发送一个音频缓冲区；编码器获取所有权。注意：时间戳被忽略；仅在与之前发送的视频帧配对时使用。'),
    ('Finalizes encoding and performs any necessary cleanup.', '完成编码并执行任何必要的清理。'),

    # Builder docblocks
    ('Sets audio bitrate in bits per second.', '设置音频比特率（比特/秒）。'),
    ('Sets number of interleaved channels.', '设置交错声道数。'),
    ('Sets sample rate in Hz.', '设置采样率（赫兹）。'),
    ('Sets bits per sample.', '设置每样本位数。'),
    ('Disables or enables audio encoding.', '禁用或启用音频编码。'),
    ('Disables or enables video encoding.', '禁用或启用视频编码。'),
    ('Sets target bitrate in bits per second.', '设置目标比特率（比特/秒）。'),
    ('Sets target frame width in pixels.', '设置目标帧宽度（像素）。'),
    ('Sets target frame height in pixels.', '设置目标帧高度（像素）。'),
    ('Sets target frame rate (fps). The denominator is fixed to 1.', '设置目标帧率（fps）。分母固定为 1。'),
    ('Sets pixel aspect ratio. 1:1 preserves square pixels.', '设置像素宽高比。1:1 保持正方形像素。'),
    ('When <code>true</code>, the encoder drops frames that arrive faster than the configured frame rate.',
     '当为 <code>true</code> 时，编码器将丢弃到达速度快于所配置帧率的帧。'),
]


# Generic standard library translations
GENERIC_REPL = [
    ('Returns the argument unchanged.', '原样返回参数。'),
    ('Calls <code>U::from(self)</code>.', '调用 <code>U::from(self)</code>。'),
    ('Calls <a class=\"primitive\" href=\"https://doc.rust-lang.org/1.95.0/core/ops/function/trait.FnOnce.html\" title=\"trait core::ops::function::FnOnce\"><code>FnOnce</code></a>(<code>&amp;self</code>).', '调用 <a class=\"primitive\" href=\"https://doc.rust-lang.org/1.95.0/core/ops/function/trait.FnOnce.html\" title=\"trait core::ops::function::FnOnce\"><code>FnOnce</code></a>(<code>&amp;self</code>)。'),
    ('<p>That is, this conversion is whatever the implementation of\n<code><a href=\"https://doc.rust-lang.org/1.95.0/core/convert/trait.From.html\" title=\"trait core::convert::From\">From</a>&lt;T&gt; for U</code> chooses to do.</p>',
     '<p>也就是说，此转换由 <code><a href=\"https://doc.rust-lang.org/1.95.0/core/convert/trait.From.html\" title=\"trait core::convert::From\">From</a>&lt;T&gt; for U</code> 的实现来决定。</p>'),
    ('<p>Performs the conversion.</p>', '<p>执行转换。</p>'),
    ('<p>Immutably borrows from an owned value. <a href=\"https://doc.rust-lang.org/1.95.0/core/borrow/trait.Borrow.html#tymethod.borrow\">Read more</a></p>',
     '<p>从拥有的值不可变地借用。<a href=\"https://doc.rust-lang.org/1.95.0/core/borrow/trait.Borrow.html#tymethod.borrow\">阅读更多</a></p>'),
    ('<p>Mutably borrows from an owned value. <a href=\"https://doc.rust-lang.org/1.95.0/core/borrow/trait.BorrowMut.html#tymethod.borrow_mut\">Read more</a></p>',
     '<p>从拥有的值可变地借用。<a href=\"https://doc.rust-lang.org/1.95.0/core/borrow/trait.BorrowMut.html#tymethod.borrow_mut\">阅读更多</a></p>'),
    ('<p>Gets the <code>TypeId</code> of <code>self</code>. <a href=\"https://doc.rust-lang.org/1.95.0/core/any/trait.Any.html#tymethod.type_id\">Read more</a></p>',
     '<p>获取 <code>self</code> 的 <code>TypeId</code>。<a href=\"https://doc.rust-lang.org/1.95.0/core/any/trait.Any.html#tymethod.type_id\">阅读更多</a></p>'),
    ('<p>The type for initializers.</p>', '<p>初始化器的类型。</p>'),
    ('<p>The alignment of pointer.</p>', '<p>指针对齐方式。</p>'),
    ('Initializes a with the given initializer. <a href=\"../../crossbeam_epoch/atomic/trait.Pointable.html#tymethod.init\">Read more</a>',
     '使用给定的初始化器初始化 a。<a href=\"../../crossbeam_epoch/atomic/trait.Pointable.html#tymethod.init\">阅读更多</a>'),
    ('Dereferences the given pointer. <a href=\"../../crossbeam_epoch/atomic/trait.Pointable.html#tymethod.deref\">Read more</a>',
     '解引用给定的指针。<a href=\"../../crossbeam_epoch/atomic/trait.Pointable.html#tymethod.deref\">阅读更多</a>'),
    ('Mutably dereferences the given pointer. <a href=\"../../crossbeam_epoch/atomic/trait.Pointable.html#tymethod.deref_mut\">Read more</a>',
     '可变地解引用给定的指针。<a href=\"../../crossbeam_epoch/atomic/trait.Pointable.html#tymethod.deref_mut\">阅读更多</a>'),
    ('Drops the object pointed to by the given pointer. <a href=\"../../crossbeam_epoch/atomic/trait.Pointable.html#tymethod.drop\">Read more</a>',
     '释放给定指针所指向的对象。<a href=\"../../crossbeam_epoch/atomic/trait.Pointable.html#tymethod.drop\">阅读更多</a>'),
    ('The type returned in the event of a conversion error.', '转换失败时返回的类型。'),
    ('<p>Performs copy-assignment from <code>source</code>. <a href=\"https://doc.rust-lang.org/1.95.0/core/clone/trait.Clone.html#method.clone_from\">Read more</a></p>',
     '<p>从 <code>source</code> 执行复制赋值。<a href=\"https://doc.rust-lang.org/1.95.0/core/clone/trait.Clone.html#method.clone_from\">阅读更多</a></p>'),
    ('Performs copy-assignment from <code>self</code> to <code>dest</code>. <a href=\"https://doc.rust-lang.org/1.95.0/core/clone/trait.Clone.html#method.clone_from\">Read more</a>',
     '执行从 <code>self</code> 到 <code>dest</code> 的复制赋值。<a href=\"https://doc.rust-lang.org/1.95.0/core/clone/trait.Clone.html#method.clone_from\">阅读更多</a>'),
    ('Returns a duplicate of the value. <a href=\"https://doc.rust-lang.org/1.95.0/core/clone/trait.Clone.html#tymethod.clone\">Read more</a>',
     '返回值的副本。<a href=\"https://doc.rust-lang.org/1.95.0/core/clone/trait.Clone.html#tymethod.clone\">阅读更多</a>'),
    ('Creates owned data from borrowed data, usually by cloning. <a href=\"https://doc.rust-lang.org/1.95.0/core/clone/trait.ToOwned.html#tymethod.to_owned\">Read more</a>',
     '从借用数据创建拥有的数据，通常通过克隆实现。<a href=\"https://doc.rust-lang.org/1.95.0/core/clone/trait.ToOwned.html#tymethod.to_owned\">阅读更多</a>'),
    ('Uses borrowed data to replace owned data, usually by cloning. <a href=\"https://doc.rust-lang.org/1.95.0/core/clone/trait.ToOwned.html#tymethod.clone_into\">Read more</a>',
     '使用借用数据替换拥有的数据，通常通过克隆实现。<a href=\"https://doc.rust-lang.org/1.95.0/core/clone/trait.ToOwned.html#tymethod.clone_into\">阅读更多</a>'),
    ('Executes the destructor for this type. <a href=\"https://doc.rust-lang.org/1.95.0/core/ops/drop/trait.Drop.html#tymethod.drop\">Read more</a>',
     '为此类型执行析构函数。<a href=\"https://doc.rust-lang.org/1.95.0/core/ops/drop/trait.Drop.html#tymethod.drop\">阅读更多</a>'),
    ('Returns the default value for a type. <a href=\"https://doc.rust-lang.org/1.95.0/core/default/trait.Default.html#tymethod.default\">Read more</a>',
     '返回类型的默认值。<a href=\"https://doc.rust-lang.org/1.95.0/core/default/trait.Default.html#tymethod.default\">阅读更多</a>'),
    ('Converts this type into the (usually inferred) input type of a generic method. <a href=\"https://doc.rust-lang.org/1.95.0/core/convert/trait.Into.html#tymethod.into\">Read more</a>',
     '将此类型转换为泛型方法的（通常可推导的）输入类型。<a href=\"https://doc.rust-lang.org/1.95.0/core/convert/trait.Into.html#tymethod.into\">阅读更多</a>'),
]

# Error type translations
ERR_REPL = [
    ('Errors that can occur when encoding raw buffers into images via <a class="struct" href="struct.ImageEncoder.html" title="struct windows_capture::encoder::ImageEncoder"><code>ImageEncoder</code></a>.',
     '通过 <a class="struct" href="struct.ImageEncoder.html" title="struct windows_capture::encoder::ImageEncoder"><code>ImageEncoder</code></a> 将原始缓冲区编码为图像时可能发生的错误。'),
]

# File-specific more docblock content
FILE_SPECIFIC_REPL = [
    # ImageEncoder encode method - extended docblock
    ('when the source format is unsupported for image encoders (e.g., <a class="enum" href="../settings/enum.ColorFormat.html#variant.Rgba16F" title="variant windows_capture::settings::ColorFormat::Rgba16F">ColorFormat::Rgba16F</a>)',
     '当源格式不被图像编码器支持时（例如 <a class="enum" href="../settings/enum.ColorFormat.html#variant.Rgba16F" title="variant windows_capture::settings::ColorFormat::Rgba16F">ColorFormat::Rgba16F</a>）'),
    ('on integer conversion failures', '在整数转换失败时'),
    ('when Windows Imaging API calls fail', '当 Windows 图像 API 调用失败时'),

    # Error list prefixes
    ('on integer conversion failure', '在整数转换失败时'),

    # Default text content for builders
    ('Subtype: <a class="variant" href="enum.VideoSettingsSubType.html#variant.HEVC" title="variant windows_capture::encoder::VideoSettingsSubType::HEVC">VideoSettingsSubType::HEVC</a>',
     '子类型：<a class="variant" href="enum.VideoSettingsSubType.html#variant.HEVC" title="variant windows_capture::encoder::VideoSettingsSubType::HEVC">VideoSettingsSubType::HEVC</a>'),
    ('Bitrate: 15 Mbps', '比特率：15 Mbps'),
    ('60 fps', '60 fps'),
    ('1:1', '1:1'),
    ('Disabled: false', '已禁用：false'),

    ('Bitrate: 192 kbps', '比特率：192 kbps'),
    ('2 channels', '2 声道'),
    ('48 kHz', '48 kHz'),
    ('16 bits per sample', '每样本 16 位'),
    ('Subtype: <a class="variant" href="enum.AudioSettingsSubType.html#variant.AAC" title="variant windows_capture::encoder::AudioSettingsSubType::AAC">AudioSettingsSubType::AAC</a>',
     '子类型：<a class="variant" href="enum.AudioSettingsSubType.html#variant.AAC" title="variant windows_capture::encoder::AudioSettingsSubType::AAC">AudioSettingsSubType::AAC</a>'),

    # VideoEncoder direct3D source explanation
    ('For <a class="variant" href="enum.VideoEncoderSource.html#variant.DirectX" title="variant windows_capture::encoder::VideoEncoderSource::DirectX">VideoEncoderSource::DirectX</a>, the COM surface pointer is ref-counted; holding the pointer is sufficient. For <a class="variant" href="enum.VideoEncoderSource.html#variant.Buffer" title="variant windows_capture::encoder::VideoEncoderSource::Buffer">VideoEncoderSource::Buffer</a>, the encoder takes ownership of the bytes, allowing callers to return immediately.',
     '对于 <a class="variant" href="enum.VideoEncoderSource.html#variant.DirectX" title="variant windows_capture::encoder::VideoEncoderSource::DirectX">VideoEncoderSource::DirectX</a>，COM 表面指针采用引用计数；持有指针即可。对于 <a class="variant" href="enum.VideoEncoderSource.html#variant.Buffer" title="variant windows_capture::encoder::VideoEncoderSource::Buffer">VideoEncoderSource::Buffer</a>，编码器获取字节的所有权，允许调用者立即返回。'),

    # ImageEncoder example
    ('# <a href=\"struct.ImageEncoder.html#method.new\" title=\"method windows_capture::encoder::ImageEncoder::new\">Create a new</a> encoder that outputs PNG',
     '# <a href=\"struct.ImageEncoder.html#method.new\" title=\"method windows_capture::encoder::ImageEncoder::new\">创建一个新的</a>输出 PNG 的编码器'),

    # VideoEncoder method returns immediately
    ('Sends a video frame (DirectX). Returns immediately.',
     '发送一帧视频（DirectX）。立即返回。'),

    # Container SettingsBuilder Default subtype
    ('Default subtype: ', '默认子类型：'),
    ('Default dimensions: ', '默认尺寸：'),
    ('Default frame rate: ', '默认帧率：'),
    ('Default bitrate: ', '默认比特率：'),
    ('Default pixel aspect ratio: ', '默认像素宽高比：'),
    ('Default codec: ', '默认编解码器：'),
    ('Default disabled: ', '默认禁用：'),

    # Common sentences
    ('Use <a class="fn" href="struct.VideoEncoder.html#method.new" title="associated function windows_capture::encoder::VideoEncoder::new">VideoEncoder::new</a> for file output or <a class="fn" href="struct.VideoEncoder.html#method.new_from_stream" title="associated function windows_capture::encoder::VideoEncoder::new_from_stream">VideoEncoder::new_from_stream</a> for stream output. Push frames with <a class="fn" href="struct.VideoEncoder.html#method.send_frame" title="associated function windows_capture::encoder::VideoEncoder::send_frame">VideoEncoder::send_frame</a> or <a class="fn" href="struct.VideoEncoder.html#method.send_frame_buffer" title="associated function windows_capture::encoder::VideoEncoder::send_frame_buffer">VideoEncoder::send_frame_buffer</a>. Optionally push audio with <a class="fn" href="struct.VideoEncoder.html#method.send_audio_buffer" title="associated function windows_capture::encoder::VideoEncoder::send_audio_buffer">VideoEncoder::send_audio_buffer</a> or use <a class="fn" href="struct.VideoEncoder.html#method.send_frame_with_audio" title="associated function windows_capture::encoder::VideoEncoder::send_frame_with_audio">VideoEncoder::send_frame_with_audio</a>. Call <a class="fn" href="struct.VideoEncoder.html#method.finish" title="associated function windows_capture::encoder::VideoEncoder::finish">VideoEncoder::finish</a> to finalize the container.',
     '使用 <a class="fn" href="struct.VideoEncoder.html#method.new" title="associated function windows_capture::encoder::VideoEncoder::new">VideoEncoder::new</a> 进行文件输出，或使用 <a class="fn" href="struct.VideoEncoder.html#method.new_from_stream" title="associated function windows_capture::encoder::VideoEncoder::new_from_stream">VideoEncoder::new_from_stream</a> 进行流输出。使用 <a class="fn" href="struct.VideoEncoder.html#method.send_frame" title="associated function windows_capture::encoder::VideoEncoder::send_frame">VideoEncoder::send_frame</a> 或 <a class="fn" href="struct.VideoEncoder.html#method.send_frame_buffer" title="associated function windows_capture::encoder::VideoEncoder::send_frame_buffer">VideoEncoder::send_frame_buffer</a> 推送帧。可选地使用 <a class="fn" href="struct.VideoEncoder.html#method.send_audio_buffer" title="associated function windows_capture::encoder::VideoEncoder::send_audio_buffer">VideoEncoder::send_audio_buffer</a> 推送音频，或使用 <a class="fn" href="struct.VideoEncoder.html#method.send_frame_with_audio" title="associated function windows_capture::encoder::VideoEncoder::send_frame_with_audio">VideoEncoder::send_frame_with_audio</a>。调用 <a class="fn" href="struct.VideoEncoder.html#method.finish" title="associated function windows_capture::encoder::VideoEncoder::finish">VideoEncoder::finish</a> 完成容器。'),
]

# Master list - all replacements combined
ALL_REPLACEMENTS = [
    LANG_REPL,
    *UI_REPL,
    *STDLIB_REPL,
    *AUDIO_REPL,
    *CONTAINER_REPL,
    *PIXEL_FORMAT_REPL,
    *IMAGE_FORMAT_REPL,
    *VIDEO_ERR_REPL,
    *IMAGE_ERR_REPL,
    *VIDEO_SUBTYPE_REPL,
    *AUDIO_BUILDER_REPL,
    *CONTAINER_BUILDER_REPL,
    *IMAGE_ENCODER_REPL,
    *VIDEO_BUILDER_REPL,
    *SOURCE_REPL,
    *VIDEO_ENCODER_REPL,
    *GENERIC_REPL,
    *ERR_REPL,
    *FILE_SPECIFIC_REPL,
    *ADDITIONAL_REPL,
]


def translate_file(path: Path) -> tuple[int, int]:
    """Translate one file. Returns (num_replacements, num_untranslated_remaining)."""
    content = path.read_text(encoding='utf-8')
    original = content
    total_replacements = 0
    for old, new in ALL_REPLACEMENTS:
        if old in content:
            count = content.count(old)
            content = content.replace(old, new)
            total_replacements += count
    if content != original:
        path.write_text(content, encoding='utf-8')
    return total_replacements, content


def main():
    encoder_dir = Path('D:/Administrator/Documents/Code/rust_doc_all/windows_capture/encoder')
    target_files = sorted([f for f in encoder_dir.glob('*.html') if f.name != 'index.html'])
    print(f'Translating {len(target_files)} files...')
    grand_total = 0
    for f in target_files:
        n, _ = translate_file(f)
        grand_total += n
        print(f'  {f.name}: {n} replacements')
    print(f'Total: {grand_total} replacements')


if __name__ == '__main__':
    main()
