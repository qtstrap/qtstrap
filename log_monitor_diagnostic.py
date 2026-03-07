#!/usr/bin/env python
"""
LogMonitor Performance Diagnostic Tool

This diagnostic measures the performance impact of the DatabaseHandler
on the logging system. Run it standalone to benchmark:

    python log_monitor_diagnostic.py

What it measures:
1. Logging overhead with DatabaseHandler vs without
2. SQLite INSERT performance under load
3. COUNT(*) and query performance as table grows
4. Stress test with sustained logging

Requirements:
- Python 3.10+
- qtpy with a Qt backend (PySide6 or PyQt6)
"""

import logging
import sys
import time
import statistics
import tempfile
import os
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class BenchmarkResult:
    """Results from a single benchmark run"""
    name: str
    iterations: int
    total_time_ms: float
    per_call_ms: float
    calls_per_second: float


@dataclass
class DiagnosticReport:
    """Full diagnostic report"""
    baseline: BenchmarkResult | None = None
    with_handler: BenchmarkResult | None = None
    async_handler: BenchmarkResult | None = None
    handler_overhead_ms: float = 0.0
    handler_overhead_percent: float = 0.0
    async_overhead_ms: float = 0.0
    async_overhead_percent: float = 0.0
    insert_benchmarks: list = field(default_factory=list)
    query_benchmarks: list = field(default_factory=list)
    recommendations: list = field(default_factory=list)
    
    def __str__(self):
        lines = [
            "=" * 70,
            "LOG MONITOR PERFORMANCE DIAGNOSTIC REPORT",
            "=" * 70,
            "",
            "## Logging Overhead Analysis",
            "",
            f"  Baseline (no handler):",
            f"    {self.baseline.iterations} calls in {self.baseline.total_time_ms:.2f}ms",
            f"    {self.baseline.per_call_ms:.4f}ms per call",
            f"    {self.baseline.calls_per_second:,.0f} calls/sec",
            "",
            f"  With Sync DatabaseHandler:",
            f"    {self.with_handler.iterations} calls in {self.with_handler.total_time_ms:.2f}ms",
            f"    {self.with_handler.per_call_ms:.4f}ms per call",
            f"    {self.with_handler.calls_per_second:,.0f} calls/sec",
            "",
            f"  SYNCHRONOUS OVERHEAD: {self.handler_overhead_ms:.4f}ms per call ({self.handler_overhead_percent:.1f}x slower)",
            "",
        ]
        
        if self.async_handler:
            lines.extend([
                f"  With AsyncDatabaseHandler:",
                f"    {self.async_handler.iterations} calls in {self.async_handler.total_time_ms:.2f}ms",
                f"    {self.async_handler.per_call_ms:.4f}ms per call",
                f"    {self.async_handler.calls_per_second:,.0f} calls/sec",
                "",
                f"  ASYNC OVERHEAD: {self.async_overhead_ms:.4f}ms per call ({self.async_overhead_percent:.1f}x slower)",
                "",
            ])
        
        if self.insert_benchmarks:
            lines.extend([
                "## SQLite INSERT Benchmarks",
                "",
            ])
            for bench in self.insert_benchmarks:
                lines.extend([
                    f"  {bench.name}:",
                    f"    {bench.iterations} inserts in {bench.total_time_ms:.2f}ms",
                    f"    {bench.per_call_ms:.4f}ms per insert",
                    f"    {bench.calls_per_second:,.0f} inserts/sec",
                    "",
                ])
        
        if self.query_benchmarks:
            lines.extend([
                "## Query Performance",
                "",
            ])
            for bench in self.query_benchmarks:
                lines.extend([
                    f"  {bench.name}:",
                    f"    {bench.total_time_ms:.2f}ms",
                    "",
                ])
        
        if self.recommendations:
            lines.extend([
                "## Recommendations",
                "",
            ])
            for rec in self.recommendations:
                lines.append(f"  - {rec}")
            lines.append("")
        
        lines.append("=" * 70)
        return "\n".join(lines)


