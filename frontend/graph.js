// ========================
// 基础配置
// ========================
const API = "http://127.0.0.1:8000";
const BOOK_COLORS = ["#3b82f6", "#22c55e", "#f59e0b", "#ef4444", "#8b5cf6"];

const canvas = document.getElementById("graph");
const ctx = canvas.getContext("2d");
const runSelect = document.getElementById("runSelect");
const themeToggle = document.getElementById("themeToggle");
const tooltip = document.getElementById("tooltip");

const state = {
    graph: null,
    expandedBooks: new Set(),
    nodes: [],
    links: [],
    simulation: null,
    transform: d3.zoomIdentity,
    hoveredNode: null,
    dimensions: { width: window.innerWidth, height: window.innerHeight },
    theme: "light",
    animationFrame: null,
};

const ActionTypes = {
    SET_GRAPH: "SET_GRAPH",
    TOGGLE_BOOK: "TOGGLE_BOOK",
    SET_HOVERED_NODE: "SET_HOVERED_NODE",
    SET_TRANSFORM: "SET_TRANSFORM",
    SET_THEME: "SET_THEME",
    RESIZE: "RESIZE",
};

function dispatch(action) {
    switch (action.type) {
        case ActionTypes.SET_GRAPH: {
            state.graph = action.payload.graph;
            state.expandedBooks.clear();
            rebuildGraph();
            break;
        }
        case ActionTypes.TOGGLE_BOOK: {
            const bookId = action.payload.bookId;
            if (state.expandedBooks.has(bookId)) {
                state.expandedBooks.delete(bookId);
            } else {
                state.expandedBooks.add(bookId);
            }
            rebuildGraph();
            break;
        }
        case ActionTypes.SET_HOVERED_NODE: {
            state.hoveredNode = action.payload.node;
            break;
        }
        case ActionTypes.SET_TRANSFORM: {
            state.transform = action.payload.transform;
            break;
        }
        case ActionTypes.SET_THEME: {
            state.theme = action.payload.theme;
            document.documentElement.dataset.theme =
                state.theme === "dark" ? "dark" : "light";
            if (themeToggle) {
                themeToggle.textContent =
                    state.theme === "dark" ? "Theme: Dark" : "Theme: Light";
            }
            break;
        }
        case ActionTypes.RESIZE: {
            state.dimensions = action.payload.dimensions;
            canvas.width = state.dimensions.width;
            canvas.height = state.dimensions.height;
            rebuildGraph();
            break;
        }
        default:
            console.warn("Unknown action", action);
    }
}

function resize() {
    dispatch({
        type: ActionTypes.RESIZE,
        payload: {
            dimensions: { width: window.innerWidth, height: window.innerHeight },
        },
    });
}

resize();
window.addEventListener("resize", resize);

function setTheme(theme) {
    dispatch({ type: ActionTypes.SET_THEME, payload: { theme } });
}

setTheme("light");

if (themeToggle) {
    themeToggle.addEventListener("click", () => {
        setTheme(state.theme === "dark" ? "light" : "dark");
    });
}

// ========================
// 工具函数
// ========================
function getBookRadius(node) {
    const count = node.chapterCount ?? 1;
    return 12 + Math.sqrt(Math.max(count, 1)) * 2.2;
}

function getNodeRadius(node) {
    return node.type === "book" ? getBookRadius(node) : 5.5;
}

function findNodeAtPosition(x, y) {
    for (let i = state.nodes.length - 1; i >= 0; i -= 1) {
        const n = state.nodes[i];
        if (n.x == null || n.y == null) continue;
        const r = getNodeRadius(n);
        const dx = x - n.x;
        const dy = y - n.y;
        if (dx * dx + dy * dy <= r * r) return n;
    }
    return null;
}

// ========================
// 加载 runs
// ========================
fetch(`${API}/runs`)
    .then(res => res.json())
    .then(runs => {
        runSelect.innerHTML = "";

        runs.forEach(run => {
            const option = document.createElement("option");
            option.value = run.id;
            option.text = `run ${run.id} (${run.book_ids.join(", ")})`;
            runSelect.appendChild(option);
        });

        if (runs.length > 0) {
            loadGraph(runs[0].id);
        }
    })
    .catch(err => {
        console.error(err);
        runSelect.innerHTML = "<option>failed to load runs</option>";
    });

// ========================
// run 切换
// ========================
runSelect.addEventListener("change", () => {
    loadGraph(runSelect.value);
});

