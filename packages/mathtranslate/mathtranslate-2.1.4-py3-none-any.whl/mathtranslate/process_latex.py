import re
import regex
from .config import math_code, test_environment

match_code = r"(" + math_code + r"_\d+(?:_\d+)*)"
match_code_replace = math_code + r"_(\d+(?:_\d+)*)*"

pattern_env = r"\\begin\{(.*?)\}(\[[a-zA-Z\s,]*?\])?(.*?)\\end\{\1\}"  # \begin{xxx} \end{xxx}, group 1: name, group 2: option, group 3: content
pattern_command_full = r"\\([a-zA-Z]+\*?)(\[[a-zA-Z\s,]*?\])?(\{((?:[^{}]++|(?3))++)\})"   # \xxx[xxx]{xxx} and \xxx{xxx}, group 1: name, group 2: option, group 4: content
pattern_command_simple = r"\\([a-zA-Z]+)"  # \xxx, group 1: name
pattern_brace = r"\{((?:[^{}]++|(?0))++)\}"  # {xxx}, group 1: content
pattern_theorem = r"\\newtheorem\{(.+?)\}"  # \newtheorem{xxx}, group 1: name
pattern_accent = r"\\([`'\"^~=.])(?:\{([a-zA-Z])\}|([a-zA-Z]))"  # match special characters with accents, group 1: accent, group 2/3: normal character
match_code_accent = rf'{math_code}([A-Z]{{2}})([a-zA-Z])'  # group 1: accent name, group 2: normal character
list_special = ['\\', '%', '&', '#', '$', '{', '}', ' ']  # all special characters in form of \x

special_character_forward = {
    '\\': 'BS',
    '%': 'PC',
    '&': 'AD',
    '#': 'NB',
    '$': 'DL',
    '{': 'LB',
    '}': 'RB',
    '^': 'UT',
    ' ': 'SP',
    '`': 'BQ',
    '~': 'TD',
    "'": 'SQ',
    '"': 'DQ',
    '=': 'EQ',
    '.': 'DT',
    '*': 'ST',
    '@': 'AT',
}
special_character_backward = {special_character_forward[key]: key for key in special_character_forward}
assert len(set(special_character_forward.values())) == len(special_character_forward)


def variable_code(count):
    # If count is 123, the code is {math_code}_1_2_3
    digits = list(str(count))
    count_str = "_".join(digits)
    return f'{math_code}_{count_str}'


def modify_text(text, modify_func):
    # modify text without touching the variable codes
    split_text = [s for s in re.split(match_code, text) if s is not None]
    for i in range(len(split_text)):
        if not re.match(match_code, split_text[i]):
            split_text[i] = modify_func(split_text[i])
    text = "".join(split_text)
    return text


def modify_before(text):
    # mathpix is stupid so sometimes does not add $ $ for \pm
    text = text.replace('\\pm', '$\\pm$')
    # the "." may be treated as end of sentence
    text = text.replace('Eq.', 'equation')
    return text


def modify_after(text):
    # the "_" in the text should be replaced to "\_"
    pattern = r"(?<!\\)_"
    text = re.sub(pattern, r"\\_", text)
    return text


def replace_latex_objects(text):
    r"""
    Replaces all LaTeX objects in a given text with the format "{math_code}_{digit1}_{digit2}_..._{digit_last}",
    applies a given function to the resulting text (excluding the "{math_code}_{digit1}_{digit2}_..._{digit_last}" parts),
    and returns both the processed text and a list of replaced LaTeX objects.
    Supported LaTeX objects: \[ xxx \], \begin{xxx} \end{xxx}, $$ $$,
    $ $, \( xxx \), \xxx[xxx]{xxx}, \xxx{xxx}, and \xxx.
    Returns the processed text and a list of replaced LaTeX objects.
    """

    # define regular expressions for each LaTeX object
    latex_obj_regex = [
        r"\$\$(.*?)\$\$",  # $$ $$
        r"\$(.*?)\$",  # $ $
        r"\\\[(.*?)\\\]",  # \[ xxx \]
        r"\\\((.*?)\\\)",  # \( xxx \)
        pattern_env,  # \begin{xxx} \end{xxx}
        pattern_command_full,  # \xxx[xxx]{xxx}
        pattern_command_simple,  # \xxx
        pattern_brace,  # {xxx}
    ]

    # iterate through each LaTeX object and replace with "{math_code}_{digit1}_{digit2}_..._{digit_last}"
    count = 0
    replaced_objs = []
    for regex_symbol in latex_obj_regex:
        pattern = regex.compile(regex_symbol, regex.DOTALL)
        while pattern.search(text):
            latex_obj = pattern.search(text).group()
            replaced_objs.append(f'{latex_obj}')
            text = pattern.sub(' ' + variable_code(count) + ' ', text, 1)
            count += 1

    text = modify_text(text, modify_before)
    return text, replaced_objs


