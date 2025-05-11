import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def display_metadata_chart(metadata):
    """
    Create a bar chart to visualize video metadata
    
    Args:
        metadata (dict): Dictionary containing video metadata
    """
    # Extract key metrics for visualization
    metrics = {
        'Frame Count': metadata['frame_count'],
        'Width (px)': metadata['frame_width'],
        'Height (px)': metadata['frame_height'],
        'FPS': round(metadata['fps'], 1),
    }

    # Filter out very large numbers that might skew the visualization
    viz_metrics = {k: v for k, v in metrics.items() if v < 10000}
    
    # Create a dataframe for plotting
    df = pd.DataFrame({
        'Metric': list(viz_metrics.keys()),
        'Value': list(viz_metrics.values())
    })
    
    # Create bar chart
    fig = px.bar(
        df, 
        x='Metric', 
        y='Value', 
        color='Metric',
        title='Video Metadata',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        text='Value'
    )
    
    fig.update_layout(
        xaxis_title=None,
        yaxis_title='Value',
        showlegend=False,
        height=400
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # For very large numbers like frame count, display them separately
    large_metrics = {k: v for k, v in metrics.items() if v >= 10000}
    if large_metrics:
        st.markdown("**Additional Metrics:**")
        for metric, value in large_metrics.items():
            st.markdown(f"- **{metric}**: {value:,}")

def plot_altered_frames(altered_frames, total_frames):
    """
    Create a line graph showing the distribution of altered frames
    
    Args:
        altered_frames (list): List of altered frame indices
        total_frames (int): Total number of frames in the video
    """
    if not altered_frames:
        st.info("No altered frames detected to visualize.")
        return
    
    # Create histogram data
    bin_count = min(50, len(altered_frames))  # Adjust bin count based on data
    hist, bin_edges = np.histogram(altered_frames, bins=bin_count)
    
    # Create dataframe for plotting
    df = pd.DataFrame({
        'Frame Range': [f"{int(bin_edges[i])}-{int(bin_edges[i+1])}" for i in range(len(bin_edges)-1)],
        'Altered Frame Count': hist,
        'Start Frame': bin_edges[:-1]
    })
    
    # Create line graph
    fig = px.line(
        df, 
        x='Start Frame', 
        y='Altered Frame Count',
        title='Distribution of Altered Frames',
        markers=True
    )
    
    fig.update_layout(
        xaxis_title='Frame Position',
        yaxis_title='Number of Altered Frames',
        height=400
    )
    
    # Add a vertical line at major clusters of altered frames
    if len(altered_frames) > 0:
        major_clusters = [frame for i, frame in enumerate(altered_frames) 
                         if i == 0 or frame - altered_frames[i-1] > 5]
        
        for cluster in major_clusters[:5]:  # Limit to first 5 major clusters
            fig.add_vline(
                x=cluster, 
                line_dash="dash", 
                line_color="red",
                annotation_text=f"Frame {cluster}",
                annotation_position="top right"
            )
    
    st.plotly_chart(fig, use_container_width=True)

def create_frame_heatmap(altered_frames, total_frames):
    """
    Create a heatmap visualization showing where alterations occur in the video timeline
    
    Args:
        altered_frames (list): List of altered frame indices
        total_frames (int): Total number of frames in the video
    """
    if not altered_frames:
        return
    
    # Create a timeline representation
    segments = 100  # Divide the video into 100 segments
    segment_size = max(1, total_frames // segments)
    
    # Count altered frames in each segment
    segment_counts = [0] * segments
    for frame in altered_frames:
        segment_idx = min(segments - 1, frame // segment_size)
        segment_counts[segment_idx] += 1
    
    # Normalize the counts for better visualization
    max_count = max(segment_counts) if segment_counts else 1
    normalized_counts = [count / max_count for count in segment_counts]
    
    # Create a dataframe for the heatmap
    df = pd.DataFrame({
        'Segment': list(range(segments)),
        'Alteration Intensity': normalized_counts
    })
    
    # Reshape for heatmap (1-row matrix)
    matrix = np.array(normalized_counts).reshape(1, -1)
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        colorscale='Reds',
        showscale=True,
        text=[[f"{int(c * 100)}%" if c > 0 else "" for c in normalized_counts]],
        texttemplate="%{text}",
        textfont={"size":10},
    ))
    
    fig.update_layout(
        title='Video Timeline Alteration Heatmap',
        xaxis_title='Video Timeline (0% to 100%)',
        yaxis_showticklabels=False,
        height=200,
        margin=dict(l=10, r=10, t=30, b=30)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add explanation
    st.caption("The heatmap shows the distribution of alterations across the video timeline. " +
            "Darker red areas indicate segments with more detected alterations.")
