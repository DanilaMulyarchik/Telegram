import language_tool_python


def __find_correct_words(wold: str):
    tool = language_tool_python.LanguageTool('ru')
    matches = tool.check(wold)
    for match in matches:
        if match.replacements != []:
            return match.replacements[0:3]
        else:
            return None


def check_for_mistakes(answer: str, correct_word):
    return True if correct_word in __find_correct_words(answer) else False
