""" this module contains a function that will search text files for: bsn, iban, email, tel, zip, adress, cv types."""

import re
import spacy
import string
import phonenumbers
from phonenumbers import timezone
from langdetect import detect, LangDetectException

PRIVACY_TYPES = [
    "bsn",
    "iban",
    "email",
    "telnr",
    "zip",
    "address",
    "cv",
    "credentials",
    "creditcard",
    "passport",
]

CV_KEYWORDS = ["resume", "cv", "curriculum vitae", "personalia"]

CREDENTIALS_KEYWORDS = [
    "gebruiker",
    "gebruikersnaam",
    "account",
    "accountnaam",
    "user",
    "username",
    "usr",
    "wachtwoord",
    "ww",
    "password",
    "pwd",
    "pass",
    "credentials",
    "inloggegevens",
    "login",
    "pw",
]

LETTERS = {ord(d): str(i) for i, d in enumerate(string.digits + string.ascii_uppercase)}


def _remove_entities(txt: str, entity_list: list[str]) -> str:
    """
    It takes a string and removes all substrings given by a list of strings
    Args:
        txt (str): an input string / document from which you want to remove substrings
        found_list (list[str]): a list of substrings to remove.

    Returns:
        A string without the substrings given in the list
    """
    assert isinstance(txt, str), "txt should be a str"
    assert isinstance(entity_list, list), "found_list should be a list of strings"
    assert all(
        isinstance(elem, str) for elem in entity_list
    ), "found_list should be a list of strings"
    if list == []:
        return txt
    else:
        for l in entity_list:
            txt = re.sub(l, "", txt)
        return txt


def _extract_ssn(txt: str) -> list[str]:
    """
    It takes a string extracts all valid dutch social security numbers from it
        Args:
            txt (str): an input string from which we want to extract social security numbers from

        Returns:
            A list of valid found ssn
    """
    assert isinstance(txt, str), "txt should be a str"
    bsn_found_list = []
    bsn_findings = re.findall("([0-9]{9})", txt)

    bsn_lambda = (
        lambda i: 7
        < len(i)
        < 10
        * (
            (S := sum(a * b for a, b in zip([-1, *range(2, 10)], map(int, i[::-1]))))
            % 11
            < 1
        )
        * S
        > 0
    )

    for possible_bsn in bsn_findings:
        if bsn_lambda(possible_bsn):
            bsn_found_list.append(possible_bsn)

    return bsn_found_list


def _valid_iban(iban: str) -> bool:
    """
    It takes an iban number in string form and checks wether it is a valid iban
        Args:
            txt (str): an input string from which we want to extract iban numbers from

        Returns:
            A list of valid found iban numbers
    """
    assert isinstance(iban, str), "iban should be a str"
    if len(iban) < 18 or not iban.isalnum():
        return False
    else:
        iban = (iban[4:] + iban[:4]).translate(LETTERS)
        return int(iban) % 97 == 1


def _extract_iban(txt: str) -> list[str]:
    """
    It takes a string and extracts all valid iban numbers from it
        Args:
            txt (str): an input string from which we want to extract iban numbers from

        Returns:
            A list of valid found iban numbers
    """
    assert isinstance(txt, str), "txt should be a str"
    iban_found_list = []
    iban_findings = re.findall(
        "([a-zA-Z]{2}[0-9]{2}[a-zA-Z0-9]{4}[0-9]{7}([a-zA-Z0-9]?){0,16})", txt
    )
    iban_findings = list(set([item for t in iban_findings for item in t]))

    for possible_iban in iban_findings:
        if _valid_iban(possible_iban):
            iban_found_list.append(possible_iban)

    return iban_found_list


def _extract_email(txt: str) -> list[str]:
    """
    It takes a string and extracts all possible email addresses from it
        Args:
            txt (str): an input string from which we want to extract email addresses from

        Returns:
            A list of possible found email addresses
    """
    assert isinstance(txt, str), "txt should be a str"
    email_findings = re.findall(r"([\w\.-]+@[\w\.-]+\.\w+)", txt)
    return email_findings