// ========================
// 加载 graph
// ========================
function loadGraph(runId) {
    fetch(`${API}/graph?run_id=${runId}`)
        .then(res => res.json())
        .then(data => {
            dispatch({ type: ActionTypes.SET_GRAPH, payload: { graph: data } });
        })
        .catch(console.error);
}

// ========================
// 构建节点/边
// ========================
function rebuildGraph() {
    if (!state.graph) return;

    const books = state.graph.nodes.filter(n => n.type === "book");
    const chapters = state.graph.nodes.filter(n => n.type === "chapter");

    const chapterCountMap = new Map();
    chapters.forEach(c => {
        chapterCountMap.set(
            c.book_id,
            (chapterCountMap.get(c.book_id) ?? 0) + 1,
        );
    });

    const bookColorMap = new Map();
    books.forEach((b, i) => {
        bookColorMap.set(b.id, BOOK_COLORS[i % BOOK_COLORS.length]);
    });

    const prevPositions = new Map();
    state.nodes.forEach(n => {
        if (n.x != null && n.y != null) {
            prevPositions.set(n.id, { x: n.x, y: n.y, fx: n.fx, fy: n.fy });
        }
    });

    const chapterCentroids = new Map();
    state.nodes.forEach(n => {
        if (n.type !== "chapter" || n.x == null || n.y == null) return;
        const current = chapterCentroids.get(n.bookId) ?? { x: 0, y: 0, count: 0 };
        chapterCentroids.set(n.bookId, {
            x: current.x + n.x,
            y: current.y + n.y,
            count: current.count + 1,
        });
    });

    const nextNodes = [];
    const nextLinks = [];
    const visibleChapterIds = new Set();

    books.forEach(book => {
        const color = bookColorMap.get(book.id);
        const bookKey = `book-${book.id}`;

        if (state.expandedBooks.has(book.id)) {
            const base = prevPositions.get(bookKey);
            const centroid = chapterCentroids.get(book.id);
            const bx = base?.x ??
                (centroid ? centroid.x / centroid.count : state.dimensions.width / 2);
            const by = base?.y ??
                (centroid ? centroid.y / centroid.count : state.dimensions.height / 2);

            const bookChapters = chapters.filter(c => c.book_id === book.id);
            bookChapters.forEach((c, i) => {
                const id = `chapter-${c.id}`;
                const prev = prevPositions.get(id);
                const angle = i * 0.55;
                const radius = 10 + i * 3.2;

                nextNodes.push({
                    id,
                    type: "chapter",
                    bookId: book.id,
                    label: c.title ? `${c.title}` : c.id,
                    chapterId: c.id,
                    color,
                    x: prev?.x ?? bx + Math.cos(angle) * radius,
                    y: prev?.y ?? by + Math.sin(angle) * radius,
                    fx: prev?.fx,
                    fy: prev?.fy,
                });
                visibleChapterIds.add(id);
            });
        } else {
            const prev = prevPositions.get(bookKey);
            nextNodes.push({
                id: bookKey,
                type: "book",
                bookId: book.id,
                label: book.id,
                color,
                chapterCount: chapterCountMap.get(book.id) ?? book.size,
                x: prev?.x,
                y: prev?.y,
                fx: prev?.fx,
                fy: prev?.fy,
            });
        }
    });

    state.graph.edges.forEach(e => {
        const s = `chapter-${e.source}`;
        const t = `chapter-${e.target}`;
        if (visibleChapterIds.has(s) && visibleChapterIds.has(t)) {
            nextLinks.push({ source: s, target: t, score: e.score });
        }
    });

    state.nodes = nextNodes;
    state.links = nextLinks;

    if (state.simulation) state.simulation.stop();
    state.simulation = d3
        .forceSimulation(state.nodes)
        .force(
            "link",
            d3.forceLink(state.links)
                .id(d => d.id)
                .strength(d => Math.min(0.2, d.score))
                .distance(d => 20 + (1 - d.score) * 60),
        )
        .force("charge", d3.forceManyBody().strength(-30))
        .force(
            "center",
            d3.forceCenter(state.dimensions.width / 2, state.dimensions.height / 2),
        );
}

