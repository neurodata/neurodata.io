#!/usr/bin/env python

#
# Generate redirects for old URLs.
#
# Use --amazon to generate AmazonS3 redirection rules which can be applied to the bucket.
# See https://docs.aws.amazon.com/AmazonS3/latest/dev/how-to-page-redirect.html for details.
#
# TODO: Create website configuration to work with aws s3api:
#       https://docs.aws.amazon.com/cli/latest/reference/s3api/put-bucket-website.html
#
# For the production site, I used the following:
# % python redirect.py --amazon --domain neurodata.io
#

import argparse

redirects = [
    ['bock11', 'data/bock11/'],
    ['harris15', 'data/kharris15/'],
    ['array-tomography', 'project/synaptomes/'],
    ['kasthuri11', 'data/kasthuri15/'],
    ['bhatla15', 'data/bhatla15/'],
    ['fly-medulla', 'data/takemura13/'],
    ['pristionchus-pacificus', 'data/bumbarger13/'],
    ['hildebrand16', 'data/hildebrand17/'],
    ['data/hildebrand16', 'data/hildebrand17/'],
    ['wanner16', 'data/wanner16/'],
    ['lee16', 'data/lee16/'],
    ['tobin16', 'data/tobin16/'],
    ['graph-services/download', 'project/connectomes/'],
    ['catmaid', 'data/'],
    ['Kasthurietal2014', 'data/kasthuri15/'],
    ['tools/mgc', 'tools/'],
    ['access', 'help/download/'],
    ['help/access', 'help/download/'],
    ['project/projectomes', 'mri-cloud/'],
    ['data', 'ocp/'],
    ['RerF', 'rerf/'],
    ['randomerforest', 'rerf/'],
    ['ndreg', 'reg/'],
    ['workshop', 'about/workshops/'],
    ['ndcloud', 'ocp/']
]


def main():
    parser = argparse.ArgumentParser()
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--amazon", help="Generate XML syntax for S3 web hosting", action="store_true")
    mode_group.add_argument(
        "--nginx", help="Config lines for nginx", action="store_true")
    parser.add_argument("--domain", default=None, help="Domain to redirect to")
    args = parser.parse_args()

    if args.nginx:
        if not args.domain:
            args.domain = "$host"
        for (src, dest) in redirects:
            print("rewrite ^{}(.*) http://{}/{}".format(src, args.domain, dest))

    if args.amazon:
        print("<RoutingRules>")
        for (src, dest) in redirects:
            print("  <RoutingRule>")
            print("    <Condition>")
            print("      <KeyPrefixEquals>{}</KeyPrefixEquals>".format(src))
            print("      <HttpErrorCodeReturnedEquals>404</HttpErrorCodeReturnedEquals>")
            print("    </Condition>")
            print("    <Redirect>")
            if args.domain:
                print("      <HostName>{}</HostName>".format(args.domain))
                print("      <Protocol>https</Protocol>")
            print("      <ReplaceKeyWith>{}</ReplaceKeyWith>".format(dest))
            print("    </Redirect>")
            print("  </RoutingRule>")
        print("</RoutingRules>")


if __name__ == "__main__":
    main()
