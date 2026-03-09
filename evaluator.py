import gradio as gr
import pandas as pd
from collections import defaultdict
from dotenv import load_dotenv

from Evaluation.eval import evaluate_all_retrieval, evaluate_all_answers

load_dotenv(override=True)

# Color coding thresholds - Retrieval
MRR_GREEN = 0.9
MRR_AMBER = 0.75
NDCG_GREEN = 0.9
NDCG_AMBER = 0.75
COVERAGE_GREEN = 90.0
COVERAGE_AMBER = 75.0

# Color coding thresholds - Answer (1-5 scale)
ANSWER_GREEN = 4.5
ANSWER_AMBER = 4.0


def get_color(value: float, metric_type: str) -> str:
    """Get color based on metric value and type."""
    if metric_type == "mrr":
        if value >= MRR_GREEN:
            return "green"
        elif value >= MRR_AMBER:
            return "orange"
        else:
            return "red"
    elif metric_type == "ndcg":
        if value >= NDCG_GREEN:
            return "green"
        elif value >= NDCG_AMBER:
            return "orange"
        else:
            return "red"
    elif metric_type == "coverage":
        if value >= COVERAGE_GREEN:
            return "green"
        elif value >= COVERAGE_AMBER:
            return "orange"
        else:
            return "red"
    elif metric_type in ["accuracy", "completeness", "relevance"]:
        if value >= ANSWER_GREEN:
            return "green"
        elif value >= ANSWER_AMBER:
            return "orange"
        else:
            return "red"
    return "black"


def format_metric_html(label: str, value: float, metric_type: str, is_percentage: bool = False, score_format: bool = False) -> str:
    """Format a metric with high-contrast text for reports."""
    color = get_color(value, metric_type)
    value_str = f"{value:.1f}%" if is_percentage else (f"{value:.2f}/5" if score_format else f"{value:.4f}")
    
    return f"""
    <div style="margin: 10px 0; padding: 15px; background-color: #ffffff; border-radius: 8px; border: 1px solid #e0e0e0; border-left: 5px solid {color}; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);">
        <div style="font-size: 14px; color: #444; font-weight: 500; margin-bottom: 5px;">{label}</div>
        <div style="font-size: 28px; font-weight: bold; color: {color};">{value_str}</div>
    </div>
    """

def format_usage_html(total_tokens: int, total_cost: float, count: int) -> str:
    """High-contrast Cost Summary box for snapshots."""
    avg_cost = total_cost / count if count > 0 else 0
    return f"""
    <div style="margin-top: 20px; padding: 20px; background-color: #fcfcfc; border-radius: 8px; border: 2px solid #333; box-shadow: 4px 4px 0px #eee;">
        <div style="font-weight: 800; color: #1a1a1a; font-size: 16px; margin-bottom: 12px; border-bottom: 2px solid #333; padding-bottom: 8px; text-transform: uppercase;">
            📊 Cost & Efficiency Analysis
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="color: #444; font-weight: 600;">Total Tokens:</span>
            <span style="font-weight: 800; color: #000;">{total_tokens:,}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="color: #444; font-weight: 600;">Total Investment (USD):</span>
            <span style="font-weight: 800; color: #1e7e34;">${total_cost:.4f}</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding-top: 8px; border-top: 1px dashed #ccc;">
            <span style="color: #666;">Unit Cost (Avg/Query):</span>
            <span style="font-weight: 700; color: #333;">${avg_cost:.4f}</span>
        </div>
    </div>
    """



def run_retrieval_evaluation(progress=gr.Progress()):
    """Run retrieval evaluation and yield updates."""
    total_mrr = 0.0
    total_ndcg = 0.0
    total_coverage = 0.0
    category_mrr = defaultdict(list)
    count = 0

    for test, result, prog_value in evaluate_all_retrieval():
        count += 1
        total_mrr += result.mrr
        total_ndcg += result.ndcg
        total_coverage += result.keyword_coverage

        category_mrr[test.category].append(result.mrr)

        # Update progress bar only
        progress(prog_value, desc=f"Evaluating test {count}...")

    # Calculate final averages
    avg_mrr = total_mrr / count
    avg_ndcg = total_ndcg / count
    avg_coverage = total_coverage / count

    # Create final summary metrics HTML
    final_html = f"""
    <div style="padding: 0;">
        {format_metric_html("Mean Reciprocal Rank (MRR)", avg_mrr, "mrr")}
        {format_metric_html("Normalized DCG (nDCG)", avg_ndcg, "ndcg")}
        {format_metric_html("Keyword Coverage", avg_coverage, "coverage", is_percentage=True)}
        <div style="margin-top: 20px; padding: 10px; background-color: #d4edda; border-radius: 5px; text-align: center; border: 1px solid #c3e6cb;">
            <span style="font-size: 14px; color: #155724; font-weight: bold;">✓ Evaluation Complete: {count} tests</span>
        </div>
    </div>
    """

    # Create final bar chart data
    category_data = []
    for category, mrr_scores in category_mrr.items():
        avg_cat_mrr = sum(mrr_scores) / len(mrr_scores)
        category_data.append({"Category": category, "Average MRR": avg_cat_mrr})

    df = pd.DataFrame(category_data)

    return final_html, df


