from os.path import splitext

import boto3


BUCKET = 'digitalglobe-hurricane-harvey-us-east-1'


def only_original_tiffs(key):
    return not any([
        key.endswith('.ovr'),
        'lzw' in key
    ])


def get_original_tiffs(client, event_prefix='pre-event/'):
    response = client.list_objects_v2(Bucket=BUCKET, Prefix=event_prefix)
    return filter(only_original_tiffs, map(lambda x: x.get('Key'), response['Contents']))


def submit_job(client, path):
    print('Submitting job [{}]...'.format(path))
    client.submit_job(
        jobName=splitext(path)[0].replace('/', '-'),
        jobQueue='queueHarrisCounty',
        jobDefinition='jobHarrisCounty',
        parameters={
            's3Uri': 's3://{}/{}'.format(BUCKET, path)
        },
        retryStrategy={
            'attempts': 3
        }
    )


if __name__ == '__main__':
    s3 = boto3.client('s3')
    batch = boto3.client('batch')

    for path in get_original_tiffs(s3, event_prefix='pre-event/'):
        submit_job(batch, path)

    for path in get_original_tiffs(s3, event_prefix='post-event/'):
        submit_job(batch, path)