def recover_latex_objects(text, replaced_objs, final=False):
    nobjs = len(replaced_objs)
    matched_indices = []

    def get_obj(digit_str):
        index = int(''.join(digit_str.split('_')))
        matched_indices.append(index)
        if index < nobjs:
            return replaced_objs[index]
        else:
            if test_environment:
                assert final
            return '???'

    text = modify_text(text, modify_after)
    pattern = re.compile(match_code_replace)
    total_num = 0
    while True:
        text, num_modify = pattern.subn(lambda match: get_obj(match.group(1)), text)
        total_num += num_modify
        if num_modify == 0:
            break
    n_good = len(set(matched_indices).intersection(set(range(nobjs))))
    n_bad1 = len(matched_indices) - n_good
    n_bad2 = nobjs - n_good
    n_bad = max(n_bad1, n_bad2)
    if final and n_bad > 0:
        print(n_bad, 'latex objects are probably wrong in total', nobjs)
    return text


def remove_tex_comments(text):
    """
    Removes all TeX comments in a given string with the format "% comment text".
    Does not match "\%".
    If "%" is at the beginning of a line then delete this line.
    Returns the processed string.
    """
    text = re.sub(r"\n\s*(?<!\\)%.*?(?=\n)", "", text)
    text = re.sub(r"(?<!\\)%.*?(?=\n)", "", text)

    return text


def split_latex_document(text, begin_code, end_code):
    """
    Splits a document into three parts: the preamble, the body, and the postamble.
    Returns a tuple of the three parts.
    """
    begin_doc_index = text.find(begin_code)
    end_doc_index = text.rfind(end_code)
    if begin_doc_index == -1 or end_doc_index == -1 or end_doc_index <= begin_doc_index:
        assert False, "latex is not complete"
    pre = text[:begin_doc_index + len(begin_code)]
    body = text[begin_doc_index + len(begin_code):end_doc_index]
    post = text[end_doc_index:]
    return body, pre, post


def process_specific_env(latex, function, env_names):
    pattern = regex.compile(pattern_env, regex.DOTALL)

    def process_function(match):
        # \begin{env_name} content \end{env_name}
        env_name = match.group(1)
        options = match.group(2)
        if options is None:
            options = ''
        content = match.group(3)
        if env_name in env_names:
            processed_content = function(content)
            return rf'\begin{{{env_name}}}{options}{processed_content}\end{{{env_name}}}'
        else:
            return match.group(0)
    return pattern.sub(process_function, latex)


def process_specific_commands(latex, function, command_names):
    pattern = regex.compile(pattern_command_full, regex.DOTALL)

    def process_function(match):
        # \{command_name}[options]{content}
        command_name = match.group(1)
        options = match.group(2)
        if options is None:
            options = ''
        content = match.group(4)
        if command_name in command_names:
            processed_content = function(content)
            return rf'\{command_name}{options}{{{processed_content}}}'
        else:
            return match.group(0)
    return pattern.sub(process_function, latex)


def remove_blank_lines(text):
    pattern = re.compile(r'\n\n+')
    text = pattern.sub('\n', text)
    return text


def insert_package(text, package):
    pattern = re.compile(r"\\documentclass(\[.*?\])?\{(.*?)\}", re.DOTALL)
    match = pattern.search(text)
    if match:
        start, end = match.span()
        new_text = text[:end] + f"\n\\usepackage{{{package}}}\n" + text[end:]
        return new_text
    else:
        return text


def is_complete(latex_code):
    # Define regular expressions for \documentclass, \begin{document}, and \end{document}
    documentclass_pattern = re.compile(r"\\documentclass(\[.*?\])?\{.*?\}", re.DOTALL)
    begin_pattern = re.compile(r"\\begin\{document\}")
    end_pattern = re.compile(r"\\end\{document\}")

    # Check if \documentclass is present
    if not documentclass_pattern.search(latex_code):
        return False

    # Check if \begin{document} is present
    begin_match = begin_pattern.search(latex_code)
    if not begin_match:
        return False
    begin_index = begin_match.start()

    # Check if \end{document} is present
    end_match = end_pattern.search(latex_code)
    if not end_match:
        return False
    end_index = end_match.end()

    # Check if the order is correct
    if begin_index < documentclass_pattern.search(latex_code).end() or end_index < begin_index:
        return False

    return True


def get_theorems(text):
    pattern = re.compile(pattern_theorem, re.DOTALL)
    matches = re.finditer(pattern, text)
    theorems = [match.group(1) for match in matches]
    return theorems


def replace_special(text):
    for special in list_special:
        # add space around
        text = text.replace(f'\\{special}', f' {math_code}{special_character_forward[special]} ')

    return text


def recover_special(text):
    for special in list_special:
        text = text.replace(math_code + special_character_forward[special], f'\\{special}')

    return text


def replace_accent(text):
    def replace_function(match):
        special = match.group(1)
        char1 = match.group(2)
        char2 = match.group(3)
        if char1 is None:
            assert char2 is not None
            char = char2
        else:
            assert char2 is None
            char = char1
        # do not add space around
        return math_code + special_character_forward[special] + f'{char}'

    text = re.compile(pattern_accent).sub(replace_function, text)

    return text


def recover_accent(text):
    def replace_function(match):
        special = special_character_backward[match.group(1)]
        char = match.group(2)
        return rf'\{special}{{{char}}}'

    text = re.compile(match_code_accent).sub(replace_function, text)

    return text
