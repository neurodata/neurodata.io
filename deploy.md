# Deploy on AWS

- Create bucket:
    - nd-website-deploy
    - bucket policy:
        ```
        {
        "Version": "2012-10-17",
        "Id": "Policy1509568446316",
        "Statement": [
            {
                "Sid": "Stmt1509568444826",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::nd-website-deploy/*"
            }
        ]
        ```
- CodePipeline
    - Name: nd-website-deploy
    - Source: GitHub
    - Branch: deploy
    - Build provider: AWS CodeBuild
- CodeBuild
    - Name: build-website
    - image: Ubuntu/Python2.7.12
- Deployment: No Deployment

- Role policy - grant s3 privaledges to role for Bucket:
    ```
    {
        "Effect": "Allow",
        "Resource": [
            "arn:aws:s3:::nd-website-deploy/*",
            "arn:aws:s3:::nd-website-deploy"
        ],
        "Action": [
            "s3:*"
        ]
    }
    ```
- S3 - use bucket hosting (because otherwise paths are not followed to their index.html objects)
- CloudFront
    - Source is the bucket host URL
    - HTTP -> HTTPS redirect
    - using default cloudfront certificate
    - index.html as base object
- Create Role for CodeBuild to modifiy CloudFront
    - ListInvalidations/GetInvalidation/CreateInvalidation (so that each build invalidates CloudFront cache)
- Redirects are handled by the properties field in the Bucket (static website `hosting/redirection rules`), and the XML for this can be generated using `misc/redirect.py` and copy/pasting into the bucket properties