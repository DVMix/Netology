SELECT ('���: �������� �������');

-- ������ 1 - ����� ���������� ������
SELECT userId, movieId,
        rating - MIN(rating) OVER (PARTITION BY userId)/
        MAX(rating) OVER (PARTITION BY userId)- MIN(rating) OVER (PARTITION BY
userId) as normed_rating,
        avg(rating) as avg_rating
        FROM  ratings group by 1,2, rating
        LIMIT 30;

--  ������ 2 - ���� ���������� �� keywords
DROP TABLE IF EXISTS keywords;
CREATE TABLE IF NOT EXISTS keywords (
    id bigint,
    tags varchar
  );

\copy keywords FROM '/data/keywords.csv' DELIMITER ',' CSV HEADER;
SELECT COUNT(*) FROM keywords;

SELECT movieId, AVG(rating) OVER (PARTITION BY movieid) rating_average
    FROM (select movieid, rating, count(rating) from ratings group by 1,2 having
count(rating)>50) as sample join keywords on sample.movieid=keywords.id
    order by rating_average DESC, movieid ASC LIMIT 150;

-- ������ 3 - ������������ ������ 2 ����� ��������� ������ � �������
DROP TABLE IF EXISTS top_keywords;

WITH top_rated as
(SELECT movieId, AVG(rating) OVER (PARTITION BY movieid) rating_average, tags
    FROM (select movieid, rating, count(rating) from ratings group by 1,2 having
count(rating)>50) as sample join keywords on sample.movieid=keywords.id
    order by rating_average DESC, movieid ASC LIMIT 150)
select movieid, tags into top_keywords from top_rated
order by rating_average DESC, movieid ASC;
\copy (SELECT * FROM top_keywords) TO '/data/tags.tsv' DELIMITER E'\t';