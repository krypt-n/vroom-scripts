# -*- coding: utf-8 -*-
import json, sys
import matplotlib.pyplot as plt
import matplotlib.colors as clrs

# Very simple plot for a VROOM solution file.

def plot_routes(sol_file_name):
  plot_file_name = sol_file_name[0:sol_file_name.rfind(".json")] + ".svg"

  print "Parsing " + sol_file_name
  with open(sol_file_name, 'r') as sol_file:
    solution = json.load(sol_file)

  color_list = []
  for name, hex in clrs.cnames.items():
    color_list.append(name)

  fig, ax1 = plt.subplots(1, 1)
  fig.set_figwidth(15)
  plt.subplots_adjust(left=0.03, right=1, top=1, bottom=0.05, wspace=0.03)

  if(not solution.has_key('routes')):
    return

  xmin = solution['routes'][0]['steps'][0]['location'][0]
  xmax = xmin
  ymin = solution['routes'][0]['steps'][0]['location'][1]
  ymax = ymin

  for route in solution['routes']:
    lons = [step['location'][0] for step in route['steps']]
    lats = [step['location'][1] for step in route['steps']]

    ax1.plot(lons, lats, color=color_list[route['vehicle']])
    ax1.scatter(lons,
                lats,
                facecolor='none',
                edgecolor='blue',
                linewidth=0.7)

    xmin = min(xmin, min(lons))
    xmax = max(xmax, max(lons))
    ymin = min(ymin, min(lats))
    ymax = max(ymax, max(lats))

    step = route['steps'][-1]
    if step["type"] == "end":
      ax1.scatter([step['location'][0]], [step['location'][1]],
                  color='red',
                  linewidth = 8)

    step = route['steps'][0]
    if step["type"] == "start":
      ax1.scatter([step['location'][0]], [step['location'][1]],
                  color='green',
                  linewidth = 1)

  if 'unassigned' in solution and len(solution['unassigned']) > 0:
    unassigned_lons = [u['location'][0] for u in solution['unassigned']]
    unassigned_lats = [u['location'][1] for u in solution['unassigned']]
    ax1.scatter(unassigned_lons,
                unassigned_lats,
                marker='x',
                color='red',
                s=100)

    xmin = min(xmin, min(unassigned_lons))
    xmax = max(xmax, max(unassigned_lons))
    ymin = min(ymin, min(unassigned_lats))
    ymax = max(ymax, max(unassigned_lats))

  computing_time = solution['summary']['computing_times']['loading']
  computing_time += solution['summary']['computing_times']['solving']
  if(solution['summary']['computing_times'].has_key('routing')):
    computing_time += solution['summary']['computing_times']['routing']

  # Handle margins.
  size_factor = max((xmax - xmin) / 100, (ymax - ymin) / 100)
  margin_delta = 3 * size_factor

  title = plot_file_name[:plot_file_name.rfind(".")]
  title += " ; cost: " + str(solution['summary']['cost'])
  title += " ; computing time: " + str(computing_time)
  title += "ms"
  ax1.set_title(title)

  ax1.set_xlim(xmin - margin_delta, xmax + margin_delta)
  ax1.set_ylim(ymin - margin_delta, ymax + margin_delta)
  ax1.set_aspect('equal')

  print "Plotting file " + plot_file_name
  plt.savefig(plot_file_name, bbox_inches='tight')
  plt.close()
  # plt.show()

if __name__ == "__main__":
  # Argument are the name of the solution files to plot.
  for f in sys.argv[1:]:
    plot_routes(f)
