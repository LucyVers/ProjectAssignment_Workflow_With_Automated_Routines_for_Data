"""
Monitoring utilities for tracking data quality metrics and generating reports.
"""
from typing import Dict, List, Optional
from datetime import datetime
import logging
import json
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataQualityMonitor:
    def __init__(self, log_dir: str = "logs/data_quality"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.metrics = {
            'validation_counts': {
                'total': 0,
                'passed': 0,
                'failed': 0
            },
            'error_types': {},
            'processing_times': []
        }
    
    def log_validation_result(self, validation_type: str, passed: bool, errors: Optional[List[str]] = None):
        """
        Log a validation result with optional error messages.
        """
        timestamp = datetime.now().isoformat()
        
        # Update metrics
        self.metrics['validation_counts']['total'] += 1
        if passed:
            self.metrics['validation_counts']['passed'] += 1
        else:
            self.metrics['validation_counts']['failed'] += 1
        
        # Log errors if any
        if errors:
            for error in errors:
                self.metrics['error_types'][error] = self.metrics['error_types'].get(error, 0) + 1
        
        # Log to file
        log_entry = {
            'timestamp': timestamp,
            'validation_type': validation_type,
            'passed': passed,
            'errors': errors or []
        }
        
        log_file = self.log_dir / f"validation_log_{datetime.now():%Y%m%d}.json"
        with open(log_file, 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
        
        # Log to console
        logger.info(f"Validation {validation_type}: {'Passed' if passed else 'Failed'}")
        if errors:
            for error in errors:
                logger.warning(f"Validation error: {error}")
    
    def get_metrics_report(self) -> Dict:
        """
        Generate a report of current metrics.
        """
        total = self.metrics['validation_counts']['total']
        if total > 0:
            pass_rate = (self.metrics['validation_counts']['passed'] / total) * 100
        else:
            pass_rate = 0
        
        return {
            'validation_counts': self.metrics['validation_counts'],
            'pass_rate_percentage': pass_rate,
            'most_common_errors': dict(sorted(
                self.metrics['error_types'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:5])
        }
    
    def reset_metrics(self):
        """
        Reset all metrics to initial state.
        """
        self.metrics = {
            'validation_counts': {
                'total': 0,
                'passed': 0,
                'failed': 0
            },
            'error_types': {},
            'processing_times': []
        }

# Create global monitor instance
monitor = DataQualityMonitor() 