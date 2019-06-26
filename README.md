# fastly-prometheus-exporter

Consume the [Fastly Real-time Analytics API][1] and export data via a [Prometheus metrics][2] endpoint.

## Requirements 

- bash
- gzip
- [Python 3][3]
	- [flask][4]
	- [jinja][5]
	- [requests][6]

## Optionals

- [Prometheus][2], metrics output validation
- [shellcheck][7], bash linting
- [Docker][8]

## Usage

```
FASTLY_API_KEY="${fastly_api_token}" bash loop.sh
```

Will start `endpoint.py` to serve the metrics files, and make a loop calling `collect_rt_metrics.py` which download 
the metrics and will format the output to be suitable with Prometheus.

## Exported metrics

See `metrics_list.txt` 

metrics names are prefixed with `fastly_` and are exported as counter

## Contributing

Contributions are subjected to reviews, please submit a pull request.

Verify your submission with:
- shellcheck
- flake8
- pylint (in case of conflict flake8 take precedence)

check formatter output with
```
promtool check metrics < output
```

## TODO

Configurables:
- Endpoint port (currently only port 5000)
- loop pause

Improvement
- Better control of loop length (exact requested time, instead of execution time  + sleep)
- use temp file name and storage
- logging


[1]: https://docs.fastly.com/api/analytics
[2]: https://prometheus.io/
[3]: https://www.python.org/
[4]: http://flask.pocoo.org/
[5]: http://jinja.pocoo.org/
[6]: https://2.python-requests.org/en/master/
[7]: https://www.shellcheck.net/
[8]: https://www.docker.com/
