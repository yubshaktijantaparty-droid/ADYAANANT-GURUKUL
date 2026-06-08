// ===============================================
// ADYAANANT GURUKUL - LIVE LEADERBOARD
// Frontend JavaScript - Live Data Polling
// ===============================================

class LeaderboardManager {
    constructor() {
        this.apiEndpoint = this.getApiEndpoint();
        this.pollingInterval = 5000; // 5 seconds
        this.pollTimer = null;
        this.lastUpdate = null;
        this.isLive = false;
        this.init();
    }

    getApiEndpoint() {
        const hostname = window.location.hostname;
        const port = window.location.port;
        const isDev = hostname === 'localhost' || hostname === '127.0.0.1';

        if (isDev) {
            // When the frontend is served separately on port 8001,
            // use the backend API on port 8000.
            if (port === '8001') {
                return 'http://127.0.0.1:8000/api';
            }

            // When the backend serves the frontend directly, use relative API path.
            return '/api';
        }

        // Production endpoint (Railway)
        return 'https://your-railway-app.up.railway.app/api';
    }

    init() {
        this.setupEventListeners();
        
        // Only initialize if on leaderboard page
        if (document.getElementById('leaderboard-table')) {
            this.startPolling();
            this.updateTimestamp();
            
            // Update timestamp every second
            setInterval(() => this.updateTimestamp(), 1000);
        }
    }

    setupEventListeners() {
        // Reload data when page becomes visible
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                this.fetchLeaderboard();
            }
        });
    }

    startPolling() {
        // Initial fetch
        this.fetchLeaderboard();
        
        // Start polling
        this.pollTimer = setInterval(() => {
            this.fetchLeaderboard();
        }, this.pollingInterval);
    }

    stopPolling() {
        if (this.pollTimer) {
            clearInterval(this.pollTimer);
            this.pollTimer = null;
        }
    }

    async fetchLeaderboard() {
        try {
            this.setConnectionStatus(false, 'Connecting...');
            
            const response = await fetch(`${this.apiEndpoint}/leaderboard`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                mode: 'cors',
                credentials: 'omit'
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.success) {
                this.lastUpdate = new Date(data.generated_at);
                this.displayLeaderboard(data);
                this.setConnectionStatus(true, 'Live');
                this.isLive = true;
            } else {
                this.handleError('API returned unsuccessful response');
            }
        } catch (error) {
            console.error('Error fetching leaderboard:', error);
            this.handleError(error.message);
            this.setConnectionStatus(false, 'Offline');
            this.isLive = false;
        }
    }

    displayLeaderboard(data) {
        const tbody = document.getElementById('leaderboard-tbody');
        const activeCount = document.getElementById('active-count');
        const noDataDiv = document.getElementById('no-data');
        const podiumSection = document.getElementById('podium-section');
        const leaderboard = data.leaderboard || [];

        // Update active members count
        if (activeCount) {
            activeCount.textContent = data.active_members || 0;
        }

        // Handle empty leaderboard
        if (!leaderboard || leaderboard.length === 0) {
            tbody.innerHTML = '';
            if (noDataDiv) {
                noDataDiv.style.display = 'block';
            }
            if (podiumSection) {
                podiumSection.style.display = 'none';
            }
            return;
        }

        if (noDataDiv) {
            noDataDiv.style.display = 'none';
        }

        // Display podium for top 3
        if (leaderboard.length >= 1 && podiumSection) {
            this.displayPodium(leaderboard.slice(0, 3));
            podiumSection.style.display = 'block';
        }

        // Display full leaderboard table
        this.displayTable(leaderboard);
    }

    displayPodium(topThree) {
        const podiumPositions = [1, 2, 3];
        
        topThree.forEach((member, index) => {
            const position = podiumPositions[index];
            const podiumCard = document.getElementById(`podium-${position}`);
            
            if (podiumCard) {
                const medalsMap = { 1: '🥇', 2: '🥈', 3: '🥉' };
                const ranksMap = { 1: '1st', 2: '2nd', 3: '3rd' };
                
                podiumCard.querySelector('.medal').textContent = medalsMap[position];
                podiumCard.querySelector('.podium-rank').textContent = ranksMap[position];
                podiumCard.querySelector('.podium-name').textContent = member.name;
                podiumCard.querySelector('.podium-points').textContent = 
                    `${member.total_points} pts`;
            }
        });
    }

    displayTable(leaderboard) {
        const tbody = document.getElementById('leaderboard-tbody');
        
        if (tbody) {
            tbody.innerHTML = leaderboard.map((member, index) => `
                <tr class="leaderboard-row" data-rank="${index + 1}">
                    <td class="rank-col">#${index + 1}</td>
                    <td class="name-col">${this.escapeHtml(member.name)}</td>
                    <td class="cam-on-col">${member.cam_on_minutes}</td>
                    <td class="cam-off-col">${member.cam_off_minutes}</td>
                    <td class="msg-col">${member.message_count}</td>
                    <td class="points-col">${member.total_points}</td>
                </tr>
            `).join('');
        }
    }

    updateTimestamp() {
        const lastUpdatedSpan = document.getElementById('last-updated');
        
        if (lastUpdatedSpan && this.lastUpdate) {
            const hours = String(this.lastUpdate.getHours()).padStart(2, '0');
            const minutes = String(this.lastUpdate.getMinutes()).padStart(2, '0');
            const seconds = String(this.lastUpdate.getSeconds()).padStart(2, '0');
            
            lastUpdatedSpan.textContent = `${hours}:${minutes}:${seconds}`;
        }
    }

    setConnectionStatus(online, text) {
        const indicator = document.getElementById('status-indicator');
        const statusText = document.getElementById('status-text');
        const refreshIndicator = document.getElementById('refresh-indicator');

        if (indicator) {
            indicator.classList.remove('online', 'offline');
            indicator.classList.add(online ? 'online' : 'offline');
        }

        if (statusText) {
            statusText.textContent = text;
        }

        if (refreshIndicator) {
            if (online && this.isLive) {
                refreshIndicator.textContent = '🔄 Live';
                refreshIndicator.style.color = 'var(--color-success)';
            } else {
                refreshIndicator.textContent = '⏳ Connecting...';
                refreshIndicator.style.color = 'var(--color-text-muted)';
            }
        }
    }

    handleError(errorMessage) {
        console.error('Leaderboard Error:', errorMessage);
        
        const tbody = document.getElementById('leaderboard-tbody');
        if (tbody) {
            tbody.innerHTML = `
                <tr class="error-row">
                    <td colspan="6" style="text-align: center; padding: 2rem; color: #ef4444;">
                        ⚠️ Error loading leaderboard: ${this.escapeHtml(errorMessage)}
                    </td>
                </tr>
            `;
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    destroy() {
        this.stopPolling();
    }
}

// Initialize leaderboard manager
let leaderboardManager;

document.addEventListener('DOMContentLoaded', () => {
    leaderboardManager = new LeaderboardManager();
});

// Cleanup on page unload
window.addEventListener('unload', () => {
    if (leaderboardManager) {
        leaderboardManager.destroy();
    }
});
