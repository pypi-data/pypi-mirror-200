from ml_util.MetricsBase import MetricsBase


class accuracy_metrics(MetricsBase):

    @property
    def name(self):
        return "accuracy"

    def call(self, confusion_matrix: []):
        m_len = len(confusion_matrix)
        TPTN = 0
        N = 0
        for x in range(m_len):
            for y in range(m_len):
                if x == y:
                    TPTN += confusion_matrix[x][y]
                N += confusion_matrix[x][y]

        if N == 0:
            return 0.0
        else:
            return TPTN / N