def run_answer_evaluation(mode="RAG", progress=gr.Progress()):
    """Run answer evaluation and yield updates (including cost stats)."""
    # 1. Load context for Pure LLM mode
    full_kb = ""
    if mode == "PURE_LLM":
        try:
            with open("knowledge_base.txt", "r", encoding="utf-8") as f:
                full_kb = f.read()
        except FileNotFoundError:
            print("Warning: knowledge_base.txt not found.")

    total_accuracy = 0.0
    total_completeness = 0.0
    total_relevance = 0.0
    total_tokens = 0
    total_cost_usd = 0.0
    category_accuracy = defaultdict(list)
    count = 0

    # 2. Run the benchmark loop
    # Note: Ensure evaluate_all_answers accepts 'mode' and 'full_kb'
    for test, result, prog_value, usage_stats in evaluate_all_answers(mode=mode, full_kb=full_kb):
        count += 1
        total_accuracy += result.accuracy
        total_completeness += result.completeness
        total_relevance += result.relevance
        
        total_tokens += usage_stats.get("total_tokens", 0)
        total_cost_usd += usage_stats.get("total_cost_usd", 0.0)

        category_accuracy[test.category].append(result.accuracy)
        progress(prog_value, desc=f"Evaluating {mode} test {count} (Cost: ${total_cost_usd:.4f})...")

    # 3. Calculate Averages
    avg_accuracy = total_accuracy / count if count > 0 else 0
    avg_completeness = total_completeness / count if count > 0 else 0
    avg_relevance = total_relevance / count if count > 0 else 0

    # 4. Generate High-Contrast HTML for the Report
    # We use the helpers here to keep the function clean and text visible
    final_html = f"""
    <div style="padding: 0; background-color: transparent;">
        {format_metric_html("Accuracy", avg_accuracy, "accuracy", score_format=True)}
        {format_metric_html("Completeness", avg_completeness, "completeness", score_format=True)}
        {format_metric_html("Relevance", avg_relevance, "relevance", score_format=True)}
        
        <!-- This helper ensures dark text on light background for your snapshot -->
        {format_usage_html(total_tokens, total_cost_usd, count)}
        
        <div style="margin-top: 15px; padding: 8px; background-color: #e7f3ff; border: 1px solid #b8daff; border-radius: 5px; text-align: center;">
            <span style="color: #004085; font-weight: bold; font-size: 13px;">✅ {mode} Benchmark Complete ({count} tests)</span>
        </div>
    </div>
    """

    category_data = [{"Category": cat, "Average Accuracy": sum(scores)/len(scores)} 
                     for cat, scores in category_accuracy.items()]
    
    return final_html, pd.DataFrame(category_data)




def main():
    # 1. Custom professional theme for report snapshots
    report_theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate",
        font=["Inter", "ui-sans-serif", "system-ui"],
    ).set(
        body_background_fill="*neutral_50",        # Very light gray for contrast
        block_background_fill="white",             # Pure white blocks for "pop"
        block_border_width="1px",
        block_title_text_color="*primary_600",
        section_header_text_size="*text_lg"
    )

    with gr.Blocks(title="HomeHaven Performance Analysis", theme=report_theme) as app:
        gr.Markdown("# 📊 HomeHaven System Benchmarks")
        gr.Markdown("Performance metrics and cost analysis for RAG vs. Long-Context LLM architectures.")

        # --- RETRIEVAL SECTION ---
        with gr.Tab("1. Retrieval Metrics"):
            retrieval_button = gr.Button("🔍 Run Retrieval Test", variant="secondary")
            with gr.Row():
                with gr.Column(scale=1):
                    retrieval_metrics = gr.HTML("<div style='text-align: center; color: #999;'>Ready for analysis</div>")
                with gr.Column(scale=2):
                    retrieval_chart = gr.BarPlot(
                        x="Category",
                        y="Average MRR",
                        title="Search Precision by Category",
                        y_lim=[0, 1],
                        height=400,
                        vertical=True,
                        # FIX: Tilt labels to 45 degrees to prevent overlap
                        x_label_angle=-45, 
                        color="Category", # Professional multi-color palette
                        tooltip=["Category", "Average MRR"]
                    )

        # --- ANSWER & COST SECTION ---
        with gr.Tab("2. Answer & Cost Analysis"):
            with gr.Row():
                test_mode = gr.Radio(
                    ["RAG", "PURE_LLM"], 
                    label="Architecture Mode", 
                    value="RAG",
                    info="Compare selective retrieval (RAG) against full 50k token context (Pure LLM)."
                )
                answer_button = gr.Button("🚀 Start Benchmark", variant="primary")

            with gr.Row():
                with gr.Column(scale=1):
                    answer_metrics = gr.HTML("<div style='text-align: center; color: #999;'>Select mode to begin</div>")
                with gr.Column(scale=2):
                    answer_chart = gr.BarPlot(
                        x="Category",
                        y="Average Accuracy",
                        title="Answer Accuracy Performance (1-5 Scale)",
                        y_lim=[1, 5],
                        height=400,
                        vertical=True,
                        # FIX: Tilt labels to 45 degrees
                        x_label_angle=-45,
                        color="Category",
                        tooltip=["Category", "Average Accuracy"]
                    )

        # --- EVENT MAPPINGS ---
        retrieval_button.click(
            fn=run_retrieval_evaluation,
            outputs=[retrieval_metrics, retrieval_chart],
        )

        answer_button.click(
            fn=run_answer_evaluation,
            inputs=[test_mode],
            outputs=[answer_metrics, answer_chart],
        )

    app.launch(inbrowser=True)




if __name__ == "__main__":
    main()
