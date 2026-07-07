function renderTree(tree) {
  const root = document.querySelector(".tree");
  root.innerHTML = "";

  for (const [db, schemas] of Object.entries(tree)) {
    const dbLi = document.createElement("li");

    dbLi.innerHTML = `
            <div class="item folder" onclick="set_current('${db}')">
                <i class="bi bi-caret-down-fill arrow"></i>
                ${db}
                <i class="bi bi-database"></i>
            </div>
        `;

    const schemaUl = document.createElement("ul");
    schemaUl.className = "children";

    for (const [schema, tables] of Object.entries(schemas)) {
      const schemaLi = document.createElement("li");

      schemaLi.innerHTML = `
                <div class="item folder">
                    <i class="bi bi-caret-down-fill arrow"></i>
                    ${schema}
                    <i class="bi bi-map"></i>
                </div>
            `;

      const tableUl = document.createElement("ul");
      tableUl.className = "children";

      for (const table of tables) {
        const tableLi = document.createElement("li");

        tableLi.innerHTML = `
                    <span
                        class="item table"
                        data-db="${db}"
                        data-schema="${schema}"
                        data-table="${table}">
                        ${table}
                        <i class="bi bi-table"></i>
                    </span>
                `;

        tableUl.appendChild(tableLi);
      }

      schemaLi.appendChild(tableUl);
      schemaUl.appendChild(schemaLi);
    }

    dbLi.appendChild(schemaUl);
    root.appendChild(dbLi);
  }
}

function attachFolderListeners() {
  document.querySelectorAll(".folder").forEach((folder) => {
    folder.addEventListener("click", () => {
      const children = folder.nextElementSibling;

      if (!children) return;

      children.classList.toggle("hidden");
      folder.querySelector(".arrow").classList.toggle("closed");
    });
  });
}

function attachTableListeners() {
  document.querySelectorAll(".table").forEach((table) => {
    table.onclick = async () => {
      currentDatabase = table.dataset.db;
      currentTable = table.dataset.table;
      currentScheme = table.dataset.schema;

      document.getElementById("selected").innerText = currentDatabase;
      document.getElementById("selected-table").innerText = currentTable;

      const res = await fetch(
        `/api/table/${currentDatabase}/${currentScheme}/${currentTable}`,
      );

      const data = await res.json();

      document.getElementById("rows").innerText = data.rows
        ? data.rows.length
        : 0;
      document.getElementById("columns").innerText = data.columns.length;

      renderTable(data);
    };
  });
}


setTimeout(async () => {
  const req = await fetch("/api/tree");
  const tree = await req.json();

  renderTree(tree);
  attachFolderListeners();
  attachTableListeners();
}, 300);