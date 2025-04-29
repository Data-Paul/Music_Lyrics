FROM postgres:15-alpine

# Copy initialization script
COPY src/package/database/init.sql /docker-entrypoint-initdb.d/

# Set environment variables
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=music_db

# Expose PostgreSQL port
EXPOSE 5432 