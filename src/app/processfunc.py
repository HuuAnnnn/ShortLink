import re

# In the case, the custom url is Vietnamese then we remove all of the accent
def remove_accent(s):
    ascii_alternate = {
        r"[àáạảãâầấậẩẫăằắặẳẵ]": "a",
        r"[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]": "A",
        r"[èéẹẻẽêềếệểễ]": "e",
        r"[ÈÉẸẺẼÊỀẾỆỂỄ]": "E",
        r"[òóọỏõôồốộổỗơờớợởỡ]": "o",
        r"[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]": "O",
        r"[ìíịỉĩ]": "i",
        r"[ÌÍỊỈĨ]": "I",
        r"[ùúụủũưừứựửữ]": "u",
        r"[ƯỪỨỰỬỮÙÚỤỦŨ]": "U",
        r"[ỳýỵỷỹ]": "y",
        r"[ỲÝỴỶỸ]": "Y",
        r"[Đ]": "D",
        r"[đ]": "d",
    }

    for accent in ascii_alternate.keys():
        s = re.sub(accent, ascii_alternate[accent], s)
    return s


# convert the users' custom url into format cannot safe to save
def process_custom_url(url: str):
    remove_url_accent = remove_accent(url)
    lower_url = remove_url_accent.replace("  +", " ").replace(" ", "-")
    extract_character = re.findall(r"[0-9A-ZA-z-]", lower_url)

    return "".join(extract_character)
