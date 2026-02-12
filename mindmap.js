// Mind Map Layout and Rendering
(function() {
  const centerTitle = "Estructura y Función del CPU";
  const MARGIN = 22; // extra spacing to avoid overlaps

  const sections = [
    {
      title: "Qué es y cómo se organiza la CPU",
      bullets: [
        "Interpreta la ISA: lee, decodifica y coordina ejecución",
        "Unidad de Control decodifica y genera señales",
        "Registros + ALU manipulan operandos y resultados",
        "Determinista: mismo estado e instrucción ⇒ mismo resultado"
      ]
    },
    {
      title: "Ciclo de instrucción (5 etapas)",
      bullets: [
        "Fetch: PC → MAR; memoria → IR",
        "Decode: UC analiza IR y genera señales",
        "Execute: ALU opera y actualiza banderas",
        "Memory: acceso si la instrucción lo requiere",
        "Write-back: escribe resultado y avanza PC"
      ]
    },
    {
      title: "Unidades internas: ALU, UC y registros",
      bullets: [
        "ALU: aritmético, lógico y comparaciones",
        "Banderas: cero, signo, acarreo",
        "UC: secuencia microoperaciones y orquesta recursos",
        "Decodificador traduce opcode a señales"
      ]
    },
    {
      title: "Mecanismo de control",
      bullets: [
        "Cableado: lógica fija, muy rápido",
        "Microprogramado: microrutinas en memoria, flexible",
        "Trade-off: rendimiento vs flexibilidad"
      ]
    },
    {
      title: "Registros: memoria inmediata",
      bullets: [
        "Control: PC, IR y banderas",
        "Direcciones: MAR (ubica memoria)",
        "Datos: MDR, acumulador, GPRs",
        "Ejemplo 8086: FLAGS, AX/BX/CX/DX, CS/DS/SS/ES, IP, SP, BP, SI, DI"
      ]
    },
    {
      title: "Pipeline y paralelismo",
      bullets: [
        "Etapas encadenadas trabajando en paralelo",
        "Instrucción por ciclo con pipeline lleno",
        "Superposición: fetch I3, decode I2, execute I1",
        "Transparente a la ISA y al programador"
      ]
    },
    {
      title: "Hazards (problemas)",
      bullets: [
        "Estructurales: contención por recursos",
        "Datos: dependencias pendientes",
        "Control: saltos y especulación"
      ]
    }
  ];

  const state = {
    nodes: [],
    links: [],
    elMap: null,
    elSvg: null,
    center: { x: 0, y: 0 }
  };

  function el(tag, cls, text) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text) e.textContent = text;
    return e;
  }

  function createNode(content, depth) {
    const box = el("div", `node depth-${depth}`);
    if (depth === 0) {
      const h = el("h1", null, content.title);
      const p = el("p", null, "CPU secuencial y determinista, coordina ALU, registros y memoria entre etapas.");
      box.appendChild(h);
      box.appendChild(p);
    } else if (depth === 1) {
      const h = el("h3", null, content.title);
      box.appendChild(h);
      if (content.badge) {
        const b = el("span", "badge", content.badge);
        box.appendChild(b);
      }
    } else {
      const ul = el("ul");
      content.bullets.forEach(t => {
        const li = el("li", null, t);
        ul.appendChild(li);
      });
      const h = el("h3", null, content.title);
      box.appendChild(h);
      box.appendChild(ul);
    }
    return box;
  }

  function mount() {
    const map = el("div", "mindmap");
    const header = el("div", "header", centerTitle);
    document.body.appendChild(header);
    document.body.appendChild(map);

    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("id", "connectors");
    map.appendChild(svg);

    state.elMap = map;
    state.elSvg = svg;

    // Central node
    const centerNode = createNode({ title: centerTitle }, 0);
    map.appendChild(centerNode);
    state.nodes.push({ depth: 0, el: centerNode, children: [] });

    // Level 1 sections + level 2 bullets
    sections.forEach((sec, idx) => {
      const secNode = createNode({ title: sec.title }, 1);
      secNode.classList.add(`section-${idx}`);
      map.appendChild(secNode);
      const secEntry = { depth: 1, el: secNode, children: [] };
      state.nodes[0].children.push(secEntry);
      state.nodes.push(secEntry);

      const bulletsNode = createNode({ title: "", bullets: sec.bullets }, 2);
      bulletsNode.classList.add(`section-${idx}`);
      map.appendChild(bulletsNode);
      const bEntry = { depth: 2, el: bulletsNode, children: [] };
      secEntry.children.push(bEntry);
      state.nodes.push(bEntry);

      // Link records for connectors
      state.links.push({ from: centerNode, to: secNode, depth: 1, section: idx });
      state.links.push({ from: secNode, to: bulletsNode, depth: 2, section: idx });
    });

    window.addEventListener("resize", layout);
    layout();
  }

  function layout() {
    const rect = state.elMap.getBoundingClientRect();
    state.center.x = rect.width / 2;
    state.center.y = rect.height / 2 + 20; // slight bias down to avoid header overlap

    // Place center
    const c = state.nodes.find(n => n.depth === 0);
    positionBox(c.el, state.center.x, state.center.y);

    // Radial placement for sections
    const secs = state.nodes.filter(n => n.depth === 1);
    const N = secs.length;
    const R1 = Math.min(rect.width, rect.height) * 0.38; // push branches farther
    const R2step = Math.min(rect.width, rect.height) * 0.18; // push bullets farther

    secs.forEach((s, i) => {
      const angle = (Math.PI * 2 * i) / N - Math.PI / 2 + (Math.PI / (N * 6)); // minor offset to reduce stacking
      const p1 = polar(state.center, R1, angle);
      positionBox(s.el, p1.x, p1.y);

      const bullets = s.children[0];
      const p2 = polar(state.center, R1 + R2step, angle);
      positionBox(bullets.el, p2.x, p2.y);
    });

    // Resolve collisions among non-center nodes
    relaxCollisions(10);

    // Size SVG and draw links
    state.elSvg.setAttribute("viewBox", `0 0 ${rect.width} ${rect.height}`);
    state.elSvg.setAttribute("width", rect.width);
    state.elSvg.setAttribute("height", rect.height);
    state.elSvg.innerHTML = "";

    state.links.forEach(l => drawLink(l));
  }

  function positionBox(el, x, y) {
    const pad = 0;
    const maxX = state.elMap.clientWidth - pad;
    const maxY = state.elMap.clientHeight - pad;
    el.style.left = Math.max(pad, Math.min(maxX, x)) + "px";
    el.style.top = Math.max(pad, Math.min(maxY, y)) + "px";
  }

  function centerOf(el) {
    const r = el.getBoundingClientRect();
    const mapR = state.elMap.getBoundingClientRect();
    return {
      x: r.left - mapR.left + r.width / 2,
      y: r.top - mapR.top + r.height / 2
    };
  }

  function polar(origin, radius, angle) {
    return {
      x: origin.x + radius * Math.cos(angle),
      y: origin.y + radius * Math.sin(angle)
    };
  }

  function drawLink(link) {
    const { from, to, depth, section } = link;
    const a = centerOf(from);
    const b = centerOf(to);

    // Slight curved connector for aesthetics
    const dx = (b.x - a.x) * 0.25;
    const dy = (b.y - a.y) * 0.25;
    const c1x = a.x + dx;
    const c1y = a.y + dy;
    const c2x = b.x - dx;
    const c2y = b.y - dy;

    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", `M ${a.x} ${a.y} C ${c1x} ${c1y}, ${c2x} ${c2y}, ${b.x} ${b.y}`);
    const cls = [`connector`, `depth-${depth}`];
    if (section !== undefined) cls.push(`section-${section}`);
    path.setAttribute("class", cls.join(" "));
    state.elSvg.appendChild(path);
  }

  function clamp(v, min, max) {
    return Math.max(min, Math.min(max, v));
  }

  function relaxCollisions(iterations) {
    const nodes = state.nodes.filter(n => n.depth > 0); // exclude center
    const mapRect = state.elMap.getBoundingClientRect();
    for (let it = 0; it < iterations; it++) {
      let movedAny = false;
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const ni = nodes[i];
          const nj = nodes[j];
          const ci = centerOf(ni.el);
          const cj = centerOf(nj.el);

          const ri = Math.max(ni.el.getBoundingClientRect().width, ni.el.getBoundingClientRect().height) / 2 + MARGIN;
          const rj = Math.max(nj.el.getBoundingClientRect().width, nj.el.getBoundingClientRect().height) / 2 + MARGIN;

          const dx = cj.x - ci.x;
          const dy = cj.y - ci.y;
          const dist = Math.sqrt(dx * dx + dy * dy) || 0.0001;
          const minDist = ri + rj;
          if (dist < minDist) {
            // push apart along the line connecting centers
            const overlap = (minDist - dist) / 2;
            const ux = dx / dist;
            const uy = dy / dist;

            const li = parseFloat(ni.el.style.left) || ci.x;
            const ti = parseFloat(ni.el.style.top) || ci.y;
            const lj = parseFloat(nj.el.style.left) || cj.x;
            const tj = parseFloat(nj.el.style.top) || cj.y;

            const newLi = clamp(li - ux * overlap, 0, mapRect.width);
            const newTi = clamp(ti - uy * overlap, 0, mapRect.height);
            const newLj = clamp(lj + ux * overlap, 0, mapRect.width);
            const newTj = clamp(tj + uy * overlap, 0, mapRect.height);

            positionBox(ni.el, newLi, newTi);
            positionBox(nj.el, newLj, newTj);
            movedAny = true;
          }
        }
      }
      if (!movedAny) break;
    }
  }

  // Boot
  document.addEventListener("DOMContentLoaded", mount);
})();
