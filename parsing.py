from browser import Browser
from bs4 import BeautifulSoup


class Parsing(object):
    def __init__(self, match_id):
        browser = Browser()
        html_code = browser.get_html_from_match_id(browser=browser, match_id=match_id)
        soup = BeautifulSoup(html_code)

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

        series_winner = ""
        if team_1_winner is not None and team_2_winner is None:
            series_winner = team_1_name
        elif team_1_winner is None and team_2_winner is not None:
            series_winner = team_2_name

        maps = soup.find_all("div", class_="flex-item flex-small")
        data = {"maps_played": len(maps)}
        data.update({"best_of": best_of})
        overall = {
            "series_winner": series_winner,
            "series_score": "-1:-1",
            "team1": {
                "name": team_1_name,
                "team1_score": team_1_score,
                "side": "n/a",
                "score": -1,
                "points_taken": -1
            },
            "team2": {
                "name": team_2_name,
                "team2_score": team_2_score,
                "side": "n/a",
                "score": -1,
                "points_taken": -1
            },
        }

        data.update({"overall": overall})
        for num, map in enumerate(maps):
            match_id = str(map.find("a").get('href')).split('/')[2]
            duration = int(map.find("div", class_="duration")
                           .get_text().replace('\r\n', '').replace(' ', '').split(':')[0]) * 60 \
                       + int(map.find("div", class_="duration")
                             .get_text().replace('\r\n', '').replace(' ', '').split(':')[1])
            match_score = map.find("span", class_="score-line")
            match_score = match_score.find_all("span")

            radiant_team = soup.find("section", class_="radiant")
            radiant_team_name = radiant_team.find("span", class_="team-image").find("img")["alt"]
            radiant_victory = radiant_team.find("span", class_="victory-icon")

            dire_team = soup.find("section", class_="dire")
            dire_team_name = dire_team.find("span", class_="team-image").find("img")["alt"]
            dire_victory = dire_team.find("span", class_="victory-icon")

            winner_score = match_score[0].get_text().replace('\r\n', '').replace(' ', '').split(':')[1]
            loser_score = match_score[2].get_text().replace('\r\n', '').replace(' ', '').split(':')[1]

            map = {
                "map_" + str(num+1): {"team1": {"name": radiant_team_name, "side": "radiant"},
                "team2": {"name": dire_team_name, "side": "dire"}}
            }

            data.update({"map_" + str(num + 1): map})
            map.update({"duration": duration, "match_id": match_id})

            if radiant_victory is not None and dire_victory is None:
                map["map_" + str(num+1)]["team1"]["score"] = winner_score
                map["map_" + str(num + 1)]["team2"]["score"] = loser_score
                map["map_" + str(num+1)]["team1"]["points_taken"] = 1
                map["map_" + str(num+1)]["team2"]["points_taken"] = 0

            elif radiant_victory is None and dire_victory is not None:
                map["map_" + str(num+1)]["team1"]["score"] = loser_score
                map["map_" + str(num + 1)]["team2"]["score"] = winner_score
                map["map_" + str(num+1)]["team1"]["points_taken"] = 0
                map["map_" + str(num+1)]["team2"]["points_taken"] = 1

        print(data)
        pass
