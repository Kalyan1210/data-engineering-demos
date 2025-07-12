#!/bin/bash

echo "🎯 Running Postgres + dbt Quick-Start Demo"

# Check if containers are running
if ! docker-compose ps | grep -q "Up"; then
    echo "❌ Containers are not running. Run setup.sh first."
    exit 1
fi

# Initialize dbt project (if not already done)
if [ ! -f "dbt_project.yml" ]; then
    echo "📁 Initializing dbt project..."
    dbt init postgres_demo
    cp dbt_project.yml postgres_demo/
    cp profiles.yml postgres_demo/
    cp -r models postgres_demo/
    cp -r seeds postgres_demo/
    cp -r macros postgres_demo/
    cd postgres_demo
else
    cd postgres_demo
fi

echo "🌱 Seeding data..."
dbt seed

echo "🔄 Running models..."
dbt run

echo "📊 Generating documentation..."
dbt docs generate

echo "✅ Demo complete!"
echo ""
echo "📊 View your results:"
echo "   - Raw data: SELECT * FROM raw_customers;"
echo "   - Staged data: SELECT * FROM stg_customers;"
echo "   - Final data: SELECT * FROM dim_customers;"
echo ""
echo "📚 Documentation: dbt docs serve"
echo "🔍 pgAdmin: http://localhost:8080" 