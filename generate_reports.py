from benchmark_qrs_detectors.dataset_helper import dataset_generators, sampling_frequency
from benchmark_qrs_detectors.algo_helper import algorithms_list, run_algo 
from benchmark_qrs_detectors.get_annotations import dataset_annot_generators
import json
import time

#
# generate_reports
#

for dataset_name in dataset_generators.keys():
    real_peaks = dict()
    for ann in dataset_annot_generators[dataset_name]:
        sample_key, peaks = ann
        real_peaks[sample_key] = len(peaks)
    counter = 0
    fs = sampling_frequency[dataset_name]
    rows = []
    for record in dataset_generators[dataset_name]:    
        counter+=1
        for algo in algorithms_list:
            sample_key, channels = record
            # get only one channel from sample
            channel_key = sorted(channels.keys())[0]
            sig = channels[channel_key]
            start_time = time.time()
            try:
                peaks = run_algo(algo, sig, fs)
            except Exception as e:
                print(e)
                peaks = []
            row = dict(
                algo=algo,
                dataset_name=dataset_name,
                sample_name=str(sample_key),
                fs=fs,
                signal_length=len(sig),
                total_peaks=len(peaks), 
                total_real=real_peaks[sample_key],
                time=time.time() - start_time
            )
            rows.append(row)
            print(counter, row)

    open("./output/" + dataset_name + ".json", "w").write(json.dumps(rows))
        
