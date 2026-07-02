#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Translate remaining untranslated <p> docblocks in tokio/time/ HTML files to Chinese.
"""
import os

ROOT = r'D:\Administrator\Documents\Code\rust_doc_all'


def P(en, zh):
    return (en, zh)


# ============================================================================
# tokio/time/struct.Instant.html
# ============================================================================
INSTANT_PAIRS = [
    # TOP description
    P('<p>A measurement of a monotonically nondecreasing clock.\nOpaque and useful only with <code>Duration</code>.</p>',
      '<p>单调递增时钟的度量值。\n类型不透明，只能与 <code>Duration</code> 配合使用。</p>'),

    P('<p>Instants are always guaranteed to be no less than any previously measured\ninstant when created, and are often useful for tasks such as measuring\nbenchmarks or timing how long an operation takes.</p>',
      '<p>Instant 在创建时始终保证不小于任何先前已测量的 instant，常用于度量基准性能或计时某个操作所耗时长等任务。</p>'),

    P('<p>Note, however, that instants are not guaranteed to be <strong>steady</strong>. In other\nwords, each tick of the underlying clock may not be the same length (e.g.\nsome seconds may be longer than others). An instant may jump forwards or\nexperience time dilation (slow down or speed up), but it will never go\nbackwards.</p>',
      '<p>但请注意，instant 不保证是<strong>稳定</strong>的。换言之，底层时钟的每一跳长度可能并不相同（例如某些秒可能比其他秒更长）。一个 instant 可能会向前跳跃或发生时间膨胀（变慢或变快），但绝不会倒退。</p>'),

    P('<p>Instants are opaque types that can only be compared to one another. There is\nno method to get “the number of seconds” from an instant. Instead, it only\nallows measuring the duration between two instants (or comparing two\ninstants).</p>',
      '<p>Instant 是不透明类型，只能彼此之间进行比较。没有方法可以从 instant 中获取“秒数”。它仅允许度量两个 instant 之间的时长（或比较两个 instant）。</p>'),

    P('<p>The size of an <code>Instant</code> struct may vary depending on the target operating\nsystem.</p>',
      '<p><code>Instant</code> 结构体的大小可能因目标操作系统不同而有所不同。</p>'),

    P('<p>This type wraps the inner <code>std</code> variant and is used to align the Tokio\nclock for uses of <code>now()</code>. This can be useful for testing where you can\ntake advantage of <code>time::pause()</code> and <code>time::advance()</code>.</p>',
      '<p>此类型是对内部 <code>std</code> 类型的封装，用于对齐 Tokio 时钟以供 <code>now()</code> 调用。这在测试场景下非常有用，因为你可以使用 <code>time::pause()</code> 与 <code>time::advance()</code>。</p>'),

    # method.now
    P('<p>Returns an instant corresponding to “now”.</p>',
      '<p>返回对应“当前”时刻的 instant。</p>'),

    # method.from_std
    P('<p>Create a <code>tokio::time::Instant</code> from a <code>std::time::Instant</code>.</p>',
      '<p>从 <code>std::time::Instant</code> 创建一个 <code>tokio::time::Instant</code>。</p>'),

    # method.into_std
    P('<p>Convert the value into a <code>std::time::Instant</code>.</p>',
      '<p>将该值转换为 <code>std::time::Instant</code>。</p>'),

    # method.duration_since
    P('<p>Returns the amount of time elapsed from another instant to this one, or\nzero duration if that instant is later than this one.</p>',
      '<p>返回从另一 instant 到此 instant 之间所经过的时间，如果另一 instant 晚于此 instant，则返回零时长。</p>'),

    # method.checked_duration_since
    P('<p>Returns the amount of time elapsed from another instant to this one, or\nNone if that instant is later than this one.</p>',
      '<p>返回从另一 instant 到此 instant 之间所经过的时间，如果另一 instant 晚于此 instant，则返回 None。</p>'),

    # method.saturating_duration_since
    P('<p>Returns the amount of time elapsed from another instant to this one, or\nzero duration if that instant is later than this one.</p>',
      '<p>返回从另一 instant 到此 instant 之间所经过的时间，如果另一 instant 晚于此 instant，则返回零时长。</p>'),

    # method.elapsed
    P('<p>Returns the amount of time elapsed since this instant was created,\nor zero duration if this instant is in the future.</p>',
      '<p>返回自此 instant 创建以来所经过的时间，如果此 instant 处于未来，则返回零时长。</p>'),

    # method.checked_add
    P('<p>Returns <code>Some(t)</code> where <code>t</code> is the time <code>self + duration</code> if <code>t</code> can be\nrepresented as <code>Instant</code> (which means it’s inside the bounds of the\nunderlying data structure), <code>None</code> otherwise.</p>',
      '<p>如果 <code>t</code> 可以表示为 <code>Instant</code>（即它处于底层数据结构的表示范围内），则返回 <code>Some(t)</code>，其中 <code>t</code> 是时间 <code>self + duration</code>；否则返回 <code>None</code>。</p>'),

    # method.checked_sub
    P('<p>Returns <code>Some(t)</code> where <code>t</code> is the time <code>self - duration</code> if <code>t</code> can be\nrepresented as <code>Instant</code> (which means it’s inside the bounds of the\nunderlying data structure), <code>None</code> otherwise.</p>',
      '<p>如果 <code>t</code> 可以表示为 <code>Instant</code>（即它处于底层数据结构的表示范围内），则返回 <code>Some(t)</code>，其中 <code>t</code> 是时间 <code>self - duration</code>；否则返回 <code>None</code>。</p>'),

    # stdlib trait method docs (From / Into blanket impls)
    P('<p>Returns the argument unchanged.</p>',
      '<p>原样返回传入的参数。</p>'),

    P('<p>Calls <code>U::from(self)</code>.</p>',
      '<p>调用 <code>U::from(self)</code>。</p>'),

    P('<p>That is, this conversion is whatever the implementation of\n<code>From&lt;T&gt; for U</code> chooses to do.</p>',
      '<p>也就是说，此转换是 <code>From&lt;T&gt; for U</code> 的实现所选择的操作。</p>'),
]


# ============================================================================
# tokio/time/struct.Interval.html
# ============================================================================
INTERVAL_PAIRS = [
    # TOP description
    P('<p>Interval returned by <a href="fn.interval.html" title="fn tokio::time::interval"><code>interval</code></a> and <a href="fn.interval_at.html" title="fn tokio::time::interval_at"><code>interval_at</code></a>.</p>',
      '<p>由 <a href="fn.interval.html" title="fn tokio::time::interval"><code>interval</code></a> 与 <a href="fn.interval_at.html" title="fn tokio::time::interval_at"><code>interval_at</code></a> 返回的 Interval。</p>'),

    P('<p>This type allows you to wait on a sequence of instants with a certain\nduration between each instant. Unlike calling <a href="fn.sleep.html" title="fn tokio::time::sleep"><code>sleep</code></a> in a loop, this lets\nyou count the time spent between the calls to <a href="fn.sleep.html" title="fn tokio::time::sleep"><code>sleep</code></a> as well.</p>',
      '<p>此类型允许你等待一系列时间点，相邻时间点之间具有固定的时长。与在循环中调用 <a href="fn.sleep.html" title="fn tokio::time::sleep"><code>sleep</code></a> 不同，它还能统计两次 <a href="fn.sleep.html" title="fn tokio::time::sleep"><code>sleep</code></a> 调用之间所耗费的时间。</p>'),

    P('<p>An <code>Interval</code> can be turned into a <code>Stream</code> with <a href="https://docs.rs/tokio-stream/latest/tokio_stream/wrappers/struct.IntervalStream.html"><code>IntervalStream</code></a>.</p>',
      '<p>可以通过 <a href="https://docs.rs/tokio-stream/latest/tokio_stream/wrappers/struct.IntervalStream.html"><code>IntervalStream</code></a> 将 <code>Interval</code> 转换为 <code>Stream</code>。</p>'),

    # method.tick
    P('<p>Completes when the next instant in the interval has been reached.</p>',
      '<p>当间隔内的下一时间点到达时完成。</p>'),

    P('<p>This method is cancellation safe. If <code>tick</code> is used as the branch in a <code>tokio::select!</code> and\nanother branch completes first, then no tick has been consumed.</p>',
      '<p>此方法是 cancel safe 的。如果 <code>tick</code> 在 <code>tokio::select!</code> 中作为某个分支且其他分支先完成，则不会有 tick 被消耗。</p>'),

    # method.poll_tick
    P('<p>Polls for the next instant in the interval to be reached.</p>',
      '<p>轮询间隔内下一时间点的到达。</p>'),

    P('<p>This method can return the following values:</p>',
      '<p>此方法可以返回以下值：</p>'),

    P('<p>When this method returns <code>Poll::Pending</code>, the current task is scheduled\nto receive a wakeup when the instant has elapsed. Note that on multiple\ncalls to <code>poll_tick</code>, only the <a href="https://doc.rust-lang.org/1.95.0/core/task/wake/struct.Waker.html" title="struct core::task::wake::Waker"><code>Waker</code></a> from the\n<a href="https://doc.rust-lang.org/1.95.0/core/task/wake/struct.Context.html" title="struct core::task::wake::Context"><code>Context</code></a> passed to the most recent call is scheduled to receive a\nwakeup.</p>',
      '<p>当此方法返回 <code>Poll::Pending</code> 时，当前任务将被调度，以在该 instant 到达时接收 wakeup。请注意，多次调用 <code>poll_tick</code> 时，只有最近一次调用所传入的 <a href="https://doc.rust-lang.org/1.95.0/core/task/wake/struct.Context.html" title="struct core::task::wake::Context"><code>Context</code></a> 中的 <a href="https://doc.rust-lang.org/1.95.0/core/task/wake/struct.Waker.html" title="struct core::task::wake::Waker"><code>Waker</code></a> 会被调度接收 wakeup。</p>'),

    # method.reset
    P('<p>Resets the interval to complete one period after the current time.</p>',
      '<p>将间隔重置为从当前时间起一个 period 之后完成。</p>'),

    P('<p>This method ignores <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> strategy.</p>',
      '<p>此方法忽略 <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> 策略。</p>'),

    P('<p>This is equivalent to calling <code>reset_at(Instant::now() + period)</code>.</p>',
      '<p>这等效于调用 <code>reset_at(Instant::now() + period)</code>。</p>'),

    # method.reset_immediately
    P('<p>Resets the interval immediately.</p>',
      '<p>立即重置该间隔。</p>'),

    P('<p>This method ignores <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> strategy.</p>',
      '<p>此方法忽略 <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> 策略。</p>'),

    P('<p>This is equivalent to calling <code>reset_at(Instant::now())</code>.</p>',
      '<p>这等效于调用 <code>reset_at(Instant::now())</code>。</p>'),

    # method.reset_after
    P('<p>Resets the interval after the specified <a href="https://doc.rust-lang.org/1.95.0/core/time/struct.Duration.html" title="struct core::time::Duration"><code>std::time::Duration</code></a>.</p>',
      '<p>在指定的 <a href="https://doc.rust-lang.org/1.95.0/core/time/struct.Duration.html" title="struct core::time::Duration"><code>std::time::Duration</code></a> 之后重置该间隔。</p>'),

    P('<p>This method ignores <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> strategy.</p>',
      '<p>此方法忽略 <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> 策略。</p>'),

    P('<p>This is equivalent to calling <code>reset_at(Instant::now() + after)</code>.</p>',
      '<p>这等效于调用 <code>reset_at(Instant::now() + after)</code>。</p>'),

    # method.reset_at
    P('<p>Resets the interval to a <a href="struct.Instant.html" title="struct tokio::time::Instant"><code>crate::time::Instant</code></a> deadline.</p>',
      '<p>将该间隔重置为一个 <a href="struct.Instant.html" title="struct tokio::time::Instant"><code>crate::time::Instant</code></a> 截止时间。</p>'),

    P('<p>Sets the next tick to expire at the given instant. If the instant is in\nthe past, then the <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> strategy will be used to\ncatch up. If the instant is in the future, then the next tick will\ncomplete at the given instant, even if that means that it will sleep for\nlonger than the duration of this <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a>. If the <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> had\nany missed ticks before calling this method, then those are discarded.</p>',
      '<p>将下一个 tick 设置为在给定的 instant 到达时过期。如果该 instant 处于过去，则会使用 <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> 策略进行追赶。如果该 instant 处于未来，则下一个 tick 将在该 instant 完成，即使这意味着它将睡眠超过此 <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> 的 duration。如果在调用此方法之前该 <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> 已有任何错过的 tick，那些 tick 将被丢弃。</p>'),

    # method.missed_tick_behavior
    P('<p>Returns the <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> strategy currently being used.</p>',
      '<p>返回当前使用的 <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> 策略。</p>'),

    # method.set_missed_tick_behavior
    P('<p>Sets the <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> strategy that should be used.</p>',
      '<p>设置应使用的 <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> 策略。</p>'),

    # method.period
    P('<p>Returns the period of the interval.</p>',
      '<p>返回该间隔的 period。</p>'),

    # stdlib trait method docs (From / Into blanket impls)
    P('<p>Returns the argument unchanged.</p>',
      '<p>原样返回传入的参数。</p>'),

    P('<p>Calls <code>U::from(self)</code>.</p>',
      '<p>调用 <code>U::from(self)</code>。</p>'),

    P('<p>That is, this conversion is whatever the implementation of\n<code>From&lt;T&gt; for U</code> chooses to do.</p>',
      '<p>也就是说，此转换是 <code>From&lt;T&gt; for U</code> 的实现所选择的操作。</p>'),
]


# ============================================================================
# tokio/time/struct.Sleep.html
# ============================================================================
SLEEP_PAIRS = [
    P('<p>Future returned by <a href="fn.sleep.html" title="fn tokio::time::sleep"><code>sleep</code></a> and <a href="fn.sleep_until.html" title="fn tokio::time::sleep_until"><code>sleep_until</code></a>.</p>',
      '<p>由 <a href="fn.sleep.html" title="fn tokio::time::sleep"><code>sleep</code></a> 和 <a href="fn.sleep_until.html" title="fn tokio::time::sleep_until"><code>sleep_until</code></a> 返回的 Future。</p>'),

    P('<p>This type does not implement the <code>Unpin</code> trait, which means that if you\nuse it with <a href="../macro.select.html"><code>select!</code></a> or by calling <code>poll</code>, you have to pin it first.\nIf you use it with <code>.await</code>, this does not apply.</p>',
      '<p>此类型未实现 <code>Unpin</code> trait，这意味着如果将其与 <a href="../macro.select.html"><code>select!</code></a> 一起使用或通过调用 <code>poll</code>，则必须先将其 pin。如果使用 <code>.await</code>，则不存在此问题。</p>'),

    P('<p>Wait 100ms and print “100 ms have elapsed”.</p>',
      '<p>等待 100ms 并输出“已过去 100ms”。</p>'),

    # method.deadline
    P('<p>Returns the instant at which the future will complete.</p>',
      '<p>返回 future 将完成的 instant。</p>'),

    # method.is_elapsed
    P('<p>Returns <code>true</code> if <code>Sleep</code> has elapsed.</p>',
      '<p>如果 <code>Sleep</code> 已过期，则返回 <code>true</code>。</p>'),

    P('<p>A <code>Sleep</code> instance is elapsed when the requested duration has elapsed.</p>',
      '<p>当所请求的时长已过去时，<code>Sleep</code> 实例处于已过期状态。</p>'),

    # method.reset
    P('<p>Resets the <code>Sleep</code> instance to a new deadline.</p>',
      '<p>将该 <code>Sleep</code> 实例重置为一个新的截止时间。</p>'),

    P('<p>Calling this function allows changing the instant at which the <code>Sleep</code>\nfuture completes without having to create new associated state.</p>',
      '<p>调用此函数允许在不创建新的关联状态的情况下，更改 <code>Sleep</code> future 完成的 instant。</p>'),

    P('<p>This function can be called both before and after the future has\ncompleted.</p>',
      '<p>此函数可在 future 完成之前或之后调用。</p>'),

    P('<p>To call this method, you will usually combine the call with\n<a href="https://doc.rust-lang.org/1.95.0/core/pin/struct.Pin.html#method.as_mut" title="method core::pin::Pin::as_mut"><code>Pin::as_mut</code></a>, which lets you call the method without consuming the\n<code>Sleep</code> itself.</p>',
      '<p>要调用此方法，通常需要将调用与 <a href="https://doc.rust-lang.org/1.95.0/core/pin/struct.Pin.html#method.as_mut" title="method core::pin::Pin::as_mut"><code>Pin::as_mut</code></a> 结合使用，从而在不必消耗 <code>Sleep</code> 自身的前提下调用该方法。</p>'),

    P('<p>See also the top-level examples.</p>',
      '<p>另请参阅顶层示例。</p>'),
]


# ============================================================================
# tokio/time/struct.Timeout.html
# ============================================================================
TIMEOUT_PAIRS = [
    P('<p>Future returned by <a href="fn.timeout.html" title="fn tokio::time::timeout"><code>timeout</code></a> and <a href="fn.timeout_at.html" title="fn tokio::time::timeout_at"><code>timeout_at</code></a>.</p>',
      '<p>由 <a href="fn.timeout.html" title="fn tokio::time::timeout"><code>timeout</code></a> 和 <a href="fn.timeout_at.html" title="fn tokio::time::timeout_at"><code>timeout_at</code></a> 返回的 Future。</p>'),

    P('<p>Gets a reference to the underlying value in this timeout.</p>',
      '<p>获取此 timeout 中底层值的引用。</p>'),

    P('<p>Gets a mutable reference to the underlying value in this timeout.</p>',
      '<p>获取此 timeout 中底层值的可变引用。</p>'),

    P('<p>Consumes this timeout, returning the underlying value.</p>',
      '<p>消费此 timeout，返回底层值。</p>'),
]


# ============================================================================
# tokio/time/error/struct.Error.html
# ============================================================================
ERROR_PAIRS = [
    # TOP description
    P('<p>Errors encountered by the timer implementation.</p>',
      '<p>定时器实现所遇到的错误。</p>'),

    P('<p>Currently, there are two different errors that can occur:</p>',
      '<p>当前可能发生的错误有两种：</p>'),

    P('<p><code>shutdown</code> occurs when a timer operation is attempted, but the timer\ninstance has been dropped. In this case, the operation will never be able\nto complete and the <code>shutdown</code> error is returned. This is a permanent\nerror, i.e., once this error is observed, timer operations will never\nsucceed in the future.</p>',
      '<p><code>shutdown</code> 发生在尝试执行定时器操作，但定时器实例已被丢弃的情况下。此时该操作将永远无法完成，并返回 <code>shutdown</code> 错误。这是一个永久性错误，即一旦观察到该错误，将来定时器操作也永远不会成功。</p>'),

    P('<p><code>at_capacity</code> occurs when a timer operation is attempted, but the timer\ninstance is currently handling its maximum number of outstanding sleep instances.\nIn this case, the operation is not able to be performed at the current\nmoment, and <code>at_capacity</code> is returned. This is a transient error, i.e., at\nsome point in the future, if the operation is attempted again, it might\nsucceed. Callers that observe this error should attempt to <a href="https://en.wikipedia.org/wiki/Load_Shedding">shed load</a>. One\nway to do this would be dropping the future that issued the timer operation.</p>',
      '<p><code>at_capacity</code> 发生在尝试执行定时器操作，但定时器实例当前正在处理最大数量的未完成 sleep 实例的情况下。此时该操作在当前时刻无法执行，并返回 <code>at_capacity</code>。这是一个瞬态错误，即将来某一时刻如果再次尝试该操作，它可能会成功。观察到该错误的调用者应当尝试进行<a href="https://en.wikipedia.org/wiki/Load_Shedding">负载削减</a>。一种做法是丢弃发起该定时器操作的 future。</p>'),

    # method.shutdown
    P('<p>Creates an error representing a shutdown timer.</p>',
      '<p>创建一个表示定时器已关闭的错误。</p>'),

    # method.is_shutdown
    P('<p>Returns <code>true</code> if the error was caused by the timer being shutdown.</p>',
      '<p>如果错误是由定时器被关闭引起的，则返回 <code>true</code>。</p>'),

    # method.at_capacity
    P('<p>Creates an error representing a timer at capacity.</p>',
      '<p>创建一个表示定时器已满载的错误。</p>'),

    # method.is_at_capacity
    P('<p>Returns <code>true</code> if the error was caused by the timer being at capacity.</p>',
      '<p>如果错误是由定时器满载引起的，则返回 <code>true</code>。</p>'),

    # method.invalid
    P('<p>Creates an error representing a misconfigured timer.</p>',
      '<p>创建一个表示定时器配置错误的错误。</p>'),

    # method.is_invalid
    P('<p>Returns <code>true</code> if the error was caused by the timer being misconfigured.</p>',
      '<p>如果错误是由定时器配置错误引起的，则返回 <code>true</code>。</p>'),

    # stdlib trait method docs (From / Into blanket impls)
    P('<p>Returns the argument unchanged.</p>',
      '<p>原样返回传入的参数。</p>'),

    P('<p>Calls <code>U::from(self)</code>.</p>',
      '<p>调用 <code>U::from(self)</code>。</p>'),

    P('<p>That is, this conversion is whatever the implementation of\n<code>From&lt;T&gt; for U</code> chooses to do.</p>',
      '<p>也就是说，此转换是 <code>From&lt;T&gt; for U</code> 的实现所选择的操作。</p>'),
]


# ============================================================================
# tokio/time/enum.MissedTickBehavior.html
# ============================================================================
MISSEDTICKBEHAVIOR_PAIRS = [
    # TOP
    P('<p>Defines the behavior of an <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> when it misses a tick.</p>',
      '<p>当 <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> 错过一次 tick 时，定义其行为。</p>'),

    P('<p>Sometimes, an <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a>’s tick is missed. For example, consider the\nfollowing:</p>',
      '<p>有时，<a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> 的 tick 会被错过。例如，考虑以下情况：</p>'),

    # TOP: a tick is missed if too much time spent
    P('<p>Generally, a tick is missed if too much time is spent without calling\n<a href="struct.Interval.html#method.tick" title="method tokio::time::Interval::tick"><code>Interval::tick()</code></a>.</p>',
      '<p>通常，如果在调用 <a href="struct.Interval.html#method.tick" title="method tokio::time::Interval::tick"><code>Interval::tick()</code></a> 上花费过多时间，则会错过 tick。</p>'),

    # TOP: by default, Interval fires ticks as quickly as it can
    P('<p>By default, when a tick is missed, <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> fires ticks as quickly as it\ncan until it is “caught up” in time to where it should be.\n<code>MissedTickBehavior</code> can be used to specify a different behavior for\n<a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> to exhibit. Each variant represents a different strategy.</p>',
      '<p>默认情况下，当错过一次 tick 时，<a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> 会尽可能快地触发 tick，直到“追上”应有的时刻。可以使用 <code>MissedTickBehavior</code> 为 <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> 指定不同的行为。每个变体代表一种不同的策略。</p>'),

    # TOP: Note that because the executor cannot guarantee
    P('<p>Note that because the executor cannot guarantee exact precision with timers,\nthese strategies will only apply when the delay is greater than 5\nmilliseconds.</p>',
      '<p>请注意，由于 executor 无法保证定时器的精确性，这些策略仅在延迟大于 5 毫秒时适用。</p>'),

    # variant.Burst
    P('<p>Ticks as fast as possible until caught up.</p>',
      '<p>尽可能快地 tick 直到追上进度。</p>'),

    P('<p>When this strategy is used, <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> schedules ticks “normally” (the\nsame as it would have if the ticks hadn’t been delayed), which results\nin it firing ticks as fast as possible until it is caught up in time to\nwhere it should be. Unlike <a href="enum.MissedTickBehavior.html#variant.Delay" title="variant tokio::time::MissedTickBehavior::Delay"><code>Delay</code></a> and <a href="enum.MissedTickBehavior.html#variant.Skip" title="variant tokio::time::MissedTickBehavior::Skip"><code>Skip</code></a>, the ticks yielded\nwhen <code>Burst</code> is used (the <a href="struct.Instant.html" title="struct tokio::time::Instant"><code>Instant</code></a>s that <a href="struct.Interval.html#method.tick" title="method tokio::time::Interval::tick"><code>tick</code></a>\nyields) aren’t different than they would have been if a tick had not\nbeen missed. Like <a href="enum.MissedTickBehavior.html#variant.Skip" title="variant tokio::time::MissedTickBehavior::Skip"><code>Skip</code></a>, and unlike <a href="enum.MissedTickBehavior.html#variant.Delay" title="variant tokio::time::MissedTickBehavior::Delay"><code>Delay</code></a>, the ticks may be\nshortened.</p>',
      '<p>使用此策略时，<a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a>“正常地”调度 tick（与 tick 未被延迟时相同），这会导致其尽可能快地触发 tick，直到追赶上应有的时刻。与 <a href="enum.MissedTickBehavior.html#variant.Delay" title="variant tokio::time::MissedTickBehavior::Delay"><code>Delay</code></a> 和 <a href="enum.MissedTickBehavior.html#variant.Skip" title="variant tokio::time::MissedTickBehavior::Skip"><code>Skip</code></a> 不同，使用 <code>Burst</code> 时所产出的 tick（即 <a href="struct.Interval.html#method.tick" title="method tokio::time::Interval::tick"><code>tick</code></a> 产出的 <a href="struct.Instant.html" title="struct tokio::time::Instant"><code>Instant</code></a>）与没有错过 tick 时并无差异。与 <a href="enum.MissedTickBehavior.html#variant.Skip" title="variant tokio::time::MissedTickBehavior::Skip"><code>Skip</code></a> 类似，但不同于 <a href="enum.MissedTickBehavior.html#variant.Delay" title="variant tokio::time::MissedTickBehavior::Delay"><code>Delay</code></a>，tick 可能会被缩短。</p>'),

    P('<p>In code:</p>',
      '<p>用代码表示：</p>'),

    P('<p>This is the default behavior when <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> is created with\n<a href="fn.interval.html" title="fn tokio::time::interval"><code>interval</code></a> and <a href="fn.interval_at.html" title="fn tokio::time::interval_at"><code>interval_at</code></a>.</p>',
      '<p>这是使用 <a href="fn.interval.html" title="fn tokio::time::interval"><code>interval</code></a> 与 <a href="fn.interval_at.html" title="fn tokio::time::interval_at"><code>interval_at</code></a> 创建 <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> 时的默认行为。</p>'),

    # variant.Delay
    P('<p>Tick at multiples of <code>period</code> from when <a href="struct.Interval.html#method.tick" title="method tokio::time::Interval::tick"><code>tick</code></a> was called, rather than\nfrom <code>start</code>.</p>',
      '<p>从调用 <a href="struct.Interval.html#method.tick" title="method tokio::time::Interval::tick"><code>tick</code></a> 时起，按 <code>period</code> 的倍数进行 tick，而非从 <code>start</code> 起。</p>'),

    P('<p>When this strategy is used and <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> has missed a tick, instead\nof scheduling ticks to fire at multiples of <code>period</code> from <code>start</code> (the\ntime when the first tick was fired), it schedules all future ticks to\nhappen at a regular <code>period</code> from the point when <a href="struct.Interval.html#method.tick" title="method tokio::time::Interval::tick"><code>tick</code></a> was called.\nUnlike <a href="enum.MissedTickBehavior.html#variant.Burst" title="variant tokio::time::MissedTickBehavior::Burst"><code>Burst</code></a> and <a href="enum.MissedTickBehavior.html#variant.Skip" title="variant tokio::time::MissedTickBehavior::Skip"><code>Skip</code></a>, ticks are not shortened, and they aren’t\nguaranteed to happen at a multiple of <code>period</code> from <code>start</code> any longer.</p>',
      '<p>使用此策略时，如果 <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> 错过了一次 tick，则不再按从 <code>start</code>（首次 tick 的触发时刻）起的 <code>period</code> 倍数来调度 tick，而是将所有未来的 tick 调度在从调用 <a href="struct.Interval.html#method.tick" title="method tokio::time::Interval::tick"><code>tick</code></a> 时起以固定 <code>period</code> 间隔发生。与 <a href="enum.MissedTickBehavior.html#variant.Burst" title="variant tokio::time::MissedTickBehavior::Burst"><code>Burst</code></a> 和 <a href="enum.MissedTickBehavior.html#variant.Skip" title="variant tokio::time::MissedTickBehavior::Skip"><code>Skip</code></a> 不同，tick 不会被缩短，并且也不再保证发生在距 <code>start</code> 的 <code>period</code> 整数倍处。</p>'),

    P('<p>In code:</p>',
      '<p>用代码表示：</p>'),

    # variant.Skip
    P('<p>Skips missed ticks and tick on the next multiple of <code>period</code> from\n<code>start</code>.</p>',
      '<p>跳过错过的 tick，并按从 <code>start</code> 起下一个 <code>period</code> 倍数进行 tick。</p>'),

    P('<p>When this strategy is used, <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> schedules the next tick to fire\nat the next-closest tick that is a multiple of <code>period</code> away from\n<code>start</code> (the point where <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> first ticked). Like <a href="enum.MissedTickBehavior.html#variant.Burst" title="variant tokio::time::MissedTickBehavior::Burst"><code>Burst</code></a>, all\nticks remain multiples of <code>period</code> away from <code>start</code>, but unlike\n<a href="enum.MissedTickBehavior.html#variant.Burst" title="variant tokio::time::MissedTickBehavior::Burst"><code>Burst</code></a>, the ticks may not be <em>one</em> multiple of <code>period</code> away from the\nlast tick. Like <a href="enum.MissedTickBehavior.html#variant.Delay" title="variant tokio::time::MissedTickBehavior::Delay"><code>Delay</code></a>, the ticks are no longer the same as they\nwould have been if ticks had not been missed, but unlike <a href="enum.MissedTickBehavior.html#variant.Delay" title="variant tokio::time::MissedTickBehavior::Delay"><code>Delay</code></a>, and\nlike <a href="enum.MissedTickBehavior.html#variant.Burst" title="variant tokio::time::MissedTickBehavior::Burst"><code>Burst</code></a>, the ticks may be shortened to be less than one <code>period</code>\naway from each other.</p>',
      '<p>使用此策略时，<a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> 会将下一次 tick 调度为距离 <code>start</code>（<a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> 首次 tick 的时刻）最近的 <code>period</code> 整数倍。与 <a href="enum.MissedTickBehavior.html#variant.Burst" title="variant tokio::time::MissedTickBehavior::Burst"><code>Burst</code></a> 类似，所有 tick 仍保持是距 <code>start</code> 的 <code>period</code> 整数倍；但与 <a href="enum.MissedTickBehavior.html#variant.Burst" title="variant tokio::time::MissedTickBehavior::Burst"><code>Burst</code></a> 不同，tick 之间可能不是距上一 tick <em>恰好一个</em> <code>period</code> 的间隔。与 <a href="enum.MissedTickBehavior.html#variant.Delay" title="variant tokio::time::MissedTickBehavior::Delay"><code>Delay</code></a> 类似，这些 tick 已不再与未错过 tick 时相同；但与 <a href="enum.MissedTickBehavior.html#variant.Delay" title="variant tokio::time::MissedTickBehavior::Delay"><code>Delay</code></a> 不同，与 <a href="enum.MissedTickBehavior.html#variant.Burst" title="variant tokio::time::MissedTickBehavior::Burst"><code>Burst</code></a> 类似，tick 之间的间隔可能会缩短到小于一个 <code>period</code>。</p>'),

    P('<p>In code:</p>',
      '<p>用代码表示：</p>'),

    # method.default
    P('<p>Returns <a href="enum.MissedTickBehavior.html#variant.Burst" title="variant tokio::time::MissedTickBehavior::Burst"><code>MissedTickBehavior::Burst</code></a>.</p>',
      '<p>返回 <a href="enum.MissedTickBehavior.html#variant.Burst" title="variant tokio::time::MissedTickBehavior::Burst"><code>MissedTickBehavior::Burst</code></a>。</p>'),

    P('<p>For most usecases, the <a href="enum.MissedTickBehavior.html#variant.Burst" title="variant tokio::time::MissedTickBehavior::Burst"><code>Burst</code></a> strategy is what is desired.\nAdditionally, to preserve backwards compatibility, the <a href="enum.MissedTickBehavior.html#variant.Burst" title="variant tokio::time::MissedTickBehavior::Burst"><code>Burst</code></a>\nstrategy must be the default. For these reasons,\n<a href="enum.MissedTickBehavior.html#variant.Burst" title="variant tokio::time::MissedTickBehavior::Burst"><code>MissedTickBehavior::Burst</code></a> is the default for <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a>.\nSee <a href="enum.MissedTickBehavior.html#variant.Burst" title="variant tokio::time::MissedTickBehavior::Burst"><code>Burst</code></a> for more details.</p>',
      '<p>对于大多数用例，<a href="enum.MissedTickBehavior.html#variant.Burst" title="variant tokio::time::MissedTickBehavior::Burst"><code>Burst</code></a> 策略是所需的选择。此外，为了保持向后兼容性，<a href="enum.MissedTickBehavior.html#variant.Burst" title="variant tokio::time::MissedTickBehavior::Burst"><code>Burst</code></a> 策略必须是默认策略。基于这些原因，<a href="enum.MissedTickBehavior.html#variant.Burst" title="variant tokio::time::MissedTickBehavior::Burst"><code>MissedTickBehavior::Burst</code></a> 是 <a href="enum.MissedTickBehavior.html" title="enum tokio::time::MissedTickBehavior"><code>MissedTickBehavior</code></a> 的默认值。有关更多详细信息，请参阅 <a href="enum.MissedTickBehavior.html#variant.Burst" title="variant tokio::time::MissedTickBehavior::Burst"><code>Burst</code></a>。</p>'),
]


# ============================================================================
# tokio/time/index.html — module top-level
# ============================================================================
TIME_INDEX_PAIRS = [
    P('<p>Utilities for tracking time.</p>',
      '<p>用于跟踪时间的工具。</p>'),

    P('<p>This module provides a number of types for executing code after a set period\nof time.</p>',
      '<p>此模块提供多种类型，用于在一段指定时间之后执行代码。</p>'),

    P('<p><a href="fn.sleep.html" title="fn tokio::time::sleep"><code>Sleep</code></a> is a future that does no work and completes at a specific <a href="struct.Instant.html" title="struct tokio::time::Instant"><code>Instant</code></a>\nin time.</p>',
      '<p><a href="fn.sleep.html" title="fn tokio::time::sleep"><code>Sleep</code></a> 是一个不做任何工作的 future，它会在特定的 <a href="struct.Instant.html" title="struct tokio::time::Instant"><code>Instant</code></a> 时刻完成。</p>'),

    P('<p><a href="fn.interval.html" title="fn tokio::time::interval"><code>Interval</code></a> is a stream yielding a value at a fixed period. It is\ninitialized with a <a href="https://doc.rust-lang.org/1.95.0/core/time/struct.Duration.html" title="struct core::time::Duration"><code>Duration</code></a> and repeatedly yields each time the duration\nelapses.</p>',
      '<p><a href="fn.interval.html" title="fn tokio::time::interval"><code>Interval</code></a> 是一个以固定周期产生值的流。它由一个 <a href="https://doc.rust-lang.org/1.95.0/core/time/struct.Duration.html" title="struct core::time::Duration"><code>Duration</code></a> 初始化，并在每次时长到达时反复产生值。</p>'),

    P('<p><a href="struct.Timeout.html" title="struct tokio::time::Timeout"><code>Timeout</code></a>: Wraps a future or stream, setting an upper bound to the amount\nof time it is allowed to execute. If the future or stream does not\ncomplete in time, then it is canceled and an error is returned.</p>',
      '<p><a href="struct.Timeout.html" title="struct tokio::time::Timeout"><code>Timeout</code></a>：包装一个 future 或 stream，为其允许执行的时间设置上限。如果该 future 或 stream 未能在规定时间内完成，则会被取消并返回一个错误。</p>'),

    P('<p>These types are sufficient for handling a large number of scenarios\ninvolving time.</p>',
      '<p>这些类型足以处理涉及时间的大量场景。</p>'),

    P('<p>These types must be used from within the context of the <a href="../runtime/struct.Runtime.html" title="struct tokio::runtime::Runtime"><code>Runtime</code></a>.</p>',
      '<p>这些类型必须在 <a href="../runtime/struct.Runtime.html" title="struct tokio::runtime::Runtime"><code>Runtime</code></a> 的上下文中使用。</p>'),

    P('<p>Wait 100ms and print “100 ms have elapsed”</p>',
      '<p>等待 100ms 并输出“已过去 100ms”</p>'),

    # Module index entry descriptions (in <dd>)
    P('<p>Time error types.</p>',
      '<p>时间相关错误类型。</p>'),

    P('<p>A measurement of a monotonically nondecreasing clock.</p>',
      '<p>单调递增时钟的度量值。</p>'),

    P('<p>Interval returned by <a href="fn.interval.html" title="fn tokio::time::interval"><code>interval</code></a> and <a href="fn.interval_at.html" title="fn tokio::time::interval_at"><code>interval_at</code></a>.</p>',
      '<p>由 <a href="fn.interval.html" title="fn tokio::time::interval"><code>interval</code></a> 与 <a href="fn.interval_at.html" title="fn tokio::time::interval_at"><code>interval_at</code></a> 返回的 Interval。</p>'),

    P('<p>Future returned by <a href="fn.sleep.html" title="fn tokio::time::sleep"><code>sleep</code></a> and <a href="fn.sleep_until.html" title="fn tokio::time::sleep_until"><code>sleep_until</code></a>.</p>',
      '<p>由 <a href="fn.sleep.html" title="fn tokio::time::sleep"><code>sleep</code></a> 和 <a href="fn.sleep_until.html" title="fn tokio::time::sleep_until"><code>sleep_until</code></a> 返回的 Future。</p>'),

    P('<p>Future returned by <a href="fn.timeout.html" title="fn tokio::time::timeout"><code>timeout</code></a> and <a href="fn.timeout_at.html" title="fn tokio::time::timeout_at"><code>timeout_at</code></a>.</p>',
      '<p>由 <a href="fn.timeout.html" title="fn tokio::time::timeout"><code>timeout</code></a> 和 <a href="fn.timeout_at.html" title="fn tokio::time::timeout_at"><code>timeout_at</code></a> 返回的 Future。</p>'),

    P('<p>Defines the behavior of an <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> when it misses a tick.</p>',
      '<p>当 <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> 错过一次 tick 时，定义其行为。</p>'),

    P('<p>Creates new <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> that yields with interval of <code>period</code>. The first\ntick completes immediately.</p>',
      '<p>创建一个以 <code>period</code> 为间隔产生值的新 <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a>。第一个 tick 立即完成。</p>'),

    P('<p>Creates new <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a> that yields with interval of <code>period</code> with the\nfirst tick completing at <code>start</code>.</p>',
      '<p>创建一个以 <code>period</code> 为间隔产生值的新 <a href="struct.Interval.html" title="struct tokio::time::Interval"><code>Interval</code></a>，第一个 tick 在 <code>start</code> 时完成。</p>'),

    P('<p>Waits until <code>duration</code> has elapsed.</p>',
      '<p>等待 <code>duration</code> 时长过去。</p>'),

    P('<p>Waits until <code>deadline</code> is reached.</p>',
      '<p>等待直到 <code>deadline</code> 到达。</p>'),

    P('<p>Requires a <a href="https://doc.rust-lang.org/1.95.0/core/future/future/trait.Future.html" title="trait core::future::future::Future"><code>Future</code></a> to complete before the specified duration has elapsed.</p>',
      '<p>要求一个 <a href="https://doc.rust-lang.org/1.95.0/core/future/future/trait.Future.html" title="trait core::future::future::Future"><code>Future</code></a> 在指定时长过去之前完成。</p>'),

    P('<p>Requires a <a href="https://doc.rust-lang.org/1.95.0/core/future/future/trait.Future.html" title="trait core::future::future::Future"><code>Future</code></a> to complete before the specified instant in time.</p>',
      '<p>要求一个 <a href="https://doc.rust-lang.org/1.95.0/core/future/future/trait.Future.html" title="trait core::future::future::Future"><code>Future</code></a> 在指定时刻之前完成。</p>'),

    # "Require that an operation takes no more than 1s." (caption for example)
    P('<p>Require that an operation takes no more than 1s.</p>',
      '<p>要求一个操作耗时不超过 1 秒。</p>'),

    # "A simple example using interval to execute a task every two seconds."
    P('<p>A simple example using <a href="fn.interval.html" title="fn tokio::time::interval"><code>interval</code></a> to execute a task every two seconds.</p>',
      '<p>一个使用 <a href="fn.interval.html" title="fn tokio::time::interval"><code>interval</code></a> 每两秒执行一次任务的简单示例。</p>'),

    # Difference between interval and sleep
    P('<p>The difference between <a href="fn.interval.html" title="fn tokio::time::interval"><code>interval</code></a> and <a href="fn.sleep.html" title="fn tokio::time::sleep"><code>sleep</code></a> is that an <a href="fn.interval.html" title="fn tokio::time::interval"><code>interval</code></a>\nmeasures the time since the last tick, which means that <code>.tick().await</code> may\nwait for a shorter time than the duration specified for the interval\nif some time has passed between calls to <code>.tick().await</code>.</p>',
      '<p><a href="fn.interval.html" title="fn tokio::time::interval"><code>interval</code></a> 与 <a href="fn.sleep.html" title="fn tokio::time::sleep"><code>sleep</code></a> 的区别在于，<a href="fn.interval.html" title="fn tokio::time::interval"><code>interval</code></a> 度量的是自上一次 tick 起经过的时间，这意味着如果两次 <code>.tick().await</code> 调用之间已经过了一段时间，<code>.tick().await</code> 等待的时间可能比为此 interval 指定的 duration 更短。</p>'),

    # "If the tick in the example below was replaced with sleep..."
    P('<p>If the tick in the example below was replaced with <a href="fn.sleep.html" title="fn tokio::time::sleep"><code>sleep</code></a>, the task\nwould only be executed once every three seconds, and not every two\nseconds.</p>',
      '<p>如果将下方示例中的 tick 替换为 <a href="fn.sleep.html" title="fn tokio::time::sleep"><code>sleep</code></a>，那么该任务将每三秒执行一次，而不是每两秒执行一次。</p>'),
]


FILES = [
    ('tokio/time/struct.Instant.html', INSTANT_PAIRS),
    ('tokio/time/struct.Interval.html', INTERVAL_PAIRS),
    ('tokio/time/struct.Sleep.html', SLEEP_PAIRS),
    ('tokio/time/struct.Timeout.html', TIMEOUT_PAIRS),
    ('tokio/time/error/struct.Error.html', ERROR_PAIRS),
    ('tokio/time/enum.MissedTickBehavior.html', MISSEDTICKBEHAVIOR_PAIRS),
    ('tokio/time/index.html', TIME_INDEX_PAIRS),
]


def apply_pair(path, en_str, zh_str):
    """Apply a single (en, zh) pair to file. Returns True if replaced.

    Expands \\n to both LF and CRLF forms to match either line ending style.
    """
    en_bytes = en_str.encode('utf-8')
    zh_bytes = zh_str.encode('utf-8')
    with open(path, 'rb') as f:
        raw = f.read()
    if en_bytes in raw:
        new_raw = raw.replace(en_bytes, zh_bytes)
        with open(path, 'wb') as f:
            f.write(new_raw)
        return True
    if b'\n' in en_bytes:
        en_crlf = en_bytes.replace(b'\n', b'\r\n')
        if en_crlf in raw:
            new_raw = raw.replace(en_crlf, zh_bytes)
            with open(path, 'wb') as f:
                f.write(new_raw)
            return True
    return False


def main():
    total = 0
    for relpath, pairs in FILES:
        path = os.path.join(ROOT, relpath)
        applied = 0
        missing = []
        for en_str, zh_str in pairs:
            if apply_pair(path, en_str, zh_str):
                applied += 1
            else:
                missing.append((en_str, zh_str))
        total += applied
        print(f'{relpath}: {applied}/{len(pairs)} applied')
        if missing:
            print(f'  MISSING ({len(missing)}):')
            for en, zh in missing[:5]:
                print(f'    EN: {en[:100]!r}')
                print(f'    ZH: {zh[:60]!r}')
    print(f'\nTotal applied: {total}')


if __name__ == '__main__':
    main()