#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from configparser import ConfigParser
from pathlib import Path
from opentelemetry import trace as OpenTelemetry
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider, sampling
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)


def main():
    # Set ENV variable for settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

    # START - Dynatrace required code for OpenTelemetry Instrumentation
    # This is for development purposes only. This does not get called when using Gunicorn, see gunicorn.config.py for production instrumentation.
    merged = dict()
    for name in ["dt_metadata_e617c525669e072eebe3d0f08212e8f2.json", "/var/lib/dynatrace/enrichment/dt_metadata.json"]:
        try:
            data = ''
            with open(name) as f:
                data = json.load(f if name.startswith("/var") else open(f.read()))
                merged.update(data)
        except:
            pass

    merged.update({
        "service.name": "Python Retail App",
        "service.version": "1.0.1",
    })
    resource = Resource.create(merged)

    tracer_provider = TracerProvider(sampler=sampling.ALWAYS_ON, resource=resource)
    OpenTelemetry.set_tracer_provider(tracer_provider)

    tracer_provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(
        endpoint=os.environ.get('DT_TENANT_URL'),
        headers={
            "Authorization": ("Api-Token " + os.environ.get("DT_API_TOKEN"))
        },
    )))
    # END - Dynatrace required code for OpenTelemetry Instrumentation
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
