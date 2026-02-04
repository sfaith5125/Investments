"""Flask web application for Tech Investment Crawler"""

import logging
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify
from tech_crawler.storage import Database
from tech_crawler.analysis import ArticleAnalyzer

logger = logging.getLogger(__name__)


def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['JSON_SORT_KEYS'] = False
    
    # Initialize database
    db = Database()
    analyzer = ArticleAnalyzer()
    
    @app.route('/')
    def index():
        """Home page with dashboard"""
        try:
            # Get statistics
            total_articles = db.get_article_count()
            sources = db.get_sources()
            
            # Get recent relevant articles
            recent_articles = db.get_articles(limit=10, days_back=30)
            
            # Format for display
            articles_data = []
            for article in recent_articles:
                articles_data.append({
                    'id': article.id,
                    'title': article.title,
                    'url': article.url,
                    'source': article.source,
                    'summary': article.summary[:200] + '...' if article.summary and len(article.summary) > 200 else article.summary,
                    'published_date': article.published_date.strftime('%Y-%m-%d %H:%M') if article.published_date else 'N/A',
                    'tags': article.tags.split(',') if article.tags else [],
                })
            
            return render_template(
                'index.html',
                total_articles=total_articles,
                num_sources=len(sources),
                sources=', '.join(sources),
                articles=articles_data,
            )
        except Exception as e:
            logger.error(f"Error loading dashboard: {str(e)}")
            return render_template('error.html', error=str(e)), 500
    
    @app.route('/api/articles')
    def api_articles():
        """API endpoint for articles"""
        try:
            # Get query parameters
            limit = request.args.get('limit', 20, type=int)
            days_back = request.args.get('days', 30, type=int)
            source = request.args.get('source', None)
            
            # Validate parameters
            limit = min(limit, 100)  # Max 100 per request
            
            # Query database
            articles = db.get_articles(limit=limit, days_back=days_back)
            
            # Filter by source if provided
            if source:
                articles = [a for a in articles if a.source == source]
            
            # Format response
            data = [a.to_dict() for a in articles]
            
            return jsonify({
                'success': True,
                'count': len(data),
                'articles': data,
            })
        except Exception as e:
            logger.error(f"Error fetching articles: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e),
            }), 500
    
    @app.route('/api/search')
    def api_search():
        """API endpoint for searching articles"""
        try:
            query = request.args.get('q', '').strip()
            
            if not query or len(query) < 2:
                return jsonify({
                    'success': False,
                    'error': 'Query must be at least 2 characters',
                }), 400
            
            results = db.search_articles(query)
            data = [a.to_dict() for a in results[:50]]  # Limit results
            
            return jsonify({
                'success': True,
                'count': len(data),
                'query': query,
                'articles': data,
            })
        except Exception as e:
            logger.error(f"Error searching articles: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e),
            }), 500
    
    @app.route('/api/stats')
    def api_stats():
        """API endpoint for statistics"""
        try:
            total = db.get_article_count()
            sources = db.get_sources()
            recent = db.get_articles(limit=1, days_back=0)
            
            return jsonify({
                'success': True,
                'total_articles': total,
                'num_sources': len(sources),
                'sources': sources,
                'last_crawled': recent[0].crawled_date.isoformat() if recent else None,
            })
        except Exception as e:
            logger.error(f"Error fetching stats: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e),
            }), 500
    
    @app.route('/articles')
    def articles():
        """Articles listing page"""
        try:
            sources = db.get_sources()
            return render_template('articles.html', sources=sources)
        except Exception as e:
            logger.error(f"Error loading articles page: {str(e)}")
            return render_template('error.html', error=str(e)), 500
    
    @app.route('/search')
    def search():
        """Search page"""
        query = request.args.get('q', '')
        results = []
        
        if query and len(query) >= 2:
            try:
                results = db.search_articles(query)
                results = [a.to_dict() for a in results[:50]]
            except Exception as e:
                logger.error(f"Error searching: {str(e)}")
        
        return render_template('search.html', query=query, results=results)
    
    @app.route('/article/<int:article_id>')
    def article_detail(article_id):
        """Article detail page"""
        try:
            articles = db.get_articles(limit=1)
            article = None
            
            for a in articles:
                if a.id == article_id:
                    article = a
                    break
            
            if not article:
                # Try to find in all articles with different query
                articles = db.get_articles(limit=1000)
                for a in articles:
                    if a.id == article_id:
                        article = a
                        break
            
            if not article:
                return render_template('error.html', error='Article not found'), 404
            
            return render_template(
                'article_detail.html',
                article=article.to_dict(),
                full_content=article.content or article.summary,
            )
        except Exception as e:
            logger.error(f"Error loading article: {str(e)}")
            return render_template('error.html', error=str(e)), 500
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return render_template('error.html', error='Page not found'), 404
    
    @app.errorhandler(500)
    def server_error(error):
        """Handle 500 errors"""
        return render_template('error.html', error='Internal server error'), 500
    
    return app


if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
