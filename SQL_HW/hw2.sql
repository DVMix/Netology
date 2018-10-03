SELECT ('���: ������� ��������');
-- ������ ������
--1.1 SELECT , LIMIT - ������� 10 ������� �� ������� rating
SELECT * FROM ratings LIMIT 10;
--1.2 WHERE, LIKE - ������� �� ������� links �� ������, � ������� imdbid ������������ �� "42", � ���� movieid ����� 100 � 1000
select * from links where movieid>100 AND movieid<1000 AND imdbid like '%42%' limit 10;

-- ������ ������
--2.1 INNER JOIN ������� �� ������� links ��� imdb_id, ������� ������� ������� 5
select imdbid from links inner join ratings on links.movieid=ratings.movieid where rating='5' limit 10;

--������ ������
--3.1 COUNT() ��������� ����� ������� ��� ������
select count(rating) from ratings where rating is NULL;

--3.2 GROUP BY, HAVING ������� top-10 �������������, � ������� ������� ������� ���� 3.5
select userid, AVG(rating) as la from ratings group by userid having avg(rating)>3.5 order by la desc limit 10;

--��������� ������
--4.1 ����������: ������� 10 imbdId �� links � ������� ������� ������� ������ 3.5.����� ���������� ������� ������� �� ��� �������������, ������� ������ ��� �������
WITH tmp_table as (select movieid, avg(rating) from ratings group by 1 having avg(rating)>3.5)
select imdbid from links join tmp_table on links.movieid=tmp_table.movieid  limit 10;

--4.2 Common Table Expressions: ��������� ������� ������� �� �������������, � ������� ����� 10 ������
WITH tmp_table as (select userid, rating, count(rating) from ratings group by 1,2 having count(rating)>10)
select avg(ratings.rating) from ratings join tmp_table on
ratings.userid=tmp_table.userid;