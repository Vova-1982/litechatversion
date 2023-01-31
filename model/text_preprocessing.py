import re

def clear_special_characters(text):

    text = text.lower()
    text = text.replace("&nbsp", ' ')
    text = text.replace("'", '')
    text = text.replace("’", '')
    reg = re.compile('[^a-zA-Zа-яА-ЯіІїЇєЄэЭёЁъґҐ]')
    text = reg.sub(' ', text)
    text = ' '.join(text.split())

    return text