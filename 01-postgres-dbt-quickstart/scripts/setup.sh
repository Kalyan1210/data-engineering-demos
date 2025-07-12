#!/bin/bash

echo "🚀 Setting up Postgres + dbt Quick-Start Demo"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Start the containers
echo "📦 Starting PostgreSQL and pgAdmin..."
docker-compose up -d

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
until docker-compose exec -T postgres pg_isready -U dbt_user -d dbt_demo; do
    sleep 2
done

echo "✅ PostgreSQL is ready!"

# Install dbt if not already installed
if ! command -v dbt &> /dev/null; then
    echo "📦 Installing dbt-postgres..."
    pip install dbt-postgres
fi

# Create profiles directory if it doesn't exist
mkdir -p ~/.dbt

# Copy profiles file
echo "⚙️ Setting up dbt profiles..."
cp profiles.yml ~/.dbt/profiles.yml

echo "🎉 Setup complete!"
echo ""
echo "📊 Access your environment:"
echo "   - PostgreSQL: localhost:5432"
echo "   - pgAdmin: http://localhost:8080 (admin@admin.com / admin)"
echo ""
echo "🚀 Run the demo:"
echo "   ./scripts/demo.sh" 