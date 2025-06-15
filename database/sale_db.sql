CREATE DATABASE sale_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sale_db;

CREATE TABLE stores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100)
);

CREATE TABLE products_category (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name ENUM('نان', 'شیرینی', 'پیستری', 'اسنک', 'نوشیدنی', 'سایر')
);

CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    unit VARCHAR(20),
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES products_category(id)
);

CREATE TABLE product_sub_category (
    id INT PRIMARY KEY AUTO_INCREMENT,
    category_id INT,
    sub_category VARCHAR(50),
    FOREIGN KEY (category_id) REFERENCES products_category(id)
);

CREATE TABLE customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    category ENUM('مشتری عادی', 'پرسنل', 'اسنپ', 'مشتری تجاری') DEFAULT 'مشتری عادی'
);

CREATE TABLE sellers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100)
);

CREATE TABLE invoices (
    id INT PRIMARY KEY AUTO_INCREMENT,
    status ENUM('ثبت شده', 'ابطال شده'),
       date DATE,
    date_time DATETIME,
    seller_id INT,
    customer_id INT,
    store_id INT,
    FOREIGN KEY (seller_id) REFERENCES sellers(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (store_id) REFERENCES stores(id)
);

CREATE TABLE invoice_products (
    invoice_id INT,
    product_id INT,
    quantity INT,
    PRIMARY KEY (invoice_id, product_id),
    FOREIGN KEY (invoice_id) REFERENCES invoices(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
