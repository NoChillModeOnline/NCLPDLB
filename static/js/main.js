// Main JavaScript for Pokemon Draft League Dashboard

// Utility function to format numbers
function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

// Utility function to format percentages
function formatPercent(num) {
    return `${(num * 100).toFixed(1)}%`;
}

// Get type badge HTML
function getTypeBadge(type) {
    if (!type) return '';
    return `<span class="type-badge type-${type.toLowerCase()}">${type}</span>`;
}

// Get Pokemon type badges
function getPokemonTypes(pokemon) {
    let html = getTypeBadge(pokemon.type1);
    if (pokemon.type2) {
        html += getTypeBadge(pokemon.type2);
    }
    return html;
}

// Show toast notification
function showToast(message, type = 'info') {
    const colors = {
        info: 'bg-blue-500',
        success: 'bg-green-500',
        warning: 'bg-yellow-500',
        error: 'bg-red-500'
    };

    const toast = document.createElement('div');
    toast.className = `fixed bottom-4 right-4 ${colors[type]} text-white px-6 py-3 rounded-lg shadow-lg z-50 fade-in`;
    toast.textContent = message;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Format time ago
function timeAgo(timestamp) {
    const now = new Date();
    const then = new Date(timestamp);
    const seconds = Math.floor((now - then) / 1000);

    const intervals = {
        year: 31536000,
        month: 2592000,
        week: 604800,
        day: 86400,
        hour: 3600,
        minute: 60
    };

    for (const [unit, secondsInUnit] of Object.entries(intervals)) {
        const interval = Math.floor(seconds / secondsInUnit);
        if (interval >= 1) {
            return `${interval} ${unit}${interval > 1 ? 's' : ''} ago`;
        }
    }

    return 'just now';
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(err => {
        showToast('Failed to copy', 'error');
    });
}

// Export data as JSON
function exportData(data, filename) {
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();

    URL.revokeObjectURL(url);
    showToast('Data exported successfully!', 'success');
}

// Fetch with error handling
async function fetchAPI(endpoint) {
    try {
        const response = await fetch(endpoint);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error(`Error fetching ${endpoint}:`, error);
        showToast(`Error loading data: ${error.message}`, 'error');
        throw error;
    }
}

// Initialize tooltips (if using a library like Tippy.js)
function initTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(el => {
        el.title = el.getAttribute('data-tooltip');
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initTooltips();

    // Add smooth scroll behavior
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add fade-in animation to elements
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.card-hover').forEach(el => {
        observer.observe(el);
    });
});

// Check for updates periodically
let updateInterval;

function startAutoRefresh(callback, interval = 30000) {
    if (updateInterval) {
        clearInterval(updateInterval);
    }
    updateInterval = setInterval(callback, interval);
}

function stopAutoRefresh() {
    if (updateInterval) {
        clearInterval(updateInterval);
        updateInterval = null;
    }
}

// Handle page visibility change
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        stopAutoRefresh();
    } else {
        // Restart auto-refresh when page becomes visible
        const refreshCallback = window.currentRefreshCallback;
        if (refreshCallback) {
            startAutoRefresh(refreshCallback);
        }
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K: Focus search (if implemented)
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('input[type="search"]');
        if (searchInput) {
            searchInput.focus();
        }
    }

    // Ctrl/Cmd + /: Show keyboard shortcuts help
    if ((e.ctrlKey || e.metaKey) && e.key === '/') {
        e.preventDefault();
        showToast('Keyboard shortcuts: Ctrl+K (Search), Ctrl+R (Refresh)', 'info');
    }

    // Ctrl/Cmd + R: Refresh current page data
    if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
        const refreshCallback = window.currentRefreshCallback;
        if (refreshCallback) {
            e.preventDefault();
            refreshCallback();
            showToast('Refreshing data...', 'info');
        }
    }
});

console.log('Pokemon Draft League Dashboard initialized!');
