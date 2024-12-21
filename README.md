### **Steps to Deploy and Start Ingesting Data**

#### **1. Prepare Your Environment**
1. **Install Docker and Docker Compose**:
   - Ensure Docker and Docker Compose are installed on your system. Use the following commands to verify:
     ```bash
     docker --version
     docker-compose --version
     ```

2. **Set Up External Storage**:
   - Confirm that the external storage path is accessible and mounted correctly (e.g., `F:/DissertationLab/realtime-analytics-debezium-cdc/docker-data`).

3. **Configure the Docker Compose File**:
   - Ensure the `docker-compose.yml` file is updated with your specific environment variables, database credentials, and volume paths.

---

#### **2. Deploy the Docker Compose Services**
1. **Navigate to the Deployment Directory**:
   ```bash
   cd /path/to/your/docker-compose-directory
   ```

2. **Start All Services**:
   ```bash
   docker-compose up -d
   ```
   - This command starts all containers in detached mode.

3. **Verify the Deployment**:
   - List running containers:
     ```bash
     docker ps
     ```
   - Ensure all services (Kafka, Zookeeper, HDFS, databases, connectors, etc.) are running.

---

#### **3. Configure Debezium Connectors**
1. **Access the Kafka Connect REST API**:
   - Kafka Connect runs at `http://localhost:8087`.

2. **Create Connector Configurations for Each Database**:
   - Example JSON payload for a PostgreSQL Debezium connector:
     ```json
     {
       "name": "postgres-connector",
       "config": {
         "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
         "tasks.max": "1",
         "database.hostname": "postgres-source",
         "database.port": "5433",
         "database.user": "postgres",
         "database.password": "postgres",
         "database.dbname": "sourcedb",
         "database.server.name": "postgresql",
         "table.include.list": "public.my_table",
         "plugin.name": "pgoutput",
         "database.history.kafka.bootstrap.servers": "kafka-broker1:9092",
         "database.history.kafka.topic": "schema-changes.postgresql"
       }
     }
     ```
   - Post the configuration to Kafka Connect:
     ```bash
     curl -X POST -H "Content-Type: application/json" --data @postgres-connector.json http://localhost:8087/connectors
     ```

3. **Repeat for Other Data Sources**:
   - Replace the relevant configurations for MySQL, Oracle, and SQL Server.

---

#### **4. Verify Data Ingestion**
1. **Check Kafka Topics**:
   - Use the Kafka CLI tools or a UI like Confluent Control Center to ensure data is flowing into Kafka topics.

2. **Access Flink and Spark**:
   - Flink UI: [http://localhost:8083](http://localhost:8083)
   - Spark UI: [http://localhost:8085](http://localhost:8085)

3. **Load Data into Persistent Storage**:
   - Ensure HDFS is set up as a sink for processed data and Druid is consuming the data from Kafka or HDFS.

---

#### **5. Set Up Monitoring**
1. **Access Grafana**:
   - URL: [http://localhost:3001](http://localhost:3001)
   - Default credentials: `admin`/`admin`.

2. **Access Prometheus**:
   - URL: [http://localhost:9090](http://localhost:9090)

3. **Configure Alerts**:
   - Update the Alertmanager configuration (`alertmanager.yml`) to send email notifications or other alerts.

---

### **Reference URLs for Resources**
1. **Debezium Documentation**:
   - [https://debezium.io/documentation/](https://debezium.io/documentation/)

2. **Kafka Connect API**:
   - [https://docs.confluent.io/platform/current/connect/index.html](https://docs.confluent.io/platform/current/connect/index.html)

3. **Apache Flink Documentation**:
   - [https://nightlies.apache.org/flink/](https://nightlies.apache.org/flink/)

4. **Apache Spark Documentation**:
   - [https://spark.apache.org/docs/latest/](https://spark.apache.org/docs/latest/)

5. **Prometheus Documentation**:
   - [https://prometheus.io/docs/](https://prometheus.io/docs/)

6. **Grafana Documentation**:
   - [https://grafana.com/docs/](https://grafana.com/docs/)

7. **Apache Druid Documentation**:
   - [https://druid.apache.org/docs/latest/](https://druid.apache.org/docs/latest/)

---

These steps will help you deploy the system, start ingesting data, and monitor the pipeline. Let me know if you encounter any issues!
