-- SQL script to create the claude_chat_logs table in Supabase
-- Run this in your Supabase SQL editor

CREATE TABLE claude_chat_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_query TEXT NOT NULL,
    claude_response TEXT NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    project_id VARCHAR(100) NOT NULL,
    interaction_timestamp TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX idx_claude_chat_logs_user_id ON claude_chat_logs(user_id);
CREATE INDEX idx_claude_chat_logs_project_id ON claude_chat_logs(project_id);
CREATE INDEX idx_claude_chat_logs_timestamp ON claude_chat_logs(interaction_timestamp);
CREATE INDEX idx_claude_chat_logs_created_at ON claude_chat_logs(created_at);

-- Row Level Security (RLS) is disabled for service key usage
-- If you need RLS, uncomment the following lines and adjust policies accordingly:
-- ALTER TABLE claude_chat_logs ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY "Service key can access all chat logs" ON claude_chat_logs
--     FOR ALL USING (true);

-- Add a function to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_claude_chat_logs_updated_at 
    BEFORE UPDATE ON claude_chat_logs 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();