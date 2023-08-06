import pickle as pkl
import os
import contur.config.config as cfg

def export(in_path, out_path, include_dominant_pools=False, include_per_pool_cls=False):
    with open(in_path, 'rb') as file:
        if not os.path.isabs(out_path):
            out_path = os.path.join(cfg.output_dir, out_path) 
        pkl.load(file).export(out_path, include_dominant_pools=include_dominant_pools, include_per_pool_cls=include_per_pool_cls)
