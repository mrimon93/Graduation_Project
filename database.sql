CREATE TABLE IF NOT EXISTS station(
	station_id INT PRIMARY KEY,
	namn VARCHAR(50)
	);


CREATE TABLE IF NOT EXISTS fact (
	id SERIAL PRIMARY KEY,
	tid TEXT,
	station_id INT REFERENCES station(station_id),
	lufttemperatur_celsius NUMERIC(3,1),
	vindhastighet_ms NUMERIC(3,1),
	price_area VARCHAR(3),
	spotprice_eur NUMERIC(24,20)
);
	
