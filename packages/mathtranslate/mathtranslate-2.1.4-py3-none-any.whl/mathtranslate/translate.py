#!/usr/bin/env python
from . import process_latex
from . import process_text
from .config import math_code
from .process_text import char_limit
import time

default_begin = r'''
\documentclass[UTF8]{article}
\usepackage{xeCJK}
\usepackage{amsmath,amssymb}
\begin{document}
'''
default_end = r'''
\end{document}
'''


class TextTranslator:
    def __init__(self, engine, language_to, language_from):
        if engine == 'google':
            import mtranslate as translator
        elif engine == 'tencent':
            from mathtranslate.tencent import Translator
            translator = Translator()
        else:
            assert False, "engine must be google or tencent"
        self.translator = translator
        self.language_to = language_to
        self.language_from = language_from

    def try_translate(self, text):
        return self.translator.translate(text, self.language_to, self.language_from)

    def translate(self, text):
        while True:
            try:
                result = self.try_translate(text)
                break
            except BaseException as e:
                if hasattr(self.translator, "is_error_request_frequency") and self.translator.is_error_request_frequency(e):
                    print("sleep 1 second to wait")
                    time.sleep(1)
                else:
                    raise e
        return result


class LatexTranslator:
    def __init__(self, translator: TextTranslator, debug=False):
        self.translator = translator
        self.debug = debug
        if self.debug:
            self.f_old = open("text_old", "w", encoding='utf-8')
            self.f_new = open("text_new", "w", encoding='utf-8')
            self.f_obj = open("objs", "w", encoding='utf-8')

    def close(self):
        if self.debug:
            self.f_old.close()
            self.f_new.close()
            self.f_obj.close()

    def translate_paragraph_text(self, text):
        '''
        Translators would have a word limit for each translation
        So here we split translation by '\n' if it's going to exceed limit
        '''
        lines = text.split('\n')
        parts = []
        part = ''
        for line in lines:
            if len(line) >= char_limit:
                assert False, "one line is too long"
            if len(part) + len(line) < char_limit - 10:
                part = part + '\n' + line
            else:
                parts.append(part)
                part = line
        parts.append(part)
        parts_translated = []
        for part in parts:
            parts_translated.append(self.translator.translate(part))
        text_translated = '\n'.join(parts_translated)
        return text_translated.replace("\u200b", "")

    def translate_paragraph_latex(self, latex_original_paragraph, num, complete):
        '''
        Translate a latex paragraph, which means that it could contain latex objects
        '''
        text_original_paragraph, objs = process_latex.replace_latex_objects(latex_original_paragraph)
        # Since \n is equivalent to space in latex, we change \n back to space
        # otherwise the translators view them as separate sentences
        text_original_paragraph = text_original_paragraph.replace('\n', '')
        text_original_paragraph = process_text.split_too_long_paragraphs(text_original_paragraph)
        if not complete:
            text_original_paragraph = process_text.split_titles(text_original_paragraph)
        text_translated_paragraph = self.translate_paragraph_text(text_original_paragraph)
        if self.debug:
            print(f'\n\nParagraph {num}\n\n', file=self.f_old)
            print(f'\n\nParagraph {num}\n\n', file=self.f_new)
            print(f'\n\nParagraph {num}\n\n', file=self.f_obj)
            print(text_original_paragraph, file=self.f_old)
            print(text_translated_paragraph, file=self.f_new)
            for i, obj in enumerate(objs):
                print(f'obj {i}', file=self.f_obj)
                print(obj, file=self.f_obj)
        latex_translated_paragraph = process_latex.recover_latex_objects(text_translated_paragraph, objs, final=True)
        return latex_translated_paragraph

    def split_latex_to_paragraphs(self, latex):
        '''
        1. convert latex to text and objects
        2. split text
        3. convert text back to objects
        '''
        text, objs = process_latex.replace_latex_objects(latex)
        paragraphs_text = text.split('\n\n')
        paragraphs_latex = [process_latex.recover_latex_objects(paragraph_text, objs) for paragraph_text in paragraphs_text]
        return paragraphs_latex

    def _translate_latex_objects(self, match_function, latex_original, names, complete):
        '''
        Terminology:
        env: '\\begin{xxx} \\end{xxx}'
        command: '\\command[options]{text}
        object: env or command
        '''
        latex_translated = latex_original

        num = 0

        def translate_function(latex):
            # Translate anything inside an environment or command
            nonlocal num
            result = self.translate_paragraph_latex(latex, num, complete)
            num += 1
            print(num)
            return result

        names = names + [item + '*' for item in names]
        latex_translated = match_function(latex_translated, translate_function, names)
        return latex_translated

    def translate_latex_env(self, latex_original, names, complete):
        return self._translate_latex_objects(process_latex.process_specific_env, latex_original, names, complete)

    def translate_latex_commands(self, latex_original, names, complete):
        return self._translate_latex_objects(process_latex.process_specific_commands, latex_original, names, complete)

    def translate_full_latex(self, latex_original, loadmain=False):
        latex_original = process_latex.remove_tex_comments(latex_original)

        latex_original = process_latex.replace_accent(latex_original)
        latex_original = process_latex.replace_special(latex_original)

        complete = process_latex.is_complete(latex_original)
        theorems = process_latex.get_theorems(latex_original)
        if complete:
            print('It is a full latex document')
            latex_original, tex_begin, tex_end = process_latex.split_latex_document(latex_original, r'\begin{document}', r'\end{document}')
            tex_begin = process_latex.remove_blank_lines(tex_begin)
            # TODO: change xeCJK to be compatible with other compiler & languages
            tex_begin = process_latex.insert_package(tex_begin, 'xeCJK')
        else:
            print('It is not a full latex document')
            latex_original = process_text.connect_paragraphs(latex_original)
            tex_begin = default_begin
            tex_end = default_end

        if loadmain:
            latex_translated = open('text_after_main.txt').read()
        else:
            latex_original_paragraphs = self.split_latex_to_paragraphs(latex_original)
            latex_translated_paragraphs = []

            num = 0
            print('processing main text')
            for latex_original_paragraph in latex_original_paragraphs:
                latex_translated_paragraph = self.translate_paragraph_latex(latex_original_paragraph, num, complete)
                latex_translated_paragraphs.append(latex_translated_paragraph)
                print(num, '/', len(latex_original_paragraphs))
                num += 1

            latex_translated = '\n\n'.join(latex_translated_paragraphs)

            if self.debug:
                print(latex_translated, file=open('text_after_main.txt', 'w'))

        # TODO: add more here
        environment_list = ['abstract', 'acknowledgments', 'itemize', 'enumerate', 'description', 'list', 'proof']
        print('processing latex environments')
        latex_translated = self.translate_latex_env(latex_translated, environment_list + theorems, complete)

        command_list = ['section', 'subsection', 'subsubsection', 'caption', 'subcaption', 'footnote', 'paragraph']
        print('processing latex commands')
        latex_translated = self.translate_latex_commands(latex_translated, command_list, complete)

        latex_translated = tex_begin + '\n' + latex_translated + '\n' + tex_end

        # Title is probably outside the body part
        print('processing title')
        latex_translated = self.translate_latex_commands(latex_translated, ['title'], complete)

        latex_translated = process_latex.recover_special(latex_translated)
        latex_translated = process_latex.recover_accent(latex_translated)

        self.close()
        return latex_translated
