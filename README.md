# realtime-analytics-debezium-cdc
Real-Time Analytics with Stream Processing and Change Data Capture: A Kafka-Based Solution for Data Warehousing

### **Steps to Deploy the Updated System**
1. **Prepare Your Local Environment**:
   - Ensure **Docker Desktop** is installed and running on your Windows machine.
   - Verify Docker and Docker Compose are properly installed:
     ```bash
     docker --version
     docker-compose --version
     ```

2. **Set Up the Deployment Directory**:
   - Create a directory for the deployment, e.g., `C:\docker-deployment\monitoring-system`.
   - Place the following files in this directory:
     - `docker-compose.yml`: The updated file you just created.
     - `prometheus.yml`: Configuration for Prometheus.
     - `alertmanager.yml`: Configuration for Alertmanager.

3. **Ensure External Storage Access**:
   - Verify that your external storage drive (e.g., `E:/docker-data`) is set up as Docker shared storage.
   - In Docker Desktop, go to **Settings > Resources > File Sharing** and ensure the external storage drive is shared.

4. **Start the System**:
   - Open **Command Prompt** or **PowerShell**, navigate to the deployment directory, and run:
     ```bash
     docker-compose up -d
     ```
   - This command will:
     - Build and start all the containers defined in `docker-compose.yml`.
     - Run them in the background.

5. **Verify Services**:
   - Check that all containers are running:
     ```bash
     docker ps
     ```

6. **Access Logs (Optional)**:
   - View logs for any container (e.g., Prometheus):
     ```bash
     docker logs prometheus
     ```

---

### **URLs to Monitor**
1. **Prometheus**:
   - URL: [http://localhost:9090](http://localhost:9090)
   - Use Prometheus to monitor system metrics and query data.

2. **Grafana**:
   - URL: [http://localhost:3000](http://localhost:3000)
   - Default login credentials:
     - Username: `admin`
     - Password: `admin`
   - Configure Prometheus as a data source in Grafana:
     1. Log in to Grafana.
     2. Go to **Configuration > Data Sources**.
     3. Add a new data source of type **Prometheus** with URL `http://prometheus:9090`.

3. **Alertmanager**:
   - URL: [http://localhost:9093](http://localhost:9093)
   - Use Alertmanager to manage and send alerts via email or other notification channels.

4. **Schema Registry**:
   - URL: [http://localhost:8081](http://localhost:8081)
   - Use the Schema Registry REST API to manage schemas.

5. **Node Exporter**:
   - URL: [http://localhost:9100/metrics](http://localhost:9100/metrics)
   - Provides metrics about the host system.

6. **Druid Coordinator Console**:
   - URL: [http://localhost:8082](http://localhost:8082)
   - Manage Druid services and data ingestion tasks.

7. **HDFS NameNode UI**:
   - URL: [http://localhost:9870](http://localhost:9870)
   - Monitor HDFS storage and block distribution.

---

### **Reference URLs**
1. **Prometheus Documentation**:
   - [https://prometheus.io/docs/](https://prometheus.io/docs/)

2. **Grafana Documentation**:
   - [https://grafana.com/docs/](https://grafana.com/docs/)

3. **Alertmanager Documentation**:
   - [https://prometheus.io/docs/alerting/latest/alertmanager/](https://prometheus.io/docs/alerting/latest/alertmanager/)

4. **Schema Registry API Reference**:
   - [https://docs.confluent.io/platform/current/schema-registry/develop/api.html](https://docs.confluent.io/platform/current/schema-registry/develop/api.html)

5. **Druid Documentation**:
   - [https://druid.apache.org/docs/latest/](https://druid.apache.org/docs/latest/)

6. **HDFS Monitoring**:
   - [https://hadoop.apache.org/docs/r3.3.0/hadoop-project-dist/hadoop-hdfs/HDFSUserGuide.html](https://hadoop.apache.org/docs/r3.3.0/hadoop-project-dist/hadoop-hdfs/HDFSUserGuide.html)

---

### **Next Steps**
- **Set Up Alerts**:
  - Configure Prometheus rules to trigger alerts, and verify email notifications are sent via Alertmanager.

- **Test the Workflow**:
  - Ingest data into Kafka topics, process it via Druid, and monitor the entire pipeline using Grafana.

- **Monitor Resource Usage**:
  - Use `docker stats` or Node Exporter metrics to track CPU, memory, and disk usage.
