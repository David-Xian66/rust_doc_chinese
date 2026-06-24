// 中文文档内容搜索 (MiniSearch)
// 由 build_chinese_index.py 生成的 JSON 索引驱动
// 搜索范围：当前 crate 的翻译文档内容（docblock 描述、模块说明等）
// 不依赖 rustdoc 主搜索 —— 完全独立的 UI 与索引

(function () {
    'use strict';

    // ===== 配置 =====
    var INDEX_DIR = 'chinese-index';
    var SCOPE_ALL = '__all__';

    // ===== 状态 =====
    var currentCrate = null;
    var currentScope = null; // 'crate' 或 SCOPE_ALL
    var crateIndex = null;   // 当前 crate 的索引数组（原始 entries）
    var allIndex = null;     // 全局索引数组
    var miniSearch = null;
    var lastQuery = '';
    var allJsonLoaded = false;

    // 当前页面所在的 crate 名（从路径推断）
    function detectCrate() {
        var path = window.location.pathname;
        // 形如 /quinn/struct.Endpoint.html 或 /tokio/runtime/...
        var m = path.match(/^\/([^\/]+)\//);
        if (m) return m[1];
        // 文件直接在根（index.html）
        return null;
    }

    // 绝对路径 — 不依赖页面深度，根路径部署时（Cloudflare Pages / 本地 http.server）
    // 始终用 /static.files/... 解析到正确位置
    //
    // scope 取值：
    //   - SCOPE_ALL ('__all__')        → 全局 all.json
    //   - 'crate'                      → 当前 crate 的 <currentCrate>.json
    //   - 其他字符串（具体 crate 名）   → 该 crate 的 .json
    //
    // 注意：之前实现直接把 scope 当文件名拼，'crate' → /chinese-index/crate.json（不存在 → 404 HTML）
    function indexUrl(scope) {
        if (scope === SCOPE_ALL) {
            return '/static.files/' + INDEX_DIR + '/all.json';
        }
        // 'crate' 是占位语义：实际指向当前 crate
        var crateName = (scope === 'crate') ? currentCrate : scope;
        if (!crateName) return null; // 无 crate 可用（例如根页面选"本 crate"），调用方须处理
        return '/static.files/' + INDEX_DIR + '/' + crateName + '.json';
    }

    // sessionStorage 缓存
    function cacheKey(url) { return 'chi-search-idx:' + url; }

    function fetchJson(url) {
        if (!url) {
            return Promise.reject(new Error('索引 URL 为空（无法识别当前 crate）'));
        }
        var cached = sessionStorage.getItem(cacheKey(url));
        if (cached) return Promise.resolve(JSON.parse(cached));
        return fetch(url).then(function (r) {
            if (!r.ok) throw new Error('HTTP ' + r.status + ' for ' + url);
            return r.json();
        }).then(function (data) {
            try { sessionStorage.setItem(cacheKey(url), JSON.stringify(data)); } catch (e) { /* quota */ }
            return data;
        });
    }

    // 加载索引
    function loadIndex(scope) {
        if (scope === SCOPE_ALL) {
            if (allIndex) return Promise.resolve(allIndex);
            return fetchJson(indexUrl(SCOPE_ALL)).then(function (data) {
                allIndex = data;
                allJsonLoaded = true;
                return data;
            });
        }
        if (currentScope === scope && crateIndex) return Promise.resolve(crateIndex);
        return fetchJson(indexUrl(scope)).then(function (data) {
            crateIndex = data;
            currentScope = scope;
            return data;
        });
    }

    // MiniSearch 包装
    function buildMiniSearch(entries) {
        return new MiniSearch({
            // 用 url 作为主键（每条目天然唯一），避免 MiniSearch 报
            // "document does not have ID field 'id'"
            idField: 'url',
            fields: ['title', 'desc', 'section_headers', 'module_doc', 'crate'],
            storeFields: ['url', 'crate', 'title', 'section', 'module_doc'],
            searchOptions: {
                boost: { title: 3, module_doc: 2 },
                prefix: true,
                fuzzy: 0.2,
                combineWith: 'AND',
            },
        }).addAll(entries);
    }

    function ensureSearch(entries) {
        if (miniSearch) return miniSearch;
        miniSearch = buildMiniSearch(entries);
        return miniSearch;
    }

    // ===== UI 创建 =====
    function createButton() {
        // 不再附加到 <rustdoc-topbar> 的 light DOM（flex 布局 + h2 的 margin:auto
        // 会把它挤到不可见区域，桌面端表现就是按钮消失，只在 400px 等窄屏能看到）。
        // 改为挂到 <body> 上，用 fixed 定位浮在右上角 —— 与 topbar 内的原生「搜索」
        // 按钮并排，互不干扰，桌面端始终可见。
        var btn = document.createElement('a');
        btn.id = 'chinese-search-button';
        btn.href = '?chinese-search#';
        btn.className = 'chinese-search-menu';
        btn.textContent = '搜索文档';
        btn.title = '搜索已翻译的文档内容（按 S 或 / 触发）';
        btn.style.cssText = [
            'position:fixed',
            'top:8px',
            'right:80px',     // 给原生 搜索 按钮（最右侧 ~80px 宽）让位，避免重叠
            'z-index:11',     // 略高于 rustdoc-topbar 的 z-index:10
            'display:inline-flex',
            'align-items:center',
            'padding:6px 14px',
            'border:1px solid var(--border-color,#ccc)',
            'border-radius:4px',
            'background:var(--main-background-color,#fff)',
            'color:var(--main-color,#222)',
            'text-decoration:none',
            'font-size:14px',
            'line-height:1.25',
            'cursor:pointer',
            'box-shadow:0 1px 2px rgba(0,0,0,0.05)',
        ].join(';');
        return btn;
    }

    function createPanel() {
        var panel = document.createElement('div');
        panel.id = 'chinese-search-panel';
        panel.style.cssText = [
            'display:none',
            'position:fixed',
            'top:50px',
            'right:20px',
            'width:540px',
            'max-width:calc(100vw - 40px)',
            'max-height:70vh',
            'background:#fff',
            'border:1px solid #ccc',
            'border-radius:6px',
            'box-shadow:0 6px 20px rgba(0,0,0,0.25)',
            'z-index:9999',
            'font-family:sans-serif',
            'font-size:14px',
            'color:#222',
            'overflow:hidden',
            'flex-direction:column',
        ].join(';');

        // 头部
        var header = document.createElement('div');
        header.style.cssText = 'padding:10px;border-bottom:1px solid #eee;display:flex;gap:8px;align-items:center';

        var input = document.createElement('input');
        input.type = 'search';
        input.id = 'chinese-search-input';
        input.placeholder = '输入中文关键词（描述、模块说明等）';
        input.style.cssText = 'flex:1;padding:6px 10px;font-size:15px;border:1px solid #aaa;border-radius:4px';

        var scopeSelect = document.createElement('select');
        scopeSelect.id = 'chinese-search-scope';
        scopeSelect.style.cssText = 'padding:5px;font-size:13px';
        scopeSelect.innerHTML = '<option value="crate">本 crate</option><option value="' + SCOPE_ALL + '">所有 crates</option>';

        var closeBtn = document.createElement('button');
        closeBtn.textContent = '×';
        closeBtn.title = '关闭';
        closeBtn.style.cssText = 'padding:0 8px;font-size:18px;border:none;background:transparent;cursor:pointer';

        header.appendChild(input);
        header.appendChild(scopeSelect);
        header.appendChild(closeBtn);

        // 状态
        var status = document.createElement('div');
        status.id = 'chinese-search-status';
        status.style.cssText = 'padding:6px 10px;font-size:12px;color:#888;border-bottom:1px solid #f0f0f0';

        // 结果区
        var results = document.createElement('div');
        results.id = 'chinese-search-results';
        results.style.cssText = 'overflow-y:auto;max-height:calc(70vh - 100px)';

        panel.appendChild(header);
        panel.appendChild(status);
        panel.appendChild(results);

        // 事件
        closeBtn.onclick = function () { panel.style.display = 'none'; };

        scopeSelect.onchange = function () {
            var scope = scopeSelect.value;
            if (scope === SCOPE_ALL && !allJsonLoaded) {
                status.textContent = '正在加载全局索引…';
                loadIndex(SCOPE_ALL).then(function () {
                    runSearch(input.value, scope);
                });
            } else {
                runSearch(input.value, scope);
            }
        };

        var debounceTimer = null;
        input.oninput = function () {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(function () {
                runSearch(input.value, scopeSelect.value);
            }, 200);
        };

        input.onkeydown = function (e) {
            if (e.key === 'Escape') panel.style.display = 'none';
        };

        return panel;
    }

    function runSearch(query, scope) {
        var status = document.getElementById('chinese-search-status');
        var results = document.getElementById('chinese-search-results');
        if (!query || query.length < 1) {
            status.textContent = '请输入关键词';
            results.innerHTML = '';
            return;
        }
        lastQuery = query;

        // 根页面（currentCrate 为空）强制使用全局索引
        var effectiveScope = (!currentCrate && scope !== SCOPE_ALL) ? SCOPE_ALL : scope;
        // 同步下拉框显示
        var sel = document.getElementById('chinese-search-scope');
        if (sel && sel.value !== effectiveScope) sel.value = effectiveScope;

        loadIndex(effectiveScope).then(function (entries) {
            var ms = ensureSearch(entries);
            var hits = ms.search(query);
            status.textContent = '找到 ' + hits.length + ' 条结果' +
                (effectiveScope === SCOPE_ALL ? '（所有 crates）' : '（' + currentCrate + '）');
            renderResults(hits);
        }).catch(function (err) {
            status.textContent = '加载索引失败：' + err.message;
        });
    }

    function renderResults(hits) {
        var results = document.getElementById('chinese-search-results');
        results.innerHTML = '';
        if (hits.length === 0) {
            results.innerHTML = '<div style="padding:20px;color:#888;text-align:center">无匹配结果</div>';
            return;
        }
        var max = Math.min(hits.length, 50);
        for (var i = 0; i < max; i++) {
            var h = hits[i];
            var div = document.createElement('div');
            div.style.cssText = 'padding:8px 10px;border-bottom:1px solid #f0f0f0;cursor:pointer';
            div.onmouseover = function () { this.style.background = '#f5f5f5'; };
            div.onmouseout = function () { this.style.background = ''; };
            div.onclick = function (url) {
                return function () { window.location.href = url; };
            }(h.url);

            var title = document.createElement('div');
            title.style.cssText = 'font-weight:bold;color:#2a6f97;font-size:13px';
            title.textContent = '[' + (h.crate || '') + '] ' + (h.title || h.url);

            var moduleDoc = document.createElement('div');
            moduleDoc.style.cssText = 'color:#444;font-size:12px;margin-top:2px';
            moduleDoc.textContent = (h.module_doc || '').slice(0, 200);

            var urlDiv = document.createElement('div');
            urlDiv.style.cssText = 'color:#999;font-size:11px;margin-top:2px';
            urlDiv.textContent = h.url;

            div.appendChild(title);
            div.appendChild(moduleDoc);
            div.appendChild(urlDiv);
            results.appendChild(div);
        }
        if (hits.length > max) {
            var more = document.createElement('div');
            more.style.cssText = 'padding:10px;text-align:center;color:#888;font-size:12px';
            more.textContent = '还有 ' + (hits.length - max) + ' 条结果未显示，请缩小查询范围';
            results.appendChild(more);
        }
    }

    // ===== 触发与打开 =====
    function openPanel() {
        var panel = document.getElementById('chinese-search-panel');
        if (!panel) return;
        panel.style.display = 'flex';
        var input = document.getElementById('chinese-search-input');
        if (input) {
            input.focus();
            input.select();
        }
    }

    // ===== 初始化 =====
    function init() {
        currentCrate = detectCrate();

        // 注入按钮到 <body>（不再用 rustdoc-topbar —— topbar 的 flex 布局 + h2 的
        // margin:auto 在桌面端会把按钮挤到不可见区域）。固定定位浮在右上角，与
        // topbar 内的原生「搜索」按钮并排显示，桌面与移动端均可见。
        if (!document.body) return;
        var btn = createButton();
        btn.onclick = function (e) {
            e.preventDefault();
            openPanel();
        };
        document.body.appendChild(btn);

        // 根页面（currentCrate 为空）— 隐藏「本 crate」选项，默认全局
        if (!currentCrate) {
            var sel = document.getElementById('chinese-search-scope');
            if (sel) {
                sel.value = SCOPE_ALL;
                var crateOpt = sel.querySelector('option[value="crate"]');
                if (crateOpt) crateOpt.disabled = true;
            }
        }

        // 注入面板
        var panel = createPanel();
        document.body.appendChild(panel);

        // 键盘快捷键 S / /
        document.addEventListener('keydown', function (e) {
            // 不在输入框中时触发
            var tag = (e.target.tagName || '').toLowerCase();
            if (tag === 'input' || tag === 'textarea') return;
            if (e.key === 's' || e.key === 'S' || e.key === '/') {
                // 避免和原生搜索冲突：原生用 S 时会触发自己
                // 我们同时打开中文面板，用户可以同时搜
                e.preventDefault();
                openPanel();
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();