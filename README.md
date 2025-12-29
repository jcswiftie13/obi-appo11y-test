# OpenTelemetry eBPF Instrumentation Memory Leak Reproduction

This repository is designed to reproduce and investigate a potential memory leak issue in the `opentelemetry-ebpf-instrumentation` when **Application Metrics** are enabled.

## Overview

The goal is to monitor the resource consumption of an eBPF-instrumented application under load to verify if memory usage grows indefinitely when metrics collection is active.

## Prerequisites

Before running the tests, ensure you have the following installed:

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
- [Go](https://go.dev/) (1.21+ recommended)
- `make` utility

## Getting Started

### 1. Initialize the Environment

To start the target application and the monitoring stack (OTel Collector, Prometheus, etc.), simply run:

```bash
make up
```

### 2. Reproduction Scenario
Once the environment is up, the following sequence occurs automatically:

1. Automated Traffic: A Python script continuously connects to the PostgreSQL instance (which is instrumented by opentelemetry-ebpf-instrumentation).

2. Execute & Disconnect: The script executes SQL commands and then disconnects, repeating this loop indefinitely.

3. The Issue: As the connections open and close, the instrumentation creates readers for the metrics.

### 3. Observations (The Leak)
You can verify the leak by accessing the Go application's pprof endpoint. You will observe that:

- Goroutine Leak: The number of goroutines related to the periodic reader does not decrease after the PostgreSQL connection is closed.

- Accumulation: These goroutines continue to accumulate over time, leading to increasing memory consumption.

To check the goroutines, you can use:

```bash
go tool pprof http://localhost:6060/debug/pprof/goroutine
```