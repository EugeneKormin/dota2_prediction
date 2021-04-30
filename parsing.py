from browser import Browser
from bs4 import BeautifulSoup
import codecs
from time import sleep


class Parsing(object):
    def __init__(self, match_id):
        browser = Browser()
        html_code = browser.match_finding_sequence(match_id=match_id)
        soup = BeautifulSoup(html_code)

        #soup = BeautifulSoup(codecs.open("html.html", 'r', "utf-8").read())

        overall = soup.find("div", class_="flex-item series-link")
        best_of = int(overall.find("a", class_="esports-link").get_text().split()[2].replace('\r\n', ''))
        head_to_head = overall.find("div", class_="head-to-head")
        teams = head_to_head.find_all("div", class_="team")
        team_1_name = teams[0].find("img")["alt"]
        team_2_name = teams[1].find("img")["alt"]

        team_1_score = int(teams[0].find("div", class_="score").get_text().replace('\r\n', '').replace(' ', ''))
        team_2_score = int(teams[1].find("div", class_="score").get_text().replace('\r\n', '').replace(' ', ''))

        team_1_winner = teams[0].find("i", class_="fa fa-trophy")
        team_2_winner = teams[1].find("i", class_="fa fa-trophy")

        series_winner = "draw"
        if team_1_winner is not None and team_2_winner is None:
            series_winner = team_1_name
        elif team_1_winner is None and team_2_winner is not None:
            series_winner = team_2_name

        maps = soup.find_all("div", class_="flex-item flex-small")

        team_1_kills = 0
        team_2_kills = 0

        match_id_list = []

        data = {"maps_played": len(maps),
                "best_of": best_of}
        overall = {
            "match_ids": [],
            "series_winner": series_winner,
            "team1": {
                "name": team_1_name,
                "kills": -1,
                "side": "n/a",
                "score": team_1_score
            },
            "team2": {
                "name": team_2_name,
                "kills": -1,
                "side": "n/a",
                "score": team_2_score
            },
        }

        data.update({"overall": overall})

        for num, map in enumerate(maps):
            check_if_game_was_played = map.find("div", class_="empty")
            if check_if_game_was_played is None:
                browser.select_game(num+1)
                sleep(3)
                html_code = browser.get_html_from_page()
                soup = BeautifulSoup(html_code)

                match_id = str(map.find("a").get('href')).split('/')[2]
                duration = int(map.find("div", class_="duration")
                               .get_text().replace('\r\n', '').replace(' ', '').split(':')[0]) * 60 \
                           + int(map.find("div", class_="duration")
                                 .get_text().replace('\r\n', '').replace(' ', '').split(':')[1])
                match_score = map.find("span", class_="score-line")
                match_score = match_score.find_all("span")

                current_map_team_1_kills = int(match_score[0].get_text().replace('\r\n', '').replace(' ', '').split(':')[1]) + 1
                current_map_team_2_kills = int(match_score[2].get_text().replace('\r\n', '').replace(' ', '').split(':')[1]) + 1

                radiant_result = soup.find("section", class_="radiant")
                radiant_team_name = radiant_result.find("span", class_="team-image").find("img")["alt"]

                dire_result = soup.find("section", class_="dire")
                dire_team_name = dire_result.find("span", class_="team-image").find("img")["alt"]
                dire_victory = dire_result.find("i", class_="fa fa-trophy")

                winner = dire_team_name
                if dire_victory is None:
                    winner = radiant_team_name

                team_1_side = "radiant"
                if team_1_name == dire_team_name:
                    team_1_side = "dire"

                team_2_side = "radiant"
                if team_2_name == dire_team_name:
                    team_2_side = "dire"

            else:
                current_map_team_1_kills = current_map_team_2_kills = 0
                match_id = map.find("div", class_="empty").get_text()
                team_1_side = team_2_side = duration = winner = radiant_team_name = dire_team_name = "n/a"

            team_1_kills += current_map_team_1_kills
            team_2_kills += current_map_team_2_kills

            current_map = {
                "match_id": match_id,
                "map_winner": winner,
                "team1": {
                    "name": team_1_name,
                    "kills": current_map_team_1_kills-1,
                    "side": team_1_side,
                    "score": team_1_score
                },
                "team2": {
                    "name": team_2_name,
                    "kills": current_map_team_2_kills,
                    "side": team_2_side,
                    "score": team_2_score
                },
            }
            data.update({"map_{}".format(num+1): current_map})
            sleep(5)

        data["overall"]["team1"]["kills"] = team_1_kills
        data["overall"]["team2"]["kills"] = team_2_kills
        data["overall"]["total_kills"] = team_1_kills + team_2_kills

        print(data)
