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

bucket_name = "zbrain"
coll = ""
host = "zbrain.viz.neurodata.io"
atlas = {
    "source": "precomputed://https://zbrain-s3.neurodata.io/atlas_owen",
    "type": "segmentation",
    "objectAlpha": 0.8,
    "segments": [
        "1",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "2",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "3",
        "30",
        "31",
        "32",
        "33",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
    ],
    "skeletonRendering": {"mode2d": "lines_and_points", "mode3d": "lines"},
    "name": "zbrain_atlas",
}
# bucket_name = "open-neurodata"
# coll = "weiler14/"
# host = "viz.neurodata.io"


exps = get_sub_dirs(bucket_name, coll)
with open(f"urls.txt", "w") as state_file:
    # for exp in exps:
    for exp in ["ZBrain/"]:
        chns = get_sub_dirs(bucket_name, exp)
        layers = []
        ch_count = 0
        for ch in chns:
            ch_parts = ch.split("/")

            layer_name = ch_parts[-2]
            layer_name = layer_name.replace("ZBB_", "")

            precomputed_path = "/".join(ch_parts[0:-1])

            if any(d in ch_parts[-2] for d in delete_chs):
                continue

            layer = {
                "name": layer_name,
                "source": f"precomputed://https://{bucket_name}.s3.amazonaws.com/{precomputed_path}",
                "type": "image",
                "blend": "additive",
                "shaderControls": {"max": 0.4},
            }
            if ch_count >= 7:
                layer["visible"] = False
            else:
                layer["shaderControls"]["color"] = colors[ch_count]

            layers.append(layer)
            ch_count += 1

        if atlas:
            layers.append(atlas)

        exp_state = {
            "layers": layers,
        }

        exp_fname = exp[0:-1].replace("/", "_")
        state_str = json.dumps(exp_state, separators=(",", ":"))
        url = f"https://{host}/#!{state_str}"
        state_file.write(url + "\n")
