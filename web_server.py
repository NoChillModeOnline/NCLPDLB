"""
Web Frontend Server for Pokemon Draft League Bot

Provides a beautiful web dashboard to view:
- Live draft progress
- Team rosters and analysis
- League standings
- Tera Captain selections
- Match history

Run with: python web_server.py
Access at: http://localhost:5000
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime
from typing import Dict, List, Optional

# Import bot services
from services.sheets_service import SheetsService
from services.team_validator import TeamValidator
from config import SPREADSHEET_ID

app = Flask(__name__)
CORS(app)  # Enable CORS for API endpoints

# Initialize services
try:
    sheets = SheetsService('.credentials.json', SPREADSHEET_ID)
    validator = TeamValidator(sheets)
    print('✅ Connected to Google Sheets')
except Exception as e:
    print(f'⚠️ Warning: Could not connect to Google Sheets: {e}')
    sheets = None
    validator = None


# ==================== WEB PAGES ====================

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/draft')
def draft_page():
    """Live draft page"""
    return render_template('draft.html')

@app.route('/teams')
def teams_page():
    """Teams overview page"""
    return render_template('teams.html')

@app.route('/standings')
def standings_page():
    """League standings page"""
    return render_template('standings.html')

@app.route('/team/<player_name>')
def team_detail(player_name):
    """Individual team detail page"""
    return render_template('team_detail.html', player=player_name)


# ==================== API ENDPOINTS ====================

@app.route('/api/status')
def api_status():
    """Get bot and server status"""
    return jsonify({
        'status': 'online',
        'connected_to_sheets': sheets is not None,
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/league/info')
def api_league_info():
    """Get league information"""
    if not sheets:
        return jsonify({'error': 'Not connected to sheets'}), 503

    try:
        league_name = sheets.get_config_value('league_name', 'Pokemon Draft League')
        total_points = sheets.get_config_value('total_points', 120)
        max_pokemon = sheets.get_config_value('max_pokemon', 12)
        min_pokemon = sheets.get_config_value('min_pokemon', 10)
        max_tera = sheets.get_config_value('max_tera_captains', 3)

        return jsonify({
            'league_name': league_name,
            'total_points': total_points,
            'max_pokemon': max_pokemon,
            'min_pokemon': min_pokemon,
            'max_tera_captains': max_tera
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/teams/all')
def api_all_teams():
    """Get all teams with basic info"""
    if not sheets:
        return jsonify({'error': 'Not connected to sheets'}), 503

    try:
        teams_data = sheets.get_all_teams()

        teams = []
        for team in teams_data:
            teams.append({
                'player': team.get('Player', ''),
                'team_name': team.get('Team_Name', ''),
                'logo_url': team.get('Logo_URL', ''),
                'points_used': team.get('Points_Used', 0),
                'pokemon_count': team.get('Pokemon_Count', 0),
                'wins': team.get('Wins', 0),
                'losses': team.get('Losses', 0)
            })

        return jsonify({'teams': teams})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/team/<player_name>')
def api_team_detail(player_name):
    """Get detailed team information"""
    if not sheets or not validator:
        return jsonify({'error': 'Not connected to sheets'}), 503

    try:
        # Get team roster
        roster = sheets.get_team_roster(player_name)

        # Get Tera Captains
        tera_captains = sheets.get_tera_captains(player_name)

        # Get team analysis
        analysis = validator.analyze_team(player_name)

        return jsonify({
            'player': player_name,
            'roster': roster,
            'tera_captains': tera_captains,
            'analysis': {
                'efficiency_score': analysis.get('efficiency_score', 0),
                'type_coverage': analysis.get('type_coverage', {}),
                'weaknesses': analysis.get('weaknesses', []),
                'strengths': analysis.get('strengths', []),
                'warnings': analysis.get('warnings', []),
                'speed_tiers': analysis.get('speed_tiers', {}),
                'tera_suggestions': analysis.get('tera_suggestions', [])
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/draft/status')
def api_draft_status():
    """Get current draft status"""
    if not sheets:
        return jsonify({'error': 'Not connected to sheets'}), 503

    try:
        draft_active = sheets.get_config_value('draft_active', False)
        current_pick = sheets.get_config_value('current_pick', 0)
        total_rounds = sheets.get_config_value('draft_rounds', 10)

        # Get draft history
        history = sheets.get_draft_history()

        return jsonify({
            'active': draft_active,
            'current_pick': current_pick,
            'total_rounds': total_rounds,
            'picks_made': len(history),
            'recent_picks': history[-10:] if history else []
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/standings')
def api_standings():
    """Get league standings"""
    if not sheets:
        return jsonify({'error': 'Not connected to sheets'}), 503

    try:
        standings = sheets.get_standings()

        # Sort by wins (descending), then losses (ascending)
        standings_sorted = sorted(
            standings,
            key=lambda x: (x.get('Wins', 0), -x.get('Losses', 0)),
            reverse=True
        )

        return jsonify({'standings': standings_sorted})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pokemon/available')
def api_available_pokemon():
    """Get list of available Pokemon"""
    if not sheets:
        return jsonify({'error': 'Not connected to sheets'}), 503

    try:
        all_pokemon = sheets.get_all_pokemon()
        drafted = sheets.get_drafted_pokemon()

        available = [
            p for p in all_pokemon
            if p.get('Name') not in drafted
        ]

        return jsonify({
            'available': available,
            'total': len(all_pokemon),
            'drafted': len(drafted),
            'remaining': len(available)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats/summary')
def api_stats_summary():
    """Get league statistics summary"""
    if not sheets:
        return jsonify({'error': 'Not connected to sheets'}), 503

    try:
        teams = sheets.get_all_teams()
        pokemon_list = sheets.get_all_pokemon()

        total_teams = len(teams)
        total_pokemon = len(pokemon_list)
        total_matches = sum(team.get('Wins', 0) + team.get('Losses', 0) for team in teams) // 2

        return jsonify({
            'total_teams': total_teams,
            'total_pokemon': total_pokemon,
            'total_matches': total_matches,
            'avg_team_size': sum(team.get('Pokemon_Count', 0) for team in teams) / total_teams if total_teams > 0 else 0
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500


# ==================== MAIN ====================

def main():
    """Start the web server"""
    print('\n' + '='*60)
    print('  POKEMON DRAFT LEAGUE - WEB DASHBOARD')
    print('='*60)
    print()
    print('🌐 Starting web server...')
    print()
    print('📊 Dashboard will be available at:')
    print('   http://localhost:5000')
    print()
    print('📄 Available pages:')
    print('   / - Main Dashboard')
    print('   /draft - Live Draft View')
    print('   /teams - Teams Overview')
    print('   /standings - League Standings')
    print('   /team/<player> - Team Details')
    print()
    print('🔌 API Endpoints:')
    print('   /api/status - Server status')
    print('   /api/league/info - League info')
    print('   /api/teams/all - All teams')
    print('   /api/team/<player> - Team details')
    print('   /api/draft/status - Draft status')
    print('   /api/standings - Standings')
    print('   /api/pokemon/available - Available Pokemon')
    print('   /api/stats/summary - Statistics')
    print()
    print('='*60)
    print('✅ Server ready! Press Ctrl+C to stop.')
    print('='*60)
    print()

    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()