def benchmark_logging(func: Callable, iterations: int, name: str) -> BenchmarkResult:
    """Benchmark a logging function"""
    start = time.perf_counter()
    for _ in range(iterations):
        func()
    elapsed = time.perf_counter() - start
    
    total_ms = elapsed * 1000
    per_call_ms = total_ms / iterations
    calls_per_sec = iterations / elapsed if elapsed > 0 else 0
    
    return BenchmarkResult(
        name=name,
        iterations=iterations,
        total_time_ms=total_ms,
        per_call_ms=per_call_ms,
        calls_per_second=calls_per_sec
    )


# SQL schema (copied from log_database_handler.py to avoid import issues)
INITIAL_SQL = """
CREATE TABLE IF NOT EXISTS log(
    TimeStamp TEXT,
    Source TEXT,
    LogLevel INT,
    LogLevelName TEXT,
    Message TEXT,
    Args TEXT,
    Module TEXT,
    FuncName TEXT,
    LineNo INT,
    Exception TEXT,
    Process INT,
    Thread TEXT,
    ThreadName TEXT
)
"""

INSERTION_SQL = """
INSERT INTO log(
    TimeStamp,
    Source,
    LogLevel,
    LogLevelName,
    Message,
    Args,
    Module,
    FuncName,
    LineNo,
    Exception,
    Process,
    Thread,
    ThreadName
)
VALUES (
    '%(dbtime)s',
    '%(name)s',
    %(levelno)d,
    '%(levelname)s',
    '%(msg)s',
    '%(args)s',
    '%(module)s',
    '%(funcName)s',
    %(lineno)d,
    '%(exc_text)s',
    %(process)d,
    '%(thread)s',
    '%(threadName)s'
);
"""


class MockDatabaseHandler(logging.Handler):
    """
    Minimal reproduction of DatabaseHandler for benchmarking.
    Matches the core behavior without importing qtstrap.
    """
    def __init__(self, db_connection):
        super().__init__()
        self.db = db_connection
        self.formatter = logging.Formatter('%(asctime)s')
    
    def format_time(self, record):
        record.dbtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(record.created))
    
    def emit(self, record):
        self.format(record)
        self.format_time(record)
        
        # Escape single quotes (matching original behavior)
        record.msg = record.msg.replace("'", "''")
        
        if record.exc_info:
            record.exc_text = logging.Formatter().formatException(record.exc_info).replace("'", "''")
        else:
            record.exc_text = ''
        
        query_string = INSERTION_SQL % record.__dict__
        self.db.exec_(query_string)


