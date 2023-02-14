CREATE TABLE IF NOT EXISTS fact (
	id SERIAL PRIMARY KEY,
	tid TEXT,
	lufttemperatur_celsius NUMERIC(4,2),
	vindhastighet_ms NUMERIC(4,2),
	price_area VARCHAR(3),
	spotprice_eur NUMERIC(9,5)
);
	
