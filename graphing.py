import matplotlib.pyplot as plt

def graph_voting_plot(results: dict):
    locations_plot_info = []
    resources_plot_info = []
    for k, v in results.items():
        #print(k)
        locations_plot_info.append(k)
        #print (v['Resource'])
        resources_plot_info.append(v['Resource'])
    # print("2 INSERT APPORTIONMENT GRAPH HERE")
    # print(results)
    #left is needed for graphing bar charts, its the x in plt.bar documentation
    left = []
    for i in range(1, len(resources_plot_info) + 1):
        left.append(i)
    #print(left)

    plt.bar(left, height = resources_plot_info, tick_label = locations_plot_info, width = 0.8, color = ['red', 'green'])
    plt.xlabel('Location number')
    plt.ylabel('Num. Resources')
    plt.title('Apportionment Results')
    plt.show()
