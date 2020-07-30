
        """Get the best/last estimate on how long it takes to find a paper.

        Returns
        -------
        dict:
            For each inclusion, key=paper_id, value=avg time.
        """
        

        labels = self.labels

        # inclusions
        one_labels = np.where(labels == 1)[0]
        # store discovery time
        time_results = {label: [] for label in one_labels}

        # for every state file
        for state in self.states.values():
            # order of labeling
            label_order, n = _get_labeled_order(state)
            # ranking of papers at last query
            proba_order = _get_last_proba_order(state)

            # time_mult = ..
            # n = n initial
            if result_format == "percentage":
                time_mult = 100 / (len(labels) - n)

            elif result_format == "fraction":
                time_mult = 1/(len(labels) - n)
            else:
                time_mult = 1

            # for ... i_time, for all papers that are 1 (labels[idx])
            for i_time, idx in enumerate(label_order[n:]):
                # for all 1s
                if labels[idx] == 1:
                    # time results for inclusions idx = time_mult * the moment paper was detected + 1 (why +1?? )
                    time_results[idx].append(time_mult*(i_time+1))

            # for all inclusions that weren't labeled (prior inclusions!! )
            for i_time, idx in enumerate(proba_order):
                if labels[idx] == 1 and idx not in label_order[:n]:
                    time_results[idx].append(
                        time_mult*(i_time + len(label_order)))

        results = {}

        # average over all state_files
        for label, trained_time in time_results.items():
            if len(trained_time) > 0:
                results[label] = np.average(trained_time)

        return results
