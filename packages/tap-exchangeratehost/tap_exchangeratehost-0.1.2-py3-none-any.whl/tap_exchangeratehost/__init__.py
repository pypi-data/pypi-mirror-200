#!/usr/bin/env python3
from __future__ import annotations
import argparse
from datetime import datetime, timedelta, date
import json
import sys
import time
from typing import Optional
import backoff
import requests
import singer


endpoint = "https://api.exchangerate.host/timeseries"
logger = singer.get_logger()

DATE_FORMAT = "%Y-%m-%d"


def parse_rates(r, rate_date):
    if not r["rates"][rate_date]:
        return None
    parsed = r["rates"][rate_date]
    parsed[r["base"]] = 1.0
    parsed["date"] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.strptime(rate_date, DATE_FORMAT))
    return parsed


def giveup(error):
    logger.error(error.response.text)
    response = error.response
    return not (response.status_code == 429 or
                response.status_code >= 500)


@backoff.on_exception(backoff.constant,
                      requests.exceptions.RequestException,
                      jitter=backoff.random_jitter,
                      max_tries=5,
                      giveup=giveup,
                      interval=30)
def request(url, params):
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    return response


def make_schema(response: dict, dates: list[str]) -> dict:
    # Make Singer schema
    schema = {
        "type": "object",
        "properties": {
            "date": {
                "type": "string",
                "format": "date-time",
            },
        },
    }
    last_date = dates[-1]
    # Populate the currencies
    for rate in response["rates"][last_date]:
        if rate not in schema["properties"]:
            # noinspection PyTypeChecker
            schema["properties"][rate] = {"type": ["null", "number"]}
    return schema


def do_sync(base, start_date: str, end_date: Optional[str] = None) -> Optional[str]:
    state = {"start_date": start_date}
    next_date = start_date

    if not end_date:
        end_date = (
            date.today() + timedelta(days=1)).strftime(DATE_FORMAT)

    params = {
        "base": base,
        "start_date": start_date,
        "end_date": end_date,
    }

    logger.info(json.dumps(params))

    try:
        response = request(endpoint, params)
        response = response.json()
    except requests.exceptions.RequestException as e:
        logger.critical(
            json.dumps(
                {"url": e.request.url,
                 "status": e.response.status_code,
                 "message": e.response.text,
                 }
            )
        )
        singer.write_state(state)
        sys.exit(-1)

    if start_date in response["rates"]:

        # Write records ordered by the date
        dates = sorted([d for d in response["rates"].keys()])

        singer.write_schema("exchange_rate", make_schema(response, dates), "date")

        for d in dates:
            record = parse_rates(response, d)
            if not record:
                continue
            singer.write_records("exchange_rate", [record])
            next_date = (datetime.strptime(d, DATE_FORMAT) +
                         timedelta(days=1)).strftime(DATE_FORMAT)
            state = {"start_date": next_date}

        singer.write_state(state)
        logger.info(json.dumps(
            {"message": f"tap completed successfully rows={len(dates)}"}
        ))
        return next_date
    else:
        logger.info(json.dumps(
            {"message": "tap completed successfully (nothing done, no new data)."}
        ))
        return None


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c", "--config", help="Config file", required=False)
    parser.add_argument(
        "-s", "--state", help="State file", required=False)

    args = parser.parse_args()

    if args.config:
        with open(args.config) as f:
            config = json.load(f)
    else:
        config = {}

    if args.state:
        with open(args.state) as f:
            state = json.load(f)
    else:
        state = {}

    start_date = (state.get("start_date") or config.get("start_date") or
                  datetime.utcnow().strftime(DATE_FORMAT))
    start_date = singer.utils.strptime_with_tz(
        start_date).date().strftime(DATE_FORMAT)

    end_date = (config.get("end_date") or
                datetime.utcnow().strftime(DATE_FORMAT))
    end_date = singer.utils.strptime_with_tz(
        end_date).date().strftime(DATE_FORMAT)

    next_date = start_date
    while next_date and datetime.strptime(next_date, DATE_FORMAT) < datetime.utcnow():
        next_date = do_sync(config.get("base", "EUR"), next_date, end_date)


if __name__ == "__main__":
    main()
