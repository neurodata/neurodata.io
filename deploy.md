# Deployment

The demo site is deployed on netlify. The production site is deployed on AWS using CodePipeline.

## Netlify

Connect it to GitHub repo, and the deployment settings are as follows:

Build command: `grow install; grow build; cp robots-demo.txt build/robots.txt`

Publish directory: `build`

Production branch: `deploy`

Since this is demo site, no custom domain.

Set to build on all branches and to add status messages to PRs.

## AWS

### Create bucket

- nd-website-deploy
- bucket policy:

  ```json
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

### CodePipeline

- Name: nd-website-deploy
- Source: GitHub
- Branch: deploy
- Build provider: AWS CodeBuild

### CodeBuild

- Name: build-website
- image: Ubuntu/Python2.7.12
- buildspec.yml: [buildspec_deploy.yml](buildspec_deploy.yml)

### Deployment: _No Deployment_

### Role policy - grant s3 privileges to role for Bucket

```json
{
  "Effect": "Allow",
  "Resource": [
    "arn:aws:s3:::nd-website-deploy/*",
    "arn:aws:s3:::nd-website-deploy"
  ],
  "Action": ["s3:*"]
}
```

### S3 bucket hosting

Otherwise paths are not followed to their index.html objects

### CloudFront

- Source is the bucket host URL (not the _bucket_ object path)
- HTTP -> HTTPS redirect
- using default CloudFront certificate
- index.html as base object

### Create Role for CodeBuild to modify CloudFront

- ListInvalidations/GetInvalidation/CreateInvalidation (so that each build invalidates CloudFront cache)
- Role needs permissions to S3 buckets as well

### Redirects

- Redirects are handled by the properties field in the Bucket (static website `hosting/redirection rules`), and the XML for this can be generated using `misc/redirect.py` and copy/pasting into the bucket properties

## Talks

- New CloudFront origin for talks (from a different bucket)
- Have a similar CodePipeline setup for the [neurodata/talks](https://github.com/neurodata/talks) repo, which just copies objects to the talks bucket.
- Under behaviors in CloudFront, we have the following hierarchy:
  1. `talks` | S3-nd-website-deploy
  2. `talks/` | S3-nd-website-deploy
  3. `talks/*` | S3-nd-talks
  4. `Default (*)` | S3-nd-website-deploy
- This allows serving the talks listing page at neurodata.io/talks/ while also serving each talk at `neurodata.io/talks/talk.html`
- Inside the bucket for talks, all the content are organized with a prefix of `talks`.
