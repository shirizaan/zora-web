from absl import logging as log
import random
from typing import List
from enum import IntEnum
from .constants import HintType
from .data_table import DataTable
from .patch import Patch
from .settings import Settings
from . import flags

COMMUNITY_HINTS = {
    HintType.WOOD_SWORD: [
        "THIS IS THE ZELDA|ONE RANDOMIZER FOR ALL|WITH HINTS IN HAIKU",
        "DID SOMEBODY SAY| ... WOOD?",
        "YAY! A POINTY STICK!",
        "GOOD LUCK! WE'RE ALL|... OOPS!|WRONG RANDOMIZER!",
        "It's dangerous|to go alone.|See ya!",
        "SPEAK SOFTLY AND|CARRY A BIG STICK",
        "I'll take|S WORDS|FOR 100!",
        "FINDING THE WOOD|SWORD FILLS YOU|WITH DETERMINATION",
    ],
    HintType.WHITE_AND_MASTER_SWORD: [
        "DON'T TAKE ANYTHING|OR I'LL DISAPPEAR|FOREVER!",
        "This is heavy",
        "EVERYBODY GETS ONE",
        "COME BACK WHEN|YOU ARE READY",
        "I hate insect puns|they really bug me.",
        "Pizza joke? No I think|it's a bit too cheesy",
        "A novice skier often|jumps to contusions.",
        "Broken pencils|are pointless.",
        "Stone golems|are created as|blank slates.",
        "Ganon is a|bacon of|despair!",
        "Best advice|for a Goron?|Be Boulder.",
    ],
    HintType.SECRET: [
        "BANANA. TAKE A BUCK!|BANANA. TAKE A BUCK!",
        "HERE'S SOME MONEY|GO SEE A STAR WAR",
        "SWEET, SWEET MONEY",
        "IF YOU GET A LOT OF|THESE, SOMETHING GOOD|IS BOUND TO HAPPEN",
        "BANK ERROR IN|YOUR FAVOR|COLLECT ...",
        "YOU HAVE WON|SECOND PRIZE IN|A BEAUTY CONTEST",
        "I'd shell out|good rupees|for a conch.",
        "There’s always|money in the|Banana Stand",
        "TAKE YOUR BLOOD|MONEY AND GO.",
        "WOOOOOAAAH!|THANK YOU COKE GAMING!",
        "YOU GOT IT FOR FREE|ARE YOU HAPPY?",
        "We're in the money|We're in the money",
    ],
    HintType.DOOR_REPAIR: [
        "DON'T AWOO.|350 RUPEE PENALTY.",
        "HELP TEMMIE PAY|FOR COOL LEG",
        "QUICK, PRESS UP|AND A BEFORE I|TAKE YOUR MONEY!",
        "THAT DOOR REALLY|TIED THE ROOM TOGETHER",
        "TOSS A RUPEE|TO YOUR WITCHER",
        "YOU ARE THE|WEAKEST LINK|GOODBYE!",
        "TIME BOMB SET|GET OUT FAST!",
        "SHOW ME THE MONEY!",
        "STAND CLEAR OF THE|CLOSING DOORS, PLEASE!",
        "YOUR HEAD A SPLODE",
        "HERE'S A RUPOOR|FOR YOUR TROUBLES",
        "HONK!",
    ],
    HintType.TAKE_ANY: [
        "AH YES,|THE TWO GENDERS ...",
        "PERRIER OR CHOCOLATES?",
        "EVERYWHERE YOU LOOK|EVERYWHERE YOU GO|THERE'S A HEART",
        "CANDYGRAM FOR LINK",
        "YOU GOTTA HAVE HEART",
        "PLEASE SELECT ITEM",
        "TAKE NEITHER ITEM.|JUST LEAVE.",
        "Cake or Death?",
        "eenie, meenie,|miney, mo",
        "Limit one per customer",
    ],
    HintType.POTION_SHOP: [
        "COKE OR PEPSI?",
        "YOU'RE GIVING ME|PAPER?|I'M SO HAPPY!",
        "IF YOU WANT TO BUY THE|POTION, BE SURE TO|BRING A BOTTLE.",
        "TAKE THE RED POTION|AND SEE HOW FAR THE|RABBIT HOLE GOES",
        "THE CDC RECOMMENDS|STAYING AT LEAST SIX|TILES FROM ENEMIES",
        "THE CORNER OF|HAPPY AND HEALTHY",
        "HOW ABOUT THAT? IT'S|MY SPECIAL MEDICINE.",
        "8 YEARS OF MED SCHOOL|AND I'M STILL|IN THIS CAVE",
        "ASK YOUR DOCTOR IF|THIS MAGIC POTION|IS RIGHT FOR YOU",
        "SIDE EFFECTS MAY|INCLUDE EXTENDED|REFILL TIMES",
    ],
    HintType.SHOP_1: [
        "NOW OFFERING|CURBSIDE PICKUP",
        "SHOP TIL YOU DROP!",
        "FRESH IMPORTS FROM|KOHOLINT ISLAND",
        "COME BACK TOMORROW|FOR A TWO FOR ONE|SALE",
        "I'D BUY THAT|FOR A RUPEE",
        "DO YOU KNOW HOW MANY|DOORS I SOLD TODAY?",
        "WOAH THERE|I'VE GOT SOME NEAT|JUNK FOR SALE",
        "YOU CAN PROBABLY|FIND THIS CHEAPER|ONLINE",
        "VISIT OUR OTHER|LOCATION IN THE|WESTLAKE MALL",
        "DOWNLOAD OUR APP TO|EARN DISCOUNTS ON|FUTURE PURCHASES!",
        "I'M NOT LIKE THOSE|OTHER MERCHANTS!",
        "Math is hard.|Let's go shopping!",
    ],
    HintType.SHOP_2: [
        "AS SEEN ON TV",
        "SORRY, WE'RE ALL OUT|OF DISINFECTING WIPES"
        "USE DISCOUNT CODE|\"ZORA\" FOR 10 PERCENT|OFF YOUR NEXT ORDER",
        "WHAT KIND OF|CHEESE SHOP|IS THIS?",
        "AND IT CAN BE YOURS|IF THE PRICE IS RIGHT!",
        "SHOP LOCAL, SUPPORT|SMALL BUSINESSES",
        "HELLO TRAVELLER!|HOW CAN I HELP YOU?",
        "I HAVE GREAT DEALS|IN STORE FOR YOU",
        "THE MIDDLE ITEM IS|MY FAMILY HEIRLOOM",
        "GET IN, LOSER,|WE'RE GOING SHOPPING",
        "SIGN UP FOR THE STORE|CARD TO GET 10 PERCENT|OFF YOUR 1ST PURCHASE",
        "See back of receipt|for the return policy",
        "Merchandising!|Where the real money|from the movie is made",
    ],
    HintType.ANY_ROAD: [
        "I CHALLENGE YOU TO|A STAIRING CONTEST!",
        "LUDICROUS SPEED. GO!",
        "DOOR 1, 2, OR 3?",
        "DO YOU KNOW THE WAY|TO SAN JOSE?",
        "JUST KEEP SWIMMING!",
        "YOU KNOW BAGU?|THEN I WILL HELP|YOU CROSS",
        "WELCOME TO|WARP ZONE",
        "BE CAREFUL, STAIRS|ARE ALWAYS UP TO|SOMETHING",
        "TRAVELLING TOO MUCH?|TRY A ZOOM MEETING",
        "MY ADVICE? TAKE THE|ROAD LESS TRAVELLED",
        "IN CASE OF EMERGENCY|PLEASE USE STAIRWAYS",
        "THIS IS A|LOST WOODS-BOUND|4 EXPRESS TRAIN",
    ],
    HintType.PAY_ME: [
        "ARE THESE HINTS|VANILLA? BUY ONE|TO FIND OUT",
        "HEY! LISTEN!",
        "I HAVE APPROXIMATE|KNOWLEDGE OF|MANY THINGS",
    ],
    HintType.PAY_ANSWER_1: [
        "YES",
        "YES. YES THEY ARE.",
        "NO",
        "I DON'T THINK SO",
        "MAYBE?",
        "KINDA?",
        "WOW, YOU'RE RICH!",
        "OUTLOOK UNCLEAR|COME BACK LATER",
    ],
    HintType.PAY_ANSWER_2: ["I DON'T THINK SO?",],
    HintType.PAY_ANSWER_3: ["MAYBE?",],
    HintType.PAY_ANSWER_4: ["YES. YES THEY ARE.",],
    HintType.HUNGRY_ENEMY: [
        "grumble grumble ...|Seriously, you were|supposed to bring food",
        "OM NOM NOM NOM TIME?",
        "ARE YOU GOING|TO EAT THAT?",
        "FEED ME SEYMOUR!",
        "MUMBLE MUMBLE|SOMETHING ABOUT FOOD"
        "BUT YOU'RE|STILL HUNGRY ...",
        "DO YOU HAVE|A VEGAN OPTION?",
        "ARE YOU MY UBER EATS|DELIVERY CARRIER?",
        "WE TALK ABOUT FOOD HERE",
        "C IS FOR COOKIE|THAT'S GOOD ENOUGH|FOR ME",
        "I'VE HAD ONE, YES.|BUT WHAT ABOUT|SECOND BREAKFAST?",
        "If you find|my lunch,|don't eat it.",
        "If you were a burrito,|what kind of a|burrito would you be?",
        "I am on a seafood|diet. Every time|I see food, I eat it.",
        "The soup is|for my family.",
    ],
    HintType.ENGLISH_COMMUNITY_HINT: [
        "WHAT'S WORLD RECORD|FOR THIS SEED?",
        "Up, Up, Down, Down,|Left, Right, Left,|Right, B, A",
        "The limit does|not exist! The limit|does not exist!",
        "MEOW!",
        "STOP TALKING ABOUT|VORING THE FAE",
        "ORB!",
        "Beware the evil Mr.|Glitch. He will eat|you if you are wrong.",
        "SAY CHEESE!",
        "IS THIS ZELDA OR|GHOSTS AND MOBLINS?",
        "YOUR AD HERE|CALL 555-ZORA",
        "THERE ARE NO |CHICKENS IN|ZELDA 1",
        "AMAZING. EVERY WORD|OF WHAT YOU JUST SAID|WAS WRONG",
        "MARCY?|MARCY?",
        "NAME THAT INKBLOT",
        "ZZZZZZZZ ... |ZZZZZZZZ... |ARE THEY GONE YET?",
        "THIS LINE HERE|IS MOSTLY|FILLER",
        "NEED MORE QUOTE|SUBMISSIONS PLEASE!",
        "HELLO WORLD!",
        "MEOW! MEOW!",
        "HAVE YOU NOTICED THESE|RANDOMIZER ITEM HINTS|ARE ALL IN HAIKU?",
        "Welcome!|You've got mail!",
        "WRITING'S NOT THAT|EASY BUT GRAMMARLY|CAN HELP",
        "MAY THE ODDS BE EVER|IN YOUR FAVOR",
        "DO IT ROCKAPELLA!",
        "WE'VE UPDATED THE|TERMS OF OUR|PRIVACY POLICY",
        "THIS IS 2020",
        "YOU ARE IN A MAZE OF|TWISTY LITTLE PASSAGES|ALL ALIKE.",
        "STAGE CLEAR|TRY NEXT",
        "ONE OF US ALWAYS|TELLS THE TRUTH.",
        "Bunnies are cute",
        "Are we in|go mode yet?",
        "This message will|self destruct|in ten seconds.",
        "ERREUR DE TRADUCTION.|S'IL TE PLAIT|REESSAYER",
        "I AM ERROR",
        "I JUST MET YOU & THIS|IS CRAZY BUT HERES MY|NUMBER. CALL ME MAYBE?",
        "IF YOU CAN READ THIS|YOU DON'T NEED|NEW GLASSES",
        "INCONCEIVABLE!",
        "Stop trying to make|fetch happen. It's not|going to happen.",
        "BY YOUR COMMAND",
        "WOW, I DON'T EVEN|KNOW WHAT TO SAY|TO YOU ANYMORE!",
    ],
    HintType.BOMB_UPGRADE: [
        "BADA BING|BADA BANG|BADA BOOM",
        "HI, I'M BOMB BARKER|please have your pets|spayed or neutered!",
        "SPLOOSH!|KABOOM!",
        "SOMEONE SET UP US|THE BOMB UPGRADE",
        "BOOM CLAP, THE SOUND|OF MY HEART THE BEAT|GOES ON AND ON AND ON",
        "KEEP TALKING AND|NOBODY EXPLODES",
        "YEAH, YOU AND|EVERYONE ELSE WANTS|TO HOARD BOMBS",
    ],
    HintType.MMG: [
        "WHAT HAPPENS IN VEGAS|STAYS IN VEGAS!",
        "LET'S PLAY MONEY|TAKING GAME",
        "THE HOUSE ALWAYS WINS",
        "TRENDY GAME|ONE PLAY|10 RUPEES",
        "THE CURRENT LOTTO|JACKPOT IS|255 RUPEES",
        "LET'S GET LUCKY!",
        "Have a rupee,|leave a rupee",
        "BONUS CHANCE||PRESS 'A' BUTTON",
    ],
    HintType.TRIFORCE_CHECK: [
        "MASK OR FACE COVERING|REQUIRED FOR ENTRY",
        "PLEASE SUGGEST MORE|TRIFORCE CHECK QUOTES|IN THE ZORA DISCORD",
        "IS THIS A|DOKI DOKI PANIC|REMAKE?",
        "One does not|simply walk into|Death Mountain",
        "YOU SHALL NOT PASS!",
        "COME BACK LATER",
        "Let me in!",
        "NO SOUP FOR YOU!|COME BACK ONE YEAR|NEXT!",
    ],
    HintType.MUGGER: [
        "GENDER ISN'T BINARY|BUT THIS CHOICE IS",
        "SUGGEST MUGGER QUOTES|IN THE ZORA DISCORD|PLEASE!",
        "I'M SORRY,|WE DON'T|TAKE DISCOVER",
        "USE E-Z PASS TO|SAVE TIME PAYING TOLLS",
        "FOR YOUR CONVENIENCE|WE ACCEPT MULTIPLE|PAYMENT METHODS",
        "TICKETS, PLEASE!",
        "GOTTA PAY TO PLAY",
        "PLEASE INSERT COIN|TO CONTINUE"
        "I KNOW ...|I DON'T LIKE IN-APP|PURCHASES EITHER",
    ],
    HintType.FRENCH_COMMUNITY_HINT: [
        "Han Ouais",
        "Redriel n'a pas|trouve l'epee",
        "Chut ne dites|rien a Redriel",
        "Aurel est deja au 9",
        "rip",
        "Raphael mets|dans l'carton",
        "Est-ce une seed|de Mme goth?",
        "Coucou, tu veux|voir ma seed?",
        "entourlipoule",
        "One Cycle Ganon,|quel plaisir",
        "C'est l'echelle !!!",
        "Ganon se cache|dans le nord",
        "Tu devrais m'voir|dans la couronne",
        "Il dit qu'il a|plus de genou",
        "Et la marmotte,|elle met le chocolat|dans le papier alu",
        "ecouter,|repeter,|en francais",
        "je suis un ananas",
        "s'il vous plait,|dessine-moi|un mouton",
        "ERREUR DE TRADUCTION.|S'IL TE PLAIT|REESSAYER",
        "WHAT DO FRENCH PEOPLE|CALL A BAD THURSDAY?|A TRAJEUDI!",
        "I have no Monet|to buy Degas|to make the Van Gogh.",
        "ARRETE-TOI ET|REPOSE-TOI ICI",
        "JE NE PEUX|PLUS T'AIDER,|MAINTENANT VA.",
        "UTILISE LES CLES|DANS LES PALAIS|ELLES S'Y TROUVENT",
        "DESOLE, JE|NE SAIS RIEN",
        "CONNAIS-TU BAGU?|ALORS JE PEUX|T'AIDER A TRAVERSER",
        "LE DEMON N'AIME|PAS LE BRUIT",
    ]
}

