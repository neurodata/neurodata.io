"""
Used to generate urls for weiler14
"""


import json

import boto3

s3 = boto3.client("s3")


def get_sub_dirs(bucket, prefix):
    res = s3.list_objects(Bucket=bucket, Prefix=prefix, Delimiter="/")
    return [r.get("Prefix") for r in res.get("CommonPrefixes")]


delete_chs = ["synapses", "dev"]

colors = ["white", "green", "red", "blue", "magenta", "yellow", "cyan"]

bucket_name = "open-neurodata"
exps = get_sub_dirs(bucket_name, "weiler14/")
with open(f"urls.txt", "w") as state_file:
    for exp in exps:
        chns = get_sub_dirs(bucket_name, exp)
        layers = []
        ch_count = 0
        for ch in chns:
            ch_parts = ch.split("/")
            precomputed_path = "/".join(ch_parts[0:-1])

            if any(d in ch_parts[-2] for d in delete_chs):
                continue

            layer = {
                "name": ch_parts[-2],
                "source": f"precomputed://https://open-neurodata.s3.amazonaws.com/{precomputed_path}",
                "type": "image",
                "blend": "additive",
                "shaderControls": {"max": 0.1},
            }
            if ch_count >= 7:
                layer["visible"] = False
            else:
                layer["shaderControls"]["color"] = colors[ch_count]

            layers.append(layer)
            ch_count += 1

        exp_state = {
            "layers": layers,
        }

        exp_fname = exp[0:-1].replace("/", "_")
        state_str = json.dumps(exp_state, separators=(",", ":"))
        url = f"https://viz.neurodata.io/#!{state_str}"
        state_file.write(url + "\n")
