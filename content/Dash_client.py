import nbformat
import requests
import plotly.graph_objects as go
import pandas as pd
import json
from IPython.display import display, HTML, clear_output
import ipywidgets as widgets
from ipywidgets import interact, Dropdown, SelectMultiple, Checkbox
from ipywidgets import HBox, VBox, GridBox, Layout
import numpy as np
from plotly.subplots import make_subplots
import plotly.io as pio


pio.renderers.default = "plotly_mimetype"
class DashNeuroTmapClient:
    def __init__(self, dash_url="http://127.0.0.1:8050"):
        """
        Client for interacting with the Dash application.

        Args:
            dash_url: Base URL of the Dash application
        """
        self.base_url = dash_url
        self.api_url = f"{dash_url}/api"
        self.current_plots = None
        self.overlays = []
        
    def check_health(self):
        """Check whether the Dash API is accessible."""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                #print(" Dash API is healthy!")
                #print(f"Available datasets: {data['available_datasets']}")
                return True
            else:
                print(f"❌ API health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Cannot connect to Dash API: {e}")
            print(f"Make sure your Dash app is running on {self.base_url}")
            return False
    
    def get_available_subjects(self, dataset='master'):
        """Retrieve the list of available subjects."""
        try:
            response = requests.get(f"{self.api_url}/subjects", 
                                  params={'dataset': dataset}, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error getting subjects: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def generate_plots(self, dataset='master', analysis_type='session_sex', 
                      session='V1', sex_filter='men', groups='A', subject=None, title=None):
        """
        Generate plots via the Dash API.

        Args:
            dataset: 'master', 'dataset1', or 'dataset2'
            analysis_type: 'single' or 'session_sex'
            session: 'V1', 'V2', or 'V3'
            sex_filter: 'all', 'men', or 'women'
            groups: List of groups (e.g., ['A', 'NA'])
            subject: Subject ID (required if analysis_type='single')
            title: Custom title for the overlay
        """

        payload = {
            'dataset': dataset,
            'analysis_type': analysis_type,
            'session': session,
            'sex_filter': sex_filter,
            'groups': groups,
            'title': title
        }
        
        if subject:
            payload['subject'] = subject
            
        try:
            response = requests.post(f"{self.api_url}/generate_plots", 
                                   json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self.current_plots = data['plots']
                #print(f"{data['message']}")
                return data['plots']
            else:
                error_data = response.json()
                print(f"❌ Error: {error_data.get('error', 'Unknown error')}")
                return None
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return None
    
    def update_plots(self, **kwargs):
        """Update the current plots with new parameters"""
        try:
            response = requests.put(f"{self.api_url}/update_plots", 
                                  json=kwargs, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self.current_plots = data['plots']
                #print(f" Plots updated successfully")
                return data['plots']
            else:
                error_data = response.json()
                print(f"❌ Update failed: {error_data.get('error', 'Unknown error')}")
                return None
                
        except Exception as e:
            print(f"❌ Update failed: {e}")
            return None
    
    def get_current_plots(self):
        """Retrieve the current plots"""
        try:
            response = requests.get(f"{self.api_url}/get_plots", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.current_plots = data['plots']
                return data['plots']
            else:
                error_data = response.json()
                print(f"❌ Error: {error_data.get('error', 'No plots available')}")
                return None
                
        except Exception as e:
            print(f"❌ Failed to get plots: {e}")
            return None
    
    def display_plots(self, plots_data=None):
        """Display the 3 Plotly charts side by side"""
        if plots_data is None:
            plots_data = self.current_plots
            
        if not plots_data:
            print("No plots to display. Generate plots first.")
            return None
        
        try:
            fig1 = go.Figure(plots_data['fig1'])
            fig2 = go.Figure(plots_data['fig2'])
            fig3 = go.Figure(plots_data['fig3'])
            
          
            for fig in [fig2, fig3]:
                fig.update_layout(height=300, 
                                  width=300,
                                  showlegend=False,
                                  title=dict( 
                                    y=1,  
                                    x=0.5,
                                    xanchor='center',
                                    yanchor='top'
                                  ))
            fig1.update_layout(height=300, 
                                width=300,
                                legend=dict(
                                    orientation="h",
                                    yanchor="top",
                                    y=-0.2,
                                    xanchor="center",
                                    x=0.5
                                ), 
                                title=dict( 
                                y=1,  
                                x=0.5,
                                xanchor='center',
                                yanchor='top'
                                ))

            display(GridBox(
                children=[
                    go.FigureWidget(fig1),
                    go.FigureWidget(fig2),
                    go.FigureWidget(fig3)
                ],
                layout=Layout(grid_template_columns="repeat(3, 33%)",
                justify_content='center',
                align_items='center')      
            ))
            
            return fig1, fig2, fig3
    
        
        except Exception as e:
            print(f"❌ Error displaying plots: {e}")
            return None

    def generate_overlay(self, dataset='master', analysis_type='session_sex', 
                        session='V1', sex_filter='women', groups='A', 
                        subject=None, title=None):
        """
        Generate an overlay in the natural state
        
        Args:
            dataset: 'master', 'dataset1', or 'dataset2'
            analysis_type: 'single' or 'session_sex' (default: session_sex)
            session: 'V1', 'V2', or 'V3' (default: V1)
            sex_filter: 'all', 'men', or 'women' (default: women)
            groups: List of groups (default: Aphasic (A))
            subject: Subject ID (required for analysis_type='single')
            title: Custom title for the overlay
        """

        if groups is None:
            groups = ['NA', 'A', 'B', 'W', 'G', 'C', 'AN', 'TCM', 'TCS', 'TCMix']
        
        if title is None:
            title = f"Session {session}"
            if sex_filter != 'all':
                title += f" ({'Men' if sex_filter == 'men' else 'Women'})"
          
        
        payload = {
            'dataset': dataset,
            'analysis_type': analysis_type,
            'session': session,
            'sex_filter': sex_filter,
            'groups': groups,
            'title': title
        }
        
        if subject:
            payload['subject'] = subject
            
        try:
            response = requests.post(f"{self.api_url}/overlay/generate", 
                                   json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self.overlays.append(data['overlay'])
                return data['overlay']
            else:
                error_data = response.json()
                print(f"❌ Error: {error_data.get('error', 'Unknown error')}")
                return None
                
        except Exception as e:
            print(f"❌ Overlay generation failed: {e}")
            return None

    def get_combined_plots(self):
        """Retrieve the combined plots, including the base and overlay plots."""
        try:
            response = requests.get(f"{self.api_url}/overlay/combine", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data['combined_plots']
            return None
        except Exception as e:
            print(f"Error getting combined plots: {e}")
            return None
    
    def display_combined_plots(self):
        """Display the combined plots including overlays."""
        combined_data = self.get_combined_plots()
        if not combined_data:
            print("No combined plots available. Generate base plots and overlays first.")
            return None
        
        try:
            fig1 = go.Figure(combined_data['fig1'])
            fig2 = go.Figure(combined_data['fig2'])
            fig3 = go.Figure(combined_data['fig3'])

            fig = make_subplots(
                rows=1, cols=3,
                specs=[[{'type': 'polar'}, {'type': 'polar'}, {'type': 'polar'}]],
                subplot_titles=(fig1.layout.title.text, 
                            fig2.layout.title.text, 
                            fig3.layout.title.text),
                horizontal_spacing=0.05,
                vertical_spacing=0.05
                )
        
            # Collect all unique trace names
            all_trace_names = set()
            for trace in fig1.data:
                all_trace_names.add(trace.name)
            for trace in fig2.data:
                all_trace_names.add(trace.name)
            for trace in fig3.data:
                all_trace_names.add(trace.name)
            
            # Add traces from fig1 (column 1)
            for i, trace in enumerate(fig1.data):
                fig.add_trace(
                    go.Barpolar(
                        r=trace.r,
                        theta=trace.theta,
                        marker_color=trace.marker.color,
                        name=trace.name,
                        legendgroup=trace.name,
                        showlegend=True,  # Show legend only for fig1
                        hovertemplate=trace.hovertemplate,
                        width=trace.width,
                        base=trace.base if hasattr(trace, 'base') else None
                    ),
                    row=1, col=1
                )
            
            # Add traces from fig2 (column 2)
            for i, trace in enumerate(fig2.data):
                fig.add_trace(
                    go.Barpolar(
                        r=trace.r,
                        theta=trace.theta,
                        marker_color=trace.marker.color,
                        name=trace.name,
                        legendgroup=trace.name,
                        showlegend=False,  # No legend for fig2
                        hovertemplate=trace.hovertemplate,
                        width=trace.width,
                        base=trace.base if hasattr(trace, 'base') else None
                    ),
                    row=1, col=2
                )
            
            # Add traces from fig3 (column 3)
            for i, trace in enumerate(fig3.data):
                fig.add_trace(
                    go.Barpolar(
                        r=trace.r,
                        theta=trace.theta,
                        marker_color=trace.marker.color,
                        name=trace.name,
                        legendgroup=trace.name,
                        showlegend=False,  # No legend for fig3
                        hovertemplate=trace.hovertemplate,
                        width=trace.width,
                        base=trace.base if hasattr(trace, 'base') else None
                    ),
                    row=1, col=3
                )
            
            # Copy the polar settings from the original figures
            if hasattr(fig1.layout, 'polar'):
                fig.update_polars(
                    angularaxis=fig1.layout.polar.angularaxis,
                    radialaxis=fig1.layout.polar.radialaxis,
                    bargap=fig1.layout.polar.bargap if hasattr(fig1.layout.polar, 'bargap') else 0.1,
                    row=1, col=1
                )
            
            if hasattr(fig2.layout, 'polar'):
                fig.update_polars(
                    angularaxis=fig2.layout.polar.angularaxis,
                    radialaxis=fig2.layout.polar.radialaxis,
                    bargap=fig2.layout.polar.bargap if hasattr(fig2.layout.polar, 'bargap') else 0.1,
                    row=1, col=2
                )
            
            if hasattr(fig3.layout, 'polar'):
                fig.update_polars(
                    angularaxis=fig3.layout.polar.angularaxis,
                    radialaxis=fig3.layout.polar.radialaxis,
                    bargap=fig3.layout.polar.bargap if hasattr(fig3.layout.polar, 'bargap') else 0.1,
                    row=1, col=3
                )
            # Overall layout
            fig.update_layout(
                height=375,
                width=820,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.15,
                    xanchor="center",
                    x=0.5
                ),
                hovermode='closest'
                )
            fig.update_annotations(
                y=1.15, 
                yanchor='bottom', 
                font=dict(size=10, color='black'),
            )
            # Layout for 3 equal charts with no spacing
            fig.update_polars(
                domain=dict(x=[0, 0.32], y=[0.1, 0.9]),  # Graph 1
                row=1, col=1
            )
            fig.update_polars(
                domain=dict(x=[0.34, 0.66], y=[0.1, 0.9]),  # Graph 2
                row=1, col=2
            )
            fig.update_polars(
                domain=dict(x=[0.66, 1.0], y=[0.1, 0.9]),   # Graph 3
                row=1, col=3
            )
            
            display(fig)
            
            return fig
            
        except Exception as e:
            print(f"Error displaying combined plots: {e}")
            return None
            
    def create_advanced_interface(self, base_session_default='V1', base_sex_default='men', overlay_session_default='V1', overlay_sex_default='women', groups_default=['A'], dataset ='master'):
        """Advanced interface with overlay management"""
        subjects_data = self.get_available_subjects(dataset="master")
        if not subjects_data:
            print("Cannot create interface: no subjects data available")
            return None

        # Base widgets 
        base_session = Dropdown(options=['V1', 'V2', 'V3'], value=base_session_default, description='Base Session:')
        base_sex = Dropdown(options=['all', 'men', 'women'], value=base_sex_default, description='Base Sex:')
        
        # Overlay widgets 
        overlay_session = Dropdown(options=['V1', 'V2', 'V3'], value=overlay_session_default, description='Overlay Session:')
        overlay_sex = Dropdown(options=['all', 'men', 'women'], value=overlay_sex_default, description='Overlay Sex:')
        
        # Graph container
        plot_output = widgets.Output()

        observers_active = False
        
        def display_base_with_overlay():
            """Display base + overlay (default state)"""
            with plot_output:
                plot_output.clear_output(wait=True)
          
                # Clear existing overlays
                self.clear_overlays()

                # Créer un titre personnalisé SANS les groupes pour la base
                base_title = f"Session {base_session.value}"
                if base_sex.value != 'all':
                    base_title += f" ({'Men' if base_sex.value == 'men' else 'Women'})"
                
                # Create a custom title for the base without groups
                base_plots = self.generate_plots(
                    dataset=dataset,
                    analysis_type="session_sex",
                    session=base_session.value,
                    sex_filter=base_sex.value,
                    groups=groups_default,
                    title=base_title
                )
                
                if base_plots:
                    # Generate the overlay (fixed groups for the natural state)
                    overlay_plots = self.generate_overlay(
                        dataset=dataset,
                        analysis_type="session_sex",
                        session=overlay_session.value,
                        sex_filter=overlay_sex.value,
                        groups=groups_default  
                    )
                    
                    if overlay_plots:
                       self.display_combined_plots()
                    else:
                        self.display_plots(base_plots)
         
        
        def reset_to_default():
            """Reset all widgets to their default values"""
            base_session.value = base_session_default #'V1'
            base_sex.value = base_sex_default #'men'
            overlay_session.value = overlay_session_default #'V1'
            overlay_sex.value = overlay_sex_default #'women'
            

        # Create the reset button
        reset_btn = widgets.Button(description="🔄 Reset to Default", button_style='warning')
        reset_btn.on_click(lambda b: reset_to_default())

        # Create the main container
        main_container = VBox([
            HBox([base_session, base_sex]),
            HBox([overlay_session, overlay_sex]),
            HBox([reset_btn]),
            plot_output
        ])

        # Initial display (base + overlay by default)
        display_base_with_overlay()

        # Link widget events – automatic update
        def on_any_change(change):
            """When a parameter changes, update base + overlay"""
            if observers_active:
                display_base_with_overlay()

        observers_active = True
        # All widgets trigger an automatic update
        for widget in [base_session, base_sex, overlay_session, overlay_sex]:
            widget.observe(on_any_change, names='value')

        # Return the container so that it can be saved as the notebook output
        return main_container
        
    def clear_overlays(self):
        """Clear all overlays locally and via the API"""
        self.overlays = []
        try:
            response = requests.delete(f"{self.api_url}/overlay/clear", timeout=10)
            if response.status_code == 200:
                return True
            return False
        except Exception as e:
            return False


    # Display 3 heatmaps side by side: ‘All’, ‘Men’, and ‘Women’, for the same variable and the same session
    def generate_correlation_heatmaps(self, dataset='master', session='V1', 
                                        system_type='Synaptic ratio', groups=['A']):
            """
            Generate correlation heatmaps identical to those in the Dash app.
            """
            payload = {
                'dataset': dataset,
                'session': session,
                'system_type': system_type,
                'groups': groups
            }
            
            try:
                response = requests.post(f"{self.api_url}/correlation/generate_heatmaps", 
                                    json=payload, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    return data['heatmaps']
                else:
                    error_data = response.json()
                    print(f"❌ Error: {error_data.get('error', 'Unknown error')}")
                    return None
                    
            except Exception as e:
                print(f"❌ Heatmap generation failed: {e}")
                return None

    def display_correlation_heatmaps(self, heatmaps_data=None, system_type="Synaptic ratio"):
        """Display 3 heatmaps identical to those in the Dash app."""
        if heatmaps_data is None:
            return None
        
        try:
            figures = []
            titles = ['All Subjects', 'Men Only', 'Women Only']
            
            for i, sex_filter in enumerate(['all', 'men', 'women']):
                if (sex_filter in heatmaps_data and 
                    heatmaps_data[sex_filter]['status'] == 'success'):
                    
                    # Use the Plotly figure generated directly by the Dash app
                    fig_dict = heatmaps_data[sex_filter]['heatmap']
                    fig = go.Figure(fig_dict)
                    figures.append(fig)
                else:
                    # Create an empty figure with an error message
                    fig = go.Figure()
                    fig.add_annotation(
                        text=f"No data for {titles[i]}",
                        xref="paper", yref="paper",
                        x=0.5, y=0.5, xanchor='center', yanchor='middle',
                        showarrow=False,
                        font=dict(size=14, color="red")
                    )
                    figures.append(fig)

            # Create a figure with 3 subplots
            fig_combined = make_subplots(
                rows=1, cols=3,
                subplot_titles=titles,
                horizontal_spacing=0.7,  
                vertical_spacing=0.05,
                specs=[[{"type": "heatmap"}, {"type": "heatmap"}, {"type": "heatmap"}]]
            )
            
            # Add each heatmap
            for idx, fig in enumerate(figures):
                if len(fig.data) > 0:
                    trace = fig.data[0]
                    trace.showscale = (idx == 2)  # Colorbar only for the last heatmap 
                    fig_combined.add_trace(trace, row=1, col=idx+1)
            
            # Global layout
            fig_combined.update_layout(
                height=400,
                width=900,  
                showlegend=False,
                margin=dict(l=80, r=80, t=60, b=120),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False)
            )
            
            # Update axes for each subplot
            for i in range(1, 4):
                fig_combined.update_xaxes(
                    tickangle=-45,
                    tickfont=dict(size=8),
                    side='bottom',
                    showgrid=False,
                    row=1, col=i
                )
                fig_combined.update_yaxes(
                    autorange='reversed',
                    tickfont=dict(size=8),
                    showgrid=False,
                    row=1, col=i
                )
            
            fig_combined.update_annotations(font_size=10)
            fig_combined.show()
            
            return fig_combined
            
        except Exception as e:
            print(f"❌ Error displaying correlation heatmaps: {e}")
            import traceback
            traceback.print_exc()
            return None
            
    def create_correlation_interface(self, dataset='master'):
        """Interactive interface for correlation heatmaps """
        
        subjects_data = self.get_available_subjects(dataset)
        if not subjects_data:
            print("Cannot create interface: no subjects data available")
            return None

        # Parameters widgets 
        session_widget = widgets.Dropdown(
            options=['V1', 'V2', 'V3'],
            value='V1',
            description='Session:'
        )

        system_widget = widgets.Dropdown(
            options=['Synaptic ratio', 'Neurotransmitter (Loc)', 'Neurotransmitter (Tract)', 'Clinical Outcomes'],
            value='Synaptic ratio',
            description='System:'
        )

        groups_widget = widgets.Dropdown(
            options=['A', 'NA'],  
            value='A',
            description='Groups:'
        )

        #  Reset button
        reset_btn = widgets.Button(
            description='🔄 Reset to Default',
            button_style='warning',
            layout=widgets.Layout(width='200px')
        )

        # Graph container 
        plot_output = widgets.Output()

        observers_active = False
        
        def display_heatmaps():
            """Display 3 heatmaps"""
            with plot_output:
                plot_output.clear_output(wait=True)
                
                try:
                    heatmaps_data = self.generate_correlation_heatmaps(
                        session=session_widget.value,
                        system_type=system_widget.value,
                        groups=groups_widget.value
                    )

                    if heatmaps_data:
                        self.display_correlation_heatmaps(heatmaps_data, system_type=system_widget.value)
                    else:
                        print("❌ No heatmaps generated (missing data or server error)")
                except Exception as e:
                    print(f"❌ Error displaying heatmaps: {e}")
        
        def reset_to_default(_=None):
            """Reset all widgets to their default values for fig 2"""
            session_widget.value = 'V1'
            system_widget.value = 'Synaptic ratio'
            groups_widget.value = ['A']
        
        # Reset button configuration
        reset_btn.on_click(reset_to_default)

        # Create the main container
        main_container = widgets.VBox([
            widgets.HBox([session_widget, system_widget, groups_widget]),
            widgets.HBox([reset_btn]),
            plot_output
        ])

        def on_any_change(change):
            """Quand un paramètre change, mettre à jour les heatmaps"""
            if observers_active:
                display_heatmaps()

        observers_active = True
  
        for widget in [session_widget, system_widget, groups_widget]:
            widget.observe(on_any_change, names='value')

        display_heatmaps()

        return main_container
   
    def create_correlation_figure(self, heatmaps_data, p_thresh, show_numbers, session, system_type):
        # Recreate the figures with the new threshold
                figures = []
                titles = ['All Subjects', 'Men Only', 'Women Only']
                
                for i, sex_filter in enumerate(['all', 'men', 'women']):
                    if (sex_filter in heatmaps_data and 
                        heatmaps_data[sex_filter]['status'] == 'success'):
                        
                        data = heatmaps_data[sex_filter]
                        corr_matrix_dict = data['correlation_matrix']
                        pval_matrix_dict = data['pvalue_matrix']
                        vars_list = data['corr_index']
                        display_vars = data['variables']
                        
                        x_labels = [var.split('_', 1)[1] if '_' in var else var for var in display_vars]
                        y_labels = [var.split('_', 1)[1] if '_' in var else var for var in display_vars]
                
                        corr_array = np.array([[corr_matrix_dict[row][col] 
                                            for col in vars_list] 
                                            for row in vars_list])
                        pval_array = np.array([[pval_matrix_dict[row][col] 
                                            for col in vars_list] 
                                            for row in vars_list])
                        
                        # Apply the p-value mask (always active)
                        corr_display = np.where(pval_array < p_thresh, corr_array, None)
                        
                        if show_numbers:
                            text_array = np.round(corr_array, 1)
                            text_template = "%{text}"
                        else:
                            # Hide the numbers
                            text_array = [["" for _ in range(len(vars_list))] for _ in range(len(vars_list))]
                            text_template = ""
                        
                        # Create heatmap
                        fig = go.Figure(data=go.Heatmap(
                            z=corr_display,
                            x= x_labels,#display_vars,
                            y= y_labels,#display_vars,
                            colorscale='RdBu_r',
                            zmin=-1,
                            zmax=1,
                            text=text_array,
                            texttemplate=text_template,
                            textfont={"size": 8},
                            hovertemplate=(
                                "Variable X: %{x}<br>"
                                "Variable Y: %{y}<br>"
                                "Correlation: %{z:.2f}<br>"
                                "<extra></extra>"
                            )
                        ))
                        
                        figures.append(fig)
                    else:
                        fig = go.Figure()
                        fig.add_annotation(
                            text=f"No data for {titles[i]}",
                            xref="paper", yref="paper",
                            x=0.5, y=0.5, xanchor='center', yanchor='middle',
                            showarrow=False,
                            font=dict(size=14, color="red")
                        )
                        figures.append(fig)
                
                # Create combined figure 
                fig_combined = make_subplots(
                    rows=1, cols=3,
                    subplot_titles=titles,
                    horizontal_spacing=0.01, 
                    vertical_spacing=0.05,
                    specs=[[{"type": "heatmap"}, {"type": "heatmap"}, {"type": "heatmap"}]]
                )
                
                for idx, fig in enumerate(figures):
                    if len(fig.data) > 0:
                        trace = fig.data[0]
                        if idx == 2:
                            trace.showscale = True
                        else:
                            trace.showscale = False
                        #trace.showscale = (idx == 2)
                        fig_combined.add_trace(trace, row=1, col=idx+1)
                
                fig_combined.update_layout(
                    height=375,
                    width=900,
                    showlegend=False,
                    margin=dict(l=30, r=40, t=80, b=80), 
                    title=dict(
                        text=f"Session {session} - {system_type}<br>",
                        x=0.5,
                        xanchor='center',
                        font=dict(size=14)
                    )
                )
                
                for i in range(1, 4):
                    fig_combined.update_xaxes(
                        tickangle=-45,
                        tickfont=dict(size=8),
                        automargin=False,
                        side='bottom',
                        showgrid=False,
                        row=1, col=i
                    )
                    fig_combined.update_yaxes(
                        autorange='reversed',
                        tickfont=dict(size=8),
                        showgrid=False,
                        row=1, col=i
                    )
                    if i == 1:
                        fig_combined.update_yaxes(showticklabels=True, row=1, col=i)
                    else:
                        fig_combined.update_yaxes(showticklabels=False, row=1, col=i)       
                return fig_combined
    
    # plotly animation without dropdown
    def create_interactive_correlation_viewer(self, dataset='master', session='V1',
                                            system_type='Synaptic ratio', groups=['A']):
        """
        Create an interactive viewer with slider for p-value only
        No dropdowns for session/system/groups (these are fixed at the time of the call)
        """
        
        # Generate the heatmaps only once
        heatmaps_data = self.generate_correlation_heatmaps(
            dataset=dataset,
            session=session,
            system_type=system_type,
            groups=groups
        )
        
        if not heatmaps_data:
            print("❌ Failed to load heatmaps data")
            return None
        
        # Slider for p-value threshold
        p_threshold_slider = widgets.FloatSlider(
            value=0.05,
            min=0.001,
            max=0.1,
            step=0.001,
            description='p-value threshold:',
            continuous_update=True,
            readout=True,
            readout_format='.3f',
            style={'description_width': '130px'},
            layout=widgets.Layout(width='500px')
        )
        
        # Checkbox to SHOW/HIDE the numbers
        show_numbers_checkbox = widgets.Checkbox(
            value=True,  # show by default
            description='Show correlation values on heatmap',
            style={'description_width': 'initial'},
            indent=False
        )

        plot_output = widgets.Output()
        
        
        initial_fig = self.create_correlation_figure(heatmaps_data, 0.05, True, session, system_type)
        fig_widget = go.FigureWidget(initial_fig)
        with plot_output:
            display(fig_widget)
        #fig_widget_container = {'widget': fig_widget}

        
        def update_heatmap_display(change=None):
            """Update ONLY the display with the current threshold"""     
            try:
                #plot_output.clear_output(wait=True)
                p_thresh = p_threshold_slider.value
                show_numbers = show_numbers_checkbox.value
                new_fig  = self.create_correlation_figure(heatmaps_data, p_thresh, show_numbers, session, system_type)

                with plot_output:
                    clear_output(wait=True) 
                   
                    with fig_widget.batch_update():
                        # Mettre à jour les données de chaque trace
                        for idx, trace in enumerate(new_fig.data):
                            if idx < len(fig_widget.data):
                                fig_widget.data[idx].z = trace.z
                                fig_widget.data[idx].text = trace.text
                                fig_widget.data[idx].texttemplate = trace.texttemplate
                        
                        # Mettre à jour le layout
                        fig_widget.layout.title.text = new_fig.layout.title.text
            except Exception as e:
                print(f"❌ Error updating display: {e}")
                import traceback
                traceback.print_exc()
                  
        # Link the widgets
        p_threshold_slider.observe(update_heatmap_display, names='value')
        show_numbers_checkbox.observe(update_heatmap_display, names='value')
        
        # Create the main container 
        main_container = widgets.VBox([
            show_numbers_checkbox,
            p_threshold_slider,
            plot_output
        ])
        
        # Initial display
        update_heatmap_display()
        
        return main_container
   
    # Interactive heatmap with cross-tabulated variables 
    def generate_cross_correlation_heatmap(self, dataset='master',
                                        session1='V1', sex_filter1='All', outcome1='Synaptic ratio', groups1=['A'],
                                        session2='V3', sex_filter2='All', outcome2='Synaptic ratio', groups2=['A']):
        """Generate a cross-correlation heatmap within the same group using distinct or similar parameters."""
        payload = {
            'dataset': dataset,
            'session1': session1,
            'sex_filter1': sex_filter1,
            'outcome1': outcome1,
            'groups1': groups1,
            'session2': session2,
            'sex_filter2': sex_filter2,
            'outcome2': outcome2,
            'groups2': groups2
        }
        
        try:
            response = requests.post(f"{self.api_url}/correlation/generate_cross_heatmaps", 
                                json=payload, timeout=30)
            #print(response.status_code, response.text)
            
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                error_data = response.json()
                print(f"❌ Error: {error_data.get('error', 'Unknown error')}")
                return None
                
        except Exception as e:
            print(f"❌ Cross correlation generation failed: {e}")
            return None

    def create_interactive_correlation_interface_auto(self):

        """Interactive interface with automatic updates"""
        
        # Widgets for Set 1
        session1 = widgets.Dropdown(options=['V1', 'V2', 'V3'], value='V1', description='Session 1:')
        sex1 = widgets.Dropdown(options=['All', 'Men only', 'Women only'], value='All', description='Sex 1:')
        outcome1 = widgets.Dropdown(
            options=['Synaptic ratio', 'Neurotransmitter (Loc)', 
                    'Neurotransmitter (Tract)', 'Clinical Outcomes'],
            value='Synaptic ratio',
            description='Outcome 1:'
        )
        
        # Widgets for Set 2
        session2 = widgets.Dropdown(options=['V1', 'V2', 'V3'], value='V3', description='Session 2:')
        sex2 = widgets.Dropdown(options=['All', 'Men only', 'Women only'], value='All', description='Sex 2:')
        
        outcome2 = widgets.Dropdown(
            options=['Synaptic ratio', 'Neurotransmitter (Loc)', 
                    'Neurotransmitter (Tract)', 'Clinical Outcomes'],
            value='Synaptic ratio',
            description='Outcome 2:'
        )
        

        permanent_message = widgets.HTML(
            value="""
            <div style='
                background-color: #e3f2fd; 
                border: 1px solid #2196f3; 
                border-radius: 5px; 
                padding: 8px; 
                margin: 10px 0;
                color: #1565c0;
                font-size: 14px;
            '>
            💡 <b>Note:</b> You must choose the same sex group for each subject set to obtain correlation analysis
            </div>
            """
        )

        output_container = widgets.VBox()
        observers_active = False
        
        def update_heatmap():
            result = self.generate_cross_correlation_heatmap(
                dataset='master',
                session1=session1.value,
                sex_filter1=sex1.value,
                outcome1=outcome1.value,
                groups1=['A'],
                session2=session2.value,
                sex_filter2=sex2.value,
                outcome2=outcome2.value,
                groups2=['A']
            )

            if result and result['status'] == 'success':
            #     for trace in result['heatmap']['data']:
            #         for key in ['x', 'y', 'z']:
            #             if key in trace:
            #                 trace[key] = trace[key].tolist() if isinstance(trace[key], np.ndarray) else trace[key]

            #     fig = go.FigureWidget(result['heatmap'])
                fig = go.FigureWidget(result['heatmap'])

                fig.update_xaxes(side="bottom")   # Force the X-axis to appear at the bottom for myST
                fig.update_yaxes(side="left")     # Force the Y-axis to appear at the left for myST

                fig.update_layout(
                    width=500,   
                    height=500, 
                    showlegend =False
                    #margin=dict(l=50, r=50, t=50, b=50)  
                )
            
                # Statistic widget
                stats_text = widgets.HTML(
                    value=f"<p><b>1st selection:</b> {result['subject_count_set1']} subjects | "
                        f"<b>2nd selection:</b> {result['subject_count_set2']} subjects | "
                        f"<b>Common:</b> {result['common_subjects']} subjects</p>"
                )
                output_container.children = [stats_text, fig]
            else:
                error_text = widgets.HTML(value="<p style='color: red;'>Failed to generate heatmap</p>")
                output_container.children = [error_text]
        
        def on_change(change):
            if observers_active:
                update_heatmap()
        

        set1_controls = widgets.VBox([
            widgets.HBox([session1, sex1]),   
            widgets.HBox([outcome1])     
             ])
     
        set2_controls = widgets.VBox([
            widgets.HBox([session2, sex2]),   
            widgets.HBox([outcome2])     
        ])
     
        main_container = widgets.VBox([
            widgets.HBox([set1_controls, set2_controls]),
            permanent_message,
            widgets.HBox([output_container], layout=widgets.Layout(justify_content='center'))
        ])

        update_heatmap()

        observers_active = True
        for widget in [session1, sex1, outcome1, session2, sex2, outcome2]:
            widget.observe(on_change, names='value')
  
        return main_container
