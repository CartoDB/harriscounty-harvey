# harriscounty-harvey

## Convert DigitalGlobe Imagery

DigitalGlobe has made a subset of [pre](https://www.digitalglobe.com/opendata/hurricane-harvey/pre-event) and [post](https://www.digitalglobe.com/opendata/hurricane-harvey/post-event) Hurricane Harvey imagery available via their Open Data Program. In order to make the imagery easier to work with, we went through the steps below to:

- Convert it to EPSG 3857 (Web Mercator)
- Compress it (LZW)
- Internally tile it

### AWS Batch

Amazon provides a service named Batch that simplifes the process of applying an instance of a container image on a pool or compute resources. We used GDAL and the AWS CLI through Batch to process all of the open source DigitalGlobe imagery.

#### Packer

Each compute instance in the AWS Batch cluster needs some amount of scratch space to manipulate imagery. Packer, a tool to codify machine image creation processes, was used to create an Amazon Machine Image (AMI) with enough scratch space to work with.

```bash
$ AWS_PROFILE="..." packer build template.json
```

This command will yield an AMI that can be supplied through an AWS Batch compute environment creation process.

#### Docker

The accompanying `Dockerfile` and `docker-entrypoint.sh` are used to build and publish a container image for use in AWS Batch. At a high level, it uses the AWS CLI to download a GeoTIFF, GDAL to convert it, and the AWS CLI again to upload it.

```bash
$ docker build -t harris-county .
$ docker tag harris-county:latest ....dkr.ecr.us-east-1.amazonaws.com/harris-county:latest
$ docker push ....dkr.ecr.us-east-1.amazonaws.com/harris-county:latest
```

#### `batch_submit.py`

This Python snippet was used to scan the source imagery in an Amazon S3 bucket and automatically submit their URIs to the AWS Batch cluster.
