#!/bin/bash

# E-Commerce API Deployment Script
# This script automates the deployment process

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}→ $1${NC}"
}

print_header() {
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "  $1"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
}

# Check if .env file exists
check_env_file() {
    if [ ! -f .env ]; then
        print_error ".env file not found!"
        print_info "Creating .env from .env.example..."
        cp .env.example .env
        print_info "Please update .env file with your configuration"
        exit 1
    fi
    print_success ".env file found"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed!"
        exit 1
    fi
    print_success "Docker is installed"
}

# Check if Docker Compose is installed
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed!"
        exit 1
    fi
    print_success "Docker Compose is installed"
}

# Main deployment
main() {
    print_header "E-Commerce API Deployment"
    
    # Step 1: Check prerequisites
    print_info "Checking prerequisites..."
    check_docker
    check_docker_compose
    check_env_file
    
    # Step 2: Create necessary directories
    print_info "Creating necessary directories..."
    mkdir -p logs static/profile_images alembic/versions
    print_success "Directories created"
    
    # Step 3: Build Docker images
    print_header "Building Docker Images"
    print_info "This may take a few minutes..."
    docker-compose build
    print_success "Docker images built successfully"
    
    # Step 4: Start services
    print_header "Starting Services"
    docker-compose up -d db redis
    print_success "Database and Redis started"
    
    # Step 5: Wait for database to be ready
    print_info "Waiting for database to be ready..."
    sleep 10
    
    # Check database health
    if docker-compose exec -T db pg_isready -U ecommerce_user &> /dev/null; then
        print_success "Database is ready"
    else
        print_error "Database is not responding"
        exit 1
    fi
    
    # Step 6: Run migrations
    print_header "Running Database Migrations"
    
    # Start API service to run migrations
    docker-compose up -d api
    sleep 5
    
    # Run migrations
    print_info "Running Alembic migrations..."
    docker-compose exec -T api alembic upgrade head
    print_success "Migrations completed"
    
    # Step 7: Verify deployment
    print_header "Verifying Deployment"
    
    # Check if API is responding
    print_info "Checking API health..."
    sleep 5
    
    if curl -f http://localhost:8000/health &> /dev/null; then
        print_success "API is responding"
    else
        print_error "API is not responding"
        print_info "Check logs with: docker-compose logs api"
        exit 1
    fi
    
    # Step 8: Display service status
    print_header "Service Status"
    docker-compose ps
    
    # Step 9: Success message
    print_header "Deployment Successful!"
    echo ""
    echo "  🚀 Application is running!"
    echo ""
    echo "  Services:"
    echo "  • API:            http://localhost:8000"
    echo "  • Swagger Docs:   http://localhost:8000/api/docs"
    echo "  • ReDoc:          http://localhost:8000/api/redoc"
    echo "  • Health Check:   http://localhost:8000/health"
    echo ""
    echo "  Useful Commands:"
    echo "  • View logs:      docker-compose logs -f api"
    echo "  • Stop services:  docker-compose down"
    echo "  • Restart:        docker-compose restart"
    echo "  • Shell access:   docker-compose exec api bash"
    echo ""
    print_info "Create superadmin user with:"
    echo "  docker-compose exec api python create_superadmin.py"
    echo ""
}

# Cleanup function
cleanup() {
    print_header "Cleanup"
    print_info "Stopping all services..."
    docker-compose down
    print_success "All services stopped"
}

# Rollback function
rollback() {
    print_header "Rollback"
    print_info "Rolling back to previous version..."
    docker-compose exec -T api alembic downgrade -1
    docker-compose restart api
    print_success "Rollback completed"
}

# Show help
show_help() {
    echo "E-Commerce API Deployment Script"
    echo ""
    echo "Usage: ./deploy.sh [command]"
    echo ""
    echo "Commands:"
    echo "  deploy      Deploy the application (default)"
    echo "  cleanup     Stop all services and cleanup"
    echo "  rollback    Rollback database migration"
    echo "  status      Show service status"
    echo "  logs        Show application logs"
    echo "  help        Show this help message"
    echo ""
}

# Parse command line arguments
case "${1:-deploy}" in
    deploy)
        main
        ;;
    cleanup)
        cleanup
        ;;
    rollback)
        rollback
        ;;
    status)
        docker-compose ps
        ;;
    logs)
        docker-compose logs -f api
        ;;
    help)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac