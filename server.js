const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');
const helmet = require('helmet');
const crypto = require('crypto');
const rateLimit = require('express-rate-limit');
const app = express();
const port = process.env.PORT || 3000;

// If behind a proxy (common in hosting platforms), let Express derive req.ip safely
app.set('trust proxy', true);

app.disable('x-powered-by');
app.use(helmet({ contentSecurityPolicy: false }));
app.use(cors({
    origin: ['https://bricolito.netlify.app'],
    methods: ['GET', 'POST'],
    allowedHeaders: ['Content-Type', 'X-Requested-With', 'X-CSRF-Token'],
}));
app.use(express.json());

// Base de datos para guardar IPs
const db = new sqlite3.Database('cartas.db');
db.serialize(() => {
    db.run("CREATE TABLE IF NOT EXISTS usuarios (ip TEXT PRIMARY KEY, terminado INTEGER)");
});

// Middleware utilitario: obtener IP del cliente sin confiar en cabeceras manipulables
function getIp(req) {
    return req.ip;
}

// Middleware simple anti-CSRF: exigir cabecera personalizada para peticiones de estado
function requireAjax(req, res, next) {
    const xrw = req.get('X-Requested-With');
    if (xrw !== 'XMLHttpRequest') {
        return res.status(403).json({ ok: false, error: 'forbidden' });
    }
    next();
}

// CSRF token simple emitido vía API y validado por IP + User-Agent
const csrfStore = new Map(); // token -> { ip, ua, exp }
const CSRF_TTL_MS = 60 * 60 * 1000; // 60 minutos

function issueCsrfToken(ip, ua) {
    const token = crypto.randomBytes(32).toString('hex');
    csrfStore.set(token, { ip, ua, exp: Date.now() + CSRF_TTL_MS });
    return token;
}

function verifyCsrf(req, res, next) {
    const token = req.get('X-CSRF-Token');
    if (!token) return res.status(403).json({ ok: false, error: 'missing_csrf' });
    const meta = csrfStore.get(token);
    if (!meta) return res.status(403).json({ ok: false, error: 'invalid_csrf' });
    if (meta.exp < Date.now()) { csrfStore.delete(token); return res.status(403).json({ ok: false, error: 'expired_csrf' }); }
    if (meta.ip !== req.ip || meta.ua !== (req.get('user-agent') || '')) {
        return res.status(403).json({ ok: false, error: 'mismatch_csrf' });
    }
    csrfStore.delete(token); // un solo uso
    next();
}

// Rate limiting para evitar abuso
const terminarLimiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 20,
    standardHeaders: true,
    legacyHeaders: false,
});

// Consulta si puede ver cartas
app.get('/puede-ver', (req, res) => {
    const ip = getIp(req);
    db.get("SELECT terminado FROM usuarios WHERE ip = ?", [ip], (err, row) => {
        if (err) {
            console.error('DB error en /puede-ver:', err);
            return res.status(500).json({ error: 'db_error' });
        }
        if (row && row.terminado) {
            res.json({ permitido: false });
        } else {
            res.json({ permitido: true });
        }
    });
});

// Emitir CSRF token
app.get('/csrf-token', requireAjax, (req, res) => {
    const ip = getIp(req);
    const ua = req.get('user-agent') || '';
    const token = issueCsrfToken(ip, ua);
    res.json({ token });
});

// Marca como terminado
app.post('/terminar', terminarLimiter, requireAjax, verifyCsrf, (req, res) => {
    const ip = getIp(req);
    if (!ip) return res.status(400).json({ ok: false, error: 'no_ip' });
    db.run("INSERT OR REPLACE INTO usuarios (ip, terminado) VALUES (?, 1)", [ip], function(err) {
        if (err) {
            console.error('DB error en /terminar:', err);
            return res.status(500).json({ ok: false, error: 'db_error' });
        }
        res.json({ ok: true });
    });
});

app.listen(port, () => {
    console.log(`Servidor backend escuchando en http://localhost:${port}`);
});