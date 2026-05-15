from datetime import datetime
import os

def generate_markdown(transcript, summary_data, metadata):
    title = metadata.get("filename", "Meeting")
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    summary_text = summary_data.get("summary", "No summary generated.")
    action_items = summary_data.get("action_items", [])

    md_content = f"# Meeting Summary — {date}\n\n"
    md_content += f"**Source File:** {title}\n\n"
    
    md_content += "## Executive Summary\n"
    md_content += f"{summary_text}\n\n"
    
    md_content += "## Action Items\n"
    md_content += "| Task | Assigned To | Deadline |\n"
    md_content += "|------|-------------|----------|\n"
    
    for item in action_items:
        task = item.get("task", "N/A")
        owner = item.get("assigned_to", "Unassigned")
        deadline = item.get("deadline", "N/A")
        md_content += f"| {task} | {owner} | {deadline} |\n"
        
    md_content += "\n## Full Transcript\n"
    md_content += f"{transcript}\n"
    
    return md_content

def save_markdown(content, filename):
    # Ensure outputs directory exists
    outputs_dir = os.path.join(os.getcwd(), "outputs")
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)

    safe_name = filename.replace(" ", "_").replace(".", "_")
    filepath = os.path.join(outputs_dir, f"{safe_name}_summary.md")
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath