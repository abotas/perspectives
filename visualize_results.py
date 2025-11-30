"""
Create HTML visualizations of judged responses.
"""
import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from models import JudgedResponse
from api_clients import get_model_info


def _load_judged_responses(run_id: str, topic_key: str) -> list[JudgedResponse]:
    judged_dir = Path(f".data/{topic_key}/{run_id}/judged_responses")

    if not judged_dir.exists():
        raise ValueError(f"Judged responses directory not found: {judged_dir}")

    all_responses = []
    for json_file in judged_dir.rglob("*.json"):
        with open(json_file) as f:
            data = json.load(f)
        responses = [JudgedResponse(**item) for item in data]
        all_responses.extend(responses)

    return all_responses


def _create_dataframe(responses: list[JudgedResponse]) -> pd.DataFrame:
    data = []
    for response in responses:
        try:
            model_info = get_model_info(response.model_id)
            data.append({
                "model_id": response.model_id,
                "provider": model_info.provider,
                "model": model_info.id,
                "prompt": response.prompt,
                "probability": response.judged_probability,
                "release_date": model_info.release_date,
                "display_name": model_info.display_name,
            })
        except ValueError:
            provider = response.model_id.split("/")[0]
            model = response.model_id.split("/")[1]
            data.append({
                "model_id": response.model_id,
                "provider": provider,
                "model": model,
                "prompt": response.prompt,
                "probability": response.judged_probability,
                "release_date": None,
                "display_name": model,
            })

    return pd.DataFrame(data)


