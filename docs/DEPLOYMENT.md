# Deployment Guide: Todo AI Chatbot

## Backend Deployment

### Heroku Deployment

1. Create a new Heroku app:
```bash
heroku create your-app-name
```

2. Set environment variables:
```bash
heroku config:set OPENAI_API_KEY=your_openai_api_key
heroku config:set DATABASE_URL=your_database_url
heroku config:set JWT_SECRET_KEY=your_jwt_secret
```

3. Deploy:
```bash
git push heroku main
```

### AWS Elastic Beanstalk Deployment

1. Install EB CLI:
```bash
pip install awsebcli
```

2. Initialize and deploy:
```bash
eb init
eb setenv OPENAI_API_KEY=your_openai_api_key
eb setenv DATABASE_URL=your_database_url
eb setenv JWT_SECRET_KEY=your_jwt_secret
eb deploy
```

### Docker Deployment

1. Create Dockerfile:
```Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. Build and run:
```bash
docker build -t todo-chatbot-backend .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key -e DATABASE_URL=your_db todo-chatbot-backend
```

## Frontend Deployment

### Vercel Deployment

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel --env NEXT_PUBLIC_API_BASE_URL=https://your-backend-url.com
```

### Netlify Deployment

1. Create a netlify.toml file:
```toml
[build]
  publish = "out"
  command = "npm run build"

[build.environment]
  NEXT_PUBLIC_API_BASE_URL = "https://your-backend-url.com"
```

2. Deploy via Netlify dashboard or CLI.

### GitHub Pages Deployment

1. Build the app:
```bash
npm run build
```

2. Use a tool like `gh-pages` to deploy to GitHub Pages.

## Environment Variables Setup

### Backend (.env)
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `DATABASE_URL`: Database connection string (required)
- `NEON_DATABASE_URL`: Neon PostgreSQL database URL (optional, overrides DATABASE_URL)
- `JWT_SECRET_KEY`: Secret key for JWT token generation (required)
- `FRONTEND_ORIGIN`: Frontend URL for CORS configuration (required in production)

### Frontend (.env.local)
- `NEXT_PUBLIC_API_BASE_URL`: Backend API URL (required)

## Scaling Recommendations

### Database Scaling
- Use a managed PostgreSQL service like Neon, AWS RDS, or Google Cloud SQL
- Enable connection pooling for better performance
- Set up read replicas for heavy read operations

### API Scaling
- Use a load balancer for multiple backend instances
- Implement caching for frequently accessed data
- Set up CDN for static assets

### AI Service Scaling
- Monitor OpenAI API usage and costs
- Implement rate limiting to control API calls
- Consider caching responses for common queries

## Security Considerations

### Authentication
- Use strong JWT secret keys
- Implement proper token expiration
- Secure token storage in frontend

### Data Protection
- Encrypt sensitive data in transit
- Sanitize all user inputs
- Implement proper access controls

### API Security
- Implement rate limiting
- Use HTTPS in production
- Validate all API requests

## Monitoring and Logging

### Application Logs
- Log all API requests and responses
- Monitor error rates and performance
- Set up alerts for critical issues

### Database Monitoring
- Monitor query performance
- Track database connection usage
- Set up backup schedules

### AI Service Monitoring
- Track API usage and costs
- Monitor response times
- Set up alerts for quota limits

## Troubleshooting

### Common Issues

#### Issue: "OpenAI API Error"
- **Cause**: Invalid API key or rate limiting
- **Solution**: Verify your API key and check usage quotas

#### Issue: "Database Connection Error"
- **Cause**: Incorrect database URL or connection issues
- **Solution**: Verify database URL and credentials

#### Issue: "JWT Authentication Error"
- **Cause**: Invalid token or expired session
- **Solution**: Check JWT configuration and token validity

#### Issue: "CORS Error"
- **Cause**: Frontend domain not whitelisted
- **Solution**: Update FRONTEND_ORIGIN in environment variables

### Performance Issues

#### Slow Response Times
1. Check database query performance
2. Verify OpenAI API response times
3. Review server resources and load

#### High Memory Usage
1. Check for memory leaks in code
2. Optimize database queries
3. Review caching strategies

## Maintenance Tasks

### Regular Maintenance
- Update dependencies regularly
- Monitor security vulnerabilities
- Backup database regularly
- Review API usage and costs

### Updates
1. Create a staging environment for testing
2. Test all functionality after updates
3. Monitor for regressions after deployment

## Rollback Procedures

### Backend Rollback
1. Identify the problematic deployment
2. Use version control to revert changes
3. Deploy the previous stable version
4. Verify functionality after rollback

### Frontend Rollback
1. Revert to the previous build
2. Clear CDN caches if necessary
3. Verify functionality across browsers

## Disaster Recovery

### Data Loss
1. Restore from the latest backup
2. Verify data integrity
3. Notify affected users if necessary

### Service Outage
1. Check all service dependencies
2. Review error logs and metrics
3. Implement temporary fixes if possible
4. Communicate with users about the issue