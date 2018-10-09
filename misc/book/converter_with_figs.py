# -*- coding: utf-8 -*-
"""
Created on Fri Sep  28 20:01:12 2018

@author: aleksandra
"""
import runpy


def convert(file_name):
    '''
    Convert python script to Markdown
    '''
    with open(file_name, 'r', encoding='utf-8') as my_file:
        my_code = my_file.readlines()

    if 'import matplotlib.pyplot as plt\n' in my_code:
        runpy.run_path(file_name)

    text = ''
    code = False
    notprint = True
    if my_code[0].startswith('#!'):
        my_code = my_code[1:]
    for string in my_code:
        notprint = True
        if string.startswith('plt.savefig'):
            fig_name = string[13:-3]
            text = (text + string + '\n ``` \n' +
                    '\n ![{}]({})'.format(fig_name[:-3], fig_name) + '\n')
            code = False
            continue
        if string.startswith('# >>>'):
            text = text + '\n' + string.replace('# >>>', '    #')
            notprint = False
            continue
        if string.startswith('# `') and string.endswith('`\n'):
            if code:
                text = (text + '\n ``` \n'
                             + string.replace('# `', '_').replace('`', '_ \n'))
            else:
                text = text + string.replace('# `', '_').replace('`', '_ \n')
            code = False
            notprint = False
            continue
        if string.startswith('#'):
            if code and notprint:
                while text.endswith('\n'):
                    text = text[:-1]
                text = text + '\n ``` \n'
                code = False
            text = text + string[1:]
            continue
        if string == '\n' or code:
            text = text + string
            continue
        text = text + '\n ```python \n' + string
        code = True
    if code:
        text = text + ' \n ``` \n'
    result_name = file_name[:-2] + 'md'
    with open(result_name, 'w', encoding='utf-8') as md:
        md.write(text)
