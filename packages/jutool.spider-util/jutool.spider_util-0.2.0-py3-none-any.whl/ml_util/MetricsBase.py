import abc


def confusion_dic_2_matrix(confusion_dic: {}):
    key_dict = {}
    index = 0
    for l in confusion_dic.keys():
        for v in confusion_dic[l].keys():
            if v not in key_dict:
                key_dict[v] = index
                index += 1
        if l not in key_dict:
            key_dict[l] = index
            index += 1

    key_count = len(key_dict.keys())
    matrix = [[0 for _ in range(key_count)] for __ in range(key_count)]

    for l in confusion_dic.keys():
        yy = key_dict[l]
        for v in confusion_dic[l].keys():
            xx = key_dict[v]
            matrix[xx][yy] += 1

    return matrix


class MetricsBase(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def call(self, confusion_matrix: []):
        pass
