import time
import datetime
from typing import Optional
from OSRS_Hiscores import Hiscores
from pydantic import BaseModel


class StatInfo(BaseModel):
    rank: int
    level: int
    experience: int
    next_level_exp: Optional[int]
    exp_to_next_level: Optional[int]


class BossInfo(BaseModel):
    rank: int
    kills: int


class UserInfo(BaseModel):
    # dict of skills <str, StatInfo>
    # dict of bosses <str, BossInfo>
    username: str
    skills: dict[str, StatInfo]
    bosses: dict[str, BossInfo]


class OsrsScrape(BaseModel):
    timestamp: float
    users: list[UserInfo]


# Get the entire stat dictionary
_BOSSES = [
    "Bounty Hunter - Hunter",
    "Bounty Hunter - Rogue",
    "Clue Scrolls (all)",
    "Clue Scrolls (beginner)",
    "Clue Scrolls (easy)",
    "Clue Scrolls (medium)",
    "Clue Scrolls (hard)",
    "Clue Scrolls (elite)",
    "Clue Scrolls (master)",
    "LMS - Rank",
    "PvP Arena - Rank",
    "Soul Wars Zeal",
    "Rifts closed",
    "Abyssal Sire",
    "Alchemical Hydra",
    "Barrows Chests",
    "Bryophyta",
    "Callisto",
    "Cerberus",
    "Chambers of Xeric",
    "Chambers of Xeric: Challenge Mode",
    "Chaos Elemental",
    "Chaos Fanatic",
    "Commander Zilyana",
    "Corporeal Beast",
    "Crazy Archaeologist",
    "Dagannoth Prime",
    "Dagannoth Rex",
    "Dagannoth Supreme",
    "Deranged Archaeologist",
    "General Graardor",
    "Giant Mole",
    "Grotesque Guardians",
    "Hespori",
    "Kalphite Queen",
    "King Black Dragon",
    "Kraken",
    "Kree'Arra",
    "K'ril Tsutsaroth",
    "Mimic",
    "Nex",
    "Nightmare",
    "Phosani's Nightmare",
    "Obor",
    "Phantom Muspah",
    "Sarachnis",
    "Scorpia",
    "Skotizo",
    "Tempoross",
    "The Gauntlet",
    "The Corrupted Gauntlet",
    "Theatre of Blood",
    "Theatre of Blood: Hard Mode",
    "Thermonuclear Smoke Devil",
    "Tombs of Amascut",
    "Tombs of Amascut: Expert Mode",
    "TzKal-Zuk",
    "TzTok-Jad",
    "Venenatis",
    "Vet'ion",
    "Vorkath",
    "Wintertodt",
    "Zalcano",
    "Zulrah",
]


def get_user_data(username: str) -> UserInfo:
    # Initialize user object, if no account type is specified, we assume 'N'
    user = Hiscores(username, "N")

    skills = {
        skill_name: StatInfo(**skill_data)
        for skill_name, skill_data in user.stats.items()
    }

    boss_data = user.data[-(len(_BOSSES) * 2 + 1) :]

    bosses = {
        boss_name: BossInfo(rank=int(boss_data[i * 2]), kills=int(boss_data[i * 2 + 1]))
        for i, boss_name in enumerate(_BOSSES)
        if boss_data[i * 2] != "-1"
    }

    return UserInfo(username=username, skills=skills, bosses=bosses)


def scrape_users(usernames: list[str]) -> OsrsScrape:
    return OsrsScrape(
        timestamp=time.time(), users=[get_user_data(username) for username in usernames]
    )


def main():
    users = [
        "shupwup",
        "jerome-o",
        "ryan the ant",
        "telemascope",
        "furion",
    ]

    data = scrape_users(users)

    # save to /data/osrs/{file friendly date, hours, minutes}.json, with permissions 644
    with open(
        f"/data/osrs/{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')}.json", "w"
    ) as f:
        f.write(data.json(indent=4))


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
