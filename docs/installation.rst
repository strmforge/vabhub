Installation Guide
==================

Requirements
------------

VabHub requires the following components:

- Docker and Docker Compose
- Git
- At least 4GB RAM (8GB recommended)
- 20GB free disk space for media storage

Installation Steps
------------------

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/strmforge/vabhub.git
      cd vabhub

2. Configure environment variables:

   Copy the example environment file and modify it according to your needs:

   .. code-block:: bash

      cp .env.example .env

3. Start the services:

   .. code-block:: bash

      docker-compose up -d

4. Access the services:

   - Web UI: http://localhost:3000
   - API: http://localhost:8081
   - Documentation: http://localhost:8082

Configuration
-------------

The main configuration file is `.env`. Here are the most important settings:

- `MEDIA_PATH`: Path to your media library
- `DOWNLOAD_PATH`: Path for downloaded content
- `TMDB_API_KEY`: Your TMDb API key for metadata
- `QBT_HOST`: qBittorrent host
- `QBT_USERNAME`: qBittorrent username
- `QBT_PASSWORD`: qBittorrent password

For a complete list of configuration options, see the `vabhub-Core` documentation.