-- Comments in SQL Start with dash-dash --
--Question 1, 2 ,3:
INSERT INTO products (name,price,can_be_returned)
  VALUES ('chair',44.00,false),('stool', 25.99, true),('table',124.00,false);
--Question 4
SELECT * FROM products;
--Question 5
SELECT name FROM products;
--Question 6
SELECT name, price FROM products;
--Question 7
INSERT INTO products (name,price,can_be_returned)
  VALUES ('couch', 200, true);
--Question 8
SELECT name FROM products WHERE can_be_returned IS true;
--Question 9
SELECT name from products where price < 44.00;
--Quesiton 10
SELECT name,price from products where price between 22.50 and 99.99;
--Question 11
UPDATE products SET price = price-20.00;
--Question 12
DELETE FROM products WHERE price < 25;
--Question 13
UPDATE products SET price = price+20.00;
--Question 14
UPDATE products SET can_be_returned = true;