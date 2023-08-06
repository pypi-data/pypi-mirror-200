from ml_util.MetricsBase import MetricsBase


class precision_metrics(MetricsBase):

    @property
    def name(self):
        return "precision"

    def call(self, confusion_matrix: []):
        m_len = len(confusion_matrix)

        p_u = [0 for _ in range(m_len)]
        p_d = [0 for _ in range(m_len)]

        for x in range(m_len):
            for y in range(m_len):
                if x == y:
                    p_u[x] += confusion_matrix[x][y]
                p_d[x] += confusion_matrix[x][y]

        p_r = [u / d if d != 0 else 0 for u, d in zip(p_u, p_d)]

        precision = sum(p_r) / m_len

        return precision
