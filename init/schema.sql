CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS flights (
    id TEXT PRIMARY KEY,
    ano INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    mercado TEXT NOT NULL,
    rpk NUMERIC NOT NULL
);

CREATE INDEX idx_flight_market_year_month ON flights (mercado, ano, mes);
