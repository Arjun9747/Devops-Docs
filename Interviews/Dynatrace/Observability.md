Information about State of Apps, Infra and Network 

what is the issue 
why is your system is behaving 
give resolutions 

Metrics --> State
Logging --> why the system is in that state
Traces --> how to fix 

Monitoring -> Metrics + alerts + Dashboards

Observability -> Metrics, Logs, Traces

open telementary--> group of APis and SDK

Metrics is raw information 

Alert manager , Premtheus, Grafana 

kube-state metrics --> get all information 

Prometheus get information from 

Node exporter --> CPU , memory , infra 
Kube-state metrics --> talks to API server, get pod state, validating web hooks
Custom metrics --> App related, time for http requests, latency 
MySQL exporter 

Stores them in TSDB 

PromQL talks to HTTP server 

Node exporter runs as a daemon sets

Grafana--> independent of Prometheus, we can set up authentication/ authorization mechanism, integrate with IAM/ SSO 

Service Monitor --> which /metrics are exposed 

Aggregation is sum, avg 

Prometheus --> Counter, Gauge ,summary, histogram 

Exporter give only particular informations, doesn't give traces, 

Custom Metrics --> For instrumentations 

Instrument the metrics through 

Counter --> Metrics always incrementing ( no of loggings, no of http requests)

Gauge --> Incrementing / decrementing (no of configmaps, cpu/memory utlizations) 

Summary --> same as histogram but it will not aggregrate

Histogram --> information block (what is latency, how many times CPU went below 50%,) 1st block for 5 ms, 2nd block for 10 ms

After creating or customizing instrumentation , we need to create service discovery , then create alert manager 

************Jaeger**************

Tracing 

Developers do instrumentation --> Configure Metrics, Logs, Tracing 
SRE / Devops --> Implement the tracing --> Deploy jaeger 

Jaeger Agent will get the information 
Collector --> Collects the information 
DB --> Elastic Search 
UI

Node Exporter  --> Prometheus Scrape the metrics --> fluentbit forward the information--> JAegar store the data in the Elastic Cache itself 
3 Interfaces --> Grafana for metrics interfaces , JAegaer for Distributor Tracing --> Kibana for Log Interface 

Installtion of JAegar 

Install Elastic Search 
IAM 
Install CSI driver 
Create namespace for loggigng, monitoring, tracing 
GEt password, CA cert for elastic search 
Configmap or elastic search configuration 









