#!/usr/bin/env python

#
# Generate redirects for old URLs.
#
# Use --amazon to generate AmazonS3 redirection rules which can be applied to the bucket.
# See https://docs.aws.amazon.com/AmazonS3/latest/dev/how-to-page-redirect.html for details.
#

import argparse

redirects = [
    ['bock11/', 'data/bock11/'],
    ['array-tomography/', 'project/synaptomes/'],
    ['kasthuri11/', 'data/kasthuri15/'],
    ['bhatla15/', 'data/bhatla15/'],
    ['fly-medulla/', 'data/takemura13/'],
    ['pristionchus-pacificus/', 'data/bumbarger13/'],
]

def main():
    parser = argparse.ArgumentParser()
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--amazon", help="Generate XML syntax for S3 web hosting", action="store_true")
    mode_group.add_argument("--nginx", help="Config lines for nginx", action="store_true")
    parser.add_argument("--domain", default="neurodata.io")
    args = parser.parse_args()

    if args.nginx:
        for (src, dest) in redirects:
            print("rewrite ^{}(.*) http://{}{}".format(src, args.domain, dest))

    if args.amazon:
        print("<RoutingRules>")
        for (src, dest) in redirects:
            print("  <RoutingRule>")
            print("    <Condition>")
            print("      <KeyPrefixEquals>{}</KeyPrefixEquals>".format(src))
            print("    </Condition>")
            print("    <Redirect>")
            print("      <ReplaceKeyWith>{}</ReplaceKeyWith>".format(dest))
            print("    </Redirect>")
            print("  </RoutingRule>")
        print("</RoutingRules>")

if __name__ == "__main__":
    main()

