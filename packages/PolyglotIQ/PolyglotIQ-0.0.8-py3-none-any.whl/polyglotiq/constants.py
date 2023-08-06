SUPPORTED_LANGS = ['gu', 'eo', 'sq', 'en', 'vi', 'af', 'gd', 'yi', 'ca', 'bn', 'ne', 'tr', 'is', 'hi', 'lv', 'hu', 'tk', 'ro', 'ru', 'pa', 'it', 'jv', 'pl', 'uk', 'fr', 'ts', 'lg', 'mk', 'ilo', 'tl', 'ug', 'st', 'ay', 'az', 'id', 'be', 'th', 'gn', 'sr', 'ht', 'sw', 'ga', 'cy', 'da', 'mn', 'ml', 'lt', 'zh-CN', 'bg', 'ku', 'kk', 'ka', 'sd', 'mg', 'sk', 'si', 'eu', 'kri', 'my', 'fa', 'lb', 'bs', 'lo', 'ceb', 'ta', 'kn', 'su', 'ar', 'hr', 'he', 'nl', 'ja', 'hy', 'ko', 'el', 'fy', 'ms', 'es', 'ps', 'so', 'no', 'ur', 'la', 'et', 'pt', 'de', 'sv', 'zh-TW', 'km', 'fi', 'mr', 'am', 'uz', 'cs', 'gl', 'te', 'ky', 'sl']
import languagecodes


# change languagecodes,ISO3_MAP dict to {val: key} instead of {key: val}

reordered_langcode_map = {v: k for k, v in languagecodes.ISO3_MAP.items()}

class DetectionResult(object):
    def __init__ (self, text: str, language: str) -> None:
        self.text = text
        self._language_code_ = language


    @property
    def language(self) -> str:
        code = self.language_code if not self.language_code in ["zh-CN", "zh-TW"] else "zh"
        code =  languagecodes.iso_639_alpha3(code)
        code = reordered_langcode_map[code] if code in reordered_langcode_map else code
        return code

    @property 
    def language_code(self) -> str:
        return self._language_code_

class DetectionResults():
    def __init__(self) -> None:
        self.results: list[DetectionResult] = []

    @property
    def languages(self) -> list[None or str]:
        return [result.language for result in self.results]

    @property
    def language_codes(self) -> list[str]:
        return [result.language_code for result in self.results]

    @property
    def texts(self) -> list[str]:
        return [result.text for result in self.results]

    def append(self, result: DetectionResult) -> None:
        self.results.append(result)

    def __getitem__(self, index: int) -> DetectionResult:
        return self.results[index]

    def __len__(self) -> int:
        return len(self.results)

    

    
        
    
