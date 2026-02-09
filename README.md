## PostgreSQL/PostGIS Database Setup

### Why Use PostgreSQL + PostGIS for Geospatial Coral Reef Data
PostgreSQL is a powerful, open-source relational database system that can handle a variety of data types. When combined with PostGIS, it becomes a robust platform for storing and analyzing geospatial data, making it particularly well-suited for coral reef data that involves geographic coordinates and spatial analysis.

### How to Install PostgreSQL on Synology NAS
1. Open the Package Center on your Synology NAS.
2. Search for "PostgreSQL" and select the appropriate package.
3. Click "Install" and follow the on-screen instructions to complete the installation.

### How to Access the Database
- **pgAdmin**: A graphical interface to manage PostgreSQL databases. Download it from the official pgAdmin website.
- **SSH**: Use `ssh` to connect to your Synology NAS and access PostgreSQL via command line.
- **Python**: Use libraries like `psycopg2` or `SQLAlchemy` to connect to the PostgreSQL database from a Python application.
- **Network Access**: Ensure your Synology NAS is configured to allow connections over the network.
- **Remote Access**: Configure PostgreSQL to accept remote connections by editing the `postgresql.conf` and `pg_hba.conf` files accordingly.

### Future Plans for Geospatial Frontend
We plan to develop a user-friendly geospatial frontend that will allow researchers and users to visualize and interact with the coral reef data seamlessly.

### Database Schema Overview
- **Sites**: Contains geographical coordinates of various coral reef sites.
- **MPAs (Marine Protected Areas)**: Information about protected areas in the database.
- **Temperature Data**: Records of sea temperatures relevant to coral health.
- **Growth Data**: Data tracking coral growth over time.
- **Surveys**: Information collected during various research surveys.
- **Photos with Geotags**: Visual data associated with specific locations, including geospatial information.

### Connection Examples
```python
import psycopg2

# Connect to the PostgreSQL database
connection = psycopg2.connect(
    host="your_host",
    database="your_db",
    user="your_user",
    password="your_password"
)
```

### PostGIS Extension Setup
1. Connect to your PostgreSQL database.
2. Run the following command to enable PostGIS:
   ```sql
   CREATE EXTENSION postgis;
   ```
3. Verify PostGIS installation with:
   ```sql
   SELECT PostGIS_Version();
   ```
