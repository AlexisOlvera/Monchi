class utilities:
    @staticmethod
    def data_to_list_ploty(data : dict):
        labels = []
        values = []
        parents = []
        for aspect, opinions_sent in data.items():
            labels.append(aspect)
            parents.append('')
            values.append(sum(opinions_sent.values()))
            for opinion, count in opinions_sent.items():
                labels.append(opinion)
                parents.append(aspect)
                values.append(count)
        return labels, parents, values