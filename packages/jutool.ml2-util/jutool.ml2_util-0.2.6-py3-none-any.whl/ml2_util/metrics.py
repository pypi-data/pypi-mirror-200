import time, abc


class MetricsBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def call(self, train_config, logits, labels, result):
        pass


def _generation_confusion_matrix(count, T_value_list, P_value_list):
    confusion_matrix = [[0 for x in range(count)] for _x in range(count)]

    m_len = len(T_value_list)
    for x in range(m_len):
        t_value = int(T_value_list[x])
        p_value = int(P_value_list[x])
        confusion_matrix[t_value][p_value] += 1

    return confusion_matrix


def _binary_calculation(confusion_m):
    TP = confusion_m[1][1]
    TN = confusion_m[0][0]
    FN = confusion_m[1][0]
    FP = confusion_m[0][1]

    accuracy = (TP + TN) / float(TP + TN + FP + FN) if (TP + TN + FP + FN) != 0 else 0
    precision = TP / float(TP + FP) if (TP + FP) != 0 else 0
    recall = TP / float(TP + FN) if (TP + FN) != 0 else 0
    f1_score = (2 * precision * recall) / float(precision + recall) if (precision + recall) != 0 else 0

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score
    }


class binary_classification(MetricsBase):
    def call(self, train_config, logits, labels, result):
        confusion_m = _generation_confusion_matrix(2, labels, result)
        metrics_dict = _binary_calculation(confusion_m)

        for key, v in metrics_dict.items():
            if key not in train_config.metrics_result:
                train_config.metrics_result[key] = []
            train_config.metrics_result[key].append(v)
