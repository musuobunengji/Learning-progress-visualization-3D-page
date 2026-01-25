import React, { useEffect, useRef, useState } from "https://esm.sh/react@18.2.0";
import ReactDOM from "https://esm.sh/react-dom@18.2.0/client";
import {
    ActionTypes,
    reducer,
    rebuildGraph,
    draw,
    findNodeAtPosition,
} from "./graph.js";

const API = "http://127.0.0.1:8000";

function createInitialState() {
    return {
        graph: null,
        expandedBooks: new Set(),
        nodes: [],
        links: [],
        transform: d3.zoomIdentity,
        hoveredNode: null,
        dimensions: { width: window.innerWidth, height: window.innerHeight },
        theme: "light",
    };
}

function App() {
    const [runs, setRuns] = useState([]);
    const [selectedRun, setSelectedRun] = useState("");
    const [state, setState] = useState(createInitialState);
    const stateRef = useRef(state);
    const simulationRef = useRef(null);
    const canvasRef = useRef(null);
    const tooltipRef = useRef(null);

    stateRef.current = state;

    const dispatch = (action) => {
        const partial = reducer(stateRef.current, action);
        const next = { ...stateRef.current, ...partial };
        stateRef.current = next;
        setState(next);

        if (action.type === ActionTypes.SET_GRAPH || action.type === ActionTypes.TOGGLE_BOOK) {
            rebuildGraph(stateRef.current, simulationRef);
            setState({ ...stateRef.current });
        }
        if (action.type === ActionTypes.RESIZE) {
            rebuildGraph(stateRef.current, simulationRef);
            setState({ ...stateRef.current });
        }
    };

    useEffect(() => {
        document.documentElement.dataset.theme =
            state.theme === "dark" ? "dark" : "light";
    }, [state.theme]);

    useEffect(() => {
        const handleResize = () => {
            dispatch({
                type: ActionTypes.RESIZE,
                payload: {
                    dimensions: { width: window.innerWidth, height: window.innerHeight },
                },
            });
        };
        handleResize();
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    useEffect(() => {
        fetch(`${API}/runs`)
            .then((res) => res.json())
            .then((data) => {
                setRuns(data);
                if (data.length > 0) {
                    setSelectedRun(String(data[0].id));
                }
            })
            .catch((err) => {
                console.error(err);
                setRuns([]);
            });
    }, []);

    useEffect(() => {
        if (!selectedRun) return;
        fetch(`${API}/graph?run_id=${selectedRun}`)
            .then((res) => res.json())
            .then((data) => {
                dispatch({ type: ActionTypes.SET_GRAPH, payload: { graph: data } });
            })
            .catch(console.error);
    }, [selectedRun]);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext("2d");
        let frame = null;
        const render = () => {
            draw(stateRef.current, ctx);
            frame = requestAnimationFrame(render);
        };
        render();
        return () => {
            if (frame) cancelAnimationFrame(frame);
        };
    }, []);

    useEffect(() => {
        const canvas = canvasRef.current;
        const tooltip = tooltipRef.current;
        if (!canvas) return;

        const zoomBehavior = d3
            .zoom()
            .scaleExtent([0.2, 5])
            .filter((event) => event.type !== "dblclick")
            .on("zoom", (event) => {
                dispatch({
                    type: ActionTypes.SET_TRANSFORM,
                    payload: { transform: event.transform },
                });
            });

        d3.select(canvas).call(zoomBehavior);

        const handleMove = (event) => {
            const rect = canvas.getBoundingClientRect();
            const x = (event.clientX - rect.left - stateRef.current.transform.x) / stateRef.current.transform.k;
            const y = (event.clientY - rect.top - stateRef.current.transform.y) / stateRef.current.transform.k;
            const hit = findNodeAtPosition(stateRef.current, x, y);
            dispatch({ type: ActionTypes.SET_HOVERED_NODE, payload: { node: hit } });
            canvas.style.cursor = hit ? "pointer" : "default";

            if (!tooltip) return;
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
        };

        const handleLeave = () => {
            dispatch({ type: ActionTypes.SET_HOVERED_NODE, payload: { node: null } });
            canvas.style.cursor = "default";
            if (tooltip) {
                tooltip.style.opacity = "0";
            }
        };

        const handleDblClick = (event) => {
            const rect = canvas.getBoundingClientRect();
            const x = (event.clientX - rect.left - stateRef.current.transform.x) / stateRef.current.transform.k;
            const y = (event.clientY - rect.top - stateRef.current.transform.y) / stateRef.current.transform.k;
            const hit = findNodeAtPosition(stateRef.current, x, y);
            if (!hit) return;
            dispatch({
                type: ActionTypes.TOGGLE_BOOK,
                payload: { bookId: hit.bookId },
            });
        };

        canvas.addEventListener("mousemove", handleMove);
        canvas.addEventListener("mouseleave", handleLeave);
        canvas.addEventListener("dblclick", handleDblClick);

        return () => {
            d3.select(canvas).on(".zoom", null);
            canvas.removeEventListener("mousemove", handleMove);
            canvas.removeEventListener("mouseleave", handleLeave);
            canvas.removeEventListener("dblclick", handleDblClick);
        };
    }, []);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        canvas.width = state.dimensions.width;
        canvas.height = state.dimensions.height;
    }, [state.dimensions]);

    const onThemeToggle = () => {
        dispatch({
            type: ActionTypes.SET_THEME,
            payload: { theme: state.theme === "dark" ? "light" : "dark" },
        });
    };

    return (
        React.createElement(React.Fragment, null,
            React.createElement("div", { id: "topbar" },
                React.createElement(
                    "select",
                    {
                        value: selectedRun,
                        onChange: (e) => setSelectedRun(e.target.value),
                    },
                    runs.length === 0
                        ? React.createElement("option", { value: "" }, "failed to load runs")
                        : runs.map((run) =>
                            React.createElement(
                                "option",
                                { key: run.id, value: String(run.id) },
                                `run ${run.id} (${run.book_ids.join(", ")})`,
                            ),
                        ),
                ),
                React.createElement(
                    "button",
                    { id: "themeToggle", type: "button", onClick: onThemeToggle },
                    state.theme === "dark" ? "Theme: Dark" : "Theme: Light",
                ),
            ),
            React.createElement("canvas", { id: "graph", ref: canvasRef }),
            React.createElement("div", { id: "tooltip", ref: tooltipRef }),
        )
    );
}

const root = ReactDOM.createRoot(document.getElementById("app"));
root.render(React.createElement(App));
