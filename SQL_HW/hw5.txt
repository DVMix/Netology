/*
        Написать запрос, который выводит общее число тегов
*/
db.tags.aggregate([{$group:{_id: "$trololo",tag_count: {$sum: 1}}}])
print("tags count: ", 'расчёт количества тегов');
/*
        Добавляем фильтрацию: считаем только количество тегов woman
*/
db.tags.aggregate([{$match: {name: "woman"}},{$group:{_id: "$woman",tag_count: {$sum: 1}}}])
print("woman tags count: ", 'расчёт количества тегов woman');
/*
        Очень сложный запрос: используем группировку данных посчитать количество вхождений для каждого тега
        и напечатать top-3 самых популярных
*/
printjson(
        db.tags.aggregate([
                {"$group": { _id: "$name",tag_count: {$sum: 1}}},
                {$sort: {tag_count: -1}},
                {$limit: 3}
        ])['_batch']
);


