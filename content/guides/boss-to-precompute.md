---
$title@: Precomputed neuroglancer format
$category: Storage
$order: 2
---

[TOC]

The precomputed format [specification](https://github.com/google/neuroglancer/tree/master/src/neuroglancer/datasource/precomputed) is a data source format for loading data into [neuroglancer](https://github.com/google/neuroglancer).  This guide demonstrates how to generate precomputed compressed segmentations & meshes from a BOSS segmentation volume.

### Steps

1. Generate the precomputed compressed segmentation files using `neuroglancer-scripts`
1. Generate meshes using `neuroglancer python` and custom script
1. Host them somewhere and point neuroglancer at the directory

### Prerequisites

Install the following software:

1. [python3](https://www.python.org/)
1. Create Python virtual environment
    - `python3 -m venv env/`
    - `. env/bin/activate`
1. [neuroglancer-scripts](https://github.com/HumanBrainProject/neuroglancer-scripts)
    - **install dev version** (pypi version has bugs)
        - `git clone https://github.com/HumanBrainProject/neuroglancer-scripts.git`
        - `cd neuroglancer-scripts`
        - `pip install -e .[dev]`
1. [neuroglancer](https://github.com/google/neuroglancer) (for meshing)
    1. Optional:
        1. [node](https://nodejs.org/) (package for [Ubuntu](https://nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions))
        1. install Java (needed for webpack)
        1. run the install scripts from neuroglancer root directory (`npm i`)
        1. start the web server `npm run dev-server` (this compiles webpack)
    1. navigate to python directory and run (installs neuroglancer package)
        1. `pip install numpy tornado==4.5.3`
        1. `python setup.py develop`
        1. `python setup.py bundle_client`

### Create compressed segmentations

1. Create basic `info` file:

        {
            "encoding": "compressed_segmentation",
            "scales": [
                {
                    "voxel_offset": [0,0,0],
                    "resolution": [798,798,2000],
                    "size": [1406,621,138]
                }
            ],
            "compressed_segmentation_block_size": [8,8,8],
            "data_type": "uint64",
            "mesh": "mesh",
            "type": "segmentation",
            "num_channels": 1
        }

1. Create additional scales (chunk size 128)

    `mkdir output; generate-scales-info info output --target-chunk-size 128`

1. Create res 0 precomputed data:

    `slices-to-precomputed data/ output/ --flat`

1. Create the downsampled data:

    `compute-scales --flat --downscaling-method majority output/`

### Create the meshes using neuroglancer

1. create mesh directory
    `mkdir mesh`
1. change directory to `neuroglancer/python`
1. run the following script: `python mesh.py DATA/ XXX YYY ZZZ`

#### `mesh.py`

```python
from pathlib import Path
import argparse

import numpy as np
import tifffile as tiff

import neuroglancer

parser = argparse.ArgumentParser(description='create meshes')
parser.add_argument('img_path_str', type=str, help='path to images')
parser.add_argument('voxel_size', nargs=3, type=int,
                    help='voxel size (x, y, z)')

args = parser.parse_args()

img_path_str = args.img_path_str
voxel_size = args.voxel_size

json_descriptor = '{{"fragments": ["mesh.{}.{}"]}}'

img_path = Path(img_path_str)

mesh_list = []
for f in sorted(img_path.glob('*.tif')):
    A = tiff.imread(str(f))
    mesh_list.append(A)
mesh = np.dstack(mesh_list)
mesh = np.transpose(mesh, (2, 0, 1))

ids = [int(i) for i in np.unique(mesh[:])]

vol = neuroglancer.LocalVolume(
    data=mesh,
    voxel_size=voxel_size,
)

img_path.parent.joinpath(
    'output', 'mesh').mkdir(exist_ok=True, parents=True)

for ID in ids[1:]:
    print(ID)
    mesh_data = vol.get_object_mesh(ID)
    with open(
            str(img_path.parent / 'output' / 'mesh' / '.'.join(
                ('mesh', str(ID), str(ID)))), 'wb') as meshfile:
        meshfile.write(mesh_data)
    with open(
            str(img_path.parent / 'output' / 'mesh' / ''.join(
                (str(ID), ':0'))), 'w') as ff:
        ff.write(json_descriptor.format(ID, ID))

print('ids to insert into URL:')
ids_string = '[\'' + '\'_\''.join([str(i) for i in ids[1:]]) + '\']'
print(ids_string)

print('done')
```

### Host the directory

#### nginx
1. Copy the `output` directory to a server to host
1. Enable CORS: [nginx config](https://enable-cors.org/server_nginx.html)
1. Enable sending compressed files in place of uncompressed files. [nginx config](https://docs.nginx.com/nginx/admin-guide/web-server/compression/#sending-compressed-files)
#### S3
<span>1.</span> Strip the .gz extension from each file (script below)

```python
# from within the output directory:
# python rename_files.py .
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('path', type=str)
args = parser.parse_args()

p = Path(args.path)
all = set(p.glob('**/*'))
mesh = set(p.glob('mesh*'))
ids_files = all-mesh

for f in ids_files:
    f.rename(f.with_suffix(''))
```

<span>2.</span> Add CORS support to the bucket (in bucket properties) -- should look something like: 

```xml
<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
<CORSRule>
    <AllowedOrigin>*</AllowedOrigin>
    <AllowedMethod>GET</AllowedMethod>
    <MaxAgeSeconds>3000</MaxAgeSeconds>
    <AllowedHeader>Authorization</AllowedHeader>
</CORSRule>
</CORSConfiguration>
```

<span>3.</span> Give the bucket read permissions using bucket policy
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::BUCKETNAME/*"
        }
    ]
}
```
<span>4.</span> Upload the directory to to the bucket

`aws s3 sync . s3://BUCKET_NAME/PROJECT_NAME --profile AWS_PROFILE`

<span>5.</span> Add metadata to all objects that are gzipped (e.g. the segments but not the meshes) to have `Content-Encoding` be `gzip` (can do this in bulk on AWS Console)

### View the output

The final URL to construct should be a neuroglancer URL with precomputed as the source.  Use the ids printed at the end of the mesh creation for the `segments` field.

Here's an examples of the json for one of our publicly available datasets:

```json
{
  "layers": {
    "em_clahe": {
      "source": "boss://https://api.boss.neurodata.io/collman/M247514_Rorb_1_Site3Align2_EM/em_clahe?",
      "type": "image",
      "opacity": 1,
      "blend": "additive"
    },
    "m247514_Site3Annotation_MN_global": {
      "source": "precomputed://https://s3.amazonaws.com/synaptomes-precomputed/M247514_Rorb_1_Site3Align2_EM",
      "type": "segmentation",
      "segments": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "100", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122", "123", "124", "125", "126", "127", "128", "129", "130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "140", "141", "142", "143", "144", "145", "146", "147", "148", "149", "150", "151", "152", "153", "154", "155", "156", "157", "158", "159", "160", "161", "162", "163", "164", "165", "166", "167", "168", "169", "170", "171", "172", "173", "174", "175", "176", "177", "178", "179", "180", "181", "182", "183", "184", "185", "186", "187", "188", "189", "190", "191", "192", "193", "194", "195", "196", "197", "198", "199", "200", "201", "202", "203", "204", "205", "206", "207", "208", "209", "210", "211", "212", "213", "214", "215", "216", "217", "218", "219", "220", "221", "222", "223", "224", "225", "226", "227", "228", "229", "230", "231", "232", "233", "234", "235", "236", "237", "238", "239", "240", "241", "242", "243", "244", "245", "246", "247", "248", "249", "250", "251", "252", "253", "254", "255", "256", "257", "258", "259", "260", "261", "262", "263", "264", "265", "266", "267", "268", "269", "270", "271", "272", "273", "274", "275", "276", "277", "278", "279", "280", "281", "282", "283", "284", "285", "286", "287", "288", "289", "290", "291", "292", "293", "294", "295", "296", "297", "298", "299", "300", "301", "302", "303", "304", "305", "306", "307", "308", "309", "310", "311", "312", "313", "314", "315", "316", "317", "318", "319", "320", "321", "322", "323", "324", "325", "326", "327", "328", "329", "330", "331", "332", "333", "334", "335", "336", "337", "338", "339", "340", "341", "342", "343", "344", "345", "346", "347", "348", "349", "350", "351", "352", "353", "354", "355", "356", "357", "358", "359", "360", "361", "362", "363", "364", "365", "366", "367", "369", "370", "371", "372", "373", "374", "375", "376", "377", "378", "379", "380", "381", "382", "383", "384", "385", "386", "387", "388", "389", "390", "391", "392", "393", "394", "395", "396", "397", "398", "400", "401", "402", "403", "404", "405", "406", "407", "408", "409", "410", "411", "412", "413", "414", "415", "416", "417", "418", "419", "420", "421", "422", "423", "424", "425", "426", "427", "428", "429", "430", "431", "432", "433", "434", "435", "436", "437", "438", "439", "440", "441", "442", "443", "444", "445", "446", "447", "448", "449", "450", "451", "452", "453", "454", "455", "456", "457", "458", "459", "460", "461", "462", "463", "464", "465", "466", "467", "468", "469", "470", "471", "472", "473", "474", "475", "476", "477", "478", "479", "480", "481", "482", "483", "484", "485", "486", "487", "488", "489", "490", "491", "492", "493", "494", "495", "496", "497", "498", "499", "500", "501", "502", "503", "504", "505", "506", "507", "508", "509", "510", "511", "512", "513", "514", "515", "516", "517", "518", "519", "520", "521", "522", "523", "524", "525", "526", "527", "528", "529", "530", "531", "532", "533", "534", "535", "536", "537", "538", "539", "540", "541", "542", "543", "544", "545", "546", "547", "548", "549", "550", "551", "552", "553", "554", "555", "556", "557", "558", "559", "560", "561", "562", "563", "564", "565", "566", "567", "568", "569", "570", "571", "572", "573", "574", "575", "576", "577", "578", "579", "580", "581", "582", "583", "584", "585", "586", "587", "588", "589", "590", "591", "592", "593", "594", "595", "596", "597", "598", "599", "600", "601", "602", "603", "604", "605", "606", "607", "608", "609", "610", "611", "612", "613", "614", "615", "616", "617", "618", "619", "620", "621", "622", "623", "624", "625", "626", "628", "629", "630", "631", "632", "633", "634", "635", "636", "637", "638", "639", "640", "641", "642", "643", "644", "645", "646", "647", "648", "649", "650", "651", "652", "653", "654", "655", "656", "657", "658", "659", "660", "661", "662", "663", "664", "665", "666", "667", "668", "669", "670", "671", "672", "673", "674", "675", "676", "677", "678", "679", "680", "681", "682", "683", "684", "685", "686", "687", "688", "689", "690", "691", "692", "693", "694", "695", "696", "697", "698", "699", "700", "701", "702", "703", "704", "705", "706", "707", "708", "709", "710", "711", "712", "713", "714", "715", "716", "717", "718", "719", "720", "721", "722", "723", "724", "725", "726", "727", "728", "729", "730", "731", "732", "733", "734", "735", "736", "737", "738", "739", "740", "741", "742", "743", "744", "745", "746", "747", "748", "749", "750", "751", "752", "753", "754", "755", "756", "757", "758", "759", "760", "761", "762", "763", "764", "765", "766", "767", "768", "769", "770", "771", "772", "773", "774", "775", "776", "777", "778", "779", "780", "781", "782", "783", "784", "785", "786", "787", "788", "789", "790", "791", "792", "793", "794", "795", "796", "797", "798", "799", "800", "801", "802", "803", "804", "805", "806", "807", "808", "809", "810", "811", "812", "813", "814", "815", "816", "817", "818", "819", "820", "821", "822", "823", "824", "825", "826", "827", "828", "829", "830", "831", "832", "833", "834", "835", "836", "837", "838", "839", "840", "841", "842", "843", "844", "845", "846", "847", "848", "849", "850", "851", "852", "853", "854", "855", "856", "857", "858", "859", "860", "861", "862", "863", "864", "865", "866", "867", "868", "869", "870", "871", "872", "873", "874", "875", "876", "877", "878", "879", "880", "881", "882", "883", "884", "885", "886", "887", "888", "889", "890", "891", "892", "893", "894", "895", "896", "897", "898", "899", "900", "901", "902", "903", "904", "905", "906", "907", "908", "909", "910", "911", "912", "913", "914", "915", "916", "917", "918", "919", "920", "921", "922", "923", "924", "925", "926", "927", "928", "929", "930", "931", "932", "933", "934", "935", "936", "937", "938", "939", "940", "941", "942", "943", "944", "945", "946", "947", "948", "949", "950", "951", "952", "953", "954", "955", "956", "957", "958", "959", "960", "961", "962", "963", "964", "965", "966", "967", "968", "969", "970", "971", "972", "973", "974", "975", "976", "977", "978", "979", "980", "981", "982", "983", "984", "985", "986", "987", "988", "989", "990", "991", "992", "993", "994", "995", "996", "997", "998", "999", "1000", "1001", "1002", "1003", "1004", "1005", "1007", "1008", "1009", "1010", "1011", "1012", "1013", "1014", "1015", "1016", "1017", "1018", "1019", "1020", "1021", "1022", "1023", "1024", "1025", "1026", "1027", "1028", "1029", "1030", "1031", "1032", "1033", "1034", "1035", "1036", "1037", "1038", "1039", "1040", "1041", "1042", "1043", "1044", "1045", "1046"]
    }
  },
  "navigation": {
    "pose": {
      "position": {
        "voxelSize": [
          3,
          3,
          50
        ],
        "voxelCoordinates": [
          7010,
          7361.5,
          24.5
        ]
      }
    },
    "zoomFactor": 3
  },
  "layout": "xy"
}
```