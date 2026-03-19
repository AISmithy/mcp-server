from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse

mcp = FastMCP("MCP Server Hub")

_UI_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MCP Server Hub</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:system-ui,sans-serif;background:#0d1117;color:#e6edf3;display:flex;height:100vh}
  #sidebar{width:230px;background:#161b22;border-right:1px solid #30363d;overflow-y:auto;flex-shrink:0;display:flex;flex-direction:column}
  #sidebar-title{font-size:13px;font-weight:700;padding:14px 16px;border-bottom:1px solid #30363d;color:#58a6ff;letter-spacing:.3px;flex-shrink:0}
  #tool-list{flex:1;overflow-y:auto}
  .category{font-size:10px;font-weight:700;letter-spacing:1px;color:#484f58;padding:10px 16px 4px;text-transform:uppercase}
  .tool-item{padding:8px 16px 8px 24px;cursor:pointer;font-size:12px;border-left:3px solid transparent;transition:background .12s;color:#8b949e}
  .tool-item:hover{background:#21262d;color:#e6edf3}
  .tool-item.active{background:#21262d;border-left-color:#58a6ff;color:#58a6ff}
  #main{flex:1;display:flex;flex-direction:column;overflow:hidden}
  #toolbar{padding:10px 20px;border-bottom:1px solid #30363d;background:#161b22;font-size:12px;color:#8b949e;min-height:36px}
  #content{flex:1;display:flex;overflow:hidden}
  #form-panel{width:320px;padding:18px;border-right:1px solid #30363d;overflow-y:auto;flex-shrink:0}
  #result-panel{flex:1;padding:18px;overflow-y:auto}
  h2{font-size:14px;margin-bottom:3px}
  .desc{font-size:11px;color:#8b949e;margin-bottom:14px}
  label{display:block;font-size:11px;color:#8b949e;margin-top:10px;margin-bottom:3px}
  input,textarea,select{width:100%;padding:6px 9px;background:#0d1117;border:1px solid #30363d;border-radius:6px;color:#e6edf3;font-size:12px;outline:none}
  input:focus,textarea:focus{border-color:#58a6ff}
  textarea{resize:vertical;min-height:72px;font-family:monospace;font-size:11px}
  .opt{color:#484f58;font-size:10px;margin-left:3px}
  button{margin-top:16px;width:100%;padding:8px;background:#238636;color:#fff;border:none;border-radius:6px;font-size:13px;cursor:pointer;font-weight:600}
  button:hover{background:#2ea043}
  button:disabled{background:#21262d;color:#484f58;cursor:not-allowed}
  #result-panel h3{font-size:12px;color:#8b949e;margin-bottom:8px}
  pre{background:#161b22;border:1px solid #30363d;border-radius:6px;padding:12px;font-size:11px;white-space:pre-wrap;word-break:break-all;line-height:1.6}
  .error{color:#f85149}
  .placeholder{color:#484f58;font-size:13px;margin-top:60px;text-align:center}
  .badge{display:inline-block;font-size:9px;padding:1px 5px;border-radius:10px;margin-left:5px;vertical-align:middle}
  .badge-github{background:#21262d;color:#58a6ff}
  .badge-jira{background:#1c2b41;color:#4a90e2}
  .badge-rest{background:#1f2d1f;color:#3fb950}
  .badge-oracle{background:#2d1f1f;color:#e36d5a}
  .badge-mongo{background:#1f2d1a;color:#57ab5a}
</style>
</head>
<body>
<div id="sidebar">
  <div id="sidebar-title">&#9672; MCP Server Hub</div>
  <div id="tool-list"><p class="placeholder" style="padding:20px;font-size:11px">Loading tools...</p></div>
</div>
<div id="main">
  <div id="toolbar">Select a tool from the sidebar</div>
  <div id="content">
    <div id="form-panel"><p class="placeholder">&#8592; Pick a tool</p></div>
    <div id="result-panel"><p class="placeholder">Results will appear here</p></div>
  </div>
</div>

<script>
let tools = [];
let activeTool = null;

const CATEGORY_COLORS = {
  GitHub: "badge-github", Jira: "badge-jira",
  "REST API": "badge-rest", Oracle: "badge-oracle", MongoDB: "badge-mongo"
};

async function loadTools() {
  const resp = await fetch("/api/tools");
  tools = await resp.json();
  renderSidebar(tools);
}

function renderSidebar(tools) {
  const grouped = {};
  tools.forEach(t => { (grouped[t.category] = grouped[t.category] || []).push(t); });
  const list = document.getElementById("tool-list");
  list.innerHTML = "";
  Object.entries(grouped).forEach(([cat, items]) => {
    const catEl = document.createElement("div");
    catEl.className = "category";
    catEl.textContent = cat;
    list.appendChild(catEl);
    items.forEach(tool => {
      const el = document.createElement("div");
      el.className = "tool-item";
      el.textContent = tool.name;
      el.onclick = () => selectTool(tool, el);
      list.appendChild(el);
    });
  });
}

function selectTool(tool, el) {
  document.querySelectorAll(".tool-item").forEach(e => e.classList.remove("active"));
  el.classList.add("active");
  activeTool = tool;
  const color = CATEGORY_COLORS[tool.category] || "";
  document.getElementById("toolbar").innerHTML =
    `<strong>${tool.name}</strong> <span class="badge ${color}">${tool.category}</span> &nbsp; ${tool.description}`;
  renderForm(tool);
  document.getElementById("result-panel").innerHTML = '<p class="placeholder">Results will appear here</p>';
}

function renderForm(tool) {
  let html = `<h2>${tool.name}</h2><p class="desc">${tool.description}</p><form id="tool-form">`;
  tool.params.forEach(p => {
    const opt = p.required ? "" : `<span class="opt">optional</span>`;
    html += `<label>${p.name}${opt}</label>`;
    const val = p.default !== null && p.default !== undefined ? p.default : "";
    if (p.type === "text") {
      html += `<textarea name="${p.name}" ${p.required ? "required" : ""}>${escHtml(String(val))}</textarea>`;
    } else if (p.type === "int") {
      html += `<input type="number" name="${p.name}" value="${val}" ${p.required ? "required" : ""}>`;
    } else if (p.type === "bool") {
      html += `<select name="${p.name}"><option value="true">true</option><option value="false">false</option></select>`;
    } else {
      html += `<input type="text" name="${p.name}" value="${escHtml(String(val === null ? "" : val))}" ${p.required ? "required" : ""}>`;
    }
  });
  html += `<button type="submit" id="run-btn">&#9654; Run</button></form>`;
  document.getElementById("form-panel").innerHTML = html;
  document.getElementById("tool-form").onsubmit = submitTool;
}

async function submitTool(e) {
  e.preventDefault();
  const btn = document.getElementById("run-btn");
  btn.disabled = true; btn.textContent = "Running...";
  document.getElementById("result-panel").innerHTML = '<p class="placeholder">Loading...</p>';

  const formData = new FormData(e.target);
  const params = {};
  activeTool.params.forEach(p => {
    const val = formData.get(p.name);
    if (val === "" || val === null) return;
    if (p.type === "int") params[p.name] = parseInt(val, 10);
    else if (p.type === "bool") params[p.name] = val === "true";
    else params[p.name] = val;
  });

  try {
    const resp = await fetch("/call-tool", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({tool: activeTool.name, params}),
    });
    const data = await resp.json();
    if (data.error) {
      document.getElementById("result-panel").innerHTML =
        `<h3>Error</h3><pre class="error">${escHtml(data.error)}</pre>`;
    } else {
      let result = data.result;
      try { result = JSON.stringify(JSON.parse(result), null, 2); } catch {}
      document.getElementById("result-panel").innerHTML =
        `<h3>Result</h3><pre>${escHtml(String(result))}</pre>`;
    }
  } catch (err) {
    document.getElementById("result-panel").innerHTML =
      `<h3>Error</h3><pre class="error">${escHtml(String(err))}</pre>`;
  }
  btn.disabled = false; btn.textContent = "&#9654; Run";
}

function escHtml(s) {
  return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}

loadTools();
</script>
</body>
</html>"""


@mcp.custom_route("/ui", methods=["GET"])
async def ui_page(request: Request) -> HTMLResponse:
    return HTMLResponse(_UI_HTML)


@mcp.custom_route("/api/tools", methods=["GET"])
async def list_tools(request: Request) -> JSONResponse:
    from mcp_server.registry import get_metadata
    return JSONResponse(get_metadata())


@mcp.custom_route("/call-tool", methods=["POST"])
async def call_tool_endpoint(request: Request) -> JSONResponse:
    from mcp_server.registry import call
    body = await request.json()
    try:
        result = call(body.get("tool"), body.get("params", {}))
        return JSONResponse({"result": result})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
