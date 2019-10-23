# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import io, os
import re
from collections import defaultdict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
import matplotlib
from copy import deepcopy


def draw_bar(df, name):
    matplotlib.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(40, 20))

    legends = df['legend'].drop_duplicates()
    margin_bottom = np.zeros(len(df['head'].drop_duplicates()))
    for num, legend in enumerate(legends):
        values = list(df[df['legend'] == legend].loc[:, 'freq'])
        ax = df[df['legend'] == legend].plot.bar(x='head', y='freq', ax=ax, stacked=True,
                                          bottom=margin_bottom, label=legend)
        margin_bottom += values

    SAVE_PATH = ".." + os.sep + "img" + os.sep + f"{name}.png"
    plt.savefig(SAVE_PATH)


def preprocess_graph(outer_dict, if_tok_outer=True):
    """
    :param outer_dict:
    :param unique: unique toks/construals
    :return: a dataframe
    """
    data = []
    head_lst = []
    legend_lst = []
    freq_lst = []
    for key,val in outer_dict.items():
        if if_tok_outer:
            head_lst += [key] * len(val)
            legend_lst += [f"{k[0]}~{k[1]}" for k in list(val.keys())]
        else:
            head_lst += [f"{key[0]}~{key[1]}"] * len(val)
            legend_lst += [k for k in list(val.keys())]
        freq_lst += list(val.values())
    assert len(head_lst) == len(legend_lst) == len(freq_lst)
    data.append(head_lst)
    data.append(legend_lst)
    data.append(freq_lst)

    rows = zip(data[0], data[1], data[2])
    headers = ['head', 'legend', 'freq']
    df = pd.DataFrame(rows, columns=headers)
    return df


def pure_freq(ss_lst):
    """
    :return: straight frequencies of tok, scene, funciton and construal
    """
    tok_freq = defaultdict(int)
    scene_freq = defaultdict(int)
    function_freq = defaultdict(int)
    construal_freq = defaultdict(int)
    for fields in ss_lst:
        tok = fields[0]
        scene = fields[3]
        function = fields[4]
        tok_freq[tok] += 1
        scene_freq[scene] += 1
        function_freq[function] += 1
        construal_freq[(scene,function)] += 1
    return tok_freq,scene_freq,function_freq,construal_freq


def build_dict(outer_lst, inner_lst):
    """
    :param outer_lst: a list of unique toks/construals
    :param inner_lst: a list of unique toks/construals
    :return: {outer_key: {inner_key1:0, ...}, ...}
    """
    inner_dict = {key:0 for key in inner_lst}
    outer_dict = {key:deepcopy(inner_dict) for key in outer_lst}
    return outer_dict


def nested_freq(ss_lst, outer_dict, if_tok_outer=True):
    """
    :param ss_lst: the (tok, pos, dependency, scene, function) list read from .conllulex
    :param outer_dict: output from the func build_dict, either a tok_dict or a construal_dict
    :param if_tok_outer: whether the outer dict is tok or construal
    :return: an outer dictionary with frequencies
    """
    for fields in ss_lst:
        tok = fields[0]
        constural = (fields[3], fields[4])
        if if_tok_outer:
            outer_dict[tok][constural] += 1
        else:
            outer_dict[constural][tok] += 1
    return outer_dict


def read_conllulex(path):
    """
    :return: A list of tuples ([tok, pos, deprel, scene, function],...)
    """
    data_slim = []
    with io.open(path, encoding="utf8") as f:
        for line in f.readlines():
            if '\t' in line:
                fields = line.split('\t')
                if fields[13] != "_":
                    # tok, pos, dependency, scene, function
                    data_slim.append((fields[1], fields[3], fields[7], fields[13], fields[14]))
    return data_slim

if __name__ == "__main__":
    PATH = ".." + os.sep + "out.conllulex"

    ss_lst = read_conllulex(PATH)
    tok_freq, scene_freq, function_freq, constural_freq = pure_freq(ss_lst)

    # Unique adpositions and construals
    unique_toks = tok_freq.keys()
    unique_scenes = scene_freq.keys()
    unique_functions = function_freq.keys()
    unique_construals = constural_freq.keys()
    print(f"The number of unique adpositions = {len(unique_toks)}")
    print(f"The number of uniquie scenes = {len(unique_scenes)}")
    print(f"The number of uniquie functions = {len(unique_functions)}")
    print(f"The number of uniquie construals = {len(unique_construals)}")

    # build the outer_dict for toks and construals
    outer_tok_dict = build_dict(unique_toks, unique_construals)
    outer_tok_dict = nested_freq(ss_lst, outer_tok_dict, if_tok_outer=True)

    outer_construal_dict = build_dict(unique_construals, unique_toks)
    outer_construal_dict = nested_freq(ss_lst, outer_construal_dict, if_tok_outer=False)

    # generate graph
    df_tok = preprocess_graph(outer_tok_dict, if_tok_outer=True)   # X=tok
    draw_bar(df_tok, name="tok")

    df_construal = preprocess_graph(outer_construal_dict, if_tok_outer=False)   # X=construal
    draw_bar(df_construal, name="construal")
