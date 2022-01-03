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
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk import trace
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)
from opentelemetry.instrumentation.django import DjangoInstrumentor


def main():
    # Set ENV variable for settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

    # Dynatrace required code for OpenTelemetry Instrumentation - START
    resource = Resource.create({
    "service.name": "Python Retail App",
    "service.version": "1.0.1"
    })


    for name in ["dt_metadata_e617c525669e072eebe3d0f08212e8f2.properties", "/var/lib/dynatrace/enrichment/dt_metadata.properties"]:
        try:
            config = ConfigParser()
            with open(Path(name).read_text()) as f:
                config.read_string('[_]\n' + f.read())
            resource.update(config['_'])
            break
        except:
            pass

    OpenTelemetry.set_tracer_provider(TracerProvider(resource=resource, sampler=trace.sampling.ALWAYS_ON))

    OpenTelemetry.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(
            endpoint=os.environ.get('DT_TENANT_URL'),
            headers={
                "Authorization": ("Api-Token " + os.environ.get("DT_API_TOKEN"))
            },
        ))
    )
    
    # Dynatrace required code for OpenTelemetry Instrumentation - END

    # OpenTelemetry instrumentation call for Django
    DjangoInstrumentor().instrument()
    
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
