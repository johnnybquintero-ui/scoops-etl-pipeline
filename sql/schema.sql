DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_flavour;
DROP TABLE IF EXISTS dim_store;

CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    full_date DATE NOT NULL,
    day INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    quarter INT NOT NULL,
    year INT NOT NULL,
    day_of_week VARCHAR(20) NOT NULL,
    is_weekend BOOLEAN NOT NULL
);

CREATE TABLE dim_flavour (
    flavour_id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    contains_nuts BOOLEAN NOT NULL,
    cost_price_in_pence INT NOT NULL
);

CREATE TABLE dim_store (
    store_id VARCHAR(10) NOT NULL PRIMARY KEY,
    store_name VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL,
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL
);

CREATE TABLE fact_sales (
    sale_id INT PRIMARY KEY,
    date_id INT NOT NULL,
    store_id VARCHAR(10) NOT NULL,
    flavour_id INT NOT NULL,
    price_in_pence INT NOT NULL,
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (store_id) REFERENCES dim_store(store_id),
    FOREIGN KEY (flavour_id) REFERENCES dim_flavour(flavour_id)
);