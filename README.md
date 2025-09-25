# GoonerSquad MCP Server

A Model Context Protocol (MCP) server that provides Supabase database integration tools for Claude Code. This server enables direct database operations and chat interaction logging through MCP tools.

## Features

- **Database Operations**: Full CRUD operations for Supabase tables
- **Chat Logging**: Log Claude Code interactions to a dedicated table
- **Chat History**: Retrieve filtered chat history with pagination
- **Environment-based Configuration**: Secure credential management

## Requirements

- Python 3.8+
- Supabase project with database access
- Environment variables configured

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export SUPABASE_URL="your_supabase_url"
export SUPABASE_KEY="your_supabase_key"
export USER_ID="your_user_id"
export PROJECT_ID="your_project_id"
```

3. Create the database table:
```bash
# Run the SQL in create_table.sql in your Supabase SQL editor
```

## Usage

Run the MCP server:
```bash
python my_server.py
```

## Available Tools

### Database Operations
- `read_from_table` - Read data with optional filtering and pagination
- `write_to_table` - Insert new records
- `update_in_table` - Update existing records based on filters
- `delete_from_table` - Delete records based on filters

### Chat Management
- `log_chat_interaction` - Log Claude Code chat interactions
- `get_chat_history` - Retrieve chat history with filtering options

### Utility
- `greet` - Simple greeting function for testing

## Configuration

The server requires the following environment variables:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Supabase service role or anon key
- `USER_ID`: Identifier for the current user
- `PROJECT_ID`: Identifier for the current project

## Database Schema

The `claude_chat_logs` table stores chat interactions with:
- User queries and Claude responses
- User and project identifiers
- Timestamps for interaction and creation
- Automatic `updated_at` triggers

## Security

- Environment variable validation on startup
- Service role key detection for RLS bypass
- Optional Row Level Security (RLS) support