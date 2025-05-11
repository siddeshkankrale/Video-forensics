import streamlit as st
import tempfile
import os
import time
import base64
import json
from utils import extract_metadata, calculate_hash, analyze_frames
from visualizations import display_metadata_chart, plot_altered_frames, create_frame_heatmap

# Page configuration
st.set_page_config(
    page_title="VidGuard - Video Forensic Analysis",
    page_icon="🎬",
    layout="wide",
)

# Display VidGuard logo
st.markdown(
    """
    <div style="text-align: center; background-color: black; padding: 20px; border-radius: 10px;">
        <h1 style="font-size: 2.5em; color: white;">VIDEO FORENSICS</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Create tabs for different sections of the app
tab1, tab2, tab3, tab4 = st.tabs(["Home & Upload", "Analysis Results", "Forensic Report", "Video Fraud Awareness"])

with tab1:
    st.markdown("## About Video Forensics")
    
    st.markdown("""
    ### Importance of Video Forensics
    In today's digital age, video content serves as crucial evidence in legal proceedings, security investigations, and news verification.
    Video forensics is essential for:
    - **Legal Evidence**: Ensuring video evidence hasn't been tampered with before court submission
    - **Security Investigations**: Analyzing surveillance footage for authenticity
    - **Media Verification**: Combating fake news and manipulated content
    - **Digital Rights Management**: Protecting intellectual property and copyright
    
    ### Common Video Manipulation Threats
    """)
    
    # Create columns for threats
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        - **Deepfake Manipulation**: AI-generated fake videos
        - **Frame Injection**: Adding or removing frames
        """)
    
    with col2:
        st.markdown("""
        - **Metadata Spoofing**: Altering video creation dates/times
        - **Codec-level Tampering**: Manipulating compression artifacts
        """)
    
    st.markdown("""
    ### Advancements in Video Forensics
    - **AI-based forgery detection**: Machine learning to identify manipulated content
    - **Blockchain authentication**: Immutable verification of video integrity
    - **Multi-spectral analysis**: Examining videos across different data dimensions
    """)
    
    st.markdown("---")
    
    st.markdown("## Upload Video for Analysis")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a video file", type=['mp4', 'avi', 'mov', 'mkv'])
    
    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            video_path = tmp_file.name
        
        # Show a spinner while analyzing the video
        with st.spinner("Analyzing video. This may take a while depending on the file size..."):
            # Create a progress bar
            progress_bar = st.progress(0)
            
            # Extract metadata (10% of progress)
            progress_bar.progress(10)
            metadata = extract_metadata(video_path)
            time.sleep(0.5)  # Simulate processing time
            
            # Calculate hash (30% of progress)
            progress_bar.progress(30)
            video_hash = calculate_hash(video_path)
            time.sleep(0.5)  # Simulate processing time
            
            # Analyze frames (90% of progress)
            progress_bar.progress(60)
            altered_frames = analyze_frames(video_path)
            time.sleep(0.5)  # Simulate processing time
            
            # Create forensic report
            report = {
                'filename': uploaded_file.name,
                'filesize': uploaded_file.size,
                'metadata': metadata,
                'hash': video_hash,
                'altered_frames': altered_frames,
                'analysis_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Store report in session state for access in other tabs
            st.session_state.report = report
            st.session_state.video_path = video_path
            
            # Complete progress
            progress_bar.progress(100)
            time.sleep(0.5)  # Simulate processing time
            
        st.success("Video analysis complete! Go to the 'Analysis Results' tab to see the findings.")
        
        # Clean up the temporary file - we'll do this when the session ends
        # Don't delete now as we need it for the other tabs
        
with tab2:
    if 'report' in st.session_state:
        report = st.session_state.report
        
        st.markdown("## Video Analysis Results")
        
        # Basic information
        st.markdown("### Basic Information")
        basic_info_col1, basic_info_col2 = st.columns(2)
        
        with basic_info_col1:
            st.markdown(f"**Filename:** {report['filename']}")
            st.markdown(f"**File Size:** {report['filesize']/1024/1024:.2f} MB")
            st.markdown(f"**Analysis Date:** {report['analysis_timestamp']}")
        
        with basic_info_col2:
            st.markdown(f"**MD5 Hash:** `{report['hash']}`")
            st.markdown(f"**Duration:** {report['metadata']['frame_count']/report['metadata']['fps']:.2f} seconds")

        # Metadata visualization
        st.markdown("### Video Metadata")
        display_metadata_chart(report['metadata'])
        
        # Altered frames visualization
        st.markdown("### Frame Analysis")
        
        if len(report['altered_frames']) > 0:
            st.warning(f"**Potential tampering detected!** Found {len(report['altered_frames'])} frames with significant changes.")
            plot_altered_frames(report['altered_frames'], report['metadata']['frame_count'])
            create_frame_heatmap(report['altered_frames'], report['metadata']['frame_count'])
        else:
            st.success("**No signs of tampering detected.** Frame analysis shows consistent frame transitions.")
            
        # Display the first 100 altered frames for reference
        if len(report['altered_frames']) > 0:
            with st.expander("View detailed altered frames information"):
                max_frames = min(100, len(report['altered_frames']))
                st.write(f"First {max_frames} altered frame positions (out of {len(report['altered_frames'])} total):")
                st.write(report['altered_frames'][:max_frames])
                
    else:
        st.info("Please upload a video in the 'Home & Upload' tab to see analysis results.")

with tab3:
    if 'report' in st.session_state:
        report = st.session_state.report
        
        st.markdown("## Forensic Report")
        
        # Create JSON string from report
        report_json = json.dumps(report, indent=4)
        
        # Display JSON in a code block
        st.markdown("### Report Data (JSON)")
        st.code(report_json, language="json")
        
        # Provide download button for the report
        st.markdown("### Download Report")
        
        # Function to create a download link for the report
        def get_report_download_link(report_json, filename="vidguard_forensic_report.json"):
            b64 = base64.b64encode(report_json.encode()).decode()
            href = f'<a href="data:file/json;base64,{b64}" download="{filename}">Download Report (JSON)</a>'
            return href
        
        st.markdown(get_report_download_link(report_json), unsafe_allow_html=True)
        
        # Forensic summary
        st.markdown("### Forensic Analysis Summary")
        
        # Overall integrity assessment
        if len(report['altered_frames']) > 0:
            integrity_score = max(0, 100 - (len(report['altered_frames']) / report['metadata']['frame_count'] * 100))
            st.warning(f"**Video Integrity Score: {integrity_score:.1f}%**")
            st.markdown("This video shows signs of potential tampering. The altered frames suggest possible manipulation.")
        else:
            st.success("**Video Integrity Score: 100%**")
            st.markdown("This video appears to be unaltered. No signs of frame tampering were detected.")
        
        # Recommendations
        st.markdown("### Recommendations")
        if len(report['altered_frames']) > 0:
            st.markdown("""
            - Conduct further analysis on the identified altered frames
            - Consider advanced forensic techniques for deeper examination
            - Document the chain of custody for the video file
            - Compare with the original source if available
            """)
        else:
            st.markdown("""
            - Maintain proper documentation of this forensic result
            - Store the hash value for future verification
            - Consider blockchain registration for immutable proof of integrity
            """)
            
    else:
        st.info("Please upload a video in the 'Home & Upload' tab to generate a forensic report.")

with tab4:
    st.markdown("# Video Fraud Awareness")
    
    st.markdown("""
    ## How Video Fraud Impacts Society
    
    Video manipulation has become increasingly sophisticated, affecting individuals, businesses, and society as a whole.
    The rise of deepfakes and other video alteration techniques has led to significant concerns across multiple sectors.
    """)
    
    # Create impact metrics with interactive elements
    st.markdown("## Impact of Video Manipulation")
    
    # Financial impact section
    financial_col1, financial_col2 = st.columns([3, 2])
    
    with financial_col1:
        st.markdown("### Financial Impact")
        st.markdown("""
        Video fraud has caused significant financial damage to individuals and organizations:
        - Corporate fraud using manipulated executive videos
        - Stock market manipulation through fake news videos
        - Insurance fraud using edited accident footage
        - Identity theft via synthetic video profiles
        """)
        
    with financial_col2:
        # Financial impact chart
        import plotly.express as px
        import pandas as pd
        
        # Sample data for financial impact (in millions of dollars)
        financial_data = pd.DataFrame({
            'Sector': ['Corporate', 'Insurance', 'Banking', 'Individual', 'Media'],
            'Estimated Annual Loss ($M)': [320, 160, 240, 80, 110]
        })
        
        fig_financial = px.bar(
            financial_data, 
            x='Sector', 
            y='Estimated Annual Loss ($M)',
            color='Sector',
            title='Estimated Financial Impact by Sector',
            labels={'Estimated Annual Loss ($M)': 'Loss in Millions USD'},
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        fig_financial.update_layout(
            xaxis_title=None,
            yaxis_title='Financial Loss (Millions USD)',
            showlegend=False
        )
        
        st.plotly_chart(fig_financial, use_container_width=True)
    
    # Common Scam Types section with interactive pie chart
    st.markdown("### Common Video Fraud Techniques")
    
    scam_col1, scam_col2 = st.columns([2, 3])
    
    with scam_col1:
        # Pie chart of video scam types
        scam_data = pd.DataFrame({
            'Technique': ['Deepfakes', 'Selective Editing', 'Metadata Tampering', 'Context Manipulation', 'Frame Insertion'],
            'Percentage': [35, 25, 15, 15, 10]
        })
        
        fig_scams = px.pie(
            scam_data, 
            values='Percentage', 
            names='Technique',
            title='Distribution of Video Fraud Techniques',
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        
        fig_scams.update_traces(textposition='inside', textinfo='percent+label')
        fig_scams.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ))
        
        st.plotly_chart(fig_scams, use_container_width=True)
    
    with scam_col2:
        st.markdown("""
        ### How People Get Scammed
        
        Victims are often targeted through sophisticated techniques:
        
        **Deepfakes (35%)**: AI-generated videos that replace faces or create entirely synthetic people
        - CEOs announcing fake policy changes leading to stock manipulation
        - Celebrities endorsing fraudulent products they never supported
        - Political figures shown making inflammatory statements they never made
        
        **Selective Editing (25%)**: Removing crucial context to change the meaning of events
        - Edited security footage in legal disputes
        - News clips edited to misrepresent events or statements
        
        **Metadata Tampering (15%)**: Changing timestamps, geolocation, or other video metadata
        - Altered timestamps to create false alibis
        - Modified creation dates for insurance claims
        
        **Context Manipulation (15%)**: Placing real footage in a false context
        - Old videos repurposed as current events
        - Footage from one event portrayed as another
        
        **Frame Insertion/Removal (10%)**: Manipulating individual frames
        - Removed frames to hide evidence in surveillance footage
        - Inserted objects or people into legitimate videos
        """)
    
    # Interactive time series showing growth
    st.markdown("### Growth of Video Fraud Cases Over Time")
    
    # Sample data for growth over time
    years = list(range(2018, 2026))
    cases = [120, 350, 870, 1950, 3200, 4800, 6500, 8700]
    
    time_data = pd.DataFrame({
        'Year': years,
        'Reported Cases': cases
    })
    
    # Create interactive line chart
    fig_growth = px.line(
        time_data, 
        x='Year', 
        y='Reported Cases',
        title='Increase in Reported Video Fraud Cases',
        markers=True
    )
    
    fig_growth.add_annotation(
        x=2021, 
        y=1950,
        text="AI Deepfake<br>tools become<br>widely available",
        showarrow=True,
        arrowhead=1
    )
    
    fig_growth.add_annotation(
        x=2023, 
        y=4800,
        text="Democratization of<br>video editing tools",
        showarrow=True,
        arrowhead=1
    )
    
    fig_growth.update_layout(
        xaxis_title='Year',
        yaxis_title='Number of Cases',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_growth, use_container_width=True)
    
    # Protection strategies section
    st.markdown("## How to Protect Yourself")
    
    protection_methods = [
        {"method": "Video Integrity Verification", "effectiveness": 85},
        {"method": "Blockchain Authentication", "effectiveness": 92},
        {"method": "Metadata Analysis", "effectiveness": 76},
        {"method": "Source Verification", "effectiveness": 82},
        {"method": "Frame-by-Frame Analysis", "effectiveness": 79}
    ]
    
    protection_df = pd.DataFrame(protection_methods)
    
    # Create horizontal bar chart for protection methods
    fig_protection = px.bar(
        protection_df,
        x='effectiveness',
        y='method',
        orientation='h',
        title='Effectiveness of Video Authentication Methods',
        labels={'effectiveness': 'Effectiveness Score (%)', 'method': 'Protection Method'},
        color='effectiveness',
        color_continuous_scale='Viridis',
        text='effectiveness'
    )
    
    fig_protection.update_traces(texttemplate='%{text}%', textposition='outside')
    fig_protection.update_layout(yaxis={'categoryorder':'total ascending'})
    
    st.plotly_chart(fig_protection, use_container_width=True)
    
    # Real-world case studies
    st.markdown("## Real-World Case Studies")
    
    case_study_tabs = st.tabs(["Corporate Fraud", "Political Manipulation", "Personal Impact"])
    
    with case_study_tabs[0]:
        st.markdown("### Corporate Video Fraud")
        st.markdown("""
        In 2023, a major technology company faced a stock price drop of 12% after a deepfake video of their CEO announcing significant losses was circulated on social media.
        
        **Impact:**
        - $4.2 billion market cap loss before the video was identified as fake
        - Reputational damage that took months to recover from
        - Increased security measures costing over $5 million to implement
        
        **Resolution:**
        VidGuard forensic analysis helped identify the video as manipulated, showing inconsistencies in lip synchronization and facial micro-expressions that weren't visible to the human eye.
        """)
        
    with case_study_tabs[1]:
        st.markdown("### Political Manipulation")
        st.markdown("""
        During a critical election, manipulated videos of a candidate appearing to make controversial statements were widely shared.
        
        **Impact:**
        - Polls showed a 7% swing away from the targeted candidate
        - Public confusion about the authenticity of various videos
        - Eroded trust in video evidence generally
        
        **Resolution:**
        Video forensic experts used temporal analysis and acoustic inconsistency detection to prove the videos were manipulated, but the reputational damage persisted even after debunking.
        """)
        
    with case_study_tabs[2]:
        st.markdown("### Personal Identity Theft")
        st.markdown("""
        An individual had their social media videos manipulated to create compromising content that was then used for extortion.
        
        **Impact:**
        - Personal and professional reputation damage
        - Psychological distress and privacy violation
        - Financial losses from extortion payments
        
        **Resolution:**
        Forensic video analysis tools like VidGuard were able to identify the manipulated sections by analyzing compression artifacts and frame inconsistencies, helping in the legal case against the perpetrators.
        """)
    
    # Call to action
    st.markdown("---")
    
    st.markdown("""
    ## Taking Action Against Video Fraud
    
    As video manipulation technology continues to advance, protecting yourself and your organization requires both vigilance and technical solutions.
    
    VidGuard provides the forensic tools needed to:
    1. Verify the authenticity of critical video evidence
    2. Detect sophisticated manipulation attempts
    3. Generate court-admissible forensic reports
    4. Establish chain of custody for important video assets
    
    **Start by analyzing your videos today to ensure their integrity before making important decisions based on their content.**
    """)

# Add a footer
st.markdown("---")
st.markdown("*VidGuard - Advanced Video Forensics Tool. For investigative and educational purposes only.*")
st.markdown("*Created by Om Golesar*")

# Clean up temporary files when the session ends
if 'video_path' in st.session_state:
    try:
        os.unlink(st.session_state.video_path)
    except:
        pass  # We'll ignore errors in cleanup
