# Three in a row with pokemon
## Проект по Pygame

Приложение написано для оттачивания навыков работы с библиотекой pygame. Это обычная игра вида "Три в ряд".

# Эксплуатация
Папка data должна лежать в той же папке, что и само приложение.
Работа приложения начинается с main, в Constants лежат все константы, необходимые для корректной работы. 

После запуска игры, вы увидете её правила и две кнопки "Старт" и "Выход" соответственно. 
При нажатии кнопки "Старт" перед вами появится клетчатое поле 8 на 8, в которой будет находится 7 разных видов покемонов.
Ваша задача собрать 3 и более покемонов в ряд или в столбец, за это вы получаете очки. Чем больше покемонов в ряду, тем больше очков вы получите.
Очки убывают с течением времени. Это необходимо для того, чтобы вы пытались быстрее найти соответствие.
Игра завершается только тогда, когда на поле не остаётся ходов. При нажатии на крестик при не окончившейся игре, результат засчитан
не будет.
В игре также есть топ 3 лучших поставленных рекорда. Файл с ними хранится в папке data с названием "three_best_score.txt"


# Доп. информация
data содержит в себе 3 папки и один файл для сохранение 3-х лучших игр.
##### В папке Backgrounds хранятся: 
1. начальная заставка;
2. фоны, которые меняются во время игры. Их четыре: утро, день, вечер, ночь. Смена происходит каждые 60 секунд;
3. конечная заставка.
##### В папке Music хранятся:
1. badswap.mp3 - звук при неудачном свапе, когда не вышло выстраить 3 покемонов в ряд;
2. complete.mp3 - играет при конечной заставке;
3. match.mp3 - звук при удачном свапе, когда вышло выстраить 3 и более покемонов в ряд.
##### В папке Sprites хранятся:
1. Семь видов покемонов.
