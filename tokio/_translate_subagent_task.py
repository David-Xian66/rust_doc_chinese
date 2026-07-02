#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Translate remaining untranslated <p> docblocks in tokio/task/ HTML files to Chinese.

Pairs are stored as (en_str, zh_str) regular strings; encoded to UTF-8 bytes at runtime.
"""
import os

ROOT = r'D:\Administrator\Documents\Code\rust_doc_all'


def P(en, zh):
    """Helper: pair of (en_str, zh_str) regular strings."""
    return (en, zh)


# ============================================================================
# tokio/task/struct.JoinSet.html — largest file, ~45 methods
# ============================================================================
JOINSET_PAIRS = [
    # ---- TOP description ----
    P('<p>A collection of tasks spawned on a Tokio runtime.</p>',
      '<p>在 Tokio runtime 上生成的若干任务的集合。</p>'),

    P('<p>A <code>JoinSet</code> can be used to await the completion of some or all of the tasks\nin the set. The set is not ordered, and the tasks will be returned in the\norder they complete.</p>',
      '<p><code>JoinSet</code> 可用于等待集合中部分或全部任务的完成。该集合是无序的，任务将按照完成的顺序返回。</p>'),

    P('<p>All of the tasks must have the same return type <code>T</code>.</p>',
      '<p>所有任务必须具有相同的返回类型 <code>T</code>。</p>'),

    P('<p>When the <code>JoinSet</code> is dropped, all tasks in the <code>JoinSet</code> are immediately aborted.</p>',
      '<p>当 <code>JoinSet</code> 被丢弃时，<code>JoinSet</code> 中的所有任务会立即被终止。</p>'),

    P('<p>Spawn multiple tasks and wait for them.</p>',
      '<p>派生多个任务并等待它们完成。</p>'),

    # ---- method.new ----
    P('<p>Create a new <code>JoinSet</code>.</p>',
      '<p>创建一个新的 <code>JoinSet</code>。</p>'),

    # ---- method.len ----
    P('<p>Returns the number of tasks currently in the <code>JoinSet</code>.</p>',
      '<p>返回当前 <code>JoinSet</code> 中的任务数量。</p>'),

    # ---- method.is_empty ----
    P('<p>Returns whether the <code>JoinSet</code> is empty.</p>',
      '<p>返回 <code>JoinSet</code> 是否为空。</p>'),

    # ---- method.spawn ----
    P('<p>Spawn the provided task on the <code>JoinSet</code>, returning an <a href="struct.AbortHandle.html" title="struct tokio::task::AbortHandle"><code>AbortHandle</code></a>\nthat can be used to remotely cancel the task.</p>',
      '<p>将提供的任务派生到 <code>JoinSet</code> 上，返回一个 <a href="struct.AbortHandle.html" title="struct tokio::task::AbortHandle"><code>AbortHandle</code></a>，可用于远程取消该任务。</p>'),

    P('<p>The provided future will start running in the background immediately\nwhen this method is called, even if you don’t await anything on this\n<code>JoinSet</code>.</p>',
      '<p>提供的 future 会在调用此方法时立即开始在后台运行，即使你没有在该 <code>JoinSet</code> 上 await 任何东西。</p>'),

    P('<p>This method panics if called outside of a Tokio runtime.</p>',
      '<p>如果在 Tokio runtime 之外调用此方法会 panic。</p>'),

    # ---- method.spawn_on ----
    P('<p>Spawn the provided task on the provided runtime and store it in this\n<code>JoinSet</code> returning an <a href="struct.AbortHandle.html" title="struct tokio::task::AbortHandle"><code>AbortHandle</code></a> that can be used to remotely\ncancel the task.</p>',
      '<p>将提供的任务派生到给定的 runtime 上并存储到此 <code>JoinSet</code>，返回一个 <a href="struct.AbortHandle.html" title="struct tokio::task::AbortHandle"><code>AbortHandle</code></a>，可用于远程取消该任务。</p>'),

    # ---- method.spawn_local ----
    P('<p>Spawn the provided task on the current <a href="struct.LocalSet.html" title="struct tokio::task::LocalSet"><code>LocalSet</code></a> or <a href="../runtime/struct.LocalRuntime.html" title="struct tokio::runtime::LocalRuntime"><code>LocalRuntime</code></a>\nand store it in this <code>JoinSet</code>, returning an <a href="struct.AbortHandle.html" title="struct tokio::task::AbortHandle"><code>AbortHandle</code></a> that can\nbe used to remotely cancel the task.</p>',
      '<p>将提供的任务派生到当前 <a href="struct.LocalSet.html" title="struct tokio::task::LocalSet"><code>LocalSet</code></a> 或 <a href="../runtime/struct.LocalRuntime.html" title="struct tokio::runtime::LocalRuntime"><code>LocalRuntime</code></a> 上并存储到此 <code>JoinSet</code>，返回一个 <a href="struct.AbortHandle.html" title="struct tokio::task::AbortHandle"><code>AbortHandle</code></a>，可用于远程取消该任务。</p>'),

    P('<p>This method panics if it is called outside of a <code>LocalSet</code> or <code>LocalRuntime</code>.</p>',
      '<p>如果在 <code>LocalSet</code> 或 <code>LocalRuntime</code> 之外调用此方法会 panic。</p>'),

    # ---- method.spawn_local_on ----
    P('<p>Spawn the provided task on the provided <a href="struct.LocalSet.html" title="struct tokio::task::LocalSet"><code>LocalSet</code></a> and store it in\nthis <code>JoinSet</code>, returning an <a href="struct.AbortHandle.html" title="struct tokio::task::AbortHandle"><code>AbortHandle</code></a> that can be used to\nremotely cancel the task.</p>',
      '<p>将提供的任务派生到给定的 <a href="struct.LocalSet.html" title="struct tokio::task::LocalSet"><code>LocalSet</code></a> 上并存储到此 <code>JoinSet</code>，返回一个 <a href="struct.AbortHandle.html" title="struct tokio::task::AbortHandle"><code>AbortHandle</code></a>，可用于远程取消该任务。</p>'),

    P('<p>Unlike the <a href="struct.JoinSet.html#method.spawn_local" title="method tokio::task::JoinSet::spawn_local"><code>spawn_local</code></a> method, this method may be used to spawn local\ntasks on a <code>LocalSet</code> that is <em>not</em> currently running. The provided\nfuture will start running whenever the <code>LocalSet</code> is next started.</p>',
      '<p>与 <a href="struct.JoinSet.html#method.spawn_local" title="method tokio::task::JoinSet::spawn_local"><code>spawn_local</code></a> 方法不同，此方法可用于在当前<em>没有</em>运行的 <code>LocalSet</code> 上派生本地任务。提供的 future 将在 <code>LocalSet</code> 下次启动时开始运行。</p>'),

    # ---- method.spawn_blocking ----
    P('<p>Spawn the blocking code on the blocking threadpool and store\nit in this <code>JoinSet</code>, returning an <a href="struct.AbortHandle.html" title="struct tokio::task::AbortHandle"><code>AbortHandle</code></a> that can be\nused to remotely cancel the task.</p>',
      '<p>将阻塞代码派生到阻塞线程池并存储到此 <code>JoinSet</code>，返回一个 <a href="struct.AbortHandle.html" title="struct tokio::task::AbortHandle"><code>AbortHandle</code></a>，可用于远程取消该任务。</p>'),

    # ---- method.spawn_blocking_on ----
    P('<p>Spawn the blocking code on the blocking threadpool of the\nprovided runtime and store it in this <code>JoinSet</code>, returning an\n<a href="struct.AbortHandle.html" title="struct tokio::task::AbortHandle"><code>AbortHandle</code></a> that can be used to remotely cancel the task.</p>',
      '<p>将阻塞代码派生到给定 runtime 的阻塞线程池上并存储到此 <code>JoinSet</code>，返回一个 <a href="struct.AbortHandle.html" title="struct tokio::task::AbortHandle"><code>AbortHandle</code></a>，可用于远程取消该任务。</p>'),

    # ---- method.join_next ----
    P('<p>Waits until one of the tasks in the set completes and returns its output.</p>',
      '<p>等待集合中的某个任务完成，并返回其输出。</p>'),

    P('<p>Returns <code>None</code> if the set is empty.</p>',
      '<p>如果集合为空则返回 <code>None</code>。</p>'),

    P('<p>This method is cancel safe. If <code>join_next</code> is used as the event in a <code>tokio::select!</code>\nstatement and some other branch completes first, it is guaranteed that no tasks were\nremoved from this <code>JoinSet</code>.</p>',
      '<p>此方法是 cancel safe 的。如果 <code>join_next</code> 在 <code>tokio::select!</code> 语句中作为事件且其他分支先完成，可以保证不会有任务从此 <code>JoinSet</code> 中被移除。</p>'),

    # ---- method.join_next_with_id ----
    P('<p>Waits until one of the tasks in the set completes and returns its\noutput, along with the <a href="struct.Id.html" title="struct tokio::task::Id">task ID</a> of the completed task.</p>',
      '<p>等待集合中的某个任务完成，并返回其输出以及完成任务对应的 <a href="struct.Id.html" title="struct tokio::task::Id">task ID</a>。</p>'),

    P('<p>When this method returns an error, then the id of the task that failed can be accessed\nusing the <a href="struct.JoinError.html#method.id" title="method tokio::task::JoinError::id"><code>JoinError::id</code></a> method.</p>',
      '<p>当此方法返回错误时，可通过 <a href="struct.JoinError.html#method.id" title="method tokio::task::JoinError::id"><code>JoinError::id</code></a> 方法访问失败任务的 ID。</p>'),

    P('<p>This method is cancel safe. If <code>join_next_with_id</code> is used as the event in a <code>tokio::select!</code>\nstatement and some other branch completes first, it is guaranteed that no tasks were\nremoved from this <code>JoinSet</code>.</p>',
      '<p>此方法是 cancel safe 的。如果 <code>join_next_with_id</code> 在 <code>tokio::select!</code> 语句中作为事件且其他分支先完成，可以保证不会有任务从此 <code>JoinSet</code> 中被移除。</p>'),

    # ---- method.try_join_next ----
    P('<p>Tries to join one of the tasks in the set that has completed and return its output.</p>',
      '<p>尝试加入集合中已完成的任务之一，并返回其输出。</p>'),

    P('<p>Returns <code>None</code> if there are no completed tasks, or if the set is empty.</p>',
      '<p>如果没有已完成的任务，或集合为空，则返回 <code>None</code>。</p>'),

    # ---- method.try_join_next_with_id ----
    P('<p>Tries to join one of the tasks in the set that has completed and return its output,\nalong with the <a href="struct.Id.html" title="struct tokio::task::Id">task ID</a> of the completed task.</p>',
      '<p>尝试加入集合中已完成的任务之一，返回其输出以及完成任务对应的 <a href="struct.Id.html" title="struct tokio::task::Id">task ID</a>。</p>'),

    # ---- method.shutdown ----
    P('<p>Aborts all tasks and waits for them to finish shutting down.</p>',
      '<p>终止所有任务，并等待它们完成关闭。</p>'),

    P('<p>Calling this method is equivalent to calling <a href="struct.JoinSet.html#method.abort_all" title="method tokio::task::JoinSet::abort_all"><code>abort_all</code></a> and then calling <a href="struct.JoinSet.html#method.join_next" title="method tokio::task::JoinSet::join_next"><code>join_next</code></a> in\na loop until it returns <code>None</code>.</p>',
      '<p>调用此方法等价于先调用 <a href="struct.JoinSet.html#method.abort_all" title="method tokio::task::JoinSet::abort_all"><code>abort_all</code></a>，然后循环调用 <a href="struct.JoinSet.html#method.join_next" title="method tokio::task::JoinSet::join_next"><code>join_next</code></a> 直到它返回 <code>None</code>。</p>'),

    P('<p>This method ignores any panics in the tasks shutting down. When this call returns, the\n<code>JoinSet</code> will be empty.</p>',
      '<p>此方法会忽略正在关闭的任务中的任何 panic。当此调用返回时，<code>JoinSet</code> 将为空。</p>'),

    # ---- method.join_all ----
    P('<p>Awaits the completion of all tasks in this <code>JoinSet</code>, returning a vector of their results.</p>',
      '<p>等待此 <code>JoinSet</code> 中所有任务完成，返回一个包含其结果的 vector。</p>'),

    P('<p>The results will be stored in the order they completed not the order they were spawned.\nThis is a convenience method that is equivalent to calling <a href="struct.JoinSet.html#method.join_next" title="method tokio::task::JoinSet::join_next"><code>join_next</code></a> in\na loop. If any tasks on the <code>JoinSet</code> fail with an <a href="struct.JoinError.html" title="struct tokio::task::JoinError"><code>JoinError</code></a>, this method\nwill return that error.</p>',
      '<p>结果将按照任务完成的顺序（而非派生的顺序）存储。这是一个便捷方法，等价于循环调用 <a href="struct.JoinSet.html#method.join_next" title="method tokio::task::JoinSet::join_next"><code>join_next</code></a>。如果 <code>JoinSet</code> 上的任何任务因 <a href="struct.JoinError.html" title="struct tokio::task::JoinError"><code>JoinError</code></a> 而失败，此方法将返回该错误。</p>'),

    # ---- method.abort_all ----
    P('<p>Aborts all tasks on this <code>JoinSet</code>.</p>',
      '<p>终止此 <code>JoinSet</code> 上的所有任务。</p>'),

    P('<p>This does not remove the tasks from the <code>JoinSet</code>. To wait for the tasks to complete\ncancellation, you should call <code>join_next</code> in a loop until the <code>JoinSet</code> is empty.</p>',
      '<p>这不会从 <code>JoinSet</code> 中移除任务。要等待任务完成取消，你应该循环调用 <code>join_next</code>，直到 <code>JoinSet</code> 为空。</p>'),

    # ---- method.detach_all ----
    P('<p>Removes all tasks from this <code>JoinSet</code> without aborting them.</p>',
      '<p>从 <code>JoinSet</code> 中移除所有任务而不终止它们。</p>'),

    P('<p>The tasks removed by this call will continue to run in the background even if the <code>JoinSet</code>\nis dropped.</p>',
      '<p>被此调用移除的任务将在后台继续运行，即使 <code>JoinSet</code> 被丢弃。</p>'),

    # ---- method.poll_join_next ----
    P('<p>Polls for one of the tasks in the set to complete.</p>',
      '<p>轮询集合中是否有任务完成。</p>'),

    P('<p>If this returns <code>Poll::Ready(Some(_))</code>, then the task that completed is removed from the set.</p>',
      '<p>如果返回 <code>Poll::Ready(Some(_))</code>，则已完成的任务将从集合中移除。</p>'),

    P('<p>When the method returns <code>Poll::Pending</code>, the <code>Waker</code> in the provided <code>Context</code> is scheduled\nto receive a wakeup when a task in the <code>JoinSet</code> completes. Note that on multiple calls to\n<code>poll_join_next</code>, only the <code>Waker</code> from the <code>Context</code> passed to the most recent call is\nscheduled to receive a wakeup.</p>',
      '<p>当方法返回 <code>Poll::Pending</code> 时，提供的 <code>Context</code> 中的 <code>Waker</code> 将被调度以在 <code>JoinSet</code> 中的任务完成时接收 wakeup。请注意，多次调用 <code>poll_join_next</code> 时，只有最近一次调用所传入 <code>Context</code> 中的 <code>Waker</code> 会被调度接收 wakeup。</p>'),

    P('<p>This function returns:</p>',
      '<p>此函数返回：</p>'),

    P('<p>Note that this method may return <code>Poll::Pending</code> even if one of the tasks has completed.\nThis can happen if the <a href="coop/index.html#cooperative-scheduling" title="mod tokio::task::coop">coop budget</a> is reached.</p>',
      '<p>请注意，即使已有任务完成，此方法也可能返回 <code>Poll::Pending</code>。当达到 <a href="coop/index.html#cooperative-scheduling" title="mod tokio::task::coop">协作预算</a> 上限时，就会发生这种情况。</p>'),

    # ---- method.drop / Extend ----
    P('<p>Extend a <a href="struct.JoinSet.html" title="struct tokio::task::JoinSet"><code>JoinSet</code></a> with futures from an iterator.</p>',
      '<p>使用来自迭代器的 future 扩展 <a href="struct.JoinSet.html" title="struct tokio::task::JoinSet"><code>JoinSet</code></a>。</p>'),

    P('<p>This is equivalent to calling <a href="struct.JoinSet.html#method.spawn" title="method tokio::task::JoinSet::spawn"><code>JoinSet::spawn</code></a> on each element of the iterator.</p>',
      '<p>这等效于对迭代器中的每个元素调用 <a href="struct.JoinSet.html#method.spawn" title="method tokio::task::JoinSet::spawn"><code>JoinSet::spawn</code></a>。</p>'),

    # ---- method.extend_reserve (note: docblock uses extend's docblock + FromIterator doc) ----
    P('<p>Collect an iterator of futures into a <a href="struct.JoinSet.html" title="struct tokio::task::JoinSet"><code>JoinSet</code></a>.</p>',
      '<p>将 future 迭代器收集到 <a href="struct.JoinSet.html" title="struct tokio::task::JoinSet"><code>JoinSet</code></a> 中。</p>'),

    P('<p>The main example from <a href="struct.JoinSet.html" title="struct tokio::task::JoinSet"><code>JoinSet</code></a>’s documentation can also be written using <a href="https://doc.rust-lang.org/1.95.0/core/iter/traits/iterator/trait.Iterator.html#method.collect" title="method core::iter::traits::iterator::Iterator::collect"><code>collect</code></a>:',
      '<p><a href="struct.JoinSet.html" title="struct tokio::task::JoinSet"><code>JoinSet</code></a> 文档中的主要示例也可以使用 <a href="https://doc.rust-lang.org/1.95.0/core/iter/traits/iterator/trait.Iterator.html#method.collect" title="method core::iter::traits::iterator::Iterator::collect"><code>collect</code></a> 来编写：'),

    # Additional JoinSet TOP and join_all patterns
    P('<p>While a task is tracked in a <code>JoinSet</code>, that task’s ID is unique relative\nto all other running tasks in Tokio. For this purpose, tracking a task in a\n<code>JoinSet</code> is equivalent to holding a <a href="struct.JoinHandle.html" title="struct tokio::task::JoinHandle"><code>JoinHandle</code></a> to it. See the <a href="struct.Id.html" title="struct tokio::task::Id">task ID</a>\ndocumentation for more info.</p>',
      '<p>当一个任务被追踪到 <code>JoinSet</code> 中时，其 ID 在 Tokio 的所有其他运行任务中是唯一的。就此目的而言，将任务追踪到 <code>JoinSet</code> 中等价于持有该任务的 <a href="struct.JoinHandle.html" title="struct tokio::task::JoinHandle"><code>JoinHandle</code></a>。有关更多信息，请参阅 <a href="struct.Id.html" title="struct tokio::task::Id">task ID</a> 文档。</p>'),

    P('<p>Spawn multiple blocking tasks and wait for them.</p>',
      '<p>派生多个阻塞任务并等待它们完成。</p>'),

    P('<p>The results will be stored in the order they completed not the order they were spawned.\nThis is a convenience method that is equivalent to calling <a href="struct.JoinSet.html#method.join_next" title="method tokio::task::JoinSet::join_next"><code>join_next</code></a> in\na loop. If any tasks on the <code>JoinSet</code> fail with an <a href="struct.JoinError.html" title="struct tokio::task::JoinError"><code>JoinError</code></a>, then this call\nto <code>join_all</code> will panic and all remaining tasks on the <code>JoinSet</code> are\ncancelled. To handle errors in any other way, manually call <a href="struct.JoinSet.html#method.join_next" title="method tokio::task::JoinSet::join_next"><code>join_next</code></a>\nin a loop.</p>',
      '<p>结果将按照任务完成的顺序（而非派生的顺序）存储。这是一个便捷方法，等价于循环调用 <a href="struct.JoinSet.html#method.join_next" title="method tokio::task::JoinSet::join_next"><code>join_next</code></a>。如果 <code>JoinSet</code> 上的任何任务因 <a href="struct.JoinError.html" title="struct tokio::task::JoinError"><code>JoinError</code></a> 而失败，那么对 <code>join_all</code> 的此次调用将 panic，并且 <code>JoinSet</code> 上所有剩余的任务都将被取消。若要以其他方式处理错误，请手动循环调用 <a href="struct.JoinSet.html#method.join_next" title="method tokio::task::JoinSet::join_next"><code>join_next</code></a>。</p>'),

    P('<p>Spawn multiple tasks and <code>join_all</code> them.</p>',
      '<p>派生多个任务并对它们调用 <code>join_all</code>。</p>'),

    P('<p>Equivalent implementation of <code>join_all</code>, using <a href="struct.JoinSet.html#method.join_next" title="method tokio::task::JoinSet::join_next"><code>join_next</code></a> and loop.</p>',
      '<p>使用 <a href="struct.JoinSet.html#method.join_next" title="method tokio::task::JoinSet::join_next"><code>join_next</code></a> 和循环实现等效的 <code>join_all</code>。</p>'),
]


# ============================================================================
# tokio/task/struct.AbortHandle.html
# ============================================================================
ABORTHANDLE_PAIRS = [
    # TOP description
    P('<p>An owned permission to abort a spawned task, without awaiting its completion.</p>',
      '<p>用于终止已派生任务的 owned 权限，不会等待任务完成。</p>'),

    P('<p>Unlike a <a href="struct.JoinHandle.html" title="struct tokio::task::JoinHandle"><code>JoinHandle</code></a>, an <code>AbortHandle</code> does <em>not</em> represent the\npermission to await the task’s completion, only to terminate it.</p>',
      '<p>与 <a href="struct.JoinHandle.html" title="struct tokio::task::JoinHandle"><code>JoinHandle</code></a> 不同，<code>AbortHandle</code> <em>并不</em>代表等待任务完成的权限，它只代表终止任务的权限。</p>'),

    P('<p>The task may be aborted by calling the <a href="struct.AbortHandle.html#method.abort" title="method tokio::task::AbortHandle::abort"><code>AbortHandle::abort</code></a> method.\nDropping an <code>AbortHandle</code> releases the permission to terminate the task\n— it does <em>not</em> abort the task.</p>',
      '<p>可以通过调用 <a href="struct.AbortHandle.html#method.abort" title="method tokio::task::AbortHandle::abort"><code>AbortHandle::abort</code></a> 方法来终止任务。\n丢弃 <code>AbortHandle</code> 会释放终止任务的权限—它<em>不会</em>终止任务。</p>'),

    P('<p>Be aware that tasks spawned using <a href="fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> cannot be aborted\nbecause they are not async. If you call <code>abort</code> on a <code>spawn_blocking</code> task,\nthen this <em>will not have any effect</em>, and the task will continue running\nnormally. The exception is if the task has not started running yet; in that\ncase, calling <code>abort</code> may prevent the task from starting.</p>',
      '<p>请注意，使用 <a href="fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> 派生的任务无法被终止，因为它们不是异步的。如果你对 <code>spawn_blocking</code> 任务调用 <code>abort</code>，则<em>不会产生任何效果</em>，任务将继续正常运行。例外情况是该任务尚未开始运行；此时调用 <code>abort</code> 可能会阻止该任务启动。</p>'),

    # method.abort
    P('<p>Abort the task associated with the handle.</p>',
      '<p>终止与此 handle 关联的任务。</p>'),

    P('<p>Awaiting a cancelled task might complete as usual if the task was\nalready completed at the time it was cancelled, but most likely it\nwill fail with a <a href="struct.JoinError.html#method.is_cancelled" title="method tokio::task::JoinError::is_cancelled">cancelled</a> <code>JoinError</code>.</p>',
      '<p>等待一个被取消的任务，如果该任务在被取消时已经完成，则可能会正常完成；但大多数情况下，它会因 <a href="struct.JoinError.html#method.is_cancelled" title="method tokio::task::JoinError::is_cancelled">取消</a> 而失败并返回 <code>JoinError</code>。</p>'),

    P('<p>If the task was already cancelled, such as by <a href="struct.JoinHandle.html#method.abort" title="method tokio::task::JoinHandle::abort"><code>JoinHandle::abort</code></a>,\nthis method will do nothing.</p>',
      '<p>如果任务已被取消（例如通过 <a href="struct.JoinHandle.html#method.abort" title="method tokio::task::JoinHandle::abort"><code>JoinHandle::abort</code></a>），则此方法不会做任何事。</p>'),

    P('<p>Be aware that tasks spawned using <a href="fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> cannot be aborted\nbecause they are not async. If you call <code>abort</code> on a <code>spawn_blocking</code>\ntask, then this <em>will not have any effect</em>, and the task will continue\nrunning normally. The exception is if the task has not started running\nyet; in that case, calling <code>abort</code> may prevent the task from starting.</p>',
      '<p>请注意，使用 <a href="fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> 派生的任务无法被终止，因为它们不是异步的。如果你对 <code>spawn_blocking</code> 任务调用 <code>abort</code>，则<em>不会产生任何效果</em>，任务将继续正常运行。例外情况是该任务尚未开始运行；此时调用 <code>abort</code> 可能会阻止该任务启动。</p>'),

    P('<p>See also <a href="index.html#cancellation" title="mod tokio::task">the module level docs</a> for more information on cancellation.</p>',
      '<p>另请参阅 <a href="index.html#cancellation" title="mod tokio::task">模块级文档</a> 以获取有关取消的更多信息。</p>'),

    # method.is_finished
    P('<p>Checks if the task associated with this <code>AbortHandle</code> has finished.</p>',
      '<p>检查与此 <code>AbortHandle</code> 关联的任务是否已完成。</p>'),

    P('<p>Please note that this method can return <code>false</code> even if <code>abort</code> has been\ncalled on the task. This is because the cancellation process may take\nsome time, and this method does not return <code>true</code> until it has\ncompleted.</p>',
      '<p>请注意，即使任务上已调用了 <code>abort</code>，此方法也可能返回 <code>false</code>。这是因为取消过程可能需要一些时间，只有在取消完成后此方法才会返回 <code>true</code>。</p>'),

    # method.id
    P('<p>Returns a <a href="struct.Id.html" title="struct tokio::task::Id">task ID</a> that uniquely identifies this task relative to other\ncurrently spawned tasks.</p>',
      '<p>返回一个相对其他当前已派生任务能唯一标识此任务的 <a href="struct.Id.html" title="struct tokio::task::Id">task ID</a>。</p>'),

    # method.clone
    P('<p>Returns a cloned <code>AbortHandle</code> that can be used to remotely abort this task.</p>',
      '<p>返回一个克隆的 <code>AbortHandle</code>，可用于远程终止此任务。</p>'),
]


# ============================================================================
# tokio/task/struct.JoinError.html
# ============================================================================
JOINERROR_PAIRS = [
    # TOP description
    P('<p>Task failed to execute to completion.</p>',
      '<p>任务未能成功执行完成。</p>'),

    # method.is_cancelled
    P('<p>Returns true if the error was caused by the task being cancelled.</p>',
      '<p>如果错误是由任务被取消引起的，则返回 true。</p>'),

    P('<p>See <a href="index.html#cancellation" title="mod tokio::task">the module level docs</a> for more information on cancellation.</p>',
      '<p>另请参阅 <a href="index.html#cancellation" title="mod tokio::task">模块级文档</a> 以获取有关取消的更多信息。</p>'),

    # method.is_panic
    P('<p>Returns true if the error was caused by the task panicking.</p>',
      '<p>如果错误是由任务 panic 引起的，则返回 true。</p>'),

    # method.into_panic
    P('<p>Consumes the join error, returning the object with which the task panicked.</p>',
      '<p>消费此 join error，返回任务因之 panic 的对象。</p>'),

    P('<p><code>into_panic()</code> panics if the <code>Error</code> does not represent the underlying\ntask terminating with a panic. Use <code>is_panic</code> to check the error reason\nor <code>try_into_panic</code> for a variant that does not panic.</p>',
      '<p>如果 <code>Error</code> 并不表示底层任务因 panic 而终止，则 <code>into_panic()</code> 会 panic。可使用 <code>is_panic</code> 检查错误原因，或使用 <code>try_into_panic</code> 获得不会 panic 的变体。</p>'),

    # method.try_into_panic
    P('<p>Consumes the join error, returning the object with which the task\npanicked if the task terminated due to a panic. Otherwise, <code>self</code> is\nreturned.</p>',
      '<p>消费此 join error。如果任务因 panic 而终止，则返回任务因之 panic 的对象；否则返回 <code>self</code>。</p>'),

    # method.id
    P('<p>Returns a <a href="struct.Id.html" title="struct tokio::task::Id">task ID</a> that identifies the task which errored relative to\nother currently spawned tasks.</p>',
      '<p>返回一个相对其他当前已派生任务能标识出错任务的 <a href="struct.Id.html" title="struct tokio::task::Id">task ID</a>。</p>'),
]


# ============================================================================
# tokio/task/struct.JoinHandle.html
# ============================================================================
JOINHANDLE_PAIRS = [
    # TOP
    P('<p>An owned permission to join on a task (await its termination).</p>',
      '<p>用于 join 一个任务（await 其终止）的 owned 权限。</p>'),

    P('<p>This can be thought of as the equivalent of <a href="https://doc.rust-lang.org/1.95.0/std/thread/join_handle/struct.JoinHandle.html" title="struct std::thread::join_handle::JoinHandle"><code>std::thread::JoinHandle</code></a>\nfor a Tokio task rather than a thread. Note that the background task\nassociated with this <code>JoinHandle</code> started running immediately when you\ncalled spawn, even if you have not yet awaited the <code>JoinHandle</code>.</p>',
      '<p>这可以看作是 Tokio 任务（而非线程）版本等价于 <a href="https://doc.rust-lang.org/1.95.0/std/thread/join_handle/struct.JoinHandle.html" title="struct std::thread::join_handle::JoinHandle"><code>std::thread::JoinHandle</code></a> 的类型。请注意，当你调用 spawn 时与此 <code>JoinHandle</code> 关联的后台任务会立即开始运行，即使你尚未 await 该 <code>JoinHandle</code>。</p>'),

    P('<p>A <code>JoinHandle</code> <em>detaches</em> the associated task when it is dropped, which\nmeans that there is no longer any handle to the task, and no way to <code>join</code>\non it.</p>',
      '<p>当 <code>JoinHandle</code> 被丢弃时，与其关联的任务会被<em>分离（detached）</em>，这意味着该任务不再有任何 handle，也无法再 <code>join</code> 它。</p>'),

    P('<p>This <code>struct</code> is created by the <a href="fn.spawn.html" title="fn tokio::task::spawn"><code>task::spawn</code></a> and <a href="fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>task::spawn_blocking</code></a>\nfunctions.</p>',
      '<p>此 <code>struct</code> 由 <a href="fn.spawn.html" title="fn tokio::task::spawn"><code>task::spawn</code></a> 和 <a href="fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>task::spawn_blocking</code></a> 函数创建。</p>'),

    P('<p>It is guaranteed that the destructor of the spawned task has finished\nbefore task completion is observed via <code>JoinHandle</code> <code>await</code>,\n<a href="struct.JoinHandle.html#method.is_finished" title="method tokio::task::JoinHandle::is_finished"><code>JoinHandle::is_finished</code></a> or <a href="struct.AbortHandle.html#method.is_finished" title="method tokio::task::AbortHandle::is_finished"><code>AbortHandle::is_finished</code></a>.</p>',
      '<p>可以保证：在通过 <code>JoinHandle</code> <code>await</code>、<a href="struct.JoinHandle.html#method.is_finished" title="method tokio::task::JoinHandle::is_finished"><code>JoinHandle::is_finished</code></a> 或 <a href="struct.AbortHandle.html#method.is_finished" title="method tokio::task::AbortHandle::is_finished"><code>AbortHandle::is_finished</code></a> 观察到任务完成之前，已派生任务的析构函数已经运行结束。</p>'),

    P('<p>The <code>&amp;mut JoinHandle&lt;T&gt;</code> type is cancel safe. If it is used as the event\nin a <code>tokio::select!</code> statement and some other branch completes first,\nthen it is guaranteed that the output of the task is not lost.</p>',
      '<p><code>&amp;mut JoinHandle&lt;T&gt;</code> 类型是 cancel safe 的。如果它在 <code>tokio::select!</code> 语句中作为事件，且其他分支先完成，可以保证任务的输出不会丢失。</p>'),

    P('<p>If a <code>JoinHandle</code> is dropped, then the task continues running in the\nbackground and its return value is lost.</p>',
      '<p>如果 <code>JoinHandle</code> 被丢弃，则任务将继续在后台运行，其返回值将丢失。</p>'),

    P('<p>Creation from <a href="fn.spawn.html" title="fn tokio::task::spawn"><code>task::spawn</code></a>:</p>',
      '<p>通过 <a href="fn.spawn.html" title="fn tokio::task::spawn"><code>task::spawn</code></a> 创建：</p>'),

    P('<p>Creation from <a href="fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>task::spawn_blocking</code></a>:</p>',
      '<p>通过 <a href="fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>task::spawn_blocking</code></a> 创建：</p>'),

    P('<p>The generic parameter <code>T</code> in <code>JoinHandle&lt;T&gt;</code> is the return type of the spawned task.\nIf the return value is an <code>i32</code>, the join handle has type <code>JoinHandle&lt;i32&gt;</code>:</p>',
      '<p><code>JoinHandle&lt;T&gt;</code> 中的泛型参数 <code>T</code> 表示已派生任务的返回类型。如果返回值是 <code>i32</code>，则该 join handle 的类型为 <code>JoinHandle&lt;i32&gt;</code>：</p>'),

    P('<p>If the task does not have a return value, the join handle has type <code>JoinHandle&lt;()&gt;</code>:</p>',
      '<p>如果任务没有返回值，则该 join handle 的类型为 <code>JoinHandle&lt;()&gt;</code>：</p>'),

    P('<p>Note that <code>handle.await</code> doesn’t give you the return type directly. It is wrapped in a\n<code>Result</code> because panics in the spawned task are caught by Tokio. The <code>?</code> operator has\nto be double chained to extract the returned value:</p>',
      '<p>请注意，<code>handle.await</code> 不会直接返回任务的返回类型。它会被包装在 <code>Result</code> 中，因为已派生任务中的 panic 会被 Tokio 捕获。要提取返回的值，需要双层链式使用 <code>?</code> 操作符：</p>'),

    P('<p>If the task panics, the error is a <a href="struct.JoinError.html" title="struct tokio::task::JoinError"><code>JoinError</code></a> that contains the panic:</p>',
      '<p>如果任务 panic，则错误为包含 panic 信息的 <a href="struct.JoinError.html" title="struct tokio::task::JoinError"><code>JoinError</code></a>：</p>'),

    P('<p>Child being detached and outliving its parent:</p>',
      '<p>子任务被分离且存活时间超过其父任务：</p>'),

    # method.abort
    P('<p>Abort the task associated with the handle.</p>',
      '<p>终止与此 handle 关联的任务。</p>'),

    P('<p>Awaiting a cancelled task might complete as usual if the task was\nalready completed at the time it was cancelled, but most likely it\nwill fail with a <a href="struct.JoinError.html#method.is_cancelled" title="method tokio::task::JoinError::is_cancelled">cancelled</a> <code>JoinError</code>.</p>',
      '<p>等待一个被取消的任务，如果该任务在被取消时已经完成，则可能会正常完成；但大多数情况下，它会因 <a href="struct.JoinError.html#method.is_cancelled" title="method tokio::task::JoinError::is_cancelled">取消</a> 而失败并返回 <code>JoinError</code>。</p>'),

    P('<p>Be aware that tasks spawned using <a href="fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> cannot be aborted\nbecause they are not async. If you call <code>abort</code> on a <code>spawn_blocking</code>\ntask, then this <em>will not have any effect</em>, and the task will continue\nrunning normally. The exception is if the task has not started running\nyet; in that case, calling <code>abort</code> may prevent the task from starting.</p>',
      '<p>请注意，使用 <a href="fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> 派生的任务无法被终止，因为它们不是异步的。如果你对 <code>spawn_blocking</code> 任务调用 <code>abort</code>，则<em>不会产生任何效果</em>，任务将继续正常运行。例外情况是该任务尚未开始运行；此时调用 <code>abort</code> 可能会阻止该任务启动。</p>'),

    P('<p>See also <a href="index.html#cancellation" title="mod tokio::task">the module level docs</a> for more information on cancellation.</p>',
      '<p>另请参阅 <a href="index.html#cancellation" title="mod tokio::task">模块级文档</a> 以获取有关取消的更多信息。</p>'),

    # method.is_finished
    P('<p>Checks if the task associated with this <code>JoinHandle</code> has finished.</p>',
      '<p>检查与此 <code>JoinHandle</code> 关联的任务是否已完成。</p>'),

    P('<p>Please note that this method can return <code>false</code> even if <a href="struct.JoinHandle.html#method.abort" title="method tokio::task::JoinHandle::abort"><code>abort</code></a> has been\ncalled on the task. This is because the cancellation process may take\nsome time, and this method does not return <code>true</code> until it has\ncompleted.</p>',
      '<p>请注意，即使任务上已调用了 <a href="struct.JoinHandle.html#method.abort" title="method tokio::task::JoinHandle::abort"><code>abort</code></a>，此方法也可能返回 <code>false</code>。这是因为取消过程可能需要一些时间，只有在取消完成后此方法才会返回 <code>true</code>。</p>'),

    # method.abort_handle
    P('<p>Returns a new <code>AbortHandle</code> that can be used to remotely abort this task.</p>',
      '<p>返回一个新的 <code>AbortHandle</code>，可用于远程终止此任务。</p>'),

    P('<p>Awaiting a task cancelled by the <code>AbortHandle</code> might complete as usual if the task was\nalready completed at the time it was cancelled, but most likely it\nwill fail with a <a href="struct.JoinError.html#method.is_cancelled" title="method tokio::task::JoinError::is_cancelled">cancelled</a> <code>JoinError</code>.</p>',
      '<p>等待被 <code>AbortHandle</code> 取消的任务，如果该任务在被取消时已经完成，则可能会正常完成；但大多数情况下，它会因 <a href="struct.JoinError.html#method.is_cancelled" title="method tokio::task::JoinError::is_cancelled">取消</a> 而失败并返回 <code>JoinError</code>。</p>'),

    # method.id
    P('<p>Returns a <a href="struct.Id.html" title="struct tokio::task::Id">task ID</a> that uniquely identifies this task relative to other\ncurrently spawned tasks.</p>',
      '<p>返回一个相对其他当前已派生任务能唯一标识此任务的 <a href="struct.Id.html" title="struct tokio::task::Id">task ID</a>。</p>'),
]


# ============================================================================
# tokio/task/struct.LocalKey.html
# ============================================================================
LOCALKEY_PAIRS = [
    # TOP
    P('<p>A key for task-local data.</p>',
      '<p>用于 task-local 数据的 key。</p>'),

    P('<p>This type is generated by the <a href="../macro.task_local.html"><code>task_local!</code></a> macro.</p>',
      '<p>此类型由 <a href="../macro.task_local.html"><code>task_local!</code></a> 宏生成。</p>'),

    P('<p>Unlike <a href="https://doc.rust-lang.org/1.95.0/std/thread/local/struct.LocalKey.html" title="struct std::thread::local::LocalKey"><code>std::thread::LocalKey</code></a>, <code>tokio::task::LocalKey</code> will\n<em>not</em> lazily initialize the value on first access. Instead, the\nvalue is first initialized when the future containing\nthe task-local is first polled by a futures executor, like Tokio.</p>',
      '<p>与 <a href="https://doc.rust-lang.org/1.95.0/std/thread/local/struct.LocalKey.html" title="struct std::thread::local::LocalKey"><code>std::thread::LocalKey</code></a> 不同，<code>tokio::task::LocalKey</code> <em>不会</em>在首次访问时惰性初始化值。相反，值会在包含 task-local 的 future 第一次被 Tokio 等 futures 执行器 poll 时初始化。</p>'),

    # method.scope
    P('<p>Sets a value <code>T</code> as the task-local value for the future <code>F</code>.</p>',
      '<p>将值 <code>T</code> 设置为 future <code>F</code> 的 task-local 值。</p>'),

    P('<p>On completion of <code>scope</code>, the task-local will be dropped.</p>',
      '<p><code>scope</code> 完成后，task-local 将被丢弃。</p>'),

    P('<p>If you poll the returned future inside a call to <a href="struct.LocalKey.html#method.with" title="method tokio::task::LocalKey::with"><code>with</code></a> or\n<a href="struct.LocalKey.html#method.try_with" title="method tokio::task::LocalKey::try_with"><code>try_with</code></a> on the same <code>LocalKey</code>, then the call to <code>poll</code> will panic.</p>',
      '<p>如果你在同一个 <code>LocalKey</code> 上调用 <a href="struct.LocalKey.html#method.with" title="method tokio::task::LocalKey::with"><code>with</code></a> 或 <a href="struct.LocalKey.html#method.try_with" title="method tokio::task::LocalKey::try_with"><code>try_with</code></a> 时 poll 返回的 future，则对 <code>poll</code> 的调用将 panic。</p>'),

    # method.sync_scope
    P('<p>Sets a value <code>T</code> as the task-local value for the closure <code>F</code>.</p>',
      '<p>将值 <code>T</code> 设置为闭包 <code>F</code> 的 task-local 值。</p>'),

    P('<p>On completion of <code>sync_scope</code>, the task-local will be dropped.</p>',
      '<p><code>sync_scope</code> 完成后，task-local 将被丢弃。</p>'),

    P('<p>This method panics if called inside a call to <a href="struct.LocalKey.html#method.with" title="method tokio::task::LocalKey::with"><code>with</code></a> or <a href="struct.LocalKey.html#method.try_with" title="method tokio::task::LocalKey::try_with"><code>try_with</code></a>\non the same <code>LocalKey</code>.</p>',
      '<p>如果在同一个 <code>LocalKey</code> 上调用 <a href="struct.LocalKey.html#method.with" title="method tokio::task::LocalKey::with"><code>with</code></a> 或 <a href="struct.LocalKey.html#method.try_with" title="method tokio::task::LocalKey::try_with"><code>try_with</code></a> 时调用此方法，则会 panic。</p>'),

    # method.with
    P('<p>Accesses the current task-local and runs the provided closure.</p>',
      '<p>访问当前 task-local 并运行提供的闭包。</p>'),

    P('<p>This function will panic if the task local doesn’t have a value set.</p>',
      '<p>如果 task-local 没有设置值，此函数将 panic。</p>'),

    # method.try_with
    P('<p>Accesses the current task-local and runs the provided closure.</p>',
      '<p>访问当前 task-local 并运行提供的闭包。</p>'),

    P('<p>If the task-local with the associated key is not present, this\nmethod will return an <code>AccessError</code>. For a panicking variant,\nsee <code>with</code>.</p>',
      '<p>如果与该 key 关联的 task-local 不存在，此方法将返回一个 <code>AccessError</code>。关于会 panic 的变体，请参阅 <code>with</code>。</p>'),

    # method.get
    P('<p>Returns a copy of the task-local value\nif the task-local value implements <code>Clone</code>.</p>',
      '<p>如果 task-local 值实现了 <code>Clone</code>，则返回该 task-local 值的一个副本。</p>'),

    P('<p>This function will panic if the task local doesn’t have a value set.</p>',
      '<p>如果 task-local 没有设置值，此函数将 panic。</p>'),

    # method.try_get
    P('<p>Returns a copy of the task-local value\nif the task-local value implements <code>Clone</code>.</p>',
      '<p>如果 task-local 值实现了 <code>Clone</code>，则返回该 task-local 值的一个副本。</p>'),

    P('<p>If the task-local with the associated key is not present, this\nmethod will return an <code>AccessError</code>. For a panicking variant,\nsee <code>get</code>.</p>',
      '<p>如果与该 key 关联的 task-local 不存在，此方法将返回一个 <code>AccessError</code>。关于会 panic 的变体，请参阅 <code>get</code>。</p>'),
]


# ============================================================================
# tokio/task/struct.LocalSet.html
# ============================================================================
LOCALSET_PAIRS = [
    # TOP
    P('<p>A set of tasks which are executed on the same thread.</p>',
      '<p>在同一线程上执行的若干任务的集合。</p>'),

    # copy-path
    P('<p>In some cases, it is necessary to run one or more futures that do not\nimplement <a href="https://doc.rust-lang.org/1.95.0/core/marker/trait.Send.html" title="trait core::marker::Send"><code>Send</code></a> and thus are unsafe to send between threads. In these\ncases, a <a href="struct.LocalSet.html" title="struct tokio::task::LocalSet">local task set</a> may be used to schedule one or more <code>!Send</code>\nfutures to run together on the same thread.</p>',
      '<p>在某些情况下，需要运行一个或多个未实现 <a href="https://doc.rust-lang.org/1.95.0/core/marker/trait.Send.html" title="trait core::marker::Send"><code>Send</code></a> 的 future，因此在线程之间发送它们是不安全的。在这些情况下，可以使用<a href="struct.LocalSet.html" title="struct tokio::task::LocalSet">本地任务集合</a>来调度一个或多个 <code>!Send</code> future 在同一线程上一起运行。</p>'),

    P('<p>For example, the following code will not compile:</p>',
      '<p>例如，以下代码将无法编译：</p>'),

    # use-with-run_until
    P('<p>To spawn <code>!Send</code> futures, we can use a local task set to schedule them\non the thread calling <a href="../runtime/struct.Runtime.html#method.block_on" title="method tokio::runtime::Runtime::block_on"><code>Runtime::block_on</code></a>. When running inside of the\nlocal task set, we can use <a href="fn.spawn_local.html" title="fn tokio::task::spawn_local"><code>task::spawn_local</code></a>, which can spawn\n<code>!Send</code> futures. For example:</p>',
      '<p>要派生 <code>!Send</code> future，我们可以使用本地任务集合，将它们调度在调用 <a href="../runtime/struct.Runtime.html#method.block_on" title="method tokio::runtime::Runtime::block_on"><code>Runtime::block_on</code></a> 的线程上。在本地任务集合内运行时，我们可以使用 <a href="fn.spawn_local.html" title="fn tokio::task::spawn_local"><code>task::spawn_local</code></a>，它可以派生 <code>!Send</code> future。例如：</p>'),

    P('<p><strong>Note:</strong> The <code>run_until</code> method can only be used in <code>#[tokio::main]</code>,\n<code>#[tokio::test]</code> or directly inside a call to <a href="../runtime/struct.Runtime.html#method.block_on" title="method tokio::runtime::Runtime::block_on"><code>Runtime::block_on</code></a>. It\ncannot be used inside a task spawned with <code>tokio::spawn</code>.</p>',
      '<p><strong>注意：</strong><code>run_until</code> 方法只能在 <code>#[tokio::main]</code>、<code>#[tokio::test]</code> 或直接调用 <a href="../runtime/struct.Runtime.html#method.block_on" title="method tokio::runtime::Runtime::block_on"><code>Runtime::block_on</code></a> 内部使用。它不能在使用 <code>tokio::spawn</code> 派生的任务内部使用。</p>'),

    # awaiting-a-localset
    P('<p>Additionally, a <code>LocalSet</code> itself implements <code>Future</code>, completing when\n<em>all</em> tasks spawned on the <code>LocalSet</code> complete. This can be used to run\nseveral futures on a <code>LocalSet</code> and drive the whole set until they\ncomplete. For example,</p>',
      '<p>此外，<code>LocalSet</code> 本身实现了 <code>Future</code>，当 <code>LocalSet</code> 上<em>所有</em>派生任务都完成时，它也会随之完成。这可用于在 <code>LocalSet</code> 上运行多个 future，并驱动整个集合直到它们全部完成。例如：</p>'),

    P('<p><strong>Note:</strong> Awaiting a <code>LocalSet</code> can only be done inside\n<code>#[tokio::main]</code>, <code>#[tokio::test]</code> or directly inside a call to\n<a href="../runtime/struct.Runtime.html#method.block_on" title="method tokio::runtime::Runtime::block_on"><code>Runtime::block_on</code></a>. It cannot be used inside a task spawned with\n<code>tokio::spawn</code>.</p>',
      '<p><strong>注意：</strong>对 <code>LocalSet</code> 的 await 只能在 <code>#[tokio::main]</code>、<code>#[tokio::test]</code> 或直接调用 <a href="../runtime/struct.Runtime.html#method.block_on" title="method tokio::runtime::Runtime::block_on"><code>Runtime::block_on</code></a> 内部进行。它不能在使用 <code>tokio::spawn</code> 派生的任务内部使用。</p>'),

    # use-inside-tokiospawn
    P('<p>The two methods mentioned above cannot be used inside <code>tokio::spawn</code>, so\nto spawn <code>!Send</code> futures from inside <code>tokio::spawn</code>, we need to do\nsomething else. The solution is to create the <code>LocalSet</code> somewhere else,\nand communicate with it using an <a href="../sync/mpsc/index.html" title="mod tokio::sync::mpsc"><code>mpsc</code></a> channel.</p>',
      '<p>上面提到的两种方法都不能在 <code>tokio::spawn</code> 内部使用，因此要在 <code>tokio::spawn</code> 内部派生 <code>!Send</code> future，我们需要采用其他方式。解决方案是在其他地方创建 <code>LocalSet</code>，并通过 <a href="../sync/mpsc/index.html" title="mod tokio::sync::mpsc"><code>mpsc</code></a> 通道与它通信。</p>'),

    P('<p>The following example puts the <code>LocalSet</code> inside a new thread.</p>',
      '<p>以下示例将 <code>LocalSet</code> 放在一个新线程中。</p>'),

    # method.new
    P('<p>Returns a new local task set.</p>',
      '<p>返回一个新的本地任务集合。</p>'),

    # method.enter
    P('<p>Enters the context of this <code>LocalSet</code>.</p>',
      '<p>进入此 <code>LocalSet</code> 的上下文。</p>'),

    P('<p>The <a href="fn.spawn_local.html" title="fn tokio::task::spawn_local"><code>spawn_local</code></a> method will spawn tasks on the <code>LocalSet</code> whose\ncontext you are inside.</p>',
      '<p><a href="fn.spawn_local.html" title="fn tokio::task::spawn_local"><code>spawn_local</code></a> 方法会将任务派生到你所进入的 <code>LocalSet</code> 上下文中。</p>'),

    # method.spawn_local
    P('<p>Spawns a <code>!Send</code> task onto the local task set.</p>',
      '<p>将一个 <code>!Send</code> 任务派生到本地任务集合上。</p>'),

    P('<p>This task is guaranteed to be run on the current thread.</p>',
      '<p>此任务保证在当前线程上运行。</p>'),

    P('<p>Unlike the free function <a href="fn.spawn_local.html" title="fn tokio::task::spawn_local"><code>spawn_local</code></a>, this method may be used to\nspawn local tasks when the <code>LocalSet</code> is <em>not</em> running. The provided\nfuture will start running once the <code>LocalSet</code> is next started, even if\nyou don’t await the returned <code>JoinHandle</code>.</p>',
      '<p>与自由函数 <a href="fn.spawn_local.html" title="fn tokio::task::spawn_local"><code>spawn_local</code></a> 不同，此方法可用于在 <code>LocalSet</code> <em>没有</em>运行时派生本地任务。提供的 future 将在 <code>LocalSet</code> 下次启动时开始运行，即使你没有 await 返回的 <code>JoinHandle</code>。</p>'),

    # method.block_on
    P('<p>Runs a future to completion on the provided runtime, driving any local\nfutures spawned on this task set on the current thread.</p>',
      '<p>在给定的 runtime 上运行 future 直到完成，同时在当前线程上驱动该任务集合上派生的所有本地 future。</p>'),

    P('<p>This runs the given future on the runtime, blocking until it is\ncomplete, and yielding its resolved result. Any tasks or timers which\nthe future spawns internally will be executed on the runtime. The future\nmay also call <a href="fn.spawn_local.html" title="fn tokio::task::spawn_local"><code>spawn_local</code></a> to <code>spawn_local</code> additional local futures on the\ncurrent thread.</p>',
      '<p>此方法在 runtime 上运行给定的 future，阻塞直到其完成，并产出其已解析的结果。该 future 内部派生的任何任务或定时器都将在 runtime 上执行。该 future 也可以调用 <a href="fn.spawn_local.html" title="fn tokio::task::spawn_local"><code>spawn_local</code></a>，在当前线程上派生其他本地 future。</p>'),

    P('<p>This method should not be called from an asynchronous context.</p>',
      '<p>不应在异步上下文中调用此方法。</p>'),

    # method.block_on panics/notes
    P('<p>This function panics if the executor is at capacity, if the provided\nfuture panics, or if called within an asynchronous execution context.</p>',
      '<p>如果 executor 处于满载状态、如果提供的 future 发生 panic，或者在异步执行上下文中调用此函数，则此函数会 panic。</p>'),

    P('<p>Since this function internally calls <a href="../runtime/struct.Runtime.html#method.block_on" title="method tokio::runtime::Runtime::block_on"><code>Runtime::block_on</code></a>, and drives\nfutures in the local task set inside that call to <code>block_on</code>, the local\nfutures may not use <a href="fn.block_in_place.html" title="fn tokio::task::block_in_place">in-place blocking</a>. If a blocking call needs to be\nissued from a local task, the <a href="fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> API may be used instead.</p>',
      '<p>由于此函数在内部调用 <a href="../runtime/struct.Runtime.html#method.block_on" title="method tokio::runtime::Runtime::block_on"><code>Runtime::block_on</code></a>，并在 <code>block_on</code> 调用内部驱动本地任务集合中的 future，因此本地 future 不得使用<a href="fn.block_in_place.html" title="fn tokio::task::block_in_place">原地阻塞</a>。如果本地任务需要发起阻塞调用，可以使用 <a href="fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> API 来替代。</p>'),

    P('<p>For example, this will panic:</p>',
      '<p>例如，这将发生 panic：</p>'),

    P('<p>This, however, will not panic:</p>',
      '<p>然而，下面的情况不会发生 panic：</p>'),

    # method.run_until
    P('<p>Runs a future to completion on the local set, returning its output.</p>',
      '<p>在本地集合上运行 future 直到完成，并返回其输出。</p>'),

    P('<p>This returns a future that runs the given future with a local set,\nallowing it to call <a href="fn.spawn_local.html" title="fn tokio::task::spawn_local"><code>spawn_local</code></a> to spawn additional <code>!Send</code> futures.\nAny local futures spawned on the local set will be driven in the\nbackground until the future passed to <code>run_until</code> completes. When the future\npassed to <code>run_until</code> finishes, any local futures which have not completed\nwill remain on the local set, and will be driven on subsequent calls to\n<code>run_until</code> or when <a href="#awaiting-a-localset">awaiting the local set</a> itself.</p>',
      '<p>此方法返回一个 future，它会在本地集合下运行给定的 future，从而允许该 future 调用 <a href="fn.spawn_local.html" title="fn tokio::task::spawn_local"><code>spawn_local</code></a> 来派生其他 <code>!Send</code> future。在传递给 <code>run_until</code> 的 future 完成之前，在本地集合上派生的任何本地 future 都将在后台被驱动。当传递给 <code>run_until</code> 的 future 结束时，任何尚未完成的本地 future 仍会保留在本地集合上，并将在后续对 <code>run_until</code> 的调用中或 <a href="#awaiting-a-localset">await 本地集合</a>本身时被驱动。</p>'),

    P('<p>This method is cancel safe when <code>future</code> is cancel safe.</p>',
      '<p>当 <code>future</code> 自身 cancel safe 时，此方法是 cancel safe 的。</p>'),

    # method.id
    P('<p>Returns the <a href="../runtime/struct.Id.html" title="struct tokio::runtime::Id"><code>Id</code></a> of the current <a href="struct.LocalSet.html" title="struct tokio::task::LocalSet"><code>LocalSet</code></a> runtime.</p>',
      '<p>返回当前 <a href="struct.LocalSet.html" title="struct tokio::task::LocalSet"><code>LocalSet</code></a> runtime 的 <a href="../runtime/struct.Id.html" title="struct tokio::runtime::Id"><code>Id</code></a>。</p>'),
]


# ============================================================================
# tokio/task/coop/struct.RestoreOnPending.html
# ============================================================================
RESTOREONPENDING_PAIRS = [
    P('<p>Value returned by the <a href="fn.poll_proceed.html" title="fn tokio::task::coop::poll_proceed"><code>poll_proceed</code></a> method.</p>',
      '<p><a href="fn.poll_proceed.html" title="fn tokio::task::coop::poll_proceed"><code>poll_proceed</code></a> 方法的返回值。</p>'),

    P('<p>Signals that the task that obtained this <code>RestoreOnPending</code> was able to make\nprogress. This prevents the task budget from being restored to the value\nit had prior to obtaining this instance when it is dropped.</p>',
      '<p>表示获得此 <code>RestoreOnPending</code> 的任务已能够取得进展。这会阻止任务预算在丢弃此实例时被恢复为获取此实例之前的值。</p>'),
]


# ============================================================================
# tokio/task/futures/struct.TaskLocalFuture.html
# ============================================================================
TASKLOCALFUTURE_PAIRS = [
    P('<p>A future that sets a value <code>T</code> of a task local for the future <code>F</code> during\nits execution.</p>',
      '<p>一个在执行期间为 future <code>F</code> 设置 task-local 值 <code>T</code> 的 future。</p>'),

    P('<p>The value of the task-local must be <code>\'static</code> and will be dropped on the\ncompletion of the future.</p>',
      '<p>task-local 的值必须是 <code>\'static</code>，并将在 future 完成时被丢弃。</p>'),

    P('<p>Created by the function <a href="../struct.LocalKey.html#method.scope" title="method tokio::task::LocalKey::scope"><code>LocalKey::scope</code></a>.</p>',
      '<p>由函数 <a href="../struct.LocalKey.html#method.scope" title="method tokio::task::LocalKey::scope"><code>LocalKey::scope</code></a> 创建。</p>'),

    P('<p>Returns the value stored in the task local by this <code>TaskLocalFuture</code>.</p>',
      '<p>返回此 <code>TaskLocalFuture</code> 存储在 task-local 中的值。</p>'),

    P('<p>The function returns:</p>',
      '<p>此函数返回：</p>'),

    P('<p>Note that this function attempts to take the task local value even if\nthe future has not yet completed. In that case, the value will no longer\nbe available via the task local after the call to <code>take_value</code>.</p>',
      '<p>请注意，即使 future 尚未完成，此函数也会尝试获取 task-local 的值。在这种情况下，调用 <code>take_value</code> 之后该值将无法再通过 task-local 访问。</p>'),

    # "Some(T)" / "None" list items
    P('<li><code>Some(T)</code> if the task local value exists.</li>',
      '<li>如果 task-local 值存在，则为 <code>Some(T)</code>。</li>'),

    P('<li><code>None</code> if the task local value has already been taken.</li>',
      '<li>如果 task-local 值已经被取走，则为 <code>None</code>。</li>'),
]


# ============================================================================
# tokio/task/index.html — module top-level
# ============================================================================
TASK_INDEX_PAIRS = [
    P('<p>Asynchronous green-threads.</p>',
      '<p>异步绿色线程。</p>'),

    P('<p>A <em>task</em> is a light weight, non-blocking unit of execution. A task is similar\nto an OS thread, but rather than being managed by the OS scheduler, they are\nmanaged by the <a href="../runtime/index.html" title="mod tokio::runtime">Tokio runtime</a>. Another name for this general pattern is\n<a href="https://en.wikipedia.org/wiki/Green_threads">green threads</a>. If you are familiar with <a href="https://tour.golang.org/concurrency/1">Go’s goroutines</a>, <a href="https://kotlinlang.org/docs/reference/coroutines-overview.html">Kotlin’s\ncoroutines</a>, or <a href="http://erlang.org/doc/getting_started/conc_prog.html#processes">Erlang’s processes</a>, you can think of Tokio’s tasks as\nsomething similar.</p>',
      '<p><em>任务（task）</em>是一个轻量级、非阻塞的执行单元。任务与 OS 线程类似，但它们不是由 OS 调度器管理，而是由 <a href="../runtime/index.html" title="mod tokio::runtime">Tokio runtime</a> 管理。这种模式的另一个名称是<a href="https://en.wikipedia.org/wiki/Green_threads">绿色线程</a>。如果你熟悉 <a href="https://tour.golang.org/concurrency/1">Go 语言的 goroutine</a>、<a href="https://kotlinlang.org/docs/reference/coroutines-overview.html">Kotlin 的协程</a> 或 <a href="http://erlang.org/doc/getting_started/conc_prog.html#processes">Erlang 的进程</a>，你可以将 Tokio 的任务视作与之类似的概念。</p>'),

    P('<p>Key points about tasks include:</p>',
      '<p>关于任务的关键要点包括：</p>'),

    P('<p>Tasks are <strong>light weight</strong>. Because tasks are scheduled by the Tokio\nruntime rather than the operating system, creating new tasks or switching\nbetween tasks does not require a context switch and has fairly low\noverhead. Creating, running, and destroying large numbers of tasks is\nquite cheap, especially compared to OS threads.</p>',
      '<p>任务是<strong>轻量级</strong>的。由于任务由 Tokio runtime（而非操作系统）进行调度，创建新任务或在任务之间切换不需要上下文切换，开销相当低。大量任务的创建、运行和销毁成本都相当低，尤其是与 OS 线程相比。</p>'),

    P('<p>Tasks are scheduled <strong>cooperatively</strong>. Most operating systems implement\n<em>preemptive multitasking</em>. This is a scheduling technique where the\noperating system allows each thread to run for a period of time, and then\n<em>preempts</em> it, temporarily pausing that thread and switching to another.\nTasks, on the other hand, implement <em>cooperative multitasking</em>. In\ncooperative multitasking, a task is allowed to run until it <em>yields</em>,\nindicating to the Tokio runtime’s scheduler that it cannot currently\ncontinue executing. When a task yields, the Tokio runtime switches to\nexecuting the next task.</p>',
      '<p>任务的调度是<strong>协作式</strong>的。大多数操作系统实现的是<em>抢占式多任务</em>。在这种调度技术中，操作系统允许每个线程运行一段时间，然后<em>抢占</em>它，临时暂停该线程并切换到另一个线程。而任务则实现<em>协作式多任务</em>。在协作式多任务中，任务被允许运行到它主动<em>让出（yield）</em>为止，这向 Tokio runtime 的调度器表明它当前无法继续执行。当任务让出时，Tokio runtime 会切换到执行下一个任务。</p>'),

    P('<p>Tasks are <strong>non-blocking</strong>. Typically, when an OS thread performs I/O or\nmust synchronize with another thread, it <em>blocks</em>, allowing the OS to\nschedule another thread. When a task cannot continue executing, it must\nyield instead, allowing the Tokio runtime to schedule another task. Tasks\nshould generally not perform system calls or other operations that could\nblock a thread, as this would prevent other tasks running on the same\nthread from executing as well. Instead, this module provides APIs for\nrunning blocking operations in an asynchronous context.</p>',
      '<p>任务是<strong>非阻塞</strong>的。通常，当 OS 线程执行 I/O 或必须与另一个线程同步时，它会<em>阻塞</em>，让操作系统调度另一个线程。当任务无法继续执行时，它必须让出（yield），从而允许 Tokio runtime 调度另一个任务。任务通常不应执行可能阻塞线程的系统调用或其他操作，因为这也会阻止同一线程上的其他任务运行。本模块提供了在异步上下文中运行阻塞操作的 API。</p>'),

    P('<p>This module provides the following APIs for working with tasks:</p>',
      '<p>此模块提供以下用于处理任务的 API：</p>'),

    P('<p>Perhaps the most important function in this module is <a href="fn.spawn.html" title="fn tokio::task::spawn"><code>task::spawn</code></a>. This\nfunction can be thought of as an async equivalent to the standard library’s\n<a href="https://doc.rust-lang.org/1.95.0/std/thread/functions/fn.spawn.html" title="fn std::thread::functions::spawn"><code>thread::spawn</code></a>. It takes an <code>async</code> block or other\n<a href="https://doc.rust-lang.org/1.95.0/core/future/future/trait.Future.html" title="trait core::future::future::Future">future</a>, and creates a new task to run that work concurrently:</p>',
      '<p>本模块中最重要的函数可能是 <a href="fn.spawn.html" title="fn tokio::task::spawn"><code>task::spawn</code></a>。该函数可视为标准库 <a href="https://doc.rust-lang.org/1.95.0/std/thread/functions/fn.spawn.html" title="fn std::thread::functions::spawn"><code>thread::spawn</code></a> 的异步等价版本。它接受一个 <code>async</code> 块或其他 <a href="https://doc.rust-lang.org/1.95.0/core/future/future/trait.Future.html" title="trait core::future::future::Future">future</a>，并创建一个新任务以并发地运行该工作：</p>'),

    # Module index entries
    P('<p>Utilities for improved cooperative scheduling.</p>',
      '<p>用于改进协作式调度的工具。</p>'),

    P('<p>Task-related futures.</p>',
      '<p>与任务相关的 futures。</p>'),

    P('<p>An owned permission to abort a spawned task, without awaiting its completion.</p>',
      '<p>用于终止已派生任务的 owned 权限，不会等待任务完成。</p>'),

    P('<p>An opaque ID that uniquely identifies a task relative to all other currently\nspawned tasks.</p>',
      '<p>一个不透明 ID，相对于所有其他当前已派生任务，能唯一标识某个任务。</p>'),

    P('<p>Task failed to execute to completion.</p>',
      '<p>任务未能成功执行完成。</p>'),

    P('<p>An owned permission to join on a task (await its termination).</p>',
      '<p>用于 join 一个任务（await 其终止）的 owned 权限。</p>'),

    P('<p>A collection of tasks spawned on a Tokio runtime.</p>',
      '<p>在 Tokio runtime 上生成的若干任务的集合。</p>'),

    P('<p>Context guard for LocalSet</p>',
      '<p>LocalSet 的上下文守卫</p>'),

    P('<p>A key for task-local data.</p>',
      '<p>用于 task-local 数据的 key。</p>'),

    P('<p>A set of tasks which are executed on the same thread.</p>',
      '<p>在同一线程上执行的若干任务的集合。</p>'),

    P('<p>Runs the provided blocking function on the current thread without\nblocking the executor.</p>',
      '<p>在当前线程上运行提供的阻塞函数，但不会阻塞 executor。</p>'),

    P('<p>Returns the Id of the currently running task.</p>',
      '<p>返回当前正在运行任务的 ID。</p>'),

    P('<p>Spawns a new asynchronous task, returning a\n<a href="struct.JoinHandle.html" title="struct tokio::task::JoinHandle">JoinHandle</a> for it.</p>',
      '<p>派生一个新的异步任务，并为其返回一个 <a href="struct.JoinHandle.html" title="struct tokio::task::JoinHandle">JoinHandle</a>。</p>'),

    P('<p>Runs the provided closure on a thread where blocking is acceptable.</p>',
      '<p>在可以接受阻塞的线程上运行提供的闭包。</p>'),

    P('<p>Spawns a !Send future on the current LocalSet or LocalRuntime.</p>',
      '<p>在当前 LocalSet 或 LocalRuntime 上派生一个 !Send future。</p>'),

    P('<p>Returns the Id of the currently running task, or None if called outside\nof a Tokio runtime.</p>',
      '<p>返回当前正在运行任务的 ID，如果在 Tokio runtime 之外调用则返回 None。</p>'),

    P('<p>Yields execution back to the Tokio runtime.</p>',
      '<p>将执行权让回给 Tokio runtime。</p>'),

    # "As we discussed" section
    P('<p>As we discussed above, code running in asynchronous tasks should not perform\nblocking I/O or CPU-heavy computation. If your code has a section that\ncannot be made to be non-blocking, you should use the\n<a href="fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> function to run that work on a thread pool dedicated\nto blocking operations, while keeping a separate thread for the executor.</p>',
      '<p>如上所述，在异步任务中运行的代码不应执行阻塞 I/O 或大量占用 CPU 的计算。如果你的代码中存在无法改为非阻塞的部分，应当使用 <a href="fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> 函数将该工作运行在专门用于阻塞操作的线程池上，同时为 executor 保留独立的线程。</p>'),

    P('<p>Be aware that if you call a non-async method from async code, that non-async\nmethod will still block the executor thread. In particular, calling\n<a href="https://doc.rust-lang.org/1.95.0/std/sync/index.html"><code>std::sync</code></a> functions from async code will block the executor thread.</p>',
      '<p>请注意，如果你在异步代码中调用非 async 方法，该非 async 方法仍会阻塞 executor 线程。特别地，在异步代码中调用 <a href="https://doc.rust-lang.org/1.95.0/std/sync/index.html"><code>std::sync</code></a> 函数会阻塞 executor 线程。</p>'),

    # "Like std::thread::spawn, task::spawn returns a JoinHandle struct."
    P('<p>Like <a href="https://doc.rust-lang.org/1.95.0/std/thread/functions/fn.spawn.html" title="fn std::thread::functions::spawn"><code>std::thread::spawn</code></a>, <code>task::spawn</code> returns a <a href="struct.JoinHandle.html" title="struct tokio::task::JoinHandle"><code>JoinHandle</code></a> struct.\nA <code>JoinHandle</code> is itself a future which may be used to await the output of\nthe spawned task. For example:</p>',
      '<p>与 <a href="https://doc.rust-lang.org/1.95.0/std/thread/functions/fn.spawn.html" title="fn std::thread::functions::spawn"><code>std::thread::spawn</code></a> 类似，<code>task::spawn</code> 返回一个 <a href="struct.JoinHandle.html" title="struct tokio::task::JoinHandle"><code>JoinHandle</code></a> 结构体。<code>JoinHandle</code> 本身也是一个 future，可用于 await 已派生任务的输出。例如：</p>'),

    # "Again, like std::thread's JoinHandle type..."
    P('<p>Again, like <code>std::thread</code>’s <a href="https://doc.rust-lang.org/1.95.0/std/thread/join_handle/struct.JoinHandle.html" title="struct std::thread::join_handle::JoinHandle"><code>JoinHandle</code> type</a>, if the spawned\ntask panics, awaiting its <code>JoinHandle</code> will return a <a href="struct.JoinError.html" title="struct tokio::task::JoinError"><code>JoinError</code></a>. For\nexample:</p>',
      '<p>同样，与 <code>std::thread</code> 的 <a href="https://doc.rust-lang.org/1.95.0/std/thread/join_handle/struct.JoinHandle.html" title="struct std::thread::join_handle::JoinHandle"><code>JoinHandle</code> 类型</a>类似，如果已派生任务 panic，则 await 其 <code>JoinHandle</code> 将返回一个 <a href="struct.JoinError.html" title="struct tokio::task::JoinError"><code>JoinError</code></a>。例如：</p>'),

    # "spawn, JoinHandle, and JoinError are present when the 'rt' feature flag is enabled."
    P('<p><code>spawn</code>, <code>JoinHandle</code>, and <code>JoinError</code> are present when the “rt”\nfeature flag is enabled.</p>',
      '<p><code>spawn</code>、<code>JoinHandle</code> 和 <code>JoinError</code> 在启用 “rt” feature flag 时可用。</p>'),

    # "Spawned tasks may be cancelled..."
    P('<p>Spawned tasks may be cancelled using the <a href="struct.JoinHandle.html#method.abort" title="method tokio::task::JoinHandle::abort"><code>JoinHandle::abort</code></a> or\n<a href="struct.AbortHandle.html#method.abort" title="method tokio::task::AbortHandle::abort"><code>AbortHandle::abort</code></a> methods. When one of these methods are called, the\ntask is signalled to shut down next time it yields at an <code>.await</code> point. If\nthe task is already idle, then it will be shut down as soon as possible\nwithout running again before being shut down. Additionally, shutting down a\nTokio runtime (e.g. by returning from <code>#[tokio::main]</code>) immediately cancels\nall tasks on it.</p>',
      '<p>已派生任务可以使用 <a href="struct.JoinHandle.html#method.abort" title="method tokio::task::JoinHandle::abort"><code>JoinHandle::abort</code></a> 或 <a href="struct.AbortHandle.html#method.abort" title="method tokio::task::AbortHandle::abort"><code>AbortHandle::abort</code></a> 方法取消。当调用这些方法之一时，任务会在下一次在 <code>.await</code> 点让出时被通知关闭。如果任务已经处于空闲状态，则会尽快关闭，且在关闭之前不再运行一次。此外，关闭 Tokio runtime（例如通过从 <code>#[tokio::main]</code> 返回）会立即取消该 runtime 上的所有任务。</p>'),

    # "When tasks are shut down..."
    P('<p>When tasks are shut down, it will stop running at whichever <code>.await</code> it has\nyielded at. All local variables are destroyed by running their destructor.\nOnce shutdown has completed, awaiting the <a href="struct.JoinHandle.html" title="struct tokio::task::JoinHandle"><code>JoinHandle</code></a> will fail with a\n<a href="struct.JoinError.html#method.is_cancelled" title="method tokio::task::JoinError::is_cancelled">cancelled error</a>.</p>',
      '<p>当任务被关闭时，它将在当前让出的 <code>.await</code> 处停止运行。所有局部变量都会通过运行其析构函数被销毁。一旦关闭完成，await <a href="struct.JoinHandle.html" title="struct tokio::task::JoinHandle"><code>JoinHandle</code></a> 将失败并返回 <a href="struct.JoinError.html#method.is_cancelled" title="method tokio::task::JoinError::is_cancelled">取消错误</a>。</p>'),

    # "Note that aborting a task does not guarantee..."
    P('<p>Note that aborting a task does not guarantee that it fails with a cancelled\nerror, since it may complete normally first. For example, if the task does\nnot yield to the runtime at any point between the call to <code>abort</code> and the\nend of the task, then the <a href="struct.JoinHandle.html" title="struct tokio::task::JoinHandle"><code>JoinHandle</code></a> will instead report that the task\nexited normally.</p>',
      '<p>请注意，终止一个任务并不保证它会以取消错误失败，因为它可能先正常完成。例如，如果在调用 <code>abort</code> 与任务结束之间的任何时刻，该任务都没有让出 runtime，那么 <a href="struct.JoinHandle.html" title="struct tokio::task::JoinHandle"><code>JoinHandle</code></a> 将改为报告任务已正常退出。</p>'),

    # "Be aware that tasks spawned using spawn_blocking cannot be aborted..."
    P('<p>Be aware that tasks spawned using <a href="fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> cannot be aborted\nbecause they are not async. If you call <code>abort</code> on a <code>spawn_blocking</code>\ntask, then this <em>will not have any effect</em>, and the task will continue\nrunning normally. The exception is if the task has not started running\nyet; in that case, calling <code>abort</code> may prevent the task from starting.</p>',
      '<p>请注意，使用 <a href="fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>spawn_blocking</code></a> 派生的任务无法被终止，因为它们不是异步的。如果你对 <code>spawn_blocking</code> 任务调用 <code>abort</code>，则<em>不会产生任何效果</em>，任务将继续正常运行。例外情况是该任务尚未开始运行；此时调用 <code>abort</code> 可能会阻止该任务启动。</p>'),

    # "Be aware that calls to JoinHandle::abort..."
    P('<p>Be aware that calls to <a href="struct.JoinHandle.html#method.abort" title="method tokio::task::JoinHandle::abort"><code>JoinHandle::abort</code></a> just schedule the task for\ncancellation, and will return before the cancellation has completed. To wait\nfor cancellation to complete, wait for the task to finish by awaiting the\n<a href="struct.JoinHandle.html" title="struct tokio::task::JoinHandle"><code>JoinHandle</code></a>. Similarly, the <a href="struct.JoinHandle.html#method.is_finished" title="method tokio::task::JoinHandle::is_finished"><code>JoinHandle::is_finished</code></a> method does not\nreturn <code>true</code> until the cancellation has finished.</p>',
      '<p>请注意，对 <a href="struct.JoinHandle.html#method.abort" title="method tokio::task::JoinHandle::abort"><code>JoinHandle::abort</code></a> 的调用只是将任务调度为待取消状态，并在取消完成之前就会返回。要等待取消完成，可通过 await <a href="struct.JoinHandle.html" title="struct tokio::task::JoinHandle"><code>JoinHandle</code></a> 来等待任务结束。类似地，<a href="struct.JoinHandle.html#method.is_finished" title="method tokio::task::JoinHandle::is_finished"><code>JoinHandle::is_finished</code></a> 方法在取消完成之前不会返回 <code>true</code>。</p>'),

    # "Calling JoinHandle::abort multiple times..."
    P('<p>Calling <a href="struct.JoinHandle.html#method.abort" title="method tokio::task::JoinHandle::abort"><code>JoinHandle::abort</code></a> multiple times has the same effect as calling\nit once.</p>',
      '<p>多次调用 <a href="struct.JoinHandle.html#method.abort" title="method tokio::task::JoinHandle::abort"><code>JoinHandle::abort</code></a> 与仅调用一次效果相同。</p>'),

    # "Tokio also provides an AbortHandle..."
    P('<p>Tokio also provides an <a href="struct.AbortHandle.html" title="struct tokio::task::AbortHandle"><code>AbortHandle</code></a>, which is like the <a href="struct.JoinHandle.html" title="struct tokio::task::JoinHandle"><code>JoinHandle</code></a>,\nexcept that it does not provide a mechanism to wait for the task to finish.\nEach task can only have one <a href="struct.JoinHandle.html" title="struct tokio::task::JoinHandle"><code>JoinHandle</code></a>, but it can have more than one\n<a href="struct.AbortHandle.html" title="struct tokio::task::AbortHandle"><code>AbortHandle</code></a>.</p>',
      '<p>Tokio 还提供了 <a href="struct.AbortHandle.html" title="struct tokio::task::AbortHandle"><code>AbortHandle</code></a>，它与 <a href="struct.JoinHandle.html" title="struct tokio::task::JoinHandle"><code>JoinHandle</code></a> 类似，但它不提供等待任务完成的机制。每个任务只能拥有一个 <a href="struct.JoinHandle.html" title="struct tokio::task::JoinHandle"><code>JoinHandle</code></a>，但可以拥有多个 <a href="struct.AbortHandle.html" title="struct tokio::task::AbortHandle"><code>AbortHandle</code></a>。</p>'),

    # "As we discussed above, code running in asynchronous tasks should not perform operations that can block..."
    P('<p>As we discussed above, code running in asynchronous tasks should not perform\noperations that can block. A blocking operation performed in a task running\non a thread that is also running other tasks would block the entire thread,\npreventing other tasks from running.</p>',
      '<p>如上所述，在异步任务中运行的代码不应执行可能阻塞的操作。在运行其他任务的线程上，某个任务执行的阻塞操作将阻塞整个线程，从而阻止其他任务的运行。</p>'),

    # "Instead, Tokio provides two APIs for running blocking operations..."
    P('<p>Instead, Tokio provides two APIs for running blocking operations in an\nasynchronous context: <a href="fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>task::spawn_blocking</code></a> and <a href="fn.block_in_place.html" title="fn tokio::task::block_in_place"><code>task::block_in_place</code></a>.</p>',
      '<p>为此，Tokio 提供了两个用于在异步上下文中运行阻塞操作的 API：<a href="fn.spawn_blocking.html" title="fn tokio::task::spawn_blocking"><code>task::spawn_blocking</code></a> 和 <a href="fn.block_in_place.html" title="fn tokio::task::block_in_place"><code>task::block_in_place</code></a>。</p>'),

    # "Be aware that if you call a non-async method from async code, that non-async method is still inside..."
    P('<p>Be aware that if you call a non-async method from async code, that non-async\nmethod is still inside the asynchronous context, so you should also avoid\nblocking operations there. This includes destructors of objects destroyed in\nasync code.</p>',
      '<p>请注意，如果你在异步代码中调用非 async 方法，该非 async 方法仍处于异步上下文之中，因此你也应避免在那里执行阻塞操作。这包括在异步代码中被销毁的对象的析构函数。</p>'),

    # "The task::spawn_blocking function is similar to the task::spawn function..."
    P('<p>The <code>task::spawn_blocking</code> function is similar to the <code>task::spawn</code> function\ndiscussed in the previous section, but rather than spawning a\n<em>non-blocking</em> future on the Tokio runtime, it instead spawns a\n<em>blocking</em> function on a dedicated thread pool for blocking tasks. For\nexample:</p>',
      '<p><code>task::spawn_blocking</code> 函数与上一节讨论的 <code>task::spawn</code> 函数类似，但后者是在 Tokio runtime 上派生<em>非阻塞</em>的 future，而前者则是在专门用于阻塞任务的线程池上派生<em>阻塞</em>函数。例如：</p>'),

    # "Just like task::spawn, task::spawn_blocking returns a JoinHandle..."
    P('<p>Just like <code>task::spawn</code>, <code>task::spawn_blocking</code> returns a <code>JoinHandle</code>\nwhich we can use to await the result of the blocking operation:</p>',
      '<p>与 <code>task::spawn</code> 一样，<code>task::spawn_blocking</code> 也会返回一个 <code>JoinHandle</code>，可用于 await 阻塞操作的结果：</p>'),

    # "When using the multi-threaded runtime..."
    P('<p>When using the <a href="../runtime/index.html#threaded-scheduler">multi-threaded runtime</a>, the <a href="fn.block_in_place.html" title="fn tokio::task::block_in_place"><code>task::block_in_place</code></a>\nfunction is also available. Like <code>task::spawn_blocking</code>, this function\nallows running a blocking operation from an asynchronous context. Unlike\n<code>spawn_blocking</code>, however, <code>block_in_place</code> works by transitioning the\n<em>current</em> worker thread to a blocking thread, moving other tasks running on\nthat thread to another worker thread. This can improve performance by avoiding\ncontext switches.</p>',
      '<p>在使用<a href="../runtime/index.html#threaded-scheduler">多线程 runtime</a>时，还可以使用 <a href="fn.block_in_place.html" title="fn tokio::task::block_in_place"><code>task::block_in_place</code></a> 函数。与 <code>task::spawn_blocking</code> 类似，该函数允许在异步上下文中运行阻塞操作。但与 <code>spawn_blocking</code> 不同，<code>block_in_place</code> 通过将<em>当前</em> worker 线程转变为阻塞线程，并把该线程上运行的其他任务转移到另一个 worker 线程上来工作。这可以通过避免上下文切换来提升性能。</p>'),

    # "In addition, this module provides a task::yield_now..."
    P('<p>In addition, this module provides a <a href="fn.yield_now.html" title="fn tokio::task::yield_now"><code>task::yield_now</code></a> async function\nthat is analogous to the standard library’s <a href="https://doc.rust-lang.org/1.95.0/std/thread/functions/fn.yield_now.html" title="fn std::thread::functions::yield_now"><code>thread::yield_now</code></a>. Calling\nand <code>await</code>ing this function will cause the current task to yield to the\nTokio runtime’s scheduler, allowing other tasks to be\nscheduled. Eventually, the yielding task will be polled again, allowing it\nto execute. For example:</p>',
      '<p>此外，本模块还提供了一个 <a href="fn.yield_now.html" title="fn tokio::task::yield_now"><code>task::yield_now</code></a> 异步函数，它类似于标准库的 <a href="https://doc.rust-lang.org/1.95.0/std/thread/functions/fn.yield_now.html" title="fn std::thread::functions::yield_now"><code>thread::yield_now</code></a>。调用并 <code>await</code> 此函数将使当前任务让出给 Tokio runtime 的调度器，从而允许调度其他任务。最终，让出的任务将再次被 poll 以允许其执行。例如：</p>'),

    # Module index <dd> entries (these go in task/index.html, not the function pages)
    P('<dd>Runs the provided blocking function on the current thread without\nblocking the executor.</dd>',
      '<dd>在当前线程上运行提供的阻塞函数，但不会阻塞 executor。</dd>'),
]


FILES = [
    ('tokio/task/struct.JoinSet.html', JOINSET_PAIRS),
    ('tokio/task/struct.AbortHandle.html', ABORTHANDLE_PAIRS),
    ('tokio/task/struct.JoinError.html', JOINERROR_PAIRS),
    ('tokio/task/struct.JoinHandle.html', JOINHANDLE_PAIRS),
    ('tokio/task/struct.LocalKey.html', LOCALKEY_PAIRS),
    ('tokio/task/struct.LocalSet.html', LOCALSET_PAIRS),
    ('tokio/task/coop/struct.RestoreOnPending.html', RESTOREONPENDING_PAIRS),
    ('tokio/task/futures/struct.TaskLocalFuture.html', TASKLOCALFUTURE_PAIRS),
    ('tokio/task/index.html', TASK_INDEX_PAIRS),
]


def apply_pair(path, en_str, zh_str):
    """Apply a single (en, zh) pair to file. Returns True if replaced.

    Expands \\n to both LF and CRLF forms to match either line ending style.
    """
    en_bytes = en_str.encode('utf-8')
    zh_bytes = zh_str.encode('utf-8')
    with open(path, 'rb') as f:
        raw = f.read()
    # Try LF form first, then CRLF
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