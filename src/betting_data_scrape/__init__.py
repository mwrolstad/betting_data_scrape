import argparse
import json
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
    resp = requests.post(
        url=odds_url,
        headers=HEADERS,
        json=JSON_DATA,
        cookies=COOKIES,
    )
    print(f"Got a {resp.status_code} response.")

    game_ls = resp.json()["Scores"] if "Scores" in resp.json() else []
    print(f"Found {len(game_ls)} games to scrape odds for!")

    game_odds = []
    for game_json in game_ls:
        game_odds.append(get_game_data(game_json))

    return game_odds


class BetScraper:
    def __init__(self, sport: str = "MLB", game_date: str = None, week_number: int = None, year_number: int = None):
        try:
            self.odds = scrape_games(sport, game_date, week_number, year_number)
        except Exception as e:
            print(f"An error occurred:\n{e}")
            return


def main(sport: str = "MLB", game_date: str = None, week_number: int = None, year_number: int = None):
    games = BetScraper(sport, game_date, week_number, year_number)
    print(json.dumps(games.odds, indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Pass in a sports to get the current odds using --sport and --current_line."
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
    main(args.sport, args.game_date, args.week_number, args.year_number)
