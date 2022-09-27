import os
from opentelemetry import trace as OpenTelemetry
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider, sampling
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)

def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

    # START - OpenTelemetry Initialization
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
    # END - OpenTelemetry Intialization