def run_diagnostic(iterations: int = 1000, verbose: bool = False) -> DiagnosticReport:
    """
    Run the full diagnostic suite.
    
    Args:
        iterations: Number of log calls per benchmark
        verbose: Print progress during execution
    
    Returns:
        DiagnosticReport with all benchmark results
    """
    from qtpy.QtSql import QSqlDatabase
    
    report = DiagnosticReport()
    report.recommendations = []
    
    # Create a temp database for testing
    temp_dir = tempfile.gettempdir()
    test_db = os.path.join(temp_dir, "log_diagnostic.db")
    
    if os.path.exists(test_db):
        os.remove(test_db)
    
    # ============================================================
    # Test 1: Baseline logging performance (no handler)
    # ============================================================
    if verbose:
        print(f"Testing baseline logging ({iterations} iterations)...")
    
    baseline_logger = logging.getLogger("diagnostic.baseline")
    baseline_logger.handlers = []
    baseline_logger.setLevel(logging.DEBUG)
    
    def baseline_log():
        baseline_logger.debug("Test message %d", 42)
    
    report.baseline = benchmark_logging(baseline_log, iterations, "Baseline")
    
    # ============================================================
    # Test 2: Logging with DatabaseHandler
    # ============================================================
    if verbose:
        print(f"Testing DatabaseHandler ({iterations} iterations)...")
    
    # Set up database connection
    conn_name = 'diagnostic_logs'
    if QSqlDatabase.contains(conn_name):
        QSqlDatabase.removeDatabase(conn_name)
    
    db = QSqlDatabase.addDatabase('QSQLITE', conn_name)
    db.setDatabaseName(test_db)
    if not db.open():
        raise RuntimeError(f"Failed to open database: {db.lastError().text()}")
    db.exec_(INITIAL_SQL)
    
    handler_logger = logging.getLogger("diagnostic.handler")
    handler_logger.handlers = []
    handler_logger.setLevel(logging.DEBUG)
    
    db_handler = MockDatabaseHandler(db)
    handler_logger.addHandler(db_handler)
    
    def handler_log():
        handler_logger.debug("Test message %d", 42)
    
    report.with_handler = benchmark_logging(handler_log, iterations, "With DatabaseHandler")
    
    # Calculate overhead
    report.handler_overhead_ms = report.with_handler.per_call_ms - report.baseline.per_call_ms
    if report.baseline.per_call_ms > 0:
        report.handler_overhead_percent = report.with_handler.per_call_ms / report.baseline.per_call_ms
    else:
        report.handler_overhead_percent = report.with_handler.per_call_ms * 1000
    
    # ============================================================
    # Test 3: INSERT performance at scale
    # ============================================================
    if verbose:
        print(f"Testing INSERT performance...")
    
    for batch_size in [100, 500, 1000]:
        def make_batch_log(size):
            def batch_log():
                for i in range(size):
                    handler_logger.debug("Batch message %d", i)
            return batch_log
        
        bench = benchmark_logging(make_batch_log(batch_size), 1, f"Batch INSERT ({batch_size} rows)")
        bench.iterations = batch_size
        bench.per_call_ms = bench.total_time_ms / batch_size
        report.insert_benchmarks.append(bench)
    
    # ============================================================
    # Test 4: Query performance as table grows
    # ============================================================
    if verbose:
        print(f"Testing query performance...")
    
    # Add more rows
    for i in range(5000):
        handler_logger.debug("Filler message %d", i)
    
    def count_query():
        query = db.exec_("SELECT COUNT(*) FROM 'log'")
        if query.next():
            return query.value(0)
        return 0
    
    bench = benchmark_logging(count_query, 10, "COUNT(*) query (10 runs)")
    report.query_benchmarks.append(bench)
    
    def select_query():
        query = db.exec_("SELECT * FROM 'log' LIMIT 100")
        while query.next():
            pass
    
    bench = benchmark_logging(select_query, 10, "SELECT * LIMIT 100 (10 runs)")
    report.query_benchmarks.append(bench)
    
    row_count = count_query()
    
    def rowid_filter_query():
        offset = max(0, row_count - 1000)
        query = db.exec_(f"SELECT * FROM 'log' WHERE rowid > {offset} LIMIT 100")
        while query.next():
            pass
    
    bench = benchmark_logging(rowid_filter_query, 10, "rowid filter query (10 runs)")
    report.query_benchmarks.append(bench)
    
    # ============================================================
    # Generate recommendations
    # ============================================================
    if report.handler_overhead_percent > 10:
        report.recommendations.append(
            f"DatabaseHandler adds {report.handler_overhead_ms:.2f}ms overhead per log call. "
            f"For high-frequency logging, consider async insertion."
        )
    
    if report.handler_overhead_ms > 1.0:
        report.recommendations.append(
            "INSERT operations exceed 1ms. SQLite synchronous writes are blocking. "
            "Consider PRAGMA synchronous=NORMAL or WAL mode."
        )
    
    count_bench = next((b for b in report.query_benchmarks if "COUNT" in b.name), None)
    if count_bench and count_bench.per_call_ms > 5:
        report.recommendations.append(
            f"COUNT(*) queries take {count_bench.per_call_ms:.1f}ms on average. "
            "This is called every 200ms by LogTableView.refresh(). "
            "Consider caching row count or using triggers."
        )
    
    if row_count > 10000:
        report.recommendations.append(
            f"Log table has {row_count:,} rows. Consider periodic cleanup or rotation."
        )
    
    if report.recommendations:
        report.recommendations.append(
            "Consider disabling LogMonitor.install() in production if logging overhead is unacceptable."
        )
    
    # Cleanup
    handler_logger.removeHandler(db_handler)
    db.close()
    QSqlDatabase.removeDatabase(conn_name)
    
    if os.path.exists(test_db):
        os.remove(test_db)
    
    return report


