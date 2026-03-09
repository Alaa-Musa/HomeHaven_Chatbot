import gradio as gr
import pandas as pd
import datetime
from Implementation.answer import answer_question
from dotenv import load_dotenv

load_dotenv(override=True)

# 1. Global storage for all benchmark tests
results_log = pd.DataFrame(columns=[
    "timestamp", "test_name", "question", "answer", 
    "total_tokens", "prompt_tokens", "completion_tokens", "total_cost_usd"
])

def format_context(context):
    result = "<h2 style='color: #ff7800;'>Relevant Context</h2>\n\n"
    for doc in context:
        result += f"<span style='color: #ff7800;'>Source: {doc.metadata['source']}</span>\n\n"
        result += doc.page_content + "\n\n"
    return result


def chat(history, test_name):
    global results_log
    
    # Validation: Ensure a test name is provided before starting
    if not test_name:
        test_name = "Default_Test"

    last_message = history[-1]["content"]
    prior = history[:-1]
    
    # 2. Call your RAG function with usage stats
    answer, context, usage_stats = answer_question(last_message, prior)
    
    # 3. Log the data into the global DataFrame
    new_entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "test_name": test_name,
        "question": last_message,
        "answer": answer,
        **usage_stats  # Unpacks total_tokens, cost, etc.
    }
    results_log = pd.concat([results_log, pd.DataFrame([new_entry])], ignore_index=True)
    
    # Update Gradio history
    history.append({"role": "assistant", "content": answer})
    
    # Return context and updated log for display (optional)
    return history, format_context(context), results_log

def export_logs():
    filename = f"benchmark_results_{datetime.date.today()}.csv"
    results_log.to_csv(filename, index=False)
    return filename

def main():
    theme = gr.themes.Soft(font=["Inter", "system-ui", "sans-serif"])

    with gr.Blocks(title="Benchmark Assistant", theme=theme) as ui:
        gr.Markdown("# 🏢 HomeHaven Benchmarking\nTrack RAG vs. Pure LLM cost and performance.")

        with gr.Row():
            # Test Configuration Column
            with gr.Column(scale=1):
                test_name_input = gr.Textbox(label="Test Run Name", placeholder="e.g., RAG_v1 or FULL_CONTEXT_50K")
                chatbot = gr.Chatbot(label="💬 Conversation", height=500, type="messages")
                message = gr.Textbox(label="Your Question", placeholder="Ask anything...")
                
            # Logging & Context Column
            with gr.Column(scale=1):
                # Live view of the benchmark log
                log_display = gr.DataFrame(label="📊 Live Usage Log", value=results_log, interactive=False)
                download_btn = gr.Button("💾 Export Benchmark to CSV")
                csv_output = gr.File(label="Download File")
                
                context_markdown = gr.Markdown(label="📚 Retrieved Context", value="*Retrieved context will appear here*", container=True)

        # Trigger logic
        message.submit(
            lambda m, h: ("", h + [{"role": "user", "content": m}]), 
            inputs=[message, chatbot], 
            outputs=[message, chatbot]
        ).then(
            chat, 
            inputs=[chatbot, test_name_input], 
            outputs=[chatbot, context_markdown, log_display]
        )

        download_btn.click(export_logs, outputs=csv_output)

    ui.launch(inbrowser=True)

if __name__ == "__main__":
    main()
