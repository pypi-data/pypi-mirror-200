import re

from pygments.lexer import RegexLexer, bygroups
from pygments.token import *


class PeriwinkleLexer(RegexLexer):
    name = 'Periwinkle'
    aliases = ['periwinkle']
    filenames = ['*.бр', '.барвінок']
    flags = re.UNICODE

    tokens = {
        'root': [
            (r'\A#!.*', Comment.Hashbang),
            (r'//.*', Comment),
            (r'/\*', Comment.Multiline, 'multilineComment'),
            (r'\b(друк|друкр|зчитати|ітератор|Число|Логічний|Стрічка|Дійсний|Масив|КінецьІтерації)\b', Name.Builtin),
            (r'(\bфункція\b)(\s*)(\b[а-яА-ЯїієґЇІЄҐ_][а-яА-ЯїієґЇІЄҐ0-9_]*\b)(?=\s*\()', bygroups(Keyword.Control, Text.Whitespace, Name.Function)),
            (r',|[.]{3}', Punctuation),
            (r'\b[а-яА-ЯїієґЇІЄҐ_][а-яА-ЯїієґЇІЄҐ0-9_]*\b(?=\()', Name.Function),
            (r'\b(якщо|або якщо|інакше|кінець|поки|завершити|продовжити|повернути|кожній|з)\b', Keyword),
            (r'(\b(не|та|або|більше|менше|більше=|менше=|є)\b)', Keyword.Operator),
            (r'=|\+=|-=|\*=|/=|\\=|%=|\+|-|\*|/|\\|%|==|!=', Operator),
            (r'"', String, 'string'),
            (r'(([0-9]+[.][0-9]*)|([0-9]*[.][0-9]+))', Number.Float),
            (r'(0|([1-9][0-9]*))', Number.Integer),
            (r'\b(істина|хиба|нич)\b', Name.Constant),
            (r'\b[а-яА-ЯїієґЇІЄҐ_][а-яА-ЯїієґЇІЄҐ0-9_]*\b', Name),
        ],
        'string': [
            (r'\\.', String.Escape),
            (r'[^*"]', String),
            (r'"', String, '#pop'),
        ],
        'multilineComment': [
            (r'[^*/]+', Comment.Multiline),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[*/]', Comment.Multiline)
        ]
    }