def run_stress_test(duration_sec: int = 5, log_rate: int = 100) -> dict:
    """
    Run a stress test to measure system behavior under sustained logging.
    
    Args:
        duration_sec: How long to run the test
        log_rate: Target logs per second
    
    Returns:
        Dict with stress test metrics
    """
    from qtpy.QtSql import QSqlDatabase
    
    temp_dir = tempfile.gettempdir()
    test_db = os.path.join(temp_dir, "log_stress.db")
    
    if os.path.exists(test_db):
        os.remove(test_db)
    
    conn_name = 'stress_logs'
    if QSqlDatabase.contains(conn_name):
        QSqlDatabase.removeDatabase(conn_name)
    
    db = QSqlDatabase.addDatabase('QSQLITE', conn_name)
    db.setDatabaseName(test_db)
    if not db.open():
        raise RuntimeError(f"Failed to open database: {db.lastError().text()}")
    db.exec_(INITIAL_SQL)
    
    logger = logging.getLogger("stress.test")
    logger.handlers = []
    logger.setLevel(logging.DEBUG)
    
    db_handler = MockDatabaseHandler(db)
    logger.addHandler(db_handler)
    
    interval = 1.0 / log_rate
    
    results = {
        "target_rate": log_rate,
        "duration_sec": duration_sec,
        "total_logged": 0,
        "actual_rate": 0,
        "max_latency_ms": 0,
        "min_latency_ms": float('inf'),
        "avg_latency_ms": 0,
        "latencies": []
    }
    
    start_time = time.perf_counter()
    end_time = start_time + duration_sec
    
    while time.perf_counter() < end_time:
        log_start = time.perf_counter()
        logger.debug("Stress test message %d", results["total_logged"])
        log_end = time.perf_counter()
        
        latency_ms = (log_end - log_start) * 1000
        results["latencies"].append(latency_ms)
        results["total_logged"] += 1
        
        # Throttle to target rate
        elapsed = time.perf_counter() - log_start
        sleep_time = interval - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)
    
    total_elapsed = time.perf_counter() - start_time
    results["actual_rate"] = results["total_logged"] / total_elapsed
    
    if results["latencies"]:
        results["max_latency_ms"] = max(results["latencies"])
        results["min_latency_ms"] = min(results["latencies"])
        results["avg_latency_ms"] = statistics.mean(results["latencies"])
    
    # Cleanup
    logger.removeHandler(db_handler)
    db.close()
    QSqlDatabase.removeDatabase(conn_name)
    if os.path.exists(test_db):
        os.remove(test_db)
    
    results["latencies"] = results["latencies"][:100]  # Trim for memory
    return results


def main():
    """Entry point for standalone execution"""
    # Ensure QApplication exists for Qt SQL operations
    from qtpy.QtWidgets import QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    print("=" * 70)
    print("LOG MONITOR PERFORMANCE DIAGNOSTIC")
    print("=" * 70)
    print()
    
    print("Running diagnostic (250 iterations)...")
    print()
    
    report = run_diagnostic(iterations=250, verbose=True)
    print(report)
    
    print("\nRunning stress test (3 seconds, 100 logs/sec target)...")
    stress = run_stress_test(duration_sec=3, log_rate=100)
    
    print("-" * 70)
    print("Stress Test Results:")
    print(f"  Target rate: {stress['target_rate']} logs/sec")
    print(f"  Achieved rate: {stress['actual_rate']:.1f} logs/sec")
    print(f"  Total logged: {stress['total_logged']}")
    print(f"  Latency range: {stress['min_latency_ms']:.2f}ms - {stress['max_latency_ms']:.2f}ms")
    print(f"  Average latency: {stress['avg_latency_ms']:.2f}ms")
    print("-" * 70)


if __name__ == "__main__":
    main()