def _extract_phonenumbers(txt: str) -> list[str]:
    """
    It takes a string and extracts all valid phone numbers from it
        Args:
            txt (str): an input string from which we want to extract phone numbers from

        Returns:
            A list of valid found phone numbers
    """
    assert isinstance(txt, str), "txt should be a str"
    phonenumbers_found_list = []

    # remove all characters that are not + or 0-9 characters
    txt = re.sub("[^0-9+]", "", txt)

    # extract all possible phonenumbers beginning with a country code like +31
    country_codes_found = re.findall(r"([\+][0-9]{10,14})", txt)

    # loop through all found country codes check for possible combinations if it is a valid number
    for nr in country_codes_found:
        possible_number = nr
        while len(possible_number) > 10:
            try:
                if phonenumbers.is_possible_number(phonenumbers.parse(possible_number)):
                    info = (
                        possible_number,
                        timezone.time_zones_for_number(
                            phonenumbers.parse(possible_number)
                        )[0],
                    )
                    phonenumbers_found_list.append(info)
                possible_number = possible_number[:-1]
            except:
                possible_number = possible_number[:-1]
                continue

    # extract all 06-x formatted mobile numbers
    mobile_found = re.findall("([0][6][0-9]{8})", txt)

    # check for all 06-x numbers if it is a valid number assuming the country code is +31
    for nr in mobile_found:
        possible_number = "+31" + nr[1:]
        if phonenumbers.is_possible_number(phonenumbers.parse(possible_number)):
            info = (
                nr,
                timezone.time_zones_for_number(phonenumbers.parse(possible_number))[0],
            )
            if ("+31" + info[0], info[1]) not in phonenumbers_found_list:
                phonenumbers_found_list.append(info)

    # remove our found phone numbers from which the region is unknown hence likely unvalid
    phonenumbers_found_list = [
        x for x in phonenumbers_found_list if x[1] != "Etc/Unknown"
    ]

    return phonenumbers_found_list


def _extract_zip(txt: str) -> list[str]:
    """
    It takes a string and extracts all valid dutch zipcodes from it
        Args:
            txt (str): an input string from which we want to extract zipcodes from

        Returns:
            A list of valid found zipcodes
    """
    assert isinstance(txt, str), "txt should be a str"

    # extract all zip codes using regex
    zip_found = re.findall(
        "([1-9][0-9][0-9][0-9][A-EGHJ-NPR-TVWXZ][A-EGHJ-NPR-TVWXZ])", txt
    )
    return zip_found


def _check_cv(txt: str) -> bool:
    """
    It takes a string and checks if there are CV keywords in it
        Args:
            txt (str): an input string from which we want to check if it contains CV keywords

        Returns:
            A boolean flag that indicate if the sting contains CV keywords
    """
    assert isinstance(txt, str), "txt should be a str"

    found_cv_words = []
    for keyword in CV_KEYWORDS:
        found_cv_words += re.findall("(" + keyword + ")", txt.lower())
    if len(found_cv_words) > 0:
        return True
    else:
        return False


def _check_credentials(txt: str) -> bool:
    """
    It takes a string and checks if there are credentials keywords in it
        Args:
            txt (str): an input string from which we want to check if it contains credential keywords

        Returns:
            A boolean flag that indicate if the sting contains credential keywords
    """
    assert isinstance(txt, str), "txt should be a str"

    found_credentials = []
    for keyword in CREDENTIALS_KEYWORDS:
        found_credentials += re.findall("(" + keyword + ")", txt.lower())
    if len(found_credentials) > 0:
        return True
    else:
        return False


def _valid_cc_number(card_number: str) -> bool:
    """
    It takes a credit card number in string and checks if the credit card number is valid using luhn's algorithm
        Args:
            card_number (str): an input that represents a credit card number

        Returns:
            A boolean flag that indicate if the sting contains credential keywords
    """
    assert isinstance(card_number, str), "card_number should be a str"

    # 1. Keep only numeric characters in string
    card_number = re.sub("[^0-9]", "", card_number)

    # 2. If not the right length return false
    if len(card_number) != 16:
        return False

    # 3. Change datatype to list[int]
    card_number = [int(num) for num in card_number]

    # 4. Remove the last digit:
    checkDigit = card_number.pop(-1)

    # 5. Reverse the remaining digits:
    card_number.reverse()

    # 6. Double digits at even indices
    card_number = [
        num * 2 if idx % 2 == 0 else num for idx, num in enumerate(card_number)
    ]

    # 7. Subtract 9 at even indices if digit is over 9
    # (or you can add the digits)
    card_number = [
        num - 9 if idx % 2 == 0 and num > 9 else num
        for idx, num in enumerate(card_number)
    ]

    # 8. Add the checkDigit back to the list:
    card_number.append(checkDigit)

    # 9. Sum all digits:
    checkSum = sum(card_number)

    # 10. If checkSum is divisible by 10, it is valid.
    return checkSum % 10 == 0


def _extract_cc_number(txt: str) -> list[str]:
    """
    It takes a string and checks if there are creditcard number available
        Args:
            txt (str): an input string from which we want to check if it contains a creditcard number

        Returns:
            A boolean flag that indicate if the sting contains a creditcard number
    """
    assert isinstance(txt, str), "txt should be a str"

    pattern = r"(?:\d{4}[ -]?){4}(?=[^\w]|$)"

    found_cc_number = re.findall(pattern, txt)
    found_cc_number = [x for x in found_cc_number if _valid_cc_number(x)]

    return found_cc_number


