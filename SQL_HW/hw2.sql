SELECT ('‘»ќ: ƒмитрий ћихалкин');
-- первый запрос
--1.1 SELECT , LIMIT - выбрать 10 записей из таблицы rating
SELECT * FROM ratings LIMIT 10;
--1.2 WHERE, LIKE - выбрать из таблицы links всЄ записи, у которых imdbid оканчиваетс€ на "42", а поле movieid между 100 и 1000
select * from links where movieid>100 AND movieid<1000 AND imdbid like '%42%' limit 10;

-- второй запрос
--2.1 INNER JOIN выбрать из таблицы links все imdb_id, которым ставили рейтинг 5
select imdbid from links inner join ratings on links.movieid=ratings.movieid where rating='5' limit 10;

--третий запрос
--3.1 COUNT() ѕосчитать число фильмов без оценок
select count(rating) from ratings where rating is NULL;

--3.2 GROUP BY, HAVING вывести top-10 пользователей, у который средний рейтинг выше 3.5
select userid, AVG(rating) as la from ratings group by userid having avg(rating)>3.5 order by la desc limit 10;

--четвертый запрос
--4.1 ѕодзапросы: достать 10 imbdId из links у которых средний рейтинг больше 3.5.Ќужно подсчитать средний рейтинг по все пользовател€м, которые попали под условие
WITH tmp_table as (select movieid, avg(rating) from ratings group by 1 having avg(rating)>3.5)
select imdbid from links join tmp_table on links.movieid=tmp_table.movieid  limit 10;

--4.2 Common Table Expressions: посчитать средний рейтинг по пользовател€м, у которых более 10 оценок
WITH tmp_table as (select userid, rating, count(rating) from ratings group by 1,2 having count(rating)>10)
select avg(ratings.rating) from ratings join tmp_table on
ratings.userid=tmp_table.userid;