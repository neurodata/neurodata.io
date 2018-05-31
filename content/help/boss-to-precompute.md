---
$title@: BOSS to precomputed neuroglancer format
options: 
    - name: steps
      link: steps
    - name: prerequisites
      link: prerequisites
    - name: download
      link: download-data-from-boss-using-ndpull
    - name: create
      link: create-compressed-segmentations
    - name: host
      link: host-the-directory-somewhere
    - name: view
      link: view-the-output
---


### Guide to generate precomputed compressed segmentations and meshes from a volume on BOSS

### Steps

1. Download data from BOSS using `ndpull`
1. Generate the precomputed compressed segmentation files using `neuroglancer-scripts` (dev version)
1. Generate meshes using `neuroglancer python`
1. Host them somewhere and point neuroglancer at the directory

### Prerequisites

Install the following software:

1. [python3](https://www.python.org/)
1. [node](https://nodejs.org/)
1. [ndpull](https://github.com/neurodata/ndpull)
1. [neuroglancer-scripts](https://github.com/HumanBrainProject/neuroglancer-scripts)
1. [neuroglancer](https://github.com/google/neuroglancer)

### Download data from BOSS using ndpull

1. create a project directory
1. create subdirectory for TIFF files
1. use ndpull to download the files

```sh
mkdir zbrain-project; cd zbrain-project

mkdir data

ndpull --config_file neurodata.cfg --collection ZBrain --experiment Zbrain --channel Masks --res 0 --full_extent --outdir data
```

### Create compressed segmentations

1. Create basic `info` file:
```json
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
```

1. Create additional scales (chunk size 256)

    `mkdir output; generate-scales-info info output --target-chunk-size 256`

1. Create res 0 precomputed data:

    `slices-to-precomputed data/ output/ --flat`

1. Create the downsampled data:

    `compute-scales --flat --downscaling-method majority output/`

### Create the meshes using neuroglancer

1. create mesh directory
    `mkdir mesh`
1. change directory to `neuroglancer/python`
1. install: 

```sh
pip install tornado==4.5.3 numpy
python setup.py develop
```

1. run the following script:
<script src="https://gist.github.com/falkben/1fa46f4acac75a5bd5fc1d91bb7e1aef.js"></script>

### Host the directory somewhere

1. nginx
    1. Copy the `output` directory to a server to host
    1. Enable CORS: [nginx config](https://enable-cors.org/server_nginx.html)
    1. Enable sending compressed files in place of uncompressed files. [nginx config](https://docs.nginx.com/nginx/admin-guide/web-server/compression/#sending-compressed-files)
1. S3
    1. Strip the .gz extension from each file
    1. Add CORS support to the bucket (in bucket properties)
    1. Give the bucket read permissions using bucket policy
    1. Upload the directory to to the bucket
    1. Add metadata to all objects that are gzipped (e.g. the segments but not the meshes) to have `Content-Encoding` be `gzip` (can do this in bulk on AWS Console)

### View the output

The final URL to construct should be a neuroglancer URL with precomputed as the source.  Use the ids printed at the end of the mesh creation for the `segments` field:

[`https://viz.boss.neurodata.io/#!{'layers':{'zbrain':{'type':'segmentation'_'source':'precomputed://https://synaptomes2.neurodata.io/data/zbrain'_'segments':['1'_'10'_'100'_'101'_'102'_'103'_'104'_'105'_'106'_'107'_'108'_'109'_'11'_'110'_'111'_'112'_'113'_'114'_'115'_'116'_'117'_'118'_'119'_'12'_'120'_'121'_'122'_'123'_'124'_'125'_'126'_'127'_'128'_'129'_'13'_'130'_'131'_'132'_'133'_'134'_'135'_'136'_'137'_'138'_'139'_'14'_'140'_'141'_'142'_'143'_'144'_'145'_'146'_'147'_'148'_'149'_'15'_'150'_'151'_'152'_'153'_'154'_'155'_'156'_'157'_'158'_'159'_'16'_'160'_'161'_'162'_'163'_'164'_'165'_'166'_'167'_'168'_'169'_'17'_'170'_'171'_'172'_'173'_'174'_'175'_'176'_'177'_'178'_'179'_'18'_'180'_'181'_'182'_'183'_'184'_'185'_'186'_'187'_'188'_'189'_'19'_'190'_'191'_'192'_'193'_'194'_'195'_'196'_'197'_'198'_'199'_'2'_'20'_'200'_'201'_'202'_'203'_'204'_'205'_'206'_'207'_'208'_'209'_'21'_'210'_'211'_'212'_'213'_'214'_'215'_'216'_'217'_'218'_'219'_'22'_'220'_'221'_'222'_'223'_'224'_'225'_'226'_'227'_'228'_'229'_'23'_'230'_'231'_'232'_'233'_'234'_'235'_'236'_'237'_'238'_'239'_'24'_'240'_'241'_'242'_'243'_'244'_'245'_'246'_'247'_'248'_'249'_'25'_'250'_'251'_'252'_'253'_'254'_'255'_'256'_'257'_'258'_'259'_'26'_'260'_'261'_'262'_'263'_'264'_'265'_'266'_'267'_'268'_'269'_'27'_'270'_'271'_'272'_'273'_'274'_'275'_'276'_'277'_'278'_'279'_'28'_'280'_'281'_'282'_'283'_'284'_'285'_'286'_'287'_'288'_'289'_'29'_'290'_'291'_'292'_'293'_'294'_'3'_'30'_'31'_'32'_'33'_'34'_'35'_'36'_'37'_'38'_'39'_'4'_'40'_'41'_'42'_'43'_'44'_'45'_'46'_'47'_'48'_'49'_'5'_'50'_'51'_'52'_'53'_'54'_'55'_'56'_'57'_'58'_'59'_'6'_'60'_'61'_'62'_'63'_'64'_'65'_'66'_'67'_'68'_'69'_'7'_'70'_'71'_'72'_'73'_'74'_'75'_'76'_'77'_'78'_'79'_'8'_'80'_'81'_'82'_'83'_'84'_'85'_'86'_'87'_'88'_'89'_'9'_'90'_'91'_'92'_'93'_'94'_'95'_'96'_'97'_'98'_'99']}}_'navigation':{'pose':{'position':{'voxelSize':[798_798_2000]_'voxelCoordinates':[660_312_83]}}_'zoomFactor':1689}_'perspectiveOrientation':[0.6550021171569824_0.13391916453838348_0.1957596242427826_0.7174371480941772]_'perspectiveZoom':17154_'showSlices':false_'layout':'4panel'}`](https://viz.boss.neurodata.io/#!{'layers':{'zbrain':{'type':'segmentation'_'source':'precomputed://https://synaptomes2.neurodata.io/data/zbrain'_'segments':['1'_'10'_'100'_'101'_'102'_'103'_'104'_'105'_'106'_'107'_'108'_'109'_'11'_'110'_'111'_'112'_'113'_'114'_'115'_'116'_'117'_'118'_'119'_'12'_'120'_'121'_'122'_'123'_'124'_'125'_'126'_'127'_'128'_'129'_'13'_'130'_'131'_'132'_'133'_'134'_'135'_'136'_'137'_'138'_'139'_'14'_'140'_'141'_'142'_'143'_'144'_'145'_'146'_'147'_'148'_'149'_'15'_'150'_'151'_'152'_'153'_'154'_'155'_'156'_'157'_'158'_'159'_'16'_'160'_'161'_'162'_'163'_'164'_'165'_'166'_'167'_'168'_'169'_'17'_'170'_'171'_'172'_'173'_'174'_'175'_'176'_'177'_'178'_'179'_'18'_'180'_'181'_'182'_'183'_'184'_'185'_'186'_'187'_'188'_'189'_'19'_'190'_'191'_'192'_'193'_'194'_'195'_'196'_'197'_'198'_'199'_'2'_'20'_'200'_'201'_'202'_'203'_'204'_'205'_'206'_'207'_'208'_'209'_'21'_'210'_'211'_'212'_'213'_'214'_'215'_'216'_'217'_'218'_'219'_'22'_'220'_'221'_'222'_'223'_'224'_'225'_'226'_'227'_'228'_'229'_'23'_'230'_'231'_'232'_'233'_'234'_'235'_'236'_'237'_'238'_'239'_'24'_'240'_'241'_'242'_'243'_'244'_'245'_'246'_'247'_'248'_'249'_'25'_'250'_'251'_'252'_'253'_'254'_'255'_'256'_'257'_'258'_'259'_'26'_'260'_'261'_'262'_'263'_'264'_'265'_'266'_'267'_'268'_'269'_'27'_'270'_'271'_'272'_'273'_'274'_'275'_'276'_'277'_'278'_'279'_'28'_'280'_'281'_'282'_'283'_'284'_'285'_'286'_'287'_'288'_'289'_'29'_'290'_'291'_'292'_'293'_'294'_'3'_'30'_'31'_'32'_'33'_'34'_'35'_'36'_'37'_'38'_'39'_'4'_'40'_'41'_'42'_'43'_'44'_'45'_'46'_'47'_'48'_'49'_'5'_'50'_'51'_'52'_'53'_'54'_'55'_'56'_'57'_'58'_'59'_'6'_'60'_'61'_'62'_'63'_'64'_'65'_'66'_'67'_'68'_'69'_'7'_'70'_'71'_'72'_'73'_'74'_'75'_'76'_'77'_'78'_'79'_'8'_'80'_'81'_'82'_'83'_'84'_'85'_'86'_'87'_'88'_'89'_'9'_'90'_'91'_'92'_'93'_'94'_'95'_'96'_'97'_'98'_'99']}}_'navigation':{'pose':{'position':{'voxelSize':[798_798_2000]_'voxelCoordinates':[660_312_83]}}_'zoomFactor':1689}_'perspectiveOrientation':[0.6550021171569824_0.13391916453838348_0.1957596242427826_0.7174371480941772]_'perspectiveZoom':17154_'showSlices':false_'layout':'4panel'})
