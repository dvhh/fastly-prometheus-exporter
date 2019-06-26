'''
Download fastly realtime
'''
import argparse
import json
import sys
import time
import multiprocessing
import requests


process_local_session = None  # process local
API_KEY = None  # global


def get_rt_metrics(
    session,
    service_id: str,
    endpoint: str = 'https://rt.fastly.com/v1/channel'
):
    '''
    get service specific metrics
    '''
    uri = '{}/{}/ts/h/limit/5'.format(endpoint, service_id)
    response = session.get(uri)
    assert response.status_code == 200, '{}\t{}\n'.format(
        response.status_code,
        response.json()
    )
    return response.json()


def get_services(
    session,
    endpoint: str = 'https://api.fastly.com/service'
):
    '''
    get services list
    '''
    response = session.get(endpoint)
    assert response.status_code == 200, '{}\t{}\n'.format(
        response.status_code,
        response.json()
    )
    return response.json()


def get_annotated_metrics(service):
    '''
    get service metrics and return an envelope also containing 
    metrics and service information
    '''
    global process_local_session
    if process_local_session is None:
        process_local_session = requests.Session()
        global API_KEY
        process_local_session.headers.update({'Fastly-Key': API_KEY})
    metrics = get_rt_metrics(process_local_session, service['id'])
    result = {}
    result['id'] = service['id']
    result['name'] = service['name']
    if not metrics['Data']:
        return None  # No metrics reported

    if time.time() - int(metrics['Data'][-1]['recorded']) > 30:
        return None
    result['metric'] = metrics['Data'][-1]
    return result


def set_api_key(value: str):
    '''
    global helper for API_KEY
    '''
    global API_KEY
    API_KEY = value


def main():
    '''
    Main entry point
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        metavar='<API_KEY>',
        dest='api_key',
        help='API key'
    )
    parser.add_argument(
        '-j', '--jobs',
        dest='jobs',
        help='number of parallel jobs',
        type=int,
        default=multiprocessing.cpu_count()
    )
    args = parser.parse_args()
    set_api_key(args.api_key)

    with requests.Session() as session:
        session.headers.update({'Fastly-Key': args.api_key})
        services = get_services(session)

    with multiprocessing.Pool(args.jobs) as pool:
        results = pool.map(get_annotated_metrics, services)

    json.dump(
        list(
            sorted(
                filter(
                    lambda result: result is not None, results),
                key=lambda result: result['id'])
        ), sys.stdout, sort_keys=True)


if __name__ == '__main__':
    main()
