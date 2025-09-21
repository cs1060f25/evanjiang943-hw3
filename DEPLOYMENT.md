# 🚀 Vercel Deployment Guide

This guide will help you deploy your AI-Assisted Grading Platform to Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI**: Install globally with `npm install -g vercel`
3. **Git Repository**: Your code should be pushed to GitHub

## Quick Deployment

### Option 1: Using the Deploy Script (Recommended)

```bash
# Make the script executable
chmod +x deploy.sh

# Run the deployment script
./deploy.sh
```

### Option 2: Manual Deployment

```bash
# Install dependencies
npm run install:all

# Build the project
npm run build

# Deploy to Vercel
vercel --prod
```

## Project Structure for Vercel

```
ai-grading-platform/
├── vercel.json              # Vercel configuration
├── package.json             # Root package.json
├── requirements.txt         # Python dependencies
├── api/
│   └── grade.py            # Serverless API function
├── frontend/
│   ├── src/                # React source code
│   ├── dist/               # Built frontend (generated)
│   └── package.json        # Frontend dependencies
└── deploy.sh               # Deployment script
```

## Configuration Details

### vercel.json
- **Framework**: Vite (React)
- **Build Command**: `cd frontend && npm install && npm run build`
- **Output Directory**: `frontend/dist`
- **API Functions**: Python 3.9 runtime
- **CORS**: Configured for all origins
- **Routing**: API calls go to `/api/*`, everything else to React app

### API Endpoints
- `GET /api/submissions` - Get all student submissions
- `GET /api/submissions/{id}` - Get specific submission
- `POST /api/grade` - Grade uploaded submission
- `POST /api/submissions/{id}/grade` - Grade existing submission
- `POST /api/submissions/{id}/release` - Release grades to student

## Environment Variables

No environment variables are required for this deployment. All data is mock data.

## Troubleshooting

### Common Issues

1. **Build Fails**: Make sure all dependencies are installed
   ```bash
   npm run install:all
   ```

2. **API Not Working**: Check that the `api/` directory is in the root
   ```bash
   ls -la api/
   ```

3. **CORS Errors**: The vercel.json includes CORS headers, but if you still see issues, check the browser console

4. **Frontend Not Loading**: Ensure the build output is in `frontend/dist/`
   ```bash
   ls -la frontend/dist/
   ```

### Debugging

1. **Check Vercel Logs**:
   ```bash
   vercel logs
   ```

2. **Test API Locally**:
   ```bash
   vercel dev
   ```

3. **Check Build Output**:
   ```bash
   npm run build
   ls -la frontend/dist/
   ```

## Post-Deployment

After successful deployment:

1. **Test the Application**: Visit your Vercel URL
2. **Test All Features**:
   - Login as TA
   - View submissions
   - Grade a submission
   - Review and edit grades
   - Release grades
   - View student feedback

3. **Update README**: Update the deployment URL in your README.md

## Custom Domain (Optional)

1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings > Domains
4. Add your custom domain
5. Follow the DNS configuration instructions

## Performance Optimization

- **Static Assets**: Vercel automatically optimizes images and assets
- **Caching**: API responses are cached by Vercel's CDN
- **Edge Functions**: Consider moving to Edge Runtime for better performance

## Monitoring

- **Analytics**: Enable Vercel Analytics in your dashboard
- **Error Tracking**: Monitor errors in the Vercel dashboard
- **Performance**: Use Vercel's built-in performance monitoring

## Support

- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **Community**: [vercel.com/community](https://vercel.com/community)
- **GitHub Issues**: Create an issue in your repository
