# ansible-dynamic-inventory

### A GraphQL web service for managing hosts, groups and roles as an Ansible Dynamic Inventory.

### Quick start 

`docker pull evya/ansible-dynamic-inventory:latest`

Make sure you have a Postgresql DB up and running.

Make sure the following environment variables are defined in the container:

DB_HOST, DB_PORT (default: 5432), DB_NAME, DB_USER, DB_PASS.

LOG_LEVEL (default: "INFO").

DEBUG( default: "False").

run:

`docker run -dit -p 8000:8000 evya/ansible-dynamic-inventory:latest`

To manage resources using the graphiQL interface send POST requests to:

`http://<hostname>:8000/v1/graphql`

To get the the JSON representation of the inventory send GET request to:

`http://<hostname>:8000/inventory/`