// ========================
// 绘制
// ========================
function draw() {
    if (!ctx) return;
    const { nodes, links, transform, hoveredNode, dimensions } = state;
    const t = transform;
    const styles = getComputedStyle(document.documentElement);
    const edgeBase = styles.getPropertyValue("--edge").trim() || "rgba(100,116,139,0.22)";
    const textColor = styles.getPropertyValue("--text").trim() || "#0f172a";

    ctx.save();
    ctx.clearRect(0, 0, dimensions.width, dimensions.height);
    ctx.translate(t.x, t.y);
    ctx.scale(t.k, t.k);

    links.forEach(l => {
        const s = typeof l.source === "string" ? nodes.find(n => n.id === l.source) : l.source;
        const tg = typeof l.target === "string" ? nodes.find(n => n.id === l.target) : l.target;
        if (!s || !tg || s.x == null || s.y == null || tg.x == null || tg.y == null) return;

        ctx.strokeStyle = edgeBase.replace(/[\d.]+\)$/g, `${0.1 + l.score * 0.8})`);
        ctx.lineWidth = 0.5 + l.score * 2;
        ctx.beginPath();
        ctx.moveTo(s.x, s.y);
        ctx.lineTo(tg.x, tg.y);
        ctx.stroke();
    });

    nodes.forEach(n => {
        if (n.x == null || n.y == null) return;
        const radius = getNodeRadius(n);
        ctx.beginPath();
        ctx.arc(n.x, n.y, radius, 0, Math.PI * 2);
        ctx.fillStyle = n.color;
        ctx.fill();

        if (n.type === "book") {
            ctx.fillStyle = textColor;
            ctx.font = "12px sans-serif";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.fillText(String(n.chapterCount ?? 0), n.x, n.y);
        }
    });

    if (hoveredNode?.x != null && hoveredNode.y != null) {
        ctx.beginPath();
        ctx.arc(
            hoveredNode.x,
            hoveredNode.y,
            getNodeRadius(hoveredNode) + 4,
            0,
            Math.PI * 2,
        );
        ctx.strokeStyle = textColor;
        ctx.lineWidth = 2;
        ctx.stroke();
    }

    ctx.restore();
}

function render() {
    draw();
    state.animationFrame = requestAnimationFrame(render);
}

render();

// ========================
// 缩放、悬停、双击
// ========================
const zoomBehavior = d3
    .zoom()
    .scaleExtent([0.2, 5])
    .filter(event => event.type !== "dblclick")
    .on("zoom", event => {
        dispatch({
            type: ActionTypes.SET_TRANSFORM,
            payload: { transform: event.transform },
        });
    });

d3.select(canvas).call(zoomBehavior);

canvas.addEventListener("mousemove", event => {
    const rect = canvas.getBoundingClientRect();
    const x = (event.clientX - rect.left - state.transform.x) / state.transform.k;
    const y = (event.clientY - rect.top - state.transform.y) / state.transform.k;
    const hit = findNodeAtPosition(x, y);
    dispatch({ type: ActionTypes.SET_HOVERED_NODE, payload: { node: hit } });
    canvas.style.cursor = hit ? "pointer" : "default";

    if (tooltip) {
        if (hit) {
            tooltip.style.opacity = "1";
            tooltip.style.left = `${event.clientX + 12}px`;
            tooltip.style.top = `${event.clientY + 12}px`;
            const typeLabel = hit.type === "book" ? "Book" : "Chapter";
            tooltip.innerHTML = `
                <div style="font-weight:600;margin-bottom:4px;">${hit.label}</div>
                <div style="opacity:0.75;">${typeLabel}</div>
            `;
            if (hit.type === "book") {
                tooltip.innerHTML += `<div style="opacity:0.75;">Chapters: ${hit.chapterCount ?? 0}</div>`;
            } else if (hit.chapterId && hit.chapterId !== hit.label) {
                tooltip.innerHTML += `<div style="opacity:0.75;">${hit.chapterId}</div>`;
            }
        } else {
            tooltip.style.opacity = "0";
        }
    }
});

canvas.addEventListener("mouseleave", () => {
    dispatch({ type: ActionTypes.SET_HOVERED_NODE, payload: { node: null } });
    canvas.style.cursor = "default";
    if (tooltip) {
        tooltip.style.opacity = "0";
    }
});

canvas.addEventListener("dblclick", event => {
    const rect = canvas.getBoundingClientRect();
    const x = (event.clientX - rect.left - state.transform.x) / state.transform.k;
    const y = (event.clientY - rect.top - state.transform.y) / state.transform.k;
    const hit = findNodeAtPosition(x, y);
    if (!hit) return;

    dispatch({
        type: ActionTypes.TOGGLE_BOOK,
        payload: { bookId: hit.bookId },
    });
});
