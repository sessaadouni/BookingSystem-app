<!-- markdownlint-disable MD033 -->

# BookingSystem Project

## Project Overview

This project is a data migration application that transfers data from an SQL database to a NoSQL database.

<details>
  <summary style="font-size: 1.5rem; font-weight: bold; margin-top: 1em; margin-bottom: 1em;">Table of Contents</summary>
  <ul>
    <li><a href="#project-overview">Project Overview</a></li>
    <li><a href="#objective">Objective</a></li>
    <li><a href="#prerequisites">Prerequisites</a></li>
    <li><a href="#installation">Installation</a>
      <ul>
        <li><a href="#clone-the-project">Clone the Project</a></li>
        <li><a href="#setting-up-environment-files">Setting Up Environment Files</a></li>
        <li><a href="#setting-up-development-environment">Setting Up Development Environment</a></li>
        <li><a href="#setting-up-the-mongodb-replica-set">Setting Up the MongoDB Replica Set</a></li>
        <li><a href="#installation-of-poetry-environment">Installation of Poetry Environment</a></li>
        <li><a href="#data-normalization">Data Normalization</a></li>
        <li><a href="#data-injection">Data Injection</a></li>
        <li><a href="#verify-data">Verify Data</a></li>
        <li><a href="#test-queries">Test Queries</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
  </ul>
</details>

<details>
  <summary style="font-size: 1.5rem; font-weight: bold; margin-top: 1em; margin-bottom: 1em;">Objective</summary>
  <p>This project is an application for migrating data from an SQL database to a NoSQL database.</p>
</details>

<details>
  <summary style="font-size: 1.5rem; font-weight: bold; margin-top: 1em; margin-bottom: 1em;">Prerequisites</summary>
  <ul>
    <li>Docker (Docker-compose)</li>
    <li>make</li>
  </ul>
</details>

<details>
  <summary style="font-size: 1.5rem; font-weight: bold; margin-top: 1em; margin-bottom: 1em;">Installation</summary>

<h3>Clone the Project</h3>
<pre><code>git clone https://github.com/sessaadouni/Bookingsystem.git
cd Bookingsystem
</code></pre>

<h3>Setting Up Environment Files</h3>
<pre><code>cp .docker/mongo/.env.mongo.example .docker/mongo/.env.mongo
cp .docker/redis/.env.redis.example .docker/redis/.env.redis
cp .env.example .env
</code></pre>

Change the values of the environment variables in the .env.\* files to match your configuration.

<h3>Setting Up Development Environment</h3>
<pre><code>make compose-up
</code></pre>

<h3>Setting Up the MongoDB Replica Set</h3>
<pre><code>make replica-init
</code></pre>

<h3>Installation of Poetry Environment</h3>
<pre><code>make install-poetry
</code></pre>

<h3>Data Normalization</h3>
<pre><code>make denormalize
</code></pre>

<h3>Data Injection</h3>
<pre><code>make inject-redis
make inject-mongo
</code></pre>

<h3>Verify Data</h3>

> For Redis:

<pre><code>make redis-cli

# Replace "Database password" with the actual password
> AUTH "Database password"
> KEYS *
> QUIT [ou Ctrl+C]
</code></pre>

> For Mongo:

<pre><code>make mongo-shell

> show dbs
> use BookingSystemDB
> db.clients.find()
> db.vols.find()
> db.reservations.find()
> quit() [Or Ctrl+C]
</code></pre>

<h3>Test Queries</h3>
<pre><code>make python file=src/api/request_json.py
make python file=src/api/request_redis.py
make python file=src/api/request_mongo.py
</code></pre>

<h3>Test Big Data</h3>
Inject fake data into MongoDB and Redis.
<pre><code>make python file=src/scripts/fake_data.py</code></pre>
Test queries with big data.
<pre><code>
make python file=src/api/req_mongo.py
make python file=src/api/request_redis.py
make python file=src/api/request_mongo.py
</code></pre>

</details>

<details>
  <summary style="font-size: 1.5rem; font-weight: bold; margin-top: 1em; margin-bottom: 1em;">Usage</summary>
  <p>The primary use case for this project is to migrate data from an SQL database to a NoSQL database. The following steps outline the process:</p>
  <ol>
    <li>Data normalization: This involves converting the data from the SQL database to a format that is easier to work with in the NoSQL database.</li>
    <li>Data injection: This involves inserting the normalized data into the NoSQL database.</li>
    <li>Querying the data: This involves querying the data in the NoSQL database using the API.</li>
    <li>Checking Performance: This involves measuring the performance of the data migration process.</li>
  </ol>
</details>

<details>
  <summary style="font-size: 1.5rem; font-weight: bold; margin-top: 1em; margin-bottom: 1em;">License</summary>
  <p>This project is licensed under the MIT License. See the <a href="LICENSE">LICENSE</a> file for more information.</p>
</details>
<!-- markdownlint-enable MD037 -->
