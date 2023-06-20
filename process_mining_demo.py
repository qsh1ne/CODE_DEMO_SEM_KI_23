import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the event log as a DataFrame
event_log = pd.read_csv('/home/qsh1ne/PM_Code_Demo/Insurance_claims_event_log.csv',
                        nrows=200, usecols=['case_id', 'activity_name', 'timestamp'])

# Perform frequency analysis to get the directly-follows relations
dfg = event_log.groupby(['case_id', event_log['activity_name'].shift(-1)]).size().reset_index(name='count')

# Create a directed graph
graph = nx.DiGraph()

# Add nodes and edges to the graph
for _, row in dfg.iterrows():
    graph.add_edge(row['activity_name'], row['activity_name'], weight=row['count'])

# Visualize the graph
pos = nx.spring_layout(graph, seed=42)
labels = nx.get_edge_attributes(graph, 'weight')
weights = [graph[u][v]['weight'] / 10 for u, v in graph.edges()]
nx.draw_networkx(graph, pos, with_labels=True, node_size=500, node_color='lightblue',
                 edge_color='gray', width=weights, font_size=8)
nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, font_size=6)

# Save the process graph as an image file
output_dir = '/home/qsh1ne/PM_Code_Demo/output'
os.makedirs(output_dir, exist_ok=True)
process_graph_file = os.path.join(output_dir, 'process_graph.png')
plt.savefig(process_graph_file)

print(f"Process graph saved as {process_graph_file}")

# Calculate process spectrum
spectrum = event_log['activity_name'].value_counts().sort_values(ascending=False)

# Plot the process spectrum
plt.figure()
spectrum.plot(kind='bar', color='lightblue')
plt.xlabel('Activity')
plt.ylabel('Frequency')
plt.title('Process Spectrum')

# Save the process spectrum plot as an image file
spectrum_plot_file = os.path.join(output_dir, 'process_spectrum.png')
plt.savefig(spectrum_plot_file)

print(f"Process spectrum saved as {spectrum_plot_file}")

# Calculate case durations
event_log['timestamp'] = pd.to_datetime(event_log['timestamp'])
start_times = event_log.groupby('case_id')['timestamp'].min()
end_times = event_log.groupby('case_id')['timestamp'].max()
case_durations = end_times - start_times

# Plot the performance spectrum
plt.figure()
case_durations.dt.total_seconds().plot(kind='bar', color='lightblue')
plt.xlabel('Case ID')
plt.ylabel('Duration (seconds)')
plt.title('Performance Spectrum')

# Save the performance spectrum plot as an image file
performance_spectrum_file = os.path.join(output_dir, 'performance_spectrum.png')
plt.savefig(performance_spectrum_file)

print(f"Performance spectrum saved as {performance_spectrum_file}")
