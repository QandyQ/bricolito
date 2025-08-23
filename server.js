const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');
const app = express();
const port = process.env.PORT || 3000;

app.use(cors({
    origin: ['https://bricolito.netlify.app']
}));
app.use(express.json());

// Base de datos para guardar IPs
const db = new sqlite3.Database('cartas.db');
db.serialize(() => {
    db.run("CREATE TABLE IF NOT EXISTS usuarios (ip TEXT PRIMARY KEY, terminado INTEGER)");
});

// Middleware para obtener IP real
function getIp(req) {
    return req.headers['x-forwarded-for'] || req.connection.remoteAddress;
}

// Consulta si puede ver cartas
app.get('/puede-ver', (req, res) => {
    const ip = getIp(req);
    db.get("SELECT terminado FROM usuarios WHERE ip = ?", [ip], (err, row) => {
        if (row && row.terminado) {
            res.json({ permitido: false });
        } else {
            res.json({ permitido: true });
        }
    });
});

// Marca como terminado
app.post('/terminar', (req, res) => {
    const ip = getIp(req);
    db.run("INSERT OR REPLACE INTO usuarios (ip, terminado) VALUES (?, 1)", [ip], () => {
        res.json({ ok: true });
    });
});

app.listen(port, () => {
    console.log(`Servidor backend escuchando en http://localhost:${port}`);
});