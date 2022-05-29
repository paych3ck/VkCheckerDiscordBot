# VkCheckerDiscordBot

_Проектная работа для повышения квалификации до преподвателя Python Pro онлайн-школы Kodland._

> Бот для Discord, написанный с использованием vk_api.
> По указанному id достает информацию о пользователе или сообществе.

## Команды бота:
> **VC!options - выводит подсказку о доступных командах.**
> **VC!user_info - информация о пользователе.**
> **VC!group_info - информация о сообществе.**

## Работа с пользователем

| Метод | Что возвращает |
| ------ | ------ |
| uparse_all_info | Список полей указанного пользователя. |
| uget_all_info | Вся полученная информация.  |
| uget_full_name | Имя и фамилия пользователя. |
| uget_about | Раздел о человеке. |
| uget_rdate | Дата регистрации. |
| uget_bdate | День рождения. |
| uget_posts_count | Количество постов на стене. |
| uget_connections | Контакты. |
| uget_contacts | Телефоны. |
| uget_city | Город. |
| uget_country | Страна. |
| uget_domain | Короткий адрес страницы. |
| uget_followers_count | Количество подписчиков. |
| uget_home_town | Родной город. |
| uget_profile_photo | Ссылка на аватар. |
| uget_sex | Пол. |
| uget_site | Личный сайт. |
| uget_status | Статус. |
| uget_games | Любимые игры. |
| uget_interests | Интересы. |
| uget_last_seen | Последний онлайн. |
| uget_movies | Любимые фильмы. |
| uget_music | Любимая музыка. |
| uget_occupation | Род деятельности. |
| uget_online | Онлайн-статус. |
| uget_personal | Жизненная позиция. |
| uget_relation | Семейное положение. |

## Работа с сообществом

| Метод | Что возвращает |
| ------ | ------ |
| gparse_all_info | Список полей указанного сообщества. |
| gget_all_info | Вся полученная информация. |
| gget_name | Название. |
| gget_screen_name | Короткий адрес. |
| gget_type | Тип сообщества.. |
| gget_members_count | Количество подписчиков. |
| gget_status | Статус. |
