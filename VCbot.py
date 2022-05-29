import asyncio
import vk_api
import urllib.request
import re
from settings import config, sex_values, platform_values, \
    occupation_values, political_values, umenu_text, gmenu_text, alc_sm_values, \
    life_main_values, people_main_values, relation_values, options_text, type_values
from discord.ext import commands
from datetime import datetime


class VkCheckerDiscordBot(commands.Bot):
    def __init__(self, prefix, app_info_getter):
        commands.Bot.__init__(self, command_prefix=prefix)
        self.vk = app_info_getter
        self.uall_fields = [
            "deactivated",
            "activities",
            "about",
            "bdate",
            "can_see_all_posts",
            "career",
            "connections",
            "contacts",
            "city",
            "country",
            "domain",
            "followers_count",
            "has_photo",
            "home_town",
            "photo_400_orig",
            "sex",
            "site",
            "schools",
            "status",
            "games",
            "interests",
            "last_seen",
            "movies",
            "music",
            "occupation",
            "online",
            "personal",
            "quotes",
            "relation",
            "relatives"]

        self.gall_fields = [
            "name",
            "screen_name",
            "type",
            "members_count",
            "status"]

        @self.command(name="options")
        async def options(ctx):
            await ctx.reply(options_text)

        @self.command(name="group_info")
        async def group_info(ctx):
            await ctx.reply("```Введите id сообщества.```")

            try:
                gid_msg = await self.wait_for("message")
                gid = int(gid_msg.content)

                deactivated = self.gparse_all_info(
                    gid)[0].get("deactivated", False)

                if deactivated:
                    await ctx.reply(f"```Сообщество удалено.```")

                else:
                    await ctx.reply(f"```Текущее сообщество: {gid}```\n{gmenu_text}")
                    action_msg = await self.wait_for("message")
                    action = int(action_msg.content)

                    match action:
                        case 1:
                            await ctx.reply(f"```{self.gget_all_info(gid)}```")

                        case 2:
                            await ctx.reply(f"```{self.gget_name(gid)}```")

                        case 3:
                            await ctx.reply(f"```{self.gget_screen_name(gid)}```")

                        case 4:
                            await ctx.reply(f"```{self.gget_type(gid)}```")

                        case 5:
                            await ctx.reply(f"```{self.gget_members_count(gid)}```")

                        case 6:
                            await ctx.reply(f"```{self.gget_status(gid)}```")

                        case 0:
                            await ctx.reply("```Запрос отменен.```")

                        case _:
                            await ctx.reply("```Такой команды не найдено.```")

            except ValueError:
                await ctx.reply("```Значение должно быть целым числом.```")

            except asyncio.TimeoutError:
                await ctx.reply("```Повторите запрос.```")

        @self.command(name="user_info")
        async def user_info(ctx):
            await ctx.reply("```Введите id пользователя.```")

            try:
                uid_msg = await self.wait_for("message")
                uid = int(uid_msg.content)

                deactivated = self.uparse_all_info(
                    uid)[0].get("deactivated", False)

                if deactivated:
                    await ctx.reply(f"```Пользователь удален.```")

                else:
                    await ctx.reply(f"```Текущий пользователь: {uid}```\n{umenu_text}")
                    action_msg = await self.wait_for("message")
                    action = int(action_msg.content)

                    match action:
                        case 1:
                            await ctx.reply(f"```{self.uget_all_info(uid)}```")

                        case 2:
                            await ctx.reply(f"```{self.uget_full_name(uid)}```")

                        case 3:
                            await ctx.reply(f"```{self.uget_rdate(uid)}```")

                        case 4:
                            await ctx.reply(f"```{self.uget_about(uid)}```")

                        case 5:
                            await ctx.reply(f"```{self.uget_bdate(uid)}```")

                        case 6:
                            await ctx.reply(f"```{self.uget_connections(uid)}```")

                        case 7:
                            await ctx.reply(f"```{self.uget_contacts(uid)}```")

                        case 8:
                            await ctx.reply(f"```{self.uget_city(uid)}```")

                        case 9:
                            await ctx.reply(f"```{self.uget_country(uid)}```")

                        case 10:
                            await ctx.reply(f"```{self.uget_domain(uid)}```")

                        case 11:
                            await ctx.reply(f"```{self.uget_followers_count(uid)}```")

                        case 12:
                            await ctx.reply(f"```{self.uget_home_town(uid)}```")

                        case 13:
                            await ctx.reply(self.uget_profile_photo(uid))

                        case 14:
                            await ctx.reply(f"```{self.uget_sex(uid)}```")

                        case 15:
                            await ctx.reply(f"```{self.uget_site(uid)}```")

                        case 16:
                            await ctx.reply(f"```{self.uget_status(uid)}```")

                        case 17:
                            await ctx.reply(f"```{self.uget_games(uid)}```")

                        case 18:
                            await ctx.reply(f"```{self.uget_interests(uid)}```")

                        case 19:
                            await ctx.reply(f"```{self.uget_last_seen(uid)}```")

                        case 20:
                            await ctx.reply(f"```{self.uget_movies(uid)}```")

                        case 21:
                            await ctx.reply(f"```{self.uget_music(uid)}```")

                        case 22:
                            await ctx.reply(f"```{self.uget_occupation(uid)}```")

                        case 23:
                            await ctx.reply(f"```{self.uget_online(uid)}```")

                        case 24:
                            await ctx.reply(f"```{self.uget_personal(uid)}```")

                        case 25:
                            await ctx.reply(f"```{self.uget_relation(uid)}```")

                        case 0:
                            await ctx.reply("```Запрос отменен.```")

                        case _:
                            await ctx.reply("```Такой команды не найдено.```")

            except ValueError:
                await ctx.reply("```Значение должно быть целым числом.```")

            except asyncio.TimeoutError:
                await ctx.reply("```Повторите запрос.```")

    def uparse_all_info(self, id):
        return self.vk.users.get(user_ids=id, fields=self.uall_fields)

    def uget_all_info(self, id):
        all_info = "\n".join([self.uget_full_name(id),
                              self.uget_about(id),
                              self.uget_rdate(id),
                              self.uget_bdate(id),
                              self.uget_posts_count(id),
                              self.uget_connections(id),
                              self.uget_contacts(id),
                              self.uget_city(id),
                              self.uget_country(id),
                              self.uget_domain(id),
                              self.uget_followers_count(id),
                              self.uget_home_town(id),
                              self.uget_sex(id),
                              self.uget_site(id),
                              self.uget_status(id),
                              self.uget_games(id),
                              self.uget_interests(id),
                              self.uget_last_seen(id),
                              self.uget_movies(id),
                              self.uget_music(id),
                              self.uget_occupation(id),
                              self.uget_online(id),
                              self.uget_personal(id),
                              self.uget_relation(id)])
        return all_info

    def uget_full_name(self, id):
        first_name = self.uparse_all_info(id)[0]["first_name"]
        last_name = self.uparse_all_info(id)[0]["last_name"]
        full_name = " ".join([first_name, last_name])
        return f"Имя: {full_name}."

    def uget_about(self, id):
        about = self.uparse_all_info(id)[0]["about"]
        about_info = "информация не указана" if not about else about
        return f"О человеке: {about_info}." if not self.uparse_all_info(
            id)[0]["is_closed"] else "профиль скрыт."

    def uget_rdate(self, id):
        user_profile_link = f"https://vk.com/foaf.php?id={id}"

        with urllib.request.urlopen(user_profile_link) as response:
            user_profile_xml = response.read().decode("windows-1251")

        rdate = re.findall(r'date="(.*)"', user_profile_xml)[0]
        rdate_day_info = f"{rdate[8:10]}/{rdate[5:7]}/{rdate[0:4]}"
        rdate_time_info = f"{int(rdate[11:13]) + 1}:{rdate[14:16]}:{rdate[17:19]}"
        return f"Зарегистрирован: {rdate_day_info} - {rdate_time_info}."

    def uget_bdate(self, id):
        bdate = self.uparse_all_info(id)[0]["bdate"]
        bdate_info = "информация не указана" if not bdate else bdate
        return f"День рождения: {bdate_info}." if not self.uparse_all_info(
            id)[0]["is_closed"] else "профиль скрыт."

    def uget_posts_count(self, id):
        posts_count = self.vk.wall.get(owner_id=id)["count"] if self.uparse_all_info(
            id)[0]["can_see_all_posts"] else "пользователь ограничил доступ к стене"
        return f"Количество постов на стене: {posts_count}."

    def uget_connections(self, id):
        connections = self.uparse_all_info(id)[0].get("skype", False)
        connections_info = "информация не указана" if not connections else connections
        return f"Контакты: {connections_info}."

    def uget_contacts(self, id):
        mobile_phone = self.uparse_all_info(id)[0].get("mobile_phone", False)
        home_phone = self.uparse_all_info(id)[0].get("home_phone", False)
        mobile_phone_info = "нформация не указана" if not mobile_phone else mobile_phone
        home_phone_info = "информация не указана" if not home_phone else home_phone
        return f"Телефоны: мобильный - {mobile_phone_info}, дополнительный - {home_phone_info}."

    def uget_city(self, id):
        city = self.uparse_all_info(id)[0]["city"]
        city_info = "Информация не указана" if not city else city["title"]
        return f"Город: {city_info}."

    def uget_country(self, id):
        country = self.uparse_all_info(id)[0]["country"]
        country_info = "информация не указана" if not country else country["title"]
        return f"Страна: {country_info}."

    def uget_domain(self, id):
        domain = self.uparse_all_info(id)[0]["domain"]
        domain_info = "информация не указана" if not domain else domain
        return f"Короткий адрес страницы: {domain_info}."

    def uget_followers_count(self, id):
        followers_count = self.uparse_all_info(id)[0]["followers_count"]
        followers_count_info = "0" if not followers_count else followers_count
        return f"Количество подписчиков: {followers_count_info}."

    def uget_home_town(self, id):
        home_town = self.uparse_all_info(id)[0]["home_town"]
        home_town_info = "информация не указана" if not home_town else home_town
        return f"Родной город: {home_town_info}."

    def uget_profile_photo(self, id):
        profile_photo = self.uparse_all_info(id)[0]["photo_400_orig"]
        profile_photo_info = "```Пользователь не установил фото профиля.```" if not self.uparse_all_info(id)[
            0]["has_photo"] else profile_photo
        return profile_photo_info

    def uget_sex(self, id):
        sex = self.uparse_all_info(id)[0]["sex"]
        sex_info = "информация не указана" if not sex else sex
        return f"Пол: {sex_values[sex_info]}."

    def uget_site(self, id):
        site = self.uparse_all_info(id)[0]["site"]
        site_info = "информация не указана" if not site else site
        return f"Личный сайт: {site_info}."

    def uget_status(self, id):
        status = self.uparse_all_info(id)[0]["status"]
        status_info = "информация не указана" if not status else status
        return f"Статус: «{status_info}»."

    def uget_games(self, id):
        games = self.uparse_all_info(id)[0]["games"]
        games_info = "информация не указана" if not games else games
        return f"Любимые игры: {games_info}."

    def uget_interests(self, id):
        interests = self.uparse_all_info(id)[0]["interests"]
        interests_info = "информация не указана" if not interests else interests
        return f"Интересы: {interests_info}."

    def uget_last_seen(self, id):
        last_seen = self.uparse_all_info(id)[0].get("last_seen", False)
        last_seen_info = "информация не найдена" if not last_seen else datetime.fromtimestamp(
            last_seen["time"]).strftime("%d/%m/%Y - %H:%M:%S")
        platform_info = "информация не найдена" if not last_seen else platform_values[
            last_seen["platform"]]
        return f"Последний онлайн: {last_seen_info}, платформа: {platform_info}."

    def uget_movies(self, id):
        movies = self.uparse_all_info(id)[0]["movies"]
        movies_info = "информация не указана" if not movies else movies
        return f"Любимое кино: {movies_info}."

    def uget_music(self, id):
        music = self.uparse_all_info(id)[0]["music"]
        music_info = "информация не указана" if not music else music
        return f"Любимая музыка: {music_info}."

    def uget_occupation(self, id):
        occupation = self.uparse_all_info(id)[0].get("occupation", False)
        occupation_info = "информация не указана" if not occupation else f"{occupation_values[occupation['type']]} в {occupation['name']}"
        return f"Род деятельности: {occupation_info}."

    def uget_online(self, id):
        online = self.uparse_all_info(id)[0]["online"]
        online_info = "не онлайн" if not online else "онлайн"
        return f"Онлайн-статус: {online_info}."

    def uget_personal(self, id):
        personal = self.uparse_all_info(id)[0]["personal"]

        if not personal:
            personal_info = "информация не указана"

        else:
            smoking_attitude = f"отношение к курению: {alc_sm_values[personal['smoking']]}"
            alcohol_attitude = f"отношение к алкоголю: {alc_sm_values[personal['alcohol']]}"
            inspired_by = f"вдохновляет: {personal['inspired_by']}"
            langs = f"языки: {', '.join(personal['langs'])}"
            life_main = f"главное в жизни: {life_main_values[personal['life_main']]}"
            people_main = f"главное в людях: {people_main_values[personal['people_main']]}"
            political = f"политические взгляды: {political_values[personal['political']]}"
            religion = f"мировоззрение: {personal['religion']}"
            personal_info = ", ".join([smoking_attitude,
                                       alcohol_attitude,
                                       inspired_by,
                                       langs,
                                       life_main,
                                       people_main,
                                       political,
                                       religion])

        return f"Жизненная позиция: {personal_info}."

    def uget_relation(self, id):
        relation = self.uparse_all_info(id)[0]["relation"]
        relation_partner = self.uparse_all_info(
            id)[0].get("relation_partner", "не указан")
        return f"Семейное положение: {relation_values[relation]}, партнер: {relation_partner}."

    def gparse_all_info(self, id):
        return self.vk.groups.getById(group_ids=id, fields=self.gall_fields)

    def gget_all_info(self, id):
        all_info = "\n".join([self.gget_name(id),
                              self.gget_screen_name(id),
                              self.gget_type(id),
                              self.gget_members_count(id),
                              self.gget_status(id)])
        return all_info

    def gget_name(self, id):
        name = self.gparse_all_info(id)[0]["name"]
        return f"Название: {name}."

    def gget_screen_name(self, id):
        screen_name = self.gparse_all_info(id)[0]["screen_name"]
        return f"Короткий адрес: {screen_name}."

    def gget_type(self, id):
        type = self.gparse_all_info(id)[0]["type"]
        return f"Тип: {type_values[type]}."

    def gget_members_count(self, id):
        members_count = self.gparse_all_info(id)[0]["members_count"]
        return f"Количество участников: {members_count}."

    def gget_status(self, id):
        status = self.gparse_all_info(id)[0].get("status", "не указан")
        return f"Статус: «{status}»."


if __name__ == "__main__":
    print("Бот запущен.")
    vk_app_helper = vk_api.VkApi(token=config["vk_app_token"])
    vk_app_info = vk_app_helper.get_api()

    discord_bot = VkCheckerDiscordBot(
        prefix=config["prefix"],
        app_info_getter=vk_app_info)
    discord_bot.run(config["discord_token"])
