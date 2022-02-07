--Q1
SELECT app_name FROM analytics WHERE id = 1880;
--Q2
SELECT id,app_name FROM analytics WHERE last_updated = '2018-08-01';
--Q3
SELECT category, COUNT(*) from analytics GROUP BY category;
--Q4
SELECT app_name, reviews FROM analytics ORDER BY reviews DESC LIMIT 5;
--Q5
SELECT app_name FROM analytics WHERE rating >= 4.8 ORDER BY reviews DESC LIMIT 1;
--Q6
SELECT category FROM analytics GROUP BY category ORDER BY avg(rating) DESC;
--Q7
SELECT app_name, price, rating FROM analytics WHERE rating < 3.0 ORDER BY price DESC;
--Q8
SELECT app_name FROM analytics WHERE min_installs <= 50 AND rating IS NOT NULL ORDER BY rating DESC;
--Q9
SELECT app_name FROM analytics WHERE rating < 3 AND reviews >= 10000;
--Q10
SELECT app_name FROM analytics WHERE price BETWEEN 0.10 AND 1.00 ORDER BY reviews DESC LIMIT 10;
--Q11
SELECT app_name FROM analytics ORDER BY last_updated LIMIT 1;
--Q12
SELECT app_name FROM analytics ORDER BY price DESC LIMIT 1;
--Q13
SELECT sum(reviews) as all_reviews FROM analytics;
--Q14
SELECT category FROM analytics GROUP BY category HAVING sum(reviews) > 300;
--Q15
SELECT app_name, reviews, min_installs, min_installs/reviews as reviews_per_install
  FROM analytics
    WHERE min_installs > 100000;
