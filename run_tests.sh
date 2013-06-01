#!/bin/bash
PYTHONPATH=/opt/bridgebeam/

export TWILIO_ACCOUNT_SID=ACCOUNT_SID
export TWILIO_AUTH_TOKEN=AUTH_TOKEN

find ./bridgebeam -name 'test_*' -exec echo "{}" \; -exec python {} \;