STAR_WARS_STORY_TEXT = [
    "  ^$%$%$ Episode II US $%$%$%^  ",
    "  @    KAIZO KAIZO PANIC     #  ",
    "  #                          @  ",
    "  @ It is a period of dream- #  ",
    "  # ing. Mario and Toad have @  ",
    "  @ won their  first victory #  ",
    "  # against the evil Mouser. @  ",
    "  @ Pursued  by  Wart's sin- #  ",
    "  # ister  agents,  Princess @  ",
    "  @ Peach  races  home  with #  ",
    "  # stolen  plans  that  can @  ",
    "  @ save  Toad  and  restore #  ",
    "  # freedom to subcon...     #  ",
    "  ^$%$%$%$%$%$%$%$%$%$%$%$%$%^  ",
]

RICK_ROLL_STORY_TEXT = [
    "  ^$%$%$%$%$%$%$%$%$%$%$%$%$%^  ",
    "  @ We're  no  strangers  to #  ",
    "  @ love. You know the rules #  ",
    "  @ and  so  do  I.  A  full #  ",
    "  @ commitment's   what  I'm #  ",
    "  @ thinking    of.      You #  ",
    "  @ wouldn't  get  this from #  ",
    "  @ any other guy ...        #  ",
    "  #                          @  ",
    "  # Never gonna give you up  @  ",
    "  # Never gonna let you down @  ",
    "  # Never gonna run around   @  ",
    "  # and desert you ...       @  ",
    "  ^$%$%$%$%$%$%$%$%$%$%$%$%$%^  ",
]


class TextDataTable():
  TEXT_SPEED_ADDRESS = 0x482D
  TEXT_LEVEL_ADDRESS = 0x19D17
  FAST_TEXT_SPEED_SETTING = 2

  def __init__(self, settings: Settings, data_table: DataTable) -> None:
    self.patch = Patch()
    self.settings = settings
    self.data_table = data_table
    self.hints = self.data_table.location_hints.copy()
    self.hints.extend(self.data_table.item_hints.copy())
    random.shuffle(self.hints)

  def RandomizeTitleStory(self) -> None:
    addr = 0x1A528
    for line in RICK_ROLL_STORY_TEXT:
      log.info("%x" % addr)
      if addr >= 0x1A8B3:
        log.warning("UH OH 1!")
        break
      self.patch.AddData(addr, self.__ascii_string_to_bytes(line))
      addr += 0x23
      if "             " in line:
        log.info("blank!")
        continue
      if addr >= 0x1A8B3:
        log.warning("UH OH 2!")
        break
      self.patch.AddData(addr, self.__ascii_string_to_bytes("  #                          @  "))
      addr += 0x23

  def GetPatch(self) -> Patch:
    self._MaybeAddTextSpeedToPatch()
    self._MaybeAddLevelNameToPatch()
    self.DoTextyStuff()
    self.RandomizeTitleStory()
    return self.patch

  def _MaybeAddTextSpeedToPatch(self) -> None:
    if self.settings.IsEnabled(flags.FastText):
      self.patch.AddData(self.TEXT_SPEED_ADDRESS, [self.FAST_TEXT_SPEED_SETTING])

  def _MaybeAddLevelNameToPatch(self) -> None:
    if not self.settings.IsEnabled(flags.RandomizeLevelText):
      return
    phrase = random_level_text = random.choice([
        'house-',
        'abode-',
        'block-',
        '_cage-',
        '_home-',
        '_maze-',
        'shape-',
        'kitty-',
        'vault-',
        'thing-',
        'world-',
        '_land-',
        'puppy-',
        '_area-',
        'roost-',
        '_hole-',
        '_cave-',
    ])
    if self.settings.IsEnabled(flags.FrenchCommunityHints):
      phrase = random.choice(["monde-", "terre-"])  #, "tempe-"])
    assert len(self.__ascii_string_to_bytes(phrase)) == 6
    self.patch.AddData(self.TEXT_LEVEL_ADDRESS, self.__ascii_string_to_bytes(phrase))

  def __ascii_string_to_bytes(self, phrase: str) -> List[int]:
    """Convert the string to a form the game can understand."""
    return list(map(self._ascii_char_to_bytes, phrase))

  @staticmethod
  def _ascii_char_to_bytes(char: str) -> int:
    if ord(char) >= 48 and ord(char) <= 57:  # 0-9
      return ord(char) - 48
    if ord(char) >= 65 and ord(char) <= 90:  # A-Z
      return ord(char) - 55
    if ord(char) >= 97 and ord(char) <= 122:  # a-z
      return ord(char) - 87

    misc_char_map = {
        ' ': 0x24,  # Meant to represent a space.
        '_': 0x24,  # Meant to represent a space.
        '~': 0x25,  # Meant to represent leading space.
        ',': 0x28,
        '!': 0x29,
        "'": 0x2A,
        '&': 0x2B,
        '.': 0x2C,
        '"': 0x2D,
        '?': 0x2E,
        '-': 0x2F,
        '@': 0xE2,
        '#': 0xE3,
        '$': 0xE4,
        '%': 0xE5,
        '^': 0xE6,
    }

    return misc_char_map[char] or misc_char_map['_']

  def DoTextyStuff(self) -> None:
    addresses: List[int] = []
    for n in range(19):
      addresses.append(0x404C + n * 0x45)
    for n in range(19):
      addresses.append(0x7770 + n * 0x45)

    counter = 0
    for address in addresses:
      low_byte = address % 0x100
      high_byte = int((address - low_byte) / 0x100)
      high_byte += 0x40
      self.patch.AddData(0x4000 + 0x10 + 2 * counter, [low_byte, high_byte])
      self.patch.AddData(address + 0x10, self.NewGenerateTestingString(counter))
      counter += 1

  def NewGenerateTestingString(self, num: int) -> List[int]:
    hint_type = HintType(num)
    if hint_type == HintType.LETTER_CAVE:
      hint = self.data_table.letter_cave_text
    elif (num in range(19, 34) and not hint_type in [HintType.BOMB_UPGRADE, HintType.MUGGER] or
          num in range(10, 14)):
      hint = self.hints.pop(0)
      log.info(hint)
    elif hint_type not in COMMUNITY_HINTS:
      log.warning("Warning! nothing for %s" % hint_type)
      hint_type = HintType.FRENCH_COMMUNITY_HINT if self.settings.IsEnabled(
          flags.FrenchCommunityHints) else HintType.ENGLISH_COMMUNITY_HINT
      hint = random.choice(COMMUNITY_HINTS[hint_type])
    else:
      if self.settings.IsEnabled(flags.FrenchCommunityHints):
        hint_type = HintType.FRENCH_COMMUNITY_HINT
      hint = random.choice(COMMUNITY_HINTS[hint_type])
    lines = hint.split('|')
    num_lines = len(lines)
    tbr: List[int] = []
    for i in range(3):
      is_last_line = True if i + 1 == num_lines else False
      log.info(lines[i])
      if len(lines[i]) > 23:
        log.warning("WARNING! long line: %s" % lines[i])
      tbr.append(0x25)
      line = lines[i].strip().center(22)
      things = self.__ascii_string_to_bytes(lines[i].strip().center(22))
      foo = True
      for n in range(len(things)):
        if foo and things[n] == 0x24:
          things[n] = 0x25
        else:
          break

      modifier = 0xC0
      if not is_last_line and i == 0:
        modifier = 0x80
      elif not is_last_line and i == 1:
        modifier = 0x40
      log.info(things)
      things[-1] += modifier
      log.info(things)
      tbr.extend(things)
      if is_last_line:
        break
    return tbr