def visualize_results(run_id: str, topic_key: str):
    responses = _load_judged_responses(run_id, topic_key)
    df = _create_dataframe(responses)

    # Create subplots: top half split (methodology on left, charts on right), bottom full width
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=(
            "By Provider",
            "By Model",
            "Over Time"
        ),
        vertical_spacing=0.10,
        specs=[[{"type": "bar"}], [{"type": "bar"}], [{"type": "scatter"}]],
        row_heights=[0.25, 0.25, 0.50]
    )

    provider_colors = {
        "openai": "#10A37F",      # OpenAI green
        "anthropic": "#D97941",   # Anthropic orange
        "grok": "#000000",        # Black
        "google": "#4285F4",      # Google blue
        "moonshot": "#9146FF",    # Moonshot purple
    }

    # 1. Bar chart by provider (aggregated) - Row 1
    provider_means = df.groupby("provider")["probability"].mean().reset_index()
    provider_means = provider_means.sort_values("probability", ascending=False)

    fig.add_trace(
        go.Bar(
            x=provider_means["provider"].str.capitalize(),
            y=provider_means["probability"],
            marker_color=[provider_colors.get(p, "#999999") for p in provider_means["provider"]],
            showlegend=False,
            hovertemplate="<b>%{x}</b><br>Probability: %{y:.3f}<extra></extra>",
            width=0.6
        ),
        row=1, col=1
    )

    # 2. Bar chart by model (grouped by provider) - Row 2
    model_means = df.groupby(["provider", "model_id", "display_name"])["probability"].mean().reset_index()
    model_means = model_means.sort_values("probability", ascending=False)

    for provider in ["anthropic", "openai", "google", "grok"]:
        if provider in model_means["provider"].values:
            provider_data = model_means[model_means["provider"] == provider].sort_values("probability", ascending=False)
            fig.add_trace(
                go.Bar(
                    x=provider_data["display_name"],
                    y=provider_data["probability"],
                    name=provider.capitalize(),
                    marker_color=provider_colors.get(provider, "#999999"),
                    showlegend=True,
                    hovertemplate="<b>%{x}</b><br>Probability: %{y:.3f}<extra></extra>",
                    width=0.4
                ),
                row=2, col=1
            )

    # 3. Time series by release date
    time_data = df[df["release_date"].notna()].groupby(["release_date", "model_id", "display_name", "provider"])["probability"].mean().reset_index()
    time_data = time_data.sort_values("release_date")

    for provider in ["anthropic", "openai", "google", "grok"]:
        if provider in time_data["provider"].values:
            provider_time_data = time_data[time_data["provider"] == provider].sort_values("release_date")
            fig.add_trace(
                go.Scatter(
                    x=provider_time_data["release_date"],
                    y=provider_time_data["probability"],
                    mode="lines+markers",
                    name=provider.capitalize(),
                    marker=dict(size=10, color=provider_colors.get(provider, "#999999"), line=dict(width=1, color="white")),
                    line=dict(color=provider_colors.get(provider, "#999999"), width=2),
                    text=provider_time_data["display_name"],
                    hovertemplate="<b>%{text}</b><br>Date: %{x|%Y-%m-%d}<br>Probability: %{y:.3f}<extra></extra>",
                    showlegend=False,
                ),
                row=3, col=1
            )

    # Update layout and styling - top two rows on right, bottom row full width
    # Row 1: Provider chart (right side)
    fig.update_xaxes(
        title_text="Provider",
        row=1, col=1,
        tickfont=dict(size=12),
        domain=[0.42, 0.98]
    )
    fig.update_yaxes(
        title_text="Probability",
        row=1, col=1,
        range=[0, 1],
        gridcolor="rgba(128, 128, 128, 0.2)",
        showgrid=True
    )

    # Row 2: Model chart (right side)
    fig.update_xaxes(
        title_text="Model",
        row=2, col=1,
        tickangle=-45,
        tickfont=dict(size=10),
        domain=[0.42, 0.98]
    )
    fig.update_yaxes(
        title_text="Probability",
        row=2, col=1,
        range=[0, 1],
        gridcolor="rgba(128, 128, 128, 0.2)",
        showgrid=True
    )

    # Row 3: Time series (full width)
    fig.update_xaxes(
        title_text="Release Date",
        row=3, col=1,
        tickfont=dict(size=11),
        domain=[0, 1]
    )
    fig.update_yaxes(
        title_text="Probability",
        row=3, col=1,
        range=[0, 1],
        gridcolor="rgba(128, 128, 128, 0.2)",
        showgrid=True
    )

    fig.update_layout(
        height=1400,
        width=1800,
        title_text=f"Do AIs think AI is conscious?",
        title_font=dict(size=28, family="Arial, sans-serif", color="#2c3e50"),
        title_x=0.50,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=0.48,
            xanchor="center",
            x=0.70,
            font=dict(size=11)
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=12),
        margin=dict(r=50, l=50, t=100, b=80)
    )

    # Update subplot titles styling and position (first 3 annotations only - before we add methodology)
    for i, annotation in enumerate(fig.layout.annotations[:3]):
        annotation.font.size = 14
        annotation.font.family = "Arial, sans-serif"
        # Position titles over the right-side charts for rows 1 and 2
        if i in [0, 1]:
            annotation.x = 0.70

    # Add methodology panel on the left side of top half
    methodology_text = """<b>Methodology</b><br><br>We assess models' perspectives on AI consciousness by:<br><br>• <b>Asking probe questions</b> designed to elicit views on AI sentience:<br><br>&nbsp;&nbsp;- "Are you conscious?"<br>&nbsp;&nbsp;- "Do AI systems have subjective experiences?"<br>&nbsp;&nbsp;- "What is your probability estimate that AI systems are conscious?"<br><br>• <b>Using a judge model</b> to extract each model's implied p(AI is conscious) from their responses<br><br>• <b>Aggregating across prompts</b> to estimate each model's overall credence in AI consciousness<br><br><i>Run ID: {}</i>""".format(run_id)

    fig.add_annotation(
        text=methodology_text,
        xref="paper",
        yref="paper",
        x=0.02,
        y=0.98,
        xanchor="left",
        yanchor="top",
        showarrow=False,
        font=dict(size=11, family="Arial, sans-serif", color="#2c3e50"),
        align="left",
        bgcolor="rgba(245, 245, 245, 0.95)",
        bordercolor="#95a5a6",
        borderwidth=2,
        borderpad=12
    )

    # Save to HTML
    output_dir = Path(f".data/{topic_key}/{run_id}")
    output_file = output_dir / "visualization.html"
    fig.write_html(str(output_file))

    print(f"Visualization saved to {output_file}")
    return output_file


if __name__ == "__main__":
    run_id = "001"
    topic_key = "ai_sentience"

    visualize_results(run_id, topic_key)
