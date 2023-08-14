# Prefect Event flows
This repo is a modernized and updated version of the `orion-flows` repo, it focuses on Prefect Events, and uses a YAML file to define deployments.

## Structure
The repo has 4 main parts:
- the `prefect.yaml` file, containing the prefect deployment definitions
- the `blocks` folder, containing the necessary blocks for the project
- the `flows` folder, containing Prefect flows divided in subfolders for tidyness
- the `ìmages` folder, containing the Dockerfiles for the different images needed


Deployments with a `prefect.yaml` file requires a work-pool with a **worker** instead of a normal **agent**. Because I am on AKS (kubernetes), I could follow the guide here: https://docs.prefect.io/2.11.3/guides/deployment/helm-worker/

The two deployments in this project is intended to test/demonstrate an interesting concept of deployments triggered by "data lineage" events. The flow `load_unemployment_data` reads data from a CSV online, and writes it to a Snowflake database.

Writing to the database is done using a `SnowflakeLineageBlock`. This block holds the snowflake connection details, and it includes functions to read/write from snowflake. When reading or writing to snowflake using this library, a Prefect event is created to record each query submitted. This event has a standardized format, and includes the URI to the table written to, and the type of event (read, write, create).

The second flow, `update_unemployment_report`, is configured via the `prefect.yaml` file to automatically run on new lineage events that writes to the unemployment table - which the `load_unemployment_data` flow does.

This flow uses the new data in the unemployment table to write a small report about the new data and creating a markdown artifact from it - with the help of the `marvin` library.


## The Lineage repo
Be aware that the `eventbased-lineage` library that holds the `SnowflakeLineageBlock` class is very young, and under development (as indicated by the fact that I'm using a feature branch here). There will, in all likelihood, be breaking changes. It was initially intended to be an integration with Marques (and to some extent it still is), but it has been adapted to work with prefect events.

It is intended to be extensible, so that new classes to work with other types of storage (postgres, file systems, etc) can be added as we go along.