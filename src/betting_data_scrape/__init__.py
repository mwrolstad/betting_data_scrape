import argparse
import json
import logging
import requests

SPORT_DICT = {
    "NBA": "nba",
    "NFL": "nfl",
    "MLB": "mlb",
    "NHL": "nhl",
    "CBB": "cbb",
}

COOKIES = {
    '_ga': 'GA1.1.1079793625.1684695553',
    '_cioanonid': '71c0d511-b820-930e-c137-1f2175ec4eec',
    '__adroll_fpc': '6f2ab55c2f2dd3849eb39eef30ab3e42-1684695553796',
    '_fbp': 'fb.1.1684695553952.700964659',
    '_ga_QXY5NYRE7Q': 'GS1.1.1684695552.1.1.1684695842.0.0.0',
    '__ar_v4': 'NHFCO3TELVGCHHJD5FHXVD%3A20230520%3A3%7CZUS4OCBXGBDWLCGQSOCSQN%3A20230520%3A3%7C2YUP7TATPFC7XD6D2GIARW%3A20230520%3A3',
}

COOKIES_CLASSIC = {
    'geo_state': '%7B%22Code%22%3A%22WA%22%2C%22Name%22%3A%22Washington%22%7D',
    'fdw_geo_state': 'WA',
    '_ga': 'GA1.1.2058534755.1692372551',
    '__adroll_fpc': '754dbbb0f6455c592921d35fbece009d-1692372552206',
    '_fbp': 'fb.1.1692372552405.1175785044',
    '_ga_QXY5NYRE7Q': 'GS1.1.1692372550.1.1.1692372719.0.0.0',
    '__ar_v4': '2YUP7TATPFC7XD6D2GIARW%3A20230817%3A6%7CZUS4OCBXGBDWLCGQSOCSQN%3A20230817%3A6%7CNHFCO3TELVGCHHJD5FHXVD%3A20230817%3A6',
}

