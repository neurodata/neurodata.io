import boto3
import botocore
from ruamel.yaml import YAML

yaml = YAML()
CLIENT = boto3.client('s3',  # region_name='us-east-1',
                      config=botocore.client.Config(signature_version=botocore.UNSIGNED))
RESOURCE = boto3.resource('s3')

REF_DIFF = {'SWU4': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/swu_4.html',
            'HNU1': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/hnu_1.html',
            'BNU3': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/bnu_3.html',
            'BNU1': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/bnu_1.html',
            'KKI2009': 'http://mri.kennedykrieger.org/databases.html#Kirby21',
            'NKIENH': 'http://fcon_1000.projects.nitrc.org/indi/enhanced/',
            'NKI1': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/nki_1.html',
            'Templeton255': '#',
            'Templeton114': '#',
            'MRN1313': '#'}

REF_FUNC = {
    'BNU1': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/bnu_1.html',
    'BNU2': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/bnu_2.html',
    'BNU3': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/bnu_3.html',
    'HNU1': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/hnu_1.html',
    'IBATRT': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/ibatrt.html',
    'IPCAS1': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/ipcas_1.html',
    'IPCAS2': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/ipcas_2.html',
    'IPCAS5': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/ipcas_5.html',
    'IPCAS6': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/ipcas_6.html',
    'IPCAS8': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/ipcas_6.html',
    'NYU1': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/nyu_1.html',
    'SWU1': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/swu_1.html',
    'SWU2': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/swu_2.html',
    'SWU3': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/swu_3.html',
    'SWU4': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/swu_4.html',
    'UWM': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/uwm.html',
    'XHCUMS': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/xhcums.html'
}


def scan_bucket(bucket, path):
    # path needs trailing '/': "data/"
    if path[-1] != '/':
        path += '/'

    result = CLIENT.list_objects(Bucket=bucket,
                                 Prefix=path,
                                 Delimiter='/'
                                 )
    listing = []
    for d in result.get('CommonPrefixes'):
        o = d['Prefix'].rsplit(path)[1]
        o = o.strip('/')
        listing.append(o)

    # getting any objects in the path
    my_bucket = RESOURCE.Bucket(bucket)
    objs = list(my_bucket.objects.filter(Prefix=path, Delimiter='/'))
    for obj in objs:
        key_name = obj.key.rsplit(path)[1]
        if key_name != '':  # sometimes the root path returns an object
            listing.append(key_name)

    return listing


def to_url(bucket, things):
    base = 'http://{}.s3-website-us-east-1.amazonaws.com/{}'
    return base.format(bucket, '/'.join(things))


def create_yaml_data(bucket_name, bpath, seqs, refs, pathtype, url_base, output_path):
    dsets = scan_bucket(bucket_name, bpath)

    # remove some stuff that isn't real:
    for seq in seqs:
        dsets.remove(seq) if seq in dsets else dsets

    for dset in dsets:
        data_dict = {}
        data_dict['name'] = dset

        path = bpath + dset
        dirt = scan_bucket(bucket_name, path)

        csv = [d for d in dirt if '.csv' in d]
        if csv:
            data_dict['csv'] = to_url(bucket_name, (url_base, path, csv[0]))

        vers = [d for d in dirt if 'ndmg' in d]
        if vers:
            ver = sorted(vers, reverse=True)[0]
            derpath = path + '/' + ver + pathtype
            derivs = scan_bucket(bucket_name, derpath)

            for d in derivs:
                data_dict[d.replace('-', '_')] = to_url(
                    bucket_name, (url_base, dset,
                                  ver, pathtype.lstrip('/'), d, '')
                )
            qapath = path + '/' + ver
            qaderivs = scan_bucket(bucket_name, qapath)
            for d in qaderivs:
                data_dict[d] = to_url(
                    bucket_name, (url_base, dset, ver, d, ''))

            data_dict['ver'] = ver.replace('-', '.', 2).strip('ndmg_')

        data_dict['link'] = refs[dset]

        # save the dict as yaml file to /content/diffusion
        fname = 'content/{}/{}.yaml'.format(output_path, dset)
        with open(fname, 'w') as f:
            yaml.dump(data_dict, f)


def main():
    bucket_name = 'mrneurodata'

    # functional
    bpath = 'data/fmri/'
    pathtype = '/func'
    url_base = 'fmri'
    create_yaml_data(bucket_name, bpath, [], REF_FUNC,
                     pathtype, url_base, 'mri_functional')

    # scan /data for directories of diffusion data
    bpath = 'data/'
    seqs = ['NKI24', 'resources', 'MRN114', 'Jung2015', 'dwi', 'fmri']
    output_path = 'mri_diffusion'
    create_yaml_data(bucket_name, bpath, seqs, REF_DIFF, '', '', output_path)


if __name__ == "__main__":
    main()
