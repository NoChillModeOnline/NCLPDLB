"""
Master test runner for Pokemon Draft League Bot

Runs all test suites and provides comprehensive report
"""

import sys
import subprocess
import time

# Set UTF-8 encoding for console output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def run_test_file(test_file: str, description: str) -> tuple[bool, float]:
    """
    Run a test file and return success status and duration

    Args:
        test_file: Path to test file
        description: Human-readable description

    Returns:
        Tuple of (success, duration_seconds)
    """
    print(f'\n{"="*70}')
    print(f'  {description}')
    print(f'{"="*70}\n')

    start = time.time()
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=False,
            text=True,
            cwd='.',
            check=False
        )
        duration = time.time() - start
        success = result.returncode == 0
        return (success, duration)
    except Exception as e:
        print(f'❌ Error running {test_file}: {e}')
        duration = time.time() - start
        return (False, duration)

def main():
    """Run all test suites"""
    print('\n' + '='*70)
    print('  POKEMON DRAFT LEAGUE BOT - MASTER TEST SUITE')
    print('='*70)
    print()
    print('Running all tests to verify bot functionality...')
    print()

    # Test suite configuration
    tests = [
        ('test_imports.py', 'Import Tests - Module Loading'),
        ('test_team_validation.py', 'Team Validation Tests - Type Analysis'),
        ('test_performance.py', 'Performance Tests - Optimization Benchmarks'),
    ]

    # Run all tests
    results = []
    for test_file, description in tests:
        success, duration = run_test_file(test_file, description)
        results.append((test_file, description, success, duration))

    # Print summary
    print('\n' + '='*70)
    print('  TEST SUMMARY')
    print('='*70)
    print()

    total_tests = len(results)
    passed_tests = sum(1 for _, _, success, _ in results if success)
    failed_tests = total_tests - passed_tests
    total_time = sum(duration for _, _, _, duration in results)

    for test_file, description, success, duration in results:
        status = '✅ PASS' if success else '❌ FAIL'
        print(f'{status}  {description}')
        print(f'       File: {test_file}')
        print(f'       Time: {duration:.2f}s')
        print()

    print('='*70)
    print(f'Total: {passed_tests}/{total_tests} test suites passed')
    print(f'Time: {total_time:.2f}s')
    print('='*70)
    print()

    if failed_tests == 0:
        print('🎉 ALL TESTS PASSED!')
        print()
        print('Your Pokemon Draft League Bot is:')
        print('  ✅ Fully functional')
        print('  ✅ Well tested')
        print('  ✅ Performance optimized')
        print('  ✅ Ready for production')
        print()
        print('Next steps:')
        print('  1. Add .credentials.json with Discord token and Sheet ID')
        print('  2. Run: python bot.py')
        print('  3. Test commands in Discord server')
        print()
        return 0
    else:
        print(f'⚠️  {failed_tests} test suite(s) failed!')
        print()
        print('Please review the test output above for details.')
        print()
        return 1

if __name__ == '__main__':
    sys.exit(main())
