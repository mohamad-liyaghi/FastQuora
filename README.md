# FastQuora

## Table of Contents
- [Introduction](#introduction)
- [Technologies](#technologies)
- [Monitoring](#monitoring)
  - [OpenTelemetry](#opentelemetry)
- [Application](#application)
  - [Authentication](#authentication)
  - [Profiles](#profiles)
  - [Questions](#questions)
  - [Answers](#answers)
  - [Votes](#votes)
- [Installation](#installation)
  - [Docker Compose](#docker-compose)
  - [Kubernetes](#kubernetes)
- [Running Tests](#running-tests)

## Introduction
FastQuora is a question-and-answer platform, similar to [Quora](https://www.quora.com/), where users can ask questions, provide answers, and vote on responses. It features a search functionality that allows users to find relevant questions and answers based on keywords. To enhance performance, a caching layer is implemented.

The project follows the `repository pattern` to manage data operations via repositories and controllers. Below is the high-level architecture of the project:
<br>
<img src="./images/structure.png">

## Technologies
This project utilizes a number of modern technologies:
<div>
  <img style="height:30px;" alt="fastapi" src="https://img.shields.io/badge/FastAPI-009688.svg?style=flat&logo=fastapi&logoColor=white">
  <img style="height:30px;" alt="postgresql" src="https://img.shields.io/badge/PostgreSQL-316192.svg?style=flat&logo=postgresql&logoColor=white">
  <img style="height:30px;" alt="elastic" src="https://img.shields.io/badge/Elasticsearch-005571.svg?style=flat&logo=elasticsearch&logoColor=white">
  <img style="height:30px;" alt="docker" src="https://img.shields.io/badge/Docker-2496ED.svg?style=flat&logo=docker&logoColor=white">
  <img style="height:30px;" alt="kubernetes" src="https://img.shields.io/badge/Kubernetes-326CE5.svg?style=flat&logo=kubernetes&logoColor=white">
  <img style="height:30px;" alt="redis" src="https://img.shields.io/badge/Redis-DC382D.svg?style=flat&logo=redis&logoColor=white">
  <img style="height:30px;" alt="pytest" src="https://img.shields.io/badge/Pytest-0A9EDC.svg?style=flat&logo=pytest&logoColor=white">
  <img style="height:30px;" alt="jaeger" src="https://img.shields.io/badge/Jaeger-FF6F00.svg?style=flat&logo=jaeger&logoColor=white">
  <img style="height:30px;" alt="opentelemetry" src="https://img.shields.io/badge/OpenTelemetry-FF6F00.svg?style=flat&logo=opentelemetry&logoColor=white">
<img style="height:30px;" alt="github actions" src="https://img.shields.io/badge/GitHub_Actions-2088FF.svg?style=flat&logo=github-actions&logoColor=white">
</div>

FastQuora uses [FastAPI](https://fastapi.tiangolo.com/) as the backend framework and [PostgreSQL](https://www.postgresql.org/) for database management. It integrates [Elasticsearch](https://www.elastic.co/) to index and search questions and answers, and uses [Redis](https://redis.io/) as a caching layer to boost performance.

The application is containerized using [Docker](https://www.docker.com/) and managed with [Kubernetes](https://kubernetes.io/). For monitoring and observability, the project employs [Jaeger](https://www.jaegertracing.io/) for distributed tracing and [OpenTelemetry](https://opentelemetry.io/) for telemetry data collection. Unit tests are written with [pytest](https://docs.pytest.org/en/stable/) to ensure code reliability.

Additionally, **GitHub Actions** is used for continuous integration and deployment (CI/CD) to automate testing and deployment pipelines. Every pull request triggers the test suite, ensuring that the code is always in a working state. The CI/CD process includes:

- Build and push the image
- Running all unit tests with `pytest` to validate changes.
- Running all unit tests on a production-like environment.
- Deploying the application to cloud infrastructure.


## Monitoring

### OpenTelemetry
This project integrates monitoring features using OpenTelemetry, which collects, processes, and exports telemetry data like traces, metrics, and logs. The metrics are visualized using Jaeger.
<br>
Below is an example of the Jaeger metrics:
<br>
<img src="./images/jaeger.png">

## Application

### Authentication
FastQuora includes a simple authentication system that allows users to register and log in. It uses JWT tokens to authenticate users and protect routes.

### Profiles
Users can view profiles to learn more about who has answered their questions. They can also update their own profiles to highlight their best features. The project does not collect any personal information, so users have the option to remain anonymous.

### Questions
The question component is the core of FastQuora. Users can ask, view, and update questions. With the search functionality, users can find questions based on specific keywords.

### Answers
The answer component allows users to respond to questions, view answers, and update their own answers.

### Votes
FastQuora includes a simple voting system where users can vote on answers to indicate agreement or disagreement. All votes are stored in the database.

## Installation
FastQuora can be run using Docker Compose or Kubernetes in either a local or production environment.

### Docker Compose
To run FastQuora using Docker Compose:
1. Clone the repository:
    ```bash
    git clone https://github.com/mohamad-liyaghi/FastQuora.git
    ```
2. Navigate to the project directory:
    ```bash
    cd FastQuora/
    ```
3. Run the application:
    ```bash
    make run
    ```
   For production mode, use:
    ```bash
    make deploy
    ```

### Kubernetes
To run FastQuora using Kubernetes:
1. Clone the repository:
    ```bash
    git clone https://github.com/mohamad-liyaghi/FastQuora.git
    ```
2. Navigate to the project directory:
    ```bash
    cd FastQuora/
    ```
3. Create the ConfigMaps:
    ```bash
    make local_confmap
    ```
   For production ConfigMaps, use:
    ```bash
    make prod_confmap
    ```
4. Deploy the application:
    ```bash
    make k8s
    ```

The application will now be running on your local machine. You can access the backend at [http://localhost:8000](http://localhost:8000) and Jaeger at [http://localhost:16686](http://localhost:16686).

## Running Tests
Unit tests cover most parts of the application to ensure code quality and reliability. To run all tests:

```bash
make test
```

After running the tests, you should see the following output:
<br>
<img src="./images/test_result.png">
