#!/usr/bin/env python3
"""Generate the current English register; drafts never count as sent offers."""
from outreach_reports import register

if __name__ == '__main__':
    register(False)
