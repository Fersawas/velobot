#!/bin/bash
set -e

alembic upgrade head
python bot.py