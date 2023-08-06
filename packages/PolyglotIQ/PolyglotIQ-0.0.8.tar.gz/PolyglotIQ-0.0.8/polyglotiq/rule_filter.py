import regex
from .constants import SUPPORTED_LANGS


CHARS_TO_LANGUAGES_MAPPING = {'Ãã': ['pt', 'vi'], 'ĄąĘę': ['lt', 'pl'], 'Żż': ['pl', 'ro'], 'Îî': ['fr', 'ro'], 'Ññ': ['eu', 'es'], 'ŇňŤť': ['cs', 'sk'], 'Ăă': ['ro', 'vi'], 'İıĞğ': ['az', 'tr'], 'ЈјЉљЊњ': ['mk', 'sr'], 'ẸẹỌọ': ['vi'], 'ÐðÞþ': ['is', 'tr'], 'Ûû': ['fr', 'hu'], 'Ōō': [], 'ĀāĒēĪī': ['lv'], 'Şş': ['az', 'ro', 'tr'], 'Ďď': ['cs', 'ro', 'sk'], 'Ćć': ['bs', 'hr', 'pl'], 'Đđ': ['bs', 'hr', 'vi'], 'Іі': ['be', 'kk', 'uk'], 'Ìì': ['it', 'vi'], 'Øø': ['da'], 'Ūū': ['lv', 'lt'], 'Ëë': ['af', 'sq', 'nl', 'fr'], 'ÈèÙù': ['fr', 'it', 'vi'], 'Êê': ['af', 'fr', 'pt', 'vi'], 'Õõ': ['et', 'hu', 'pt', 'vi'], 'Ôô': ['fr', 'pt', 'sk', 'vi'], 'ЁёЫыЭэ': ['be', 'kk', 'mn', 'ru'], 'ЩщЪъ': ['bg', 'kk', 'mn', 'ru'], 'Òò': ['ca', 'it', 'vi'], 'Ææ': ['da', 'is'], 'Åå': ['da', 'sv'], 'Ââ': ['fr', 'pt', 'ro', 'tr', 'vi'], 'Ýý': ['cs', 'is', 'sk', 'tr', 'vi'], 'Ää': ['et', 'fi', 'de', 'sk', 'sv'], 'Àà': ['ca', 'fr', 'it', 'pt', 'vi'], 'Üü': ['az', 'ca', 'et', 'de', 'hu', 'es', 'tr'], 'ČčŠšŽž': ['bs', 'cs', 'hr', 'lv', 'lt', 'sk', 'sl'], 'Çç': ['sq', 'az', 'eu', 'ca', 'fr', 'de', 'pt', 'tr'], 'Öö': ['az', 'et', 'fi', 'de', 'hu', 'is', 'sv', 'tr'], 'Óó': ['ca', 'de', 'hu', 'is', 'ga', 'pl', 'pt', 'sk', 'es', 'vi'], 'ÁáÍíÚú': ['ca', 'cs', 'de', 'is', 'ga', 'hu', 'pt', 'sk', 'es', 'vi'], 'Éé': ['ca', 'cs', 'fr', 'de', 'hu', 'is', 'ga', 'it', 'pt', 'sk', 'es', 'vi']}


CHAR_SET_LANGUAGES = {
    "Latin": ["af", "al", "az", "eu", "be", "nb", "ca", "cs", "da", "nl", "en", "et", "fi",
              "fr", "lg", "eo", "de", "hu", "is", "id", "ga", "it", "kk", "la", "lv", "lt", 
              "mk", "ms", "mi", "pl", "pt", "ro", "sk", "sl", "so", "st", "es", "sw", "sv",
              "tl", "ts", "tn", "tr", "vi", "cy", "xh", "yo", "zu", "kri", "tk", "su", "ceb", 
              "ht", "hr", "sq", "bs", "no", "ku", "jv", "gn", "gd", "lb", "ilo", "ay", "fy", 
              "uz", "gl", "mg"],
    "Arabic": ["fa", "ar", "ur", "ug", "ps", "sd"],
    "Myanmar": ["my"],
    "Georgian": ["ka"],
    "Khmer": ["km"],
    "Kannada": ["kn"],
    "Armenian": ["hy"],
    "Cyrillic": ["bg", "mn", "ru", "sr", "sn", "uk", "ug", "ky"],
    "Han": ["zh-CN", "zh-TW", "ja"],
    "Hiragana": ["ja"],
    "Katakana": ["ja"],
    "Malayalam": ["ml"],
    "Sinhala": ["si"],
    "Thai": ["th"],
    "Lao": ["lo"],
    "Ethiopic": ["am", "ti"],
    "Tamil": ["ta"],
    "Greek": ["el"],
    "Mongolian": ["mn"],
    "Bengali": ["bn"],
    "Gurmukhi": ["pa"],
    "Gujarati": ["gu"],
    "Hangul": ["ko"],
    "Hebrew": ["he"],
    "Telugu": ["te"],
    "Devanagari": ["hi", "mr", "yi", "ne"],
}

class RuleFilter:
    def __init__(self, restrict_to_langs: list[str] =SUPPORTED_LANGS):
        self.ALPHABET_LANGS: dict[str, list[str]] = CHAR_SET_LANGUAGES
        self.CHARS_TO_LANGUAGES_MAPPING: dict[str, list[str]] = CHARS_TO_LANGUAGES_MAPPING
        for chars in self.CHARS_TO_LANGUAGES_MAPPING:
            for i, lang in enumerate(self.CHARS_TO_LANGUAGES_MAPPING[chars]):
                if lang not in restrict_to_langs:
                    self.CHARS_TO_LANGUAGES_MAPPING[chars][i] = None

        self.CHARS_TO_LANGUAGES_MAPPING  = {chars: set([lang for lang in langs if lang is not None]) for chars, langs in self.CHARS_TO_LANGUAGES_MAPPING.items()}

    def _regex_mapping_alphabet_ (self, alphabet_name, text) -> bool:
        match_String = r"[\p{IsREPLACEMENT_LANG}]".replace("REPLACEMENT_LANG", alphabet_name)
        
        if regex.match(match_String, text):
            return True
        return False

    def _regex_mapping_chars_ (self, chars, text) -> bool:
        if regex.match(r"[{}]".format(chars), text):
            return True
        return False

    def _unique_chars_ (self, text) -> set[str]:
        return set([x for x in text])

    def _search_custom_chars_ (self, text: str) -> set[str]:
        eligible_langs = set()
        for chars, langs in self.CHARS_TO_LANGUAGES_MAPPING.items():
            if regex.match(r"[{}]".format(chars), text):
                eligible_langs = eligible_langs.union(langs)
        return eligible_langs
        

    def filter_langs(self, text) -> set[str]:
        eligible_langs = set()
        
        for alphabet_name, alphabet_langs in self.ALPHABET_LANGS.items():
            if self._regex_mapping_alphabet_(alphabet_name, text):
                eligible_langs = eligible_langs.union(alphabet_langs)

        custom_chars_langs = self._search_custom_chars_(text)

        eligible_langs.union(custom_chars_langs)

        return eligible_langs