HEADERS = {
    'authority': 'bettingdata.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,ht;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://bettingdata.com',
    'pragma': 'no-cache',
    # 'referer': 'https://bettingdata.com/mlb/moneyline?scope=2&subscope=1&season=2023&seasontype=1&date=05-21-2023&teamkey=ARI&client=1&state=WORLD&league=mlb&widget_scope=1',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}

HEADERS_CLASSIC = {
    'authority': 'bettingdata.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9,ht;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'cookie': 'geo_state=%7B%22Code%22%3A%22WA%22%2C%22Name%22%3A%22Washington%22%7D; fdw_geo_state=WA; _ga=GA1.1.2058534755.1692372551; __adroll_fpc=754dbbb0f6455c592921d35fbece009d-1692372552206; _fbp=fb.1.1692372552405.1175785044; _ga_QXY5NYRE7Q=GS1.1.1692372550.1.1.1692372719.0.0.0; __ar_v4=2YUP7TATPFC7XD6D2GIARW%3A20230817%3A6%7CZUS4OCBXGBDWLCGQSOCSQN%3A20230817%3A6%7CNHFCO3TELVGCHHJD5FHXVD%3A20230817%3A6',
    'origin': 'https://bettingdata.com',
    'pragma': 'no-cache',
    'referer': 'https://bettingdata.com/mlb/moneyline',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

JSON_DATA = {
    'filters': {
        'scope': 2,
        'subscope': 1,
        # 'week': None,
        # 'season': 2023,
        'seasontype': 1,
        'team': None,
        'conference': None,
        'exportType': None,
        # 'date': '05-21-2023',
        'teamkey': 'ARI',
        'show_no_odds': False,
        'client': 1,
        'state': 'WORLD',
        'geo_state': None,
        # 'league': 'mlb',
        'widget_scope': 1,
    },
}

JSON_DATA_CLASSIC = {
    'sort': '',
    'group': '',
    'filter': '',
    'filters.scope': '2',
    'filters.subscope': '1',
    'filters.week': '',
    'filters.season': '2023',
    'filters.seasontype': '1',
    'filters.team': '',
    'filters.conference': '',
    'filters.exportType': '',
    'filters.date': '08-18-2023',
    'filters.teamkey': 'ARI',
    'filters.show_no_odds': 'false',
    'filters.client': '1',
    'filters.state': 'WORLD',
    'filters.geo_state': '',
    'filters.league': 'mlb',
    'filters.widget_scope': '1',
}

BASE_URL = "https://bettingdata.com"

def get_game_data(game_json: dict) -> dict:
    team_json = {}
    try:
        team_json["game_date"] = game_json["DayString"]
        team_json["home_team"] = game_json["HomeTeamDetails"]["FullName"]
        team_json["home_team_loc"] = game_json["HomeTeamDetails"]["City"]
        team_json["home_team_name"] = game_json["HomeTeamDetails"]["Name"]
        team_json["home_team_abrv"] = game_json["HomeTeam"]
        team_json["home_moneyline"] = game_json["Consensus"]["HomeMoneyLine"]
        team_json["home_run_line"] = game_json["Consensus"]["HomePointSpread"]
        team_json["home_run_line_payout"] = game_json["Consensus"]["HomePointSpreadPayout"]

        team_json["away_team"] = game_json["AwayTeamDetails"]["FullName"]
        team_json["away_team_loc"] = game_json["AwayTeamDetails"]["City"]
        team_json["away_team_name"] = game_json["AwayTeamDetails"]["Name"]
        team_json["away_team_abrv"] = game_json["AwayTeam"]
        team_json["away_moneyline"] = game_json["Consensus"]["AwayMoneyLine"]
        team_json["away_run_line"] = game_json["Consensus"]["AwayPointSpread"]
        team_json["away_run_line_payout"] = game_json["Consensus"]["AwayPointSpreadPayout"]

        team_json["over_under"] = game_json["Consensus"]["OverUnder"]
        team_json["over"] = game_json["Consensus"]["OverPayout"]
        team_json["under"] = game_json["Consensus"]["UnderPayout"]
    except Exception as e:
        print("Exception:", e)
    finally:
        return team_json

def get_game_data_classic(game_json: dict, game_date: str) -> dict:
    team_json = {}
    try:
        team_json["game_date"] = game_date
        team_json["home_team"] = game_json["HomeTeamAbbv"] + " " + game_json["HomeTeamName"]
        team_json["home_team_loc"] = game_json["HomeTeamAbbv"]
        team_json["home_team_name"] = game_json["HomeTeamName"]
        team_json["home_team_abrv"] = game_json["HomeTeamAbbv"]
        team_json["home_moneyline"] = game_json["HomeTeamMoneyLine"]
        team_json["home_run_line"] = game_json["PointSpread"] if game_json["HomeTeamName"] in game_json["Favorite"] else game_json["PointSpread"].replace("-", "+")
        team_json["home_run_line_payout"] = None

        team_json["away_team"] = game_json["AwayTeamAbbv"] + " " + game_json["AwayTeamName"]
        team_json["away_team_loc"] = game_json["AwayTeamAbbv"]
        team_json["away_team_name"] = game_json["AwayTeamName"]
        team_json["away_team_abrv"] = game_json["AwayTeamAbbv"]
        team_json["away_moneyline"] = game_json["AwayTeamMoneyLine"]
        team_json["away_run_line"] = game_json["PointSpread"] if game_json["awayTeamName"] in game_json["Favorite"] else game_json["PointSpread"].replace("-", "+")
        team_json["away_run_line_payout"] = None

        team_json["over_under"] = game_json["OverUnder"]
        team_json["over"] = None
        team_json["under"] = None
    except Exception as e:
        print("Exception:", e)
    finally:
        return team_json


def scrape_games_classic(sport: str = "MLB", game_date: str = None, week_number: int = None, year_number: int = None):
    odds_url = f"{BASE_URL}/{sport}_Odds/OddsClassic_Read"
    JSON_DATA_CLASSIC.update(
        {
            "filter.league": SPORT_DICT[sport],
            "filter.date": game_date,
            "filter.week": "",
            "filter.season": int(game_date.split("-")[2]) if game_date else year_number,
        }
    )
    print(f"Making the call to URL: {odds_url}")
    print(f"Making the call with payload:\n{JSON_DATA_CLASSIC}")
    try:
        resp = requests.post(
            url=odds_url,
            headers=HEADERS_CLASSIC,
            data=JSON_DATA_CLASSIC,
            cookies=COOKIES_CLASSIC,
        )
        print(f"Got a {resp.status_code} response.")
        print(f"Got some JSON:\n{resp.json()}")
    except Exception as e:
        print(f"Got an error:\n{e}")

    game_ls = resp.json()["Data"] if "Data" in resp.json() else []
    print(f"Found {len(game_ls)} games to scrape odds for!")

    game_odds = []
    for game_json in game_ls:
        game_odds.append(get_game_data_classic(game_json, game_date))

    return game_odds


def scrape_games(sport: str = "MLB", game_date: str = None, week_number: int = None, year_number: int = None):
    odds_url = f"{BASE_URL}/{sport}_Odds/Odds_Read"
    JSON_DATA["filters"].update(
        {
            "league": SPORT_DICT[sport],
            "date": game_date,
            "week": week_number,
            "season": int(game_date.split("-")[2]) if game_date else year_number,
        }
    )
    print(f"Making the call to URL: {odds_url}")
    try:
        resp = requests.post(
            url=odds_url,
            headers=HEADERS,
            json=JSON_DATA,
            cookies=COOKIES,
        )
        print(f"Got a {resp.status_code} response.")
    except Exception as e:
        print(f"Got an error:\n{e}")

    game_ls = resp.json()["Scores"] if "Scores" in resp.json() else []
    print(f"Found {len(game_ls)} games to scrape odds for!")

    game_odds = []
    for game_json in game_ls:
        game_odds.append(get_game_data(game_json))

    return game_odds


class BetScraper:
    def __init__(self, sport: str = "MLB", game_date: str = None, week_number: int = None, year_number: int = None, classic: bool = False):
        try:
            self.odds = scrape_games_classic(sport, game_date, week_number, year_number) if classic else scrape_games(sport, game_date, week_number, year_number)

        except Exception as e:
            print(f"An error occurred:\n{e}")
            return


def main(sport: str = "MLB", game_date: str = None, week_number: int = None, year_number: int = None, classic: bool = False):
    games = BetScraper(sport, game_date, week_number, year_number, classic)
    print(json.dumps(games.odds, indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Pass in a sports to get the current odds using --sport and --current_line."
    )
    parser.add_argument(
        "--classic",
        required=False,
        action="store_true",
        default=False,
        help="Indicate if you want to use the OddsClassic endpoint.",
    )
    parser.add_argument(
        "--sport",
        required=False,
        help="Pass in a sport to scrape, i.e. NFL, NBA, or MLB.",
    )
    parser.add_argument(
        "--game_date",
        required=False,
        help="Pass the date to scrape in the format `MM-DD-YYYY`, i.e. 05-04-2023.",
    )
    parser.add_argument(
        "--week_number",
        required=False,
        help="If your are scraping NFL data, this is the week number to scrape.",
    )
    parser.add_argument(
        "--year_number",
        required=False,
        help="If your are scraping NFL data, this is the year number to scrape.",
    )
    args = parser.parse_args()
    main(args.sport, args.game_date, args.week_number, args.year_number, args.classic)
