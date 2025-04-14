# Inventory Tracking System

A scalable, real-time inventory management system designed to handle thousands of stores with concurrent operations and audit logging.

## Objectives

1. **Scalability**
   - Support thousands of stores
   - Handle concurrent operations
   - Ensure horizontal scalability
   - Maintain performance under heavy load

2. **Real-time Operations**
   - Near real-time stock synchronization
   - Immediate audit logging
   - Event-driven updates
   - Asynchronous processing

3. **Reliability**
   - Data consistency
   - Fault tolerance
   - Backup and recovery
   - Transaction management

4. **Security**
   - Authentication and authorization
   - Audit logging
   - Rate limiting
   - Data validation

## Assumptions

1. **System Scale**
   - Expected to handle 1000+ stores
   - Support 100+ concurrent users
   - Process 1000+ stock updates per minute
   - Store 1M+ audit logs

2. **Performance Requirements**
   - API response time < 500ms
   - Stock sync delay < 5 seconds
   - 99.9% uptime
   - Handle peak loads efficiently

3. **Data Requirements**
   - PostgreSQL as primary database
   - Redis for caching and messaging
   - Regular backup requirements
   - Data retention policies

4. **Security Requirements**
   - Basic authentication
   - Rate limiting
   - Audit trail
   - Data validation

## Technology Stack

### Backend
- **Framework**: Django 5.2
- **Database**: PostgreSQL
- **Cache**: Redis
- **Task Queue**: Celery
- **API**: Django REST Framework

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Kubernetes (optional)
- **Monitoring**: Prometheus + Grafana (optional)
- **CI/CD**: GitHub Actions (optional)

## Solution Architecture

### 1. Database Layer
- Primary/Replica setup for read/write separation
- Connection pooling
- Transaction management
- Efficient indexing

### 2. Caching Layer
- Redis for caching
- View-level caching
- Cache invalidation
- Session storage

### 3. Application Layer
- Django REST Framework
- Rate limiting
- Authentication
- API endpoints

### 4. Background Processing
- Celery workers
- Task queues
- Scheduled tasks
- Event handling

### 5. Monitoring and Logging
- Audit logging
- Performance monitoring
- Error tracking
- System health checks

## Implementation Details

### Database Configuration
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'inventory_tracker'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    },
    'read_replica': {
        # Similar configuration for read replica
    }
}
```

### Caching Configuration
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_CACHE_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'RETRY_ON_TIMEOUT': True,
            'MAX_CONNECTIONS': 1000,
        }
    }
}
```

### Rate Limiting
```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
        'stock_updates': '100/minute',
        'audit_logs': '50/minute',
        'store_operations': '200/minute',
    }
}
```

## Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL
- Redis
- Celery

### Installation
1. Clone the repository
2. Create virtual environment
3. Install dependencies
4. Configure environment variables
5. Run migrations
6. Start services

### Running the Application
```bash
# Start PostgreSQL
docker run --name postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=inventory_tracker -p 5432:5432 -d postgres

# Start Redis
docker run --name redis -p 6379:6379 -d redis

# Start Celery worker
celery -A InventoryTrackerPhase1 worker -l info

# Start Celery beat
celery -A InventoryTrackerPhase1 beat -l info

# Run Django server
python manage.py runserver
```

## API Endpoints

### Stores
- `GET /api/stores/` - List all stores
- `POST /api/stores/` - Create new store
- `GET /api/stores/{id}/` - Get store details

### Products
- `GET /api/products/` - List all products
- `POST /api/products/` - Create new product
- `GET /api/products/{id}/` - Get product details
- `POST /api/products/{id}/stock_in/` - Update stock

### Audit Logs
- `GET /api/audit-logs/` - List audit logs
- `GET /api/audit-logs/{id}/` - Get audit log details

## Monitoring and Maintenance

### Performance Monitoring
- Redis cache usage
- Database connection pool
- API response times
- Celery task queue

### Maintenance Tasks
- Regular backups
- Cache cleanup
- Log rotation
- Database optimization

## Future Enhancements

1. **Scalability**
   - Kubernetes deployment
   - Auto-scaling
   - Load balancing

2. **Features**
   - Advanced reporting
   - Predictive analytics
   - Mobile app integration

3. **Security**
   - JWT authentication
   - API key management
   - Enhanced encryption

4. **Monitoring**
   - Advanced logging
   - Real-time alerts
   - Performance metrics

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Syed Muqeet Ur Rehman (muqeet007)