def _extract_passport(txt: str) -> list[str]:
    """
    It takes a string and extracts possible NL password numbers from the input. An NL passport number has the following layout
    pos 1 and 2: letters; pos 3-8: letters or digits; pos 9: digit. The letter 'O' is not used while the digit zero may be used.
        Args:
            txt (str): an input string from which we want to extract NL passport numbers

        Returns:
            A list of valid found passport numbers
    """
    assert isinstance(txt, str), "txt should be a str"

    passport_number = re.findall("[A-Z]{2}[A-Z0-9]{6}[0-9]{1}(?=[^A-Z0-9]|$)", txt)

    return passport_number


def search_text_file(text_file: str) -> dict:
    """
    It takes a string/text file to checks and validate the following privacy types:
    bsn, iban, email, tel, zip, cv and credentials
        Args:
            txt (str): an input string from which we want to extract privacy types

        Returns:
            A dictionary with lists of entities that are privacy types
    """
    assert isinstance(text_file, str), "text_file should be a str"

    output_dict = {}
    for type in PRIVACY_TYPES:
        output_dict[type] = []

    # extract iban from text
    iban_numbers = _extract_iban(text_file)
    output_dict["iban"] += iban_numbers
    text_file = _remove_entities(text_file, iban_numbers)

    # extract bsn numbers from text
    bsn_numbers = _extract_ssn(text_file)
    output_dict["bsn"] += bsn_numbers
    text_file = _remove_entities(text_file, bsn_numbers)

    # extract email from text
    emails = _extract_email(text_file)
    output_dict["email"] += emails
    text_file = _remove_entities(text_file, emails)

    # extract phone numbers
    phonenumbers = _extract_phonenumbers(text_file)
    output_dict["telnr"] += phonenumbers

    # extract zipcodes
    zipcodes = _extract_zip(text_file)
    output_dict["zip"] += zipcodes

    # check credentials and cv flags
    output_dict["credentials"] = _check_credentials(text_file)
    output_dict["cv"] = _check_cv(text_file)

    # check creditcard number
    creditcard_numbers = _extract_cc_number(text_file)
    output_dict["creditcard"] += creditcard_numbers

    # check for passport numbers
    passport_numbers = _extract_passport(text_file)
    output_dict["passport"] += passport_numbers

    return output_dict


def _load_spacy_model(model_name: str):
    try:
        ner = spacy.load(
            model_name,
            exclude=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"],
        )
    except OSError:
        spacy.cli.download(model=model_name)
        package_path = spacy.util.get_package_path(model_name)
        spacy.cli.link(model_name, model_name, force=True, package_path=package_path)
        ner = spacy.load(
            model_name,
            exclude=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"],
        )
    return ner


def _detect_language(input: str) -> str:
    try:
        lang = detect(input)
    except LangDetectException:
        lang = "unknown"
    return lang


def extract_NER(input: str, NER_select: list[str] = ["PERSON"]):
    """
    It takes a string as input and returns a list of choosen Named Entities as output

    Args:
        input (str): an input string / document from which you want to extract entities
        NER_select (list[str], optional): a list of possible entities to extract, defaults to ['PERSON'].

        PERSON:      People, including fictional.
        NORP:        Nationalities or religious or political groups.
        FAC:         Buildings, airports, highways, bridges, etc.
        ORG:         Companies, agencies, institutions, etc.
        GPE:         Countries, cities, states.
        LOC:         Non-GPE locations, mountain ranges, bodies of water.
        PRODUCT:     Objects, vehicles, foods, etc. (Not services.)
        EVENT:       Named hurricanes, battles, wars, sports events, etc.
        WORK_OF_ART: Titles of books, songs, etc.
        LAW:         Named documents made into laws.
        LANGUAGE:    Any named language.
        DATE:        Absolute or relative dates or periods.
        TIME:        Times smaller than a day.
        PERCENT:     Percentage, including ”%“.
        MONEY:       Monetary values, including unit.
        QUANTITY:    Measurements, as of weight or distance.
        ORDINAL:     “first”, “second”, etc.
        CARDINAL:    Numerals that do not fall under another type.

    Requirements:
        This function requires a Dutch Spacy model the be available
        Get it using: python -m spacy download nl_core_news_sm, en_core_web_sm, xx_ent_wiki_sm

    Returns:
        A list of strings with entities and entity types
    """
    # input test before we go
    assert isinstance(input, str), "Input should be a string"

    # Make sure we use the right lang-model
    lang = _detect_language(input)

    if lang == "nl":
        ner = _load_spacy_model("nl_core_news_sm")
    elif lang == "en":
        ner = _load_spacy_model("en_core_web_sm")
    else:  # multi-language fall-back
        ner = _load_spacy_model("xx_ent_wiki_sm")
    # use the Spacy lib to tokenize and parse the input text
    doc = ner(input)

    # create an empy list to store results
    entities = []

    # extract entity names and labels and add the entities to the dictionary
    for ent in (ent for ent in doc.ents if ent.label_ in NER_select):
        entity_text = ent.text
        entity_label = ent.label_
        entities.append([entity_text, entity_label])

    # return entities
    return entities
