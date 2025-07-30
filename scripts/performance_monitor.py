#!/usr/bin/env python3
"""
PepeluGPT Performance Monitor
=============================

Performance analysis and optimization utilities for PepeluGPT.
"""

import sys
import time
import psutil
import tracemalloc
from pathlib import Path
from typing import Dict, Any, List
from functools import wraps
from datetime import datetime

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


class PerformanceMonitor:
    """Monitor system performance and resource usage."""
    
    def __init__(self):
        """Initialize the performance monitor."""
        self.metrics = {}
        self.start_time = time.time()
        tracemalloc.start()
    
    def measure_function(self, func):
        """Decorator to measure function performance."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = tracemalloc.get_traced_memory()[0]
            
            try:
                result = func(*args, **kwargs)
                success = True
                error = None
            except Exception as e:
                result = None
                success = False
                error = str(e)
            
            end_time = time.time()
            end_memory = tracemalloc.get_traced_memory()[0]
            
            # Store metrics
            func_name = f"{func.__module__}.{func.__name__}"
            if func_name not in self.metrics:
                self.metrics[func_name] = []
            
            self.metrics[func_name].append({
                'duration': end_time - start_time,
                'memory_delta': end_memory - start_memory,
                'success': success,
                'error': error,
                'timestamp': datetime.now().isoformat()
            })
            
            return result
        return wrapper
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system resource usage."""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('.').percent,
            'process_memory': psutil.Process().memory_info().rss / 1024 / 1024,  # MB
            'uptime': time.time() - self.start_time
        }
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        report = {
            'system_metrics': self.get_system_metrics(),
            'function_metrics': {},
            'summary': {
                'total_functions_monitored': len(self.metrics),
                'total_calls': sum(len(calls) for calls in self.metrics.values())
            }
        }
        
        # Analyze function metrics
        for func_name, calls in self.metrics.items():
            if calls:
                durations = [call['duration'] for call in calls]
                memory_deltas = [call['memory_delta'] for call in calls]
                success_rate = sum(1 for call in calls if call['success']) / len(calls)
                
                report['function_metrics'][func_name] = {
                    'call_count': len(calls),
                    'avg_duration': sum(durations) / len(durations),
                    'max_duration': max(durations),
                    'min_duration': min(durations),
                    'avg_memory_delta': sum(memory_deltas) / len(memory_deltas),
                    'success_rate': success_rate,
                    'recent_errors': [call['error'] for call in calls[-5:] 
                                    if call['error'] is not None]
                }
        
        return report
    
    def identify_bottlenecks(self) -> List[Dict[str, Any]]:
        """Identify performance bottlenecks."""
        bottlenecks = []
        
        for func_name, metrics in self.get_performance_report()['function_metrics'].items():
            issues = []
            
            # Check for slow functions (> 1 second average)
            if metrics['avg_duration'] > 1.0:
                issues.append(f"Slow execution: {metrics['avg_duration']:.2f}s average")
            
            # Check for high memory usage (> 10MB average)
            if metrics['avg_memory_delta'] > 10 * 1024 * 1024:
                issues.append(f"High memory usage: {metrics['avg_memory_delta'] / 1024 / 1024:.1f}MB average")
            
            # Check for low success rate (< 90%)
            if metrics['success_rate'] < 0.9:
                issues.append(f"Low success rate: {metrics['success_rate']:.1%}")
            
            if issues:
                bottlenecks.append({
                    'function': func_name,
                    'issues': issues,
                    'call_count': metrics['call_count'],
                    'severity': len(issues)
                })
        
        # Sort by severity and call count
        bottlenecks.sort(key=lambda x: (x['severity'], x['call_count']), reverse=True)
        return bottlenecks


def run_performance_analysis():
    """Run comprehensive performance analysis."""
    print("📊 PepeluGPT Performance Analysis")
    print("=" * 50)
    
    monitor = PerformanceMonitor()
    
    # Test core imports
    print("🧪 Testing Core Imports...")
    
    @monitor.measure_function
    def test_core_imports():
        try:
            from core import utilities
            return "success"
        except Exception as e:
            return f"error: {e}"
    
    @monitor.measure_function
    def test_personality_imports():
        try:
            from personalities import PersonalityRouter
            return "success"
        except Exception as e:
            return f"error: {e}"
    
    @monitor.measure_function
    def test_vector_db_imports():
        try:
            from storage.vector_db import config
            return "success"
        except Exception as e:
            return f"error: {e}"
    
    # Run tests
    results = {
        'core': test_core_imports(),
        'personalities': test_personality_imports(),
        'vector_db': test_vector_db_imports()
    }
    
    # Display results
    for module, result in results.items():
        status = "✅" if "success" in result else "❌"
        print(f"  {status} {module}: {result}")
    
    # Generate performance report
    print("\n📈 Performance Report:")
    print("-" * 30)
    
    report = monitor.get_performance_report()
    system_metrics = report['system_metrics']
    
    print(f"💾 Memory Usage: {system_metrics['memory_percent']:.1f}%")
    print(f"🖥️  CPU Usage: {system_metrics['cpu_percent']:.1f}%")
    print(f"💿 Disk Usage: {system_metrics['disk_usage']:.1f}%")
    print(f"📊 Process Memory: {system_metrics['process_memory']:.1f} MB")
    print(f"⏱️  Uptime: {system_metrics['uptime']:.2f} seconds")
    
    # Check for bottlenecks
    print("\n🔍 Bottleneck Analysis:")
    print("-" * 30)
    
    bottlenecks = monitor.identify_bottlenecks()
    if bottlenecks:
        for bottleneck in bottlenecks[:3]:  # Show top 3
            print(f"⚠️  {bottleneck['function']}:")
            for issue in bottleneck['issues']:
                print(f"    • {issue}")
    else:
        print("✅ No significant bottlenecks detected")
    
    # Optimization recommendations
    print("\n💡 Optimization Recommendations:")
    print("-" * 30)
    
    recommendations = []
    
    if system_metrics['memory_percent'] > 80:
        recommendations.append("🔧 Consider implementing memory caching strategies")
    
    if system_metrics['cpu_percent'] > 80:
        recommendations.append("🔧 Consider optimizing CPU-intensive operations")
    
    if bottlenecks:
        recommendations.append("🔧 Focus on optimizing identified bottleneck functions")
    
    if not recommendations:
        recommendations.append("✅ System performance is within acceptable ranges")
    
    for rec in recommendations:
        print(f"  {rec}")
    
    print(f"\n🎯 Analysis Complete: {report['summary']['total_calls']} function calls monitored")
    
    return report


if __name__ == "__main__":
    try:
        report = run_performance_analysis()
    except KeyboardInterrupt:
        print("\n⏹️  Performance analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Performance analysis failed: {e}")
        sys.exit(1)
