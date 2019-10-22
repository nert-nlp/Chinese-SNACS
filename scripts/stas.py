import io, os
import re
from pyecharts.charts import Bar


def draw_bar():
    a = 1


def read_conllulex(path):
    """
    :param path:
    :return: A list of tuples ([tok, pos, deprel, scene, function],...)
    """
    data_slim = []
    with io.open(path, encoding="utf8") as f:
        for line in f.readlines():
            if '\t' in line:
                fields = line.split('\t')
                if fields[13] != "_":
                    data_slim.append((fields[1], fields[3], fields[7], fields[13], fields[14]))
    return data_slim

if __name__ == "__main__":
    PATH = ".." + os.sep + "out.conllulex"

    ss_lst = read_conllulex(PATH)
    a = 1