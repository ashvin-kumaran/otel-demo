# Adding Observability to a Multiple Flask Apps

This project demonstrates monitoring and troubleshooting  applications via OpenTelemetry. Instrumentation of code allows us to see the end to end lifecycle of a request in a microservices architecture. We use open source observability backends (jaeger, zipkin, and prometheus) for visualization of metrics, logs, and traces. The otel collector serves as a middleman between your app and your observability backends.

## Getting Started

### Dependencies

* Docker 
* Docker Compose
* Pipenv

### Installing

* Clone the otel-demo project.

* Use pipenv to enter the virtual environment and install dependencies.
  ```
  pipenv --python 3.12 shell
  pipenv install
  ```

### Executing program

* To start up the observability backends and otel collector, use the `otel/docker-compose.yaml` file.
  ```
  docker-compose -f otel/docker-compose.yaml up
  ```
  * The configs for the otel collector and prometheus backend are in the ```otel``` folder
    * ```otel/otel-collector-config.yaml```
      * Defines how we want to receive Telemetry (as OTLP GRPC requests)
      * How we want to process Telemetry (in Batches)
      * And how we want to export Telemetry (to Prometheus, Zipkin, and Jaeger)
    * ```otel/prometheus.yaml```
      * Defines where we want to gather Metrics Telemetry from (the Otel Collector)
* Check if the containers are running successfully (OpenTelemetry Collector and 3 observability tools: Jaeger, Zipkin, and Prometheus.)
  ```
  docker ps
  ```
* Run the opentelemetry bootstrap command to read through the list of packages installed in your active site-packages folder, and installs the corresponding instrumentation libraries for these packages, if applicable.
  ```
  opentelemetry-bootstrap -a install 
  ```
* Open a terminal window to run the arithmetic application. Make sure to activate the environment again.
  ```
  opentelemetry-instrument \
    --traces_exporter console,otlp \
    --metrics_exporter console \
    --service_name arithmetic-service \
    --exporter_otlp_endpoint 0.0.0.0:4317 \
    --exporter_otlp_traces_insecure=true \
    pipenv run arithmetic
  ```
* Now, open a second terminal window to run the demo application. Make sure to activate the environment again.
  ```
  opentelemetry-instrument \
    --traces_exporter console,otlp \
    --metrics_exporter console \
    --service_name demo-service \
    --exporter_otlp_endpoint 0.0.0.0:4317 \
    --exporter_otlp_traces_insecure=true \
    pipenv run demo
  ```
  
# Observing the application

* Our collector and observability tools are up and running!
* View the tools at:
  * Jaeger = [localhost:16686](http://0.0.0.0:16686)
  * Zipkin = [localhost:9411](http://0.0.0.0:9411)
  * Prometheus = [localhost:9090](http://0.0.0.0:9090)
* Send a request to our demo server.
  ```
  curl "localhost:5001"
  ```
* On Jaeger, select the demo-service and find traces. You can see that our get request was reported to jaeger by our app.
* Send another request to our demo server.
  ```
  curl "localhost:5001/dog"
  ```
* Find traces again. This time, you can see that it is a bigger trace than before, with multiple spans.
* That was pretty simple. Let's try sending a request that will cause the demo app to talk with the arithmetic app. 
  ```
  curl "localhost:5001/divide?arg1=1&arg2=2"
  ```
* Inspecting the trace, we can see the path our request took. It is as expected.
* Now, let's try seeing how OpenTelemetry can help debug issues with our app. Let's induce an error by dividing by 0.
  ```
  curl "localhost:5001/divide?arg1=1&arg2=0"
  ```
* When finding traces, we can see that jaeger has reported an error. Inspecting the trace further, the logs report the source of the error is division by zero, and we know exactly where it happened.
  
# Inspiration, code snippets, etc.

* [open telemetry overview](https://www.aspecto.io/blog/what-is-opentelemetry-the-infinitive-guide/)
* [python automatic instrumentation](https://opentelemetry.io/docs/languages/python/automatic/)
* [otel collector significance](https://grafana.com/blog/2023/11/21/do-you-need-an-opentelemetry-collector/)
* [open telemetry documentation](https://opentelemetry.io/docs/)