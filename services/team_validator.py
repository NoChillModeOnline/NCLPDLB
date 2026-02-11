"""
Team Validator Service

Provides comprehensive team validation and analysis:
- Type coverage analysis
- Weakness identification
- Offensive coverage gaps
- Defensive synergy
- Tera Captain optimization suggestions
- Point budget efficiency
"""

from typing import Dict, List, Set, Tuple
from collections import defaultdict
from utils.constants import VALID_TERA_TYPES, TYPE_CHART


class TeamValidator:
    """Validates and analyzes team composition for strategic insights"""

    def __init__(self, sheets_service):
        self.sheets = sheets_service

    def analyze_team(self, player: str) -> Dict:
        """
        Comprehensive team analysis

        Returns:
            {
                'team_data': {...},
                'type_coverage': {...},
                'weaknesses': {...},
                'offensive_coverage': {...},
                'defensive_synergy': {...},
                'tera_suggestions': [...],
                'efficiency_score': float,
                'warnings': [...],
                'strengths': [...]
            }
        """
        # Get team data
        team_data = self.sheets.get_team_by_player(player)
        if not team_data:
            return {'error': 'Team not found'}

        pokemon_list = team_data.get('pokemon_list', [])
        if not pokemon_list:
            return {'error': 'No Pokémon on team'}

        # Get detailed Pokémon data
        team_pokemon = []
        for pkmn_name in pokemon_list:
            pkmn_data = self.sheets.get_pokemon_data(pkmn_name)
            if pkmn_data:
                team_pokemon.append(pkmn_data)

        # Perform all analyses
        analysis = {
            'team_data': team_data,
            'pokemon_count': len(team_pokemon),
            'type_coverage': self._analyze_type_coverage(team_pokemon),
            'weaknesses': self._analyze_weaknesses(team_pokemon),
            'offensive_coverage': self._analyze_offensive_coverage(team_pokemon),
            'defensive_synergy': self._analyze_defensive_synergy(team_pokemon),
            'tera_suggestions': self._suggest_tera_types(team_pokemon, player),
            'speed_tiers': self._analyze_speed_tiers(team_pokemon),
            'stat_distribution': self._analyze_stat_distribution(team_pokemon),
            'efficiency_score': self._calculate_efficiency_score(team_data, team_pokemon),
            'warnings': [],
            'strengths': []
        }

        # Add warnings and strengths
        analysis['warnings'] = self._generate_warnings(analysis)
        analysis['strengths'] = self._generate_strengths(analysis)

        return analysis

    def _analyze_type_coverage(self, team_pokemon: List[Dict]) -> Dict:
        """Analyze type representation on the team"""
        type_counts = defaultdict(int)
        dual_types = []

        for pkmn in team_pokemon:
            type1 = pkmn.get('type1', '').title()
            type2 = pkmn.get('type2', '').title()

            if type1:
                type_counts[type1] += 1
            if type2:
                type_counts[type2] += 1
                dual_types.append(f"{type1}/{type2}")

        # Find missing types
        all_types = set(VALID_TERA_TYPES) - {'Stellar'}
        represented_types = set(type_counts.keys())
        missing_types = all_types - represented_types

        # Find over-represented types
        over_represented = {t: c for t, c in type_counts.items() if c >= 3}

        return {
            'type_counts': dict(type_counts),
            'dual_types': dual_types,
            'missing_types': list(missing_types),
            'over_represented': over_represented,
            'total_unique_types': len(represented_types)
        }

    def _analyze_weaknesses(self, team_pokemon: List[Dict]) -> Dict:
        """Identify common weaknesses across the team"""
        weakness_counts = defaultdict(int)
        pokemon_weaknesses = {}

        for pkmn in team_pokemon:
            name = pkmn.get('name', 'Unknown')
            type1 = pkmn.get('type1', '').title()
            type2 = pkmn.get('type2', '').title()

            weaknesses = self._get_type_weaknesses(type1, type2)
            pokemon_weaknesses[name] = weaknesses

            for weakness in weaknesses:
                weakness_counts[weakness] += 1

        # Find critical weaknesses (affects 4+ Pokémon)
        critical_weaknesses = {
            w: c for w, c in weakness_counts.items() if c >= 4
        }

        # Find shared weaknesses (affects 50%+ of team)
        team_size = len(team_pokemon)
        shared_weaknesses = {
            w: c for w, c in weakness_counts.items()
            if c >= team_size / 2
        }

        return {
            'weakness_counts': dict(weakness_counts),
            'pokemon_weaknesses': pokemon_weaknesses,
            'critical_weaknesses': critical_weaknesses,
            'shared_weaknesses': shared_weaknesses
        }

    def _analyze_offensive_coverage(self, team_pokemon: List[Dict]) -> Dict:
        """Analyze offensive type coverage (what types can the team hit super-effectively)"""
        offensive_types = set()
        coverage_gaps = []

        # Collect all offensive types on team
        for pkmn in team_pokemon:
            type1 = pkmn.get('type1', '').title()
            type2 = pkmn.get('type2', '').title()

            if type1:
                offensive_types.add(type1)
            if type2:
                offensive_types.add(type2)

        # Check coverage against all types
        all_types = set(VALID_TERA_TYPES) - {'Stellar'}
        coverage_matrix = defaultdict(list)

        for target_type in all_types:
            super_effective_against = []

            for offensive_type in offensive_types:
                effectiveness = self._get_type_effectiveness(offensive_type, target_type)
                if effectiveness > 1.0:
                    super_effective_against.append(offensive_type)

            if super_effective_against:
                coverage_matrix[target_type] = super_effective_against
            else:
                coverage_gaps.append(target_type)

        return {
            'offensive_types': list(offensive_types),
            'coverage_matrix': dict(coverage_matrix),
            'coverage_gaps': coverage_gaps,
            'coverage_percentage': ((len(all_types) - len(coverage_gaps)) / len(all_types)) * 100
        }

    def _analyze_defensive_synergy(self, team_pokemon: List[Dict]) -> Dict:
        """Analyze defensive synergy and resistances"""
        resistance_counts = defaultdict(int)
        immunity_counts = defaultdict(int)

        for pkmn in team_pokemon:
            type1 = pkmn.get('type1', '').title()
            type2 = pkmn.get('type2', '').title()

            resistances, immunities = self._get_type_resistances(type1, type2)

            for resistance in resistances:
                resistance_counts[resistance] += 1

            for immunity in immunities:
                immunity_counts[immunity] += 1

        # Find strong defensive cores (types resisted by 3+ Pokémon)
        defensive_cores = {
            t: c for t, c in resistance_counts.items() if c >= 3
        }

        return {
            'resistance_counts': dict(resistance_counts),
            'immunity_counts': dict(immunity_counts),
            'defensive_cores': defensive_cores,
            'total_resistances': sum(resistance_counts.values()),
            'total_immunities': sum(immunity_counts.values())
        }

    def _suggest_tera_types(self, team_pokemon: List[Dict], player: str) -> List[Dict]:
        """Suggest optimal Tera types based on team analysis"""
        suggestions = []

        # Get current Tera Captains
        current_teras = self.sheets.get_tera_captains(player)

        # Get team weaknesses
        team_types = []
        for pkmn in team_pokemon:
            type1 = pkmn.get('type1', '').title()
            type2 = pkmn.get('type2', '').title()
            team_types.append((type1, type2 if type2 else None))

        # Find common weaknesses to cover
        weakness_counts = defaultdict(int)
        for type1, type2 in team_types:
            weaknesses = self._get_type_weaknesses(type1, type2)
            for w in weaknesses:
                weakness_counts[w] += 1

        # Sort by most common weaknesses
        sorted_weaknesses = sorted(weakness_counts.items(), key=lambda x: x[1], reverse=True)

        # Suggest Tera types to cover top 3 weaknesses
        for weakness_type, count in sorted_weaknesses[:3]:
            # Find types that resist this weakness
            resisting_types = self._find_resisting_types(weakness_type)

            suggestions.append({
                'covers_weakness': weakness_type,
                'affects_pokemon': count,
                'suggested_tera_types': resisting_types[:3],
                'priority': 'HIGH' if count >= 4 else 'MEDIUM' if count >= 2 else 'LOW'
            })

        return suggestions

    def _analyze_speed_tiers(self, team_pokemon: List[Dict]) -> Dict:
        """Analyze speed distribution on the team"""
        speed_tiers = {
            'fast': [],      # Speed >= 100
            'medium': [],    # Speed 60-99
            'slow': []       # Speed < 60
        }

        for pkmn in team_pokemon:
            name = pkmn.get('name', 'Unknown')
            speed = pkmn.get('speed', 0)

            if speed >= 100:
                speed_tiers['fast'].append((name, speed))
            elif speed >= 60:
                speed_tiers['medium'].append((name, speed))
            else:
                speed_tiers['slow'].append((name, speed))

        # Sort by speed within each tier
        for tier in speed_tiers.values():
            tier.sort(key=lambda x: x[1], reverse=True)

        avg_speed = sum(p.get('speed', 0) for p in team_pokemon) / len(team_pokemon)

        return {
            'tiers': speed_tiers,
            'average_speed': round(avg_speed, 1),
            'fastest': max((p.get('name', 'Unknown'), p.get('speed', 0)) for p in team_pokemon),
            'slowest': min((p.get('name', 'Unknown'), p.get('speed', 0)) for p in team_pokemon),
            'speed_balance': len(speed_tiers['fast']) / len(team_pokemon)
        }

    def _analyze_stat_distribution(self, team_pokemon: List[Dict]) -> Dict:
        """Analyze overall stat distribution (physical vs special, bulk, etc.)"""
        total_attack = 0
        total_sp_attack = 0
        total_defense = 0
        total_sp_defense = 0
        total_hp = 0

        physical_attackers = []
        special_attackers = []
        mixed_attackers = []
        tanks = []

        for pkmn in team_pokemon:
            name = pkmn.get('name', 'Unknown')
            attack = pkmn.get('attack', 0)
            sp_attack = pkmn.get('sp_attack', 0)
            defense = pkmn.get('defense', 0)
            sp_defense = pkmn.get('sp_defense', 0)
            hp = pkmn.get('hp', 0)

            total_attack += attack
            total_sp_attack += sp_attack
            total_defense += defense
            total_sp_defense += sp_defense
            total_hp += hp

            # Categorize by offensive stats
            if attack >= 100 and sp_attack < 80:
                physical_attackers.append(name)
            elif sp_attack >= 100 and attack < 80:
                special_attackers.append(name)
            elif attack >= 90 and sp_attack >= 90:
                mixed_attackers.append(name)

            # Categorize by defensive stats
            if defense >= 90 and sp_defense >= 90:
                tanks.append(name)

        team_size = len(team_pokemon)

        return {
            'avg_attack': round(total_attack / team_size, 1),
            'avg_sp_attack': round(total_sp_attack / team_size, 1),
            'avg_defense': round(total_defense / team_size, 1),
            'avg_sp_defense': round(total_sp_defense / team_size, 1),
            'avg_hp': round(total_hp / team_size, 1),
            'physical_attackers': physical_attackers,
            'special_attackers': special_attackers,
            'mixed_attackers': mixed_attackers,
            'tanks': tanks,
            'offensive_balance': total_attack / (total_attack + total_sp_attack) if (total_attack + total_sp_attack) > 0 else 0.5
        }

    def _calculate_efficiency_score(self, team_data: Dict, team_pokemon: List[Dict]) -> float:
        """
        Calculate team efficiency score (0-100)
        Based on: point usage, type coverage, weakness management, stat balance
        """
        score = 0.0

        # Point usage efficiency (0-25 points)
        total_points = team_data.get('total_points_used', 0)
        point_efficiency = (total_points / 120) * 25
        score += point_efficiency

        # Type coverage (0-25 points)
        offensive_types = set()
        for pkmn in team_pokemon:
            type1 = pkmn.get('type1', '').title()
            type2 = pkmn.get('type2', '').title()
            if type1:
                offensive_types.add(type1)
            if type2:
                offensive_types.add(type2)

        type_coverage = (len(offensive_types) / 18) * 25  # 18 standard types
        score += type_coverage

        # Weakness management (0-25 points)
        weakness_counts = defaultdict(int)
        for pkmn in team_pokemon:
            type1 = pkmn.get('type1', '').title()
            type2 = pkmn.get('type2', '').title()
            weaknesses = self._get_type_weaknesses(type1, type2)
            for w in weaknesses:
                weakness_counts[w] += 1

        # Penalize shared weaknesses
        max_weakness = max(weakness_counts.values()) if weakness_counts else 0
        weakness_score = max(0, 25 - (max_weakness * 3))
        score += weakness_score

        # Stat balance (0-25 points)
        has_physical = any(p.get('attack', 0) >= 100 for p in team_pokemon)
        has_special = any(p.get('sp_attack', 0) >= 100 for p in team_pokemon)
        has_tank = any(p.get('defense', 0) >= 90 and p.get('sp_defense', 0) >= 90 for p in team_pokemon)
        has_speed = any(p.get('speed', 0) >= 100 for p in team_pokemon)

        balance_score = 0
        if has_physical:
            balance_score += 6.25
        if has_special:
            balance_score += 6.25
        if has_tank:
            balance_score += 6.25
        if has_speed:
            balance_score += 6.25

        score += balance_score

        return round(score, 1)

    def _generate_warnings(self, analysis: Dict) -> List[str]:
        """Generate warnings based on analysis"""
        warnings = []

        # Check for critical weaknesses
        critical_weaknesses = analysis['weaknesses'].get('critical_weaknesses', {})
        if critical_weaknesses:
            for weakness_type, count in critical_weaknesses.items():
                warnings.append(f"⚠️ {count} Pokémon weak to {weakness_type} - consider Tera types to cover this")

        # Check for offensive coverage gaps
        coverage_gaps = analysis['offensive_coverage'].get('coverage_gaps', [])
        if len(coverage_gaps) >= 5:
            warnings.append(f"⚠️ Limited offensive coverage - cannot hit {len(coverage_gaps)} types super-effectively")

        # Check for speed issues
        speed_tiers = analysis['speed_tiers'].get('tiers', {})
        if len(speed_tiers.get('fast', [])) == 0:
            warnings.append("⚠️ No fast Pokémon (Speed ≥ 100) - may struggle with speed control")

        # Check for defensive issues
        if len(speed_tiers.get('slow', [])) >= 6 and not analysis['stat_distribution'].get('tanks'):
            warnings.append("⚠️ Many slow Pokémon without defensive bulk - may be vulnerable")

        # Check team size
        pokemon_count = analysis.get('pokemon_count', 0)
        if pokemon_count < 10:
            warnings.append(f"⚠️ Only {pokemon_count} Pokémon - minimum is 10")

        # Check point efficiency
        efficiency = analysis.get('efficiency_score', 0)
        if efficiency < 60:
            warnings.append(f"⚠️ Low team efficiency ({efficiency}/100) - consider optimizing team composition")

        return warnings

    def _generate_strengths(self, analysis: Dict) -> List[str]:
        """Generate strengths based on analysis"""
        strengths = []

        # Check type coverage
        coverage_pct = analysis['offensive_coverage'].get('coverage_percentage', 0)
        if coverage_pct >= 80:
            strengths.append(f"✅ Excellent type coverage ({coverage_pct:.0f}% of types covered)")

        # Check defensive cores
        defensive_cores = analysis['defensive_synergy'].get('defensive_cores', {})
        if len(defensive_cores) >= 3:
            strengths.append(f"✅ Strong defensive synergy - {len(defensive_cores)} types well-resisted")

        # Check speed control
        speed_tiers = analysis['speed_tiers'].get('tiers', {})
        if len(speed_tiers.get('fast', [])) >= 3:
            strengths.append(f"✅ Good speed control - {len(speed_tiers['fast'])} fast Pokémon")

        # Check stat balance
        stat_dist = analysis['stat_distribution']
        if stat_dist.get('physical_attackers') and stat_dist.get('special_attackers'):
            strengths.append("✅ Balanced offensive threats (physical + special)")

        # Check efficiency
        efficiency = analysis.get('efficiency_score', 0)
        if efficiency >= 80:
            strengths.append(f"✅ High team efficiency ({efficiency}/100)")

        # Check unique types
        type_coverage = analysis['type_coverage']
        if type_coverage.get('total_unique_types', 0) >= 10:
            strengths.append(f"✅ Diverse type representation ({type_coverage['total_unique_types']} unique types)")

        return strengths

    # ============================================================================
    # Type Chart Helper Methods
    # ============================================================================

    def _get_type_weaknesses(self, type1: str, type2: str = None) -> List[str]:
        """Get weaknesses for a type combination"""
        if not type1:
            return []

        weaknesses = set()

        # Get weaknesses from TYPE_CHART
        for attacking_type, matchups in TYPE_CHART.items():
            effectiveness1 = matchups.get(type1, 1.0)
            effectiveness2 = matchups.get(type2, 1.0) if type2 else 1.0

            combined_effectiveness = effectiveness1 * effectiveness2

            if combined_effectiveness > 1.0:
                weaknesses.add(attacking_type)

        return list(weaknesses)

    def _get_type_resistances(self, type1: str, type2: str = None) -> Tuple[List[str], List[str]]:
        """Get resistances and immunities for a type combination"""
        if not type1:
            return [], []

        resistances = set()
        immunities = set()

        # Get resistances and immunities from TYPE_CHART
        for attacking_type, matchups in TYPE_CHART.items():
            effectiveness1 = matchups.get(type1, 1.0)
            effectiveness2 = matchups.get(type2, 1.0) if type2 else 1.0

            combined_effectiveness = effectiveness1 * effectiveness2

            if combined_effectiveness == 0:
                immunities.add(attacking_type)
            elif combined_effectiveness < 1.0:
                resistances.add(attacking_type)

        return list(resistances), list(immunities)

    def _get_type_effectiveness(self, attacking_type: str, defending_type: str) -> float:
        """Get effectiveness multiplier for an attack"""
        if not attacking_type or not defending_type:
            return 1.0

        return TYPE_CHART.get(attacking_type, {}).get(defending_type, 1.0)

    def _find_resisting_types(self, attacking_type: str) -> List[str]:
        """Find types that resist a given attacking type"""
        resisting = []

        matchups = TYPE_CHART.get(attacking_type, {})
        for defending_type, effectiveness in matchups.items():
            if effectiveness < 1.0:
                resisting.append(defending_type)

        return resisting
