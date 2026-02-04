/**
 * Main JavaScript for Tech Investment Crawler Web Interface
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Tech Investment Crawler web interface loaded');
});

/**
 * Format date to readable string
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

/**
 * Truncate text to specified length
 */
function truncateText(text, length = 300) {
    if (!text) return '';
    return text.length > length ? text.substring(0, length) + '...' : text;
}

/**
 * Highlight search terms in text
 */
function highlightText(text, searchTerm) {
    if (!searchTerm) return text;
    
    const regex = new RegExp(`(${searchTerm})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
}

/**
 * Fetch articles from API
 */
async function fetchArticles(options = {}) {
    const {
        limit = 20,
        days = 30,
        source = null,
    } = options;

    try {
        const url = new URL('/api/articles', window.location.origin);
        url.searchParams.append('limit', limit);
        url.searchParams.append('days', days);
        if (source) url.searchParams.append('source', source);

        const response = await fetch(url);
        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || 'Failed to fetch articles');
        }

        return data.articles;
    } catch (error) {
        console.error('Error fetching articles:', error);
        throw error;
    }
}

/**
 * Search articles
 */
async function searchArticles(query) {
    if (!query || query.length < 2) {
        console.warn('Search query must be at least 2 characters');
        return [];
    }

    try {
        const url = new URL('/api/search', window.location.origin);
        url.searchParams.append('q', query);

        const response = await fetch(url);
        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || 'Search failed');
        }

        return data.articles;
    } catch (error) {
        console.error('Error searching articles:', error);
        throw error;
    }
}

/**
 * Get database statistics
 */
async function getStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || 'Failed to fetch stats');
        }

        return data;
    } catch (error) {
        console.error('Error fetching stats:', error);
        throw error;
    }
}

/**
 * Create article card HTML
 */
function createArticleCard(article) {
    const publishedDate = new Date(article.published_date).toLocaleDateString();
    const tagsHtml = article.tags && article.tags.length > 0
        ? `<div class="article-tags">${article.tags.map(tag => `<span class="tag">${tag.trim()}</span>`).join('')}</div>`
        : '';

    return `
        <div class="article-card">
            <div class="article-header">
                <h3><a href="${article.url}" target="_blank" rel="noopener noreferrer">${article.title}</a></h3>
                <span class="source-badge">${article.source}</span>
            </div>
            <p class="article-summary">${truncateText(article.summary)}</p>
            <div class="article-footer">
                <span class="article-date">${publishedDate}</span>
                ${tagsHtml}
            </div>
        </div>
    `;
}

/**
 * Update page statistics
 */
async function updateStatistics() {
    try {
        const stats = await getStats();
        
        // Update elements if they exist
        const totalElement = document.querySelector('[data-stat="total"]');
        const sourcesElement = document.querySelector('[data-stat="sources"]');

        if (totalElement) totalElement.textContent = stats.total_articles;
        if (sourcesElement) sourcesElement.textContent = stats.num_sources;

        console.log('Statistics updated:', stats);
    } catch (error) {
        console.error('Error updating statistics:', error);
    }
}

/**
 * Initialize infinite scroll
 */
function initializeInfiniteScroll(options = {}) {
    const {
        container = '#articles-container',
        pageSize = 20,
        onLoadMore = null,
    } = options;

    const element = document.querySelector(container);
    if (!element) return;

    let isLoading = false;
    let page = 1;

    window.addEventListener('scroll', async () => {
        if (isLoading) return;

        const scrollPercentage = (window.scrollY + window.innerHeight) / document.documentElement.scrollHeight;
        
        if (scrollPercentage > 0.8) {
            isLoading = true;
            page++;

            if (onLoadMore) {
                await onLoadMore(page);
            }

            isLoading = false;
        }
    });
}

/**
 * Dark mode toggle
 */
function toggleDarkMode() {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    document.documentElement.setAttribute('data-theme', isDark ? 'light' : 'dark');
    localStorage.setItem('theme', isDark ? 'light' : 'dark');
}

/**
 * Initialize dark mode from localStorage
 */
function initializeDarkMode() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

// Initialize dark mode on page load
initializeDarkMode();
