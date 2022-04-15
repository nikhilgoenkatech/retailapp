"""
WSGI config for ecommerce project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware
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
from opentelemetry.instrumentation.requests import RequestsInstrumentor

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

application = get_wsgi_application()
application = OpenTelemetryMiddleware(application)

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

# OpenTelemetry instrumentation call for Django
DjangoInstrumentor().instrument()

# OpenTelemetry instrumentation call for Requestse
RequestsInstrumentor().instrument()