import os
from typing import Dict, Any, Optional
from datetime import datetime
from fastmcp import FastMCP
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("my-mcp-server")

supabase_url: str = os.environ.get("SUPABASE_URL")
supabase_key: str = os.environ.get("SUPABASE_KEY")
user_id: str = os.environ.get("USER_ID")
project_id: str = os.environ.get("PROJECT_ID")

if not supabase_url or not supabase_key:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

if not user_id or not project_id:
    raise ValueError("USER_ID and PROJECT_ID must be set in environment variables")

# Use service role key to bypass RLS, or use anon key with user authentication
supabase: Client = create_client(supabase_url, supabase_key)

def is_service_key() -> bool:
    """Check if we're using a service role key (which bypasses RLS)"""
    return supabase_key.startswith('eyJ') and len(supabase_key) > 100

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

@mcp.tool
def read_from_table(table_name: str, columns: Optional[str] = "*", filters: Optional[Dict[str, Any]] = None, limit: Optional[int] = None) -> Dict[str, Any]:
    """Read data from a Supabase table with optional filtering and column selection."""
    try:
        query = supabase.table(table_name).select(columns)
        
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        
        if limit:
            query = query.limit(limit)
        
        response = query.execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool
def write_to_table(table_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Insert a new record into a Supabase table."""
    try:
        response = supabase.table(table_name).insert(data).execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool
def update_in_table(table_name: str, filters: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """Update existing records in a Supabase table based on filters."""
    try:
        query = supabase.table(table_name).update(updates)
        
        for key, value in filters.items():
            query = query.eq(key, value)
        
        response = query.execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool
def delete_from_table(table_name: str, filters: Dict[str, Any]) -> Dict[str, Any]:
    """Delete records from a Supabase table based on filters."""
    try:
        query = supabase.table(table_name).delete()
        
        for key, value in filters.items():
            query = query.eq(key, value)
        
        response = query.execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool
def log_chat_interaction(user_query: str, claude_response: str, timestamp: Optional[str] = None) -> Dict[str, Any]:
    """Log a Claude Code chat interaction to the claude_chat_logs table."""
    try:
        interaction_timestamp = timestamp if timestamp else datetime.now().isoformat()
        
        chat_data = {
            "user_query": user_query,
            "claude_response": claude_response,
            "user_id": user_id,
            "project_id": project_id,
            "interaction_timestamp": interaction_timestamp
        }
        
        response = supabase.table("claude_chat_logs").insert(chat_data).execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool
def get_chat_history(limit: Optional[int] = 50, filter_user_id: Optional[str] = None, filter_project_id: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
    """Retrieve chat history from claude_chat_logs table with optional filtering."""
    try:
        query = supabase.table("claude_chat_logs").select("*")
        
        # Apply filters
        if filter_user_id:
            query = query.eq("user_id", filter_user_id)
        else:
            query = query.eq("user_id", user_id)  # Default to current user
            
        if filter_project_id:
            query = query.eq("project_id", filter_project_id)
        else:
            query = query.eq("project_id", project_id)  # Default to current project
            
        if start_date:
            query = query.gte("interaction_timestamp", start_date)
            
        if end_date:
            query = query.lte("interaction_timestamp", end_date)
        
        # Order by most recent first and apply limit
        query = query.order("interaction_timestamp", desc=True)
        
        if limit:
            query = query.limit(limit)
        
        response = query.execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    mcp